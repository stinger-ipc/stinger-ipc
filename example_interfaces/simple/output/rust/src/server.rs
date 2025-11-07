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

use std::sync::atomic::{AtomicU32, Ordering};

use std::future::Future;
use std::pin::Pin;
use stinger_mqtt_trait::message::{MqttMessage, QoS};
use stinger_mqtt_trait::{Mqtt5PubSub, Mqtt5PubSubError, MqttPublishSuccess};
use tokio::task::JoinError;
type SentMessageFuture = Pin<Box<dyn Future<Output = Result<(), MethodReturnCode>> + Send>>;
use crate::message;
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
    school: Arc<AsyncMutex<Option<SchoolProperty>>>,
    school_tx_channel: watch::Sender<Option<String>>,
    school_version: Arc<AtomicU32>,
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
}

impl<C: Mqtt5PubSub + Clone + Send> SimpleServer<C> {
    pub async fn new(
        mut connection: C,
        method_handlers: Arc<AsyncMutex<Box<dyn SimpleMethodHandlers<C>>>>,
        instance_id: String,
    ) -> Self {
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
            school: Arc::new(AsyncMutex::new(None)),
            school_tx_channel: watch::channel(None).0,
            school_version: Arc::new(AtomicU32::new(0)),
        };

        SimpleServer {
            mqtt_client: connection.clone(),

            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,
            method_handlers,
            properties: property_values,
            subscription_ids: sub_ids,

            client_id: connection.get_client_id(),
            instance_id,
        }
    }

    pub async fn oneshot_to_future(
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

    pub async fn wrap_return_code_in_future(rc: MethodReturnCode) -> SentMessageFuture {
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

    async fn publish_school_value(
        mut publisher: C,
        topic: String,
        data: SchoolProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        SimpleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_school_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<SchoolProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<String>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: SchoolProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!(
                        "Failed to parse JSON received over MQTT to update 'school' property: {:?}",
                        e
                    );
                    return SimpleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'school' payload".to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.name.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'school' property: {:?}",
                    e
                );
            }
        };

        SimpleServer::publish_school_value(publisher, topic2, new_property_structure, new_version)
            .await
    }

    pub async fn watch_school(&self) -> watch::Receiver<Option<String>> {
        self.properties.school_tx_channel.subscribe()
    }

    /// Sets the value of the school property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_school(&mut self, data: String) -> SentMessageFuture {
        let prop = self.properties.school.clone();

        let new_prop_obj = SchoolProperty { name: data.clone() };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .school_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'school' value not changed, so not notifying watchers.");
            SimpleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None)).await
        } else if let Some(prop_obj) = property_obj {
            let publisher2 = self.mqtt_client.clone();
            let topic2 = format!("simple/{}/property/school/value", self.instance_id);
            let new_version = self
                .properties
                .school_version
                .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            SimpleServer::<C>::publish_school_value(publisher2, topic2, prop_obj, new_version).await
        } else {
            SimpleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                "Could not find property object".to_string(),
            ))
            .await
        }
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

        let properties = self.properties.clone();

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

        let instance_id = self.instance_id.clone();
        let loop_task = tokio::spawn(async move {
            loop {
                match message_receiver.recv().await {
                    Ok(msg) => {
                        let opt_resp_topic = msg.response_topic.clone();
                        let opt_corr_data = msg.correlation_data.clone();

                        if let Some(subscription_id) = msg.subscription_id {
                            if subscription_id == sub_ids.trade_numbers_method_req {
                                SimpleServer::<C>::handle_trade_numbers_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else {
                                let update_prop_future = {
                                    if subscription_id == sub_ids.school_property_update {
                                        let prop_topic =
                                            format!("simple/{}/property/school/value", instance_id);
                                        SimpleServer::<C>::update_school_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.school.clone(),
                                            properties.school_version.clone(),
                                            properties.school_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else {
                                        SimpleServer::<C>::wrap_return_code_in_future(
                                            MethodReturnCode::NotImplemented(
                                                "Could not find a property matching the request"
                                                    .to_string(),
                                            ),
                                        )
                                        .await
                                    }
                                };
                                match update_prop_future.await {
                                    Ok(_) => debug!("Successfully processed update  property"),
                                    Err(e) => {
                                        error!("Error processing update to '' property: {:?}", e);
                                        if let Some(resp_topic) = opt_resp_topic {
                                            SimpleServer::<C>::publish_error_response(
                                                publisher.clone(),
                                                Some(resp_topic),
                                                opt_corr_data,
                                                e,
                                            )
                                            .await;
                                        } else {
                                            warn!("No response topic found in message properties; cannot send error response.");
                                        }
                                    }
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
