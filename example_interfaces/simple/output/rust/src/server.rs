//! Server module for Simple IPC
//!
//! This module is only available when the "server" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
use bytes::Bytes;
use tokio::sync::oneshot;

use async_trait::async_trait;
use std::any::Any;
use std::sync::{Arc, Mutex};
use tokio::sync::Mutex as AsyncMutex;

use serde_json;
use tokio::sync::{broadcast, watch};

use crate::property::SimpleInitialPropertyValues;
use std::sync::atomic::{AtomicU32, Ordering};

use std::future::Future;
use std::pin::Pin;
use stinger_mqtt_trait::message::{MqttMessage, QoS};
use stinger_mqtt_trait::{Mqtt5PubSub, Mqtt5PubSubError, MqttPublishSuccess};
use stinger_rwlock_watch::RwLockWatch;
#[allow(unused_imports)]
use stinger_rwlock_watch::{CommitResult, WriteRequestLockWatch};
use tokio::task::JoinError;
type SentMessageFuture = Pin<Box<dyn Future<Output = Result<(), MethodReturnCode>> + Send>>;
use crate::message;
#[cfg(feature = "metrics")]
use serde::Serialize;
#[cfg(feature = "server")]
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct SimpleServerSubscriptionIds {
    trade_numbers_method_req: u32,

    school_property_update: u32,
}

#[derive(Clone)]
struct SimpleProperties {
    pub school: Arc<RwLockWatch<String>>,
    school_version: Arc<AtomicU32>,
}

#[cfg(feature = "metrics")]
#[derive(Debug, Serialize)]
pub struct SimpleServerMetrics {
    pub trade_numbers_calls: u64,
    pub trade_numbers_errors: u64,

    pub initial_property_publish_time: std::time::Duration,
}

#[cfg(feature = "metrics")]
impl Default for SimpleServerMetrics {
    fn default() -> Self {
        SimpleServerMetrics {
            trade_numbers_calls: 0,
            trade_numbers_errors: 0,

            initial_property_publish_time: std::time::Duration::from_secs(0),
        }
    }
}

#[derive(Clone)]
pub struct SimpleServer<C: Mqtt5PubSub> {
    mqtt_client: C,

    /// Temporarily holds the receiver for the broadcast channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<broadcast::Receiver<MqttMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: broadcast::Sender<MqttMessage>,

    /// Struct contains all the method handlers.
    method_handlers: Arc<AsyncMutex<Box<dyn SimpleMethodHandlers<C>>>>,

    /// Struct contains all the properties.
    properties: SimpleProperties,

    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: SimpleServerSubscriptionIds,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,

    pub instance_id: String,

    #[cfg(feature = "metrics")]
    metrics: Arc<AsyncMutex<SimpleServerMetrics>>,
}

impl<C: Mqtt5PubSub + Clone + Send> SimpleServer<C> {
    pub async fn new(
        mut connection: C,
        method_handlers: Arc<AsyncMutex<Box<dyn SimpleMethodHandlers<C>>>>,
        instance_id: String,
        initial_property_values: SimpleInitialPropertyValues,
    ) -> Self {
        #[cfg(feature = "metrics")]
        let mut metrics = SimpleServerMetrics::default();

        // Create a channel for messages to get from the Mqtt5PubSub object to this SimpleServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = broadcast::channel::<MqttMessage>(64);

        // Create method handler struct
        let subscription_id_trade_numbers_method_req = connection
            .subscribe(
                format!("simple/{}/method/tradeNumbers", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_trade_numbers_method_req =
            subscription_id_trade_numbers_method_req.unwrap_or(u32::MAX);

        let subscription_id_school_property_update = connection
            .subscribe(
                format!("simple/{}/property/school/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_school_property_update =
            subscription_id_school_property_update.unwrap_or(u32::MAX);

        // Create structure for subscription ids.
        let sub_ids = SimpleServerSubscriptionIds {
            trade_numbers_method_req: subscription_id_trade_numbers_method_req,

            school_property_update: subscription_id_school_property_update,
        };

        let property_values = SimpleProperties {
            school: Arc::new(RwLockWatch::new(initial_property_values.school.clone())),
            school_version: Arc::new(AtomicU32::new(initial_property_values.school_version)),
        };

        // Publish the initial property values for all the properties.
        #[cfg(feature = "metrics")]
        let start_prop_publish_time = std::time::Instant::now();
        {
            let topic = format!("simple/{}/property/school/value", instance_id);

            let payload_obj = SchoolProperty {
                name: initial_property_values.school,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.school_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        #[cfg(feature = "metrics")]
        {
            metrics.initial_property_publish_time = start_prop_publish_time.elapsed();
            debug!(
                "Published 1 initial property value in {:?}",
                metrics.initial_property_publish_time
            );
        }

        SimpleServer {
            mqtt_client: connection.clone(),

            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,
            method_handlers,
            properties: property_values,
            subscription_ids: sub_ids,

            client_id: connection.get_client_id(),
            instance_id,
            #[cfg(feature = "metrics")]
            metrics: Arc::new(AsyncMutex::new(metrics)),
        }
    }

    #[cfg(feature = "metrics")]
    pub fn get_metrics(&self) -> Arc<AsyncMutex<SimpleServerMetrics>> {
        self.metrics.clone()
    }

    /// Converts a oneshot channel receiver into a future.
    async fn oneshot_to_future(
        ch: oneshot::Receiver<Result<MqttPublishSuccess, Mqtt5PubSubError>>,
    ) -> SentMessageFuture {
        Box::pin(async move {
            let chan_result = ch.await;
            match chan_result {
                Ok(transferred_result) => match transferred_result {
                    Ok(MqttPublishSuccess::Acknowledged) => Ok(()),
                    Ok(MqttPublishSuccess::Completed) => Ok(()),
                    Ok(MqttPublishSuccess::Sent) => Ok(()),
                    Ok(MqttPublishSuccess::Queued) => Ok(()),
                    Err(e) => Err(MethodReturnCode::TransportError(format!(
                        "MQTT publish error: {:?}",
                        e
                    ))),
                },
                Err(e) => Err(MethodReturnCode::TransportError(format!(
                    "MQTT publish oneshot receive error: {:?}",
                    e
                ))),
            }
        })
    }

    async fn wrap_return_code_in_future(rc: MethodReturnCode) -> SentMessageFuture {
        Box::pin(async move {
            match rc {
                MethodReturnCode::Success(_) => Ok(()),
                _ => Err(rc),
            }
        })
    }

    /// Publishes an error response to the given response topic with the given correlation data.
    async fn publish_error_response(
        mut publisher: C,
        response_topic: Option<String>,
        correlation_data: Option<Bytes>,
        err: MethodReturnCode,
    ) {
        if let Some(resp_topic) = response_topic {
            let msg = message::error_response(&resp_topic, correlation_data, err).unwrap();
            let _ = publisher.publish(msg).await;
        } else {
            info!("No response topic found in message properties; cannot send error response.");
        }
    }
    /// Emits the person_entered signal with the given arguments.
    pub async fn emit_person_entered(&mut self, person: Person) -> SentMessageFuture {
        let data = PersonEnteredSignalPayload { person };
        let topic = format!("simple/{}/signal/personEntered", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the person_entered signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_person_entered_nowait(
        &mut self,
        person: Person,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = PersonEnteredSignalPayload { person };
        let topic = format!("simple/{}/signal/personEntered", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }

    /// Handles a request message for the trade_numbers method.
    async fn handle_trade_numbers_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn SimpleMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<TradeNumbersRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for trade_numbers: {:?}",
                payload_obj.err()
            );
            SimpleServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<i32, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_trade_numbers(payload.your_number)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = TradeNumbersReturnValues { my_number: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling trade_numbers: {:?}", &err);
                    SimpleServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `trade_numbers`.");
        }
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_school_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<String>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<SchoolProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the name field of the struct.
                        *write_request = new_property_structure.name.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'school' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'school' payload".to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    SchoolProperty { name: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    SchoolProperty {
                        name: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!(
                        "Error occurred while handling property update for 'school': {:?}",
                        &err
                    );
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'school'.");
        }
    }

    /// Watch for changes to the `school` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_school(&self) -> watch::Receiver<String> {
        self.properties.school.subscribe()
    }

    pub fn get_school_handle(&self) -> WriteRequestLockWatch<String> {
        self.properties.school.write_request()
    }

    /// Sets the value of the school property.
    pub async fn set_school(&mut self, value: String) -> SentMessageFuture {
        let write_request_lock = self.get_school_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// Starts the tasks that process messages received.
    /// In the task, it loops over messages received from the rx side of the message_receiver channel.
    /// Based on the subscription id of the received message, it will call a function to handle the
    /// received message.
    pub async fn run_loop(&mut self) -> Result<(), JoinError>
    where
        C: 'static,
    {
        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = {
            self.msg_streamer_rx
                .lock()
                .unwrap()
                .take()
                .expect("msg_streamer_rx should be Some")
        };

        let method_handlers = self.method_handlers.clone();
        let _ = self
            .method_handlers
            .lock()
            .await
            .initialize(self.clone())
            .await;
        let sub_ids = self.subscription_ids.clone();
        let publisher = self.mqtt_client.clone();

        let props = self.properties.clone();
        {
            // Set up property change request handling task
            let instance_id_for_school_prop = self.instance_id.clone();
            let mut publisher_for_school_prop = self.mqtt_client.clone();
            let school_prop_version = props.school_version.clone();
            if let Some(mut rx_for_school_prop) = props.school.take_request_receiver() {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) = rx_for_school_prop.recv().await {
                        let payload_obj = SchoolProperty {
                            name: request.clone(),
                        };

                        let version_value =
                            school_prop_version.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "simple/{}/property/school/value",
                            instance_id_for_school_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_school_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'school' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'school' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        // Spawn a task to periodically publish interface info.
        let mut interface_publisher = self.mqtt_client.clone();
        let instance_id = self.instance_id.clone();
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(std::time::Duration::from_secs(120));
            loop {
                interval.tick().await;
                let topic = format!("simple/{}/interface", instance_id);
                let info = crate::interface::InterfaceInfoBuilder::default()
                    .interface_name("Simple".to_string())
                    .title("Simple Example Interface".to_string())
                    .version("0.0.1".to_string())
                    .instance(instance_id.clone())
                    .connection_topic(topic.clone())
                    .build()
                    .unwrap();
                let msg = message::interface_online(&topic, &info, 150 /*seconds*/).unwrap();
                let _ = interface_publisher.publish(msg).await;
            }
        });

        let properties = self.properties.clone();
        let loop_task = tokio::spawn(async move {
            loop {
                match message_receiver.recv().await {
                    Ok(msg) => {
                        if let Some(subscription_id) = msg.subscription_id {
                            match subscription_id {
                                _i if _i == sub_ids.trade_numbers_method_req => {
                                    debug!("Received trade_numbers method invocation message.");
                                    SimpleServer::<C>::handle_trade_numbers_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.school_property_update => {
                                    debug!("Received school property update request message.");
                                    SimpleServer::<C>::update_school_value(
                                        publisher.clone(),
                                        properties.school.clone(),
                                        properties.school_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _ => {
                                    error!(
                                        "Received MQTT message with unknown subscription id: {}",
                                        subscription_id
                                    );
                                }
                            }
                        } else {
                            warn!("Received MQTT message without subscription id; cannot process.");
                        }
                    }
                    Err(e) => {
                        warn!("Error receiving MQTT message in server loop: {:?}", e);
                    }
                }
            }
        });

        let _ = tokio::join!(loop_task);

        warn!("Server receive loop completed. Exiting run_loop.");
        Ok(())
    }
}

#[async_trait]
pub trait SimpleMethodHandlers<C: Mqtt5PubSub>: Send + Sync {
    async fn initialize(&mut self, server: SimpleServer<C>) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the trade_numbers method request.
    async fn handle_trade_numbers(&self, your_number: i32) -> Result<i32, MethodReturnCode>;

    fn as_any(&self) -> &dyn Any;
}
