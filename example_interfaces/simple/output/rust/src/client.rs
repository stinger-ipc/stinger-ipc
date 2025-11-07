//! Client module for Simple IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/
use crate::discovery::DiscoveredService;
use crate::message;
#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
#[allow(unused_imports)]
use iso8601_duration::Duration as IsoDuration;
use serde_json;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use stinger_mqtt_trait::message::{MqttMessage, QoS};
#[cfg(feature = "client")]
use stinger_mqtt_trait::Mqtt5PubSub;
use tokio::sync::{broadcast, oneshot, watch};
use tokio::task::JoinError;
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};
use uuid::Uuid;

use std::sync::atomic::{AtomicU32, Ordering};
#[allow(unused_imports)]
use stinger_rwlock_watch::ReadOnlyLockWatch;
use stinger_rwlock_watch::RwLockWatch;
#[allow(unused_imports)]
use stinger_rwlock_watch::WriteRequestLockWatch;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct SimpleSubscriptionIds {
    trade_numbers_method_resp: u32,

    person_entered_signal: Option<u32>,
    school_property_value: u32,
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When SimpleClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct SimpleSignalChannels {
    person_entered_sender: broadcast::Sender<Person>,
}

#[derive(Clone)]
struct SimpleProperties {
    pub school: Arc<RwLockWatch<String>>,
    pub school_version: Arc<AtomicU32>,
}

/// This is the struct for our API client.
#[derive(Clone)]
pub struct SimpleClient<C: Mqtt5PubSub> {
    mqtt_client: C,
    /// Temporarily holds oneshot channels for responses to method calls.
    pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<MethodReturnCode>>>>,

    /// Temporarily holds the receiver for the broadcast channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<broadcast::Receiver<MqttMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: broadcast::Sender<MqttMessage>,

    /// Struct contains all the properties.
    properties: SimpleProperties,

    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: SimpleSubscriptionIds,
    /// Holds the channels used for sending signals to the application.
    signal_channels: SimpleSignalChannels,

    /// Copy of MQTT Client ID
    pub client_id: String,

    /// Instance ID of the server
    service_instance_id: String,
}

impl<C: Mqtt5PubSub + Clone + Send + 'static> SimpleClient<C> {
    /// Creates a new SimpleClient that uses an Mqtt5PubSub.
    pub async fn new(mut connection: C, discovery_info: DiscoveredService) -> Self {
        // Create a channel for messages to get from the Connection object to this SimpleClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = broadcast::channel(64);

        let client_id = connection.get_client_id();

        let topic_trade_numbers_method_resp =
            format!("client/{}/trade_numbers/response", client_id);
        let subscription_id_trade_numbers_method_resp = connection
            .subscribe(
                topic_trade_numbers_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_trade_numbers_method_resp =
            subscription_id_trade_numbers_method_resp.unwrap_or(u32::MAX);
        debug!(
            "Subscription (id={}) to method response topic for 'trade_numbers'",
            subscription_id_trade_numbers_method_resp
        );

        // Subscribe to all the topics needed for signals.
        let topic_person_entered_signal = format!(
            "simple/{}/signal/personEntered",
            discovery_info.interface_info.instance
        );
        let subscription_id_person_entered_signal = connection
            .subscribe(
                topic_person_entered_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_person_entered_signal =
            subscription_id_person_entered_signal.unwrap_or(u32::MAX);
        debug!(
            "Subscription (id={}) to signal topic for 'person_entered'",
            subscription_id_person_entered_signal
        );

        // Subscribe to all the topics needed for properties.

        let topic_school_property_value = format!(
            "simple/{}/property/school/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_school_property_value = connection
            .subscribe(
                topic_school_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_school_property_value =
            subscription_id_school_property_value.unwrap_or(u32::MAX);
        debug!(
            "Subscription (id={}) to property value topic for 'school'",
            subscription_id_school_property_value
        );

        let property_values = SimpleProperties {
            school: Arc::new(RwLockWatch::new(discovery_info.properties.school)),
            school_version: Arc::new(AtomicU32::new(discovery_info.properties.school_version)),
        };

        // Create structure for subscription ids.
        let sub_ids = SimpleSubscriptionIds {
            trade_numbers_method_resp: subscription_id_trade_numbers_method_resp,
            person_entered_signal: Some(subscription_id_person_entered_signal),
            school_property_value: subscription_id_school_property_value,
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = SimpleSignalChannels {
            person_entered_sender: broadcast::channel(64).0,
        };

        // Create SimpleClient structure.
        SimpleClient {
            mqtt_client: connection,
            pending_responses: Arc::new(Mutex::new(HashMap::new())),
            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,

            properties: property_values,

            subscription_ids: sub_ids,
            signal_channels,
            client_id,

            service_instance_id: discovery_info.interface_info.instance,
        }
    }

    /// Get the RX receiver side of the broadcast channel for the person_entered signal.
    /// The signal payload, `PersonEnteredSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_person_entered_receiver(&self) -> broadcast::Receiver<Person> {
        self.signal_channels.person_entered_sender.subscribe()
    }

    async fn start_trade_numbers(
        &mut self,
        your_number: i32,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id, sender);
        }

        let data = TradeNumbersRequestObject { your_number };

        let response_topic: String = format!("client/{}/trade_numbers/response", self.client_id);
        let msg = message::request(
            &format!("simple/{}/method/tradeNumbers", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        info!(
            "Sending request to topic '{}': {:?}",
            format!("simple/{}/method/tradeNumbers", self.service_instance_id),
            data
        );
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `trade_numbers` method.
    /// Method arguments are packed into a TradeNumbersRequestObject structure
    /// and published to the `simple/{}/method/tradeNumbers` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn trade_numbers(&mut self, your_number: i32) -> Result<i32, MethodReturnCode> {
        let receiver = self.start_trade_numbers(your_number).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        info!(
            "Received response for method 'trade_numbers': {:?}",
            return_code
        );
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: TradeNumbersReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.my_number)
            }
            _ => Err(return_code),
        }
    }

    /// Watch for changes to the `school` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_school(&self) -> watch::Receiver<String> {
        self.properties.school.subscribe()
    }

    /// Sets the `school` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_school(&mut self, value: String) -> MethodReturnCode {
        let data = SchoolProperty { name: value };
        let topic: String = format!(
            "simple/{}/property/school/setValue",
            self.service_instance_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties.school_version.load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_school_handle(&self) -> Arc<WriteRequestLockWatch<String>> {
        self.properties.school.write_request().into()
    }

    fn get_return_code_from_message(msg: &MqttMessage) -> MethodReturnCode {
        let payload = String::from_utf8_lossy(&msg.payload).to_string();
        let mut return_code: MethodReturnCode = MethodReturnCode::Success(Some(payload));
        if let Some(retval) = msg.user_properties.get("ReturnCode") {
            let opt_dbg_info = msg.user_properties.get("DebugInfo").cloned();
            if let Ok(return_code_u32) = retval.parse::<u32>() {
                if return_code_u32 != 0 {
                    return_code = MethodReturnCode::from_code(return_code_u32, opt_dbg_info);
                } else {
                    info!("Received Debug Info: {:?}", opt_dbg_info);
                }
            }
        }
        return_code
    }

    /// Starts the tasks that process messages received.
    pub async fn run_loop(&mut self) -> Result<(), JoinError> {
        // Clone the Arc pointer to the map.  This will be moved into the loop_task.
        let resp_map: Arc<Mutex<HashMap<Uuid, oneshot::Sender<MethodReturnCode>>>> =
            self.pending_responses.clone();

        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = {
            let mut guard = self.msg_streamer_rx.lock().expect("Mutex was poisoned");
            guard.take().expect("msg_streamer_rx should be Some")
        };

        let sig_chans = self.signal_channels.clone();

        let sub_ids = self.subscription_ids.clone();
        let props = self.properties.clone();
        {
            // Set up property change request handling task
            let instance_id_for_school_prop = self.service_instance_id.clone();
            let mut publisher_for_school_prop = self.mqtt_client.clone();
            let school_prop_version = props.school_version.clone();
            if let Some(mut rx_for_school_prop) = props.school.take_request_receiver() {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_school_prop.recv().await {
                        let payload_obj = SchoolProperty { name: request };

                        let topic: String = format!(
                            "simple/{}/property/school/setValue",
                            instance_id_for_school_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &payload_obj,
                            school_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_school_prop.publish(msg).await;
                    }
                });
            }
        }

        let _loop_task = tokio::spawn(async move {
            while let Ok(msg) = message_receiver.recv().await {
                let opt_corr_id: Option<Uuid> = msg.correlation_data.as_ref().and_then(|b| {
                    // Try parsing as 16-byte binary UUID first
                    if b.len() == 16 {
                        Uuid::from_slice(b.as_ref()).ok()
                    } else {
                        // Try parsing as string UUID (36 bytes for hyphenated format)
                        String::from_utf8(b.to_vec())
                            .ok()
                            .and_then(|s| Uuid::parse_str(&s).ok())
                    }
                });

                if let Some(subscription_id) = msg.subscription_id {
                    let return_code = SimpleClient::<C>::get_return_code_from_message(&msg);
                    if subscription_id == sub_ids.trade_numbers_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                if oss.send(return_code.clone()).is_err() {
                                    warn!("Failed to send method response for 'trade_numbers' to waiting receiver");
                                }
                            }
                        } else {
                            warn!("Received method response for 'trade_numbers' without correlation ID");
                        }
                    } // end trade_numbers method response handling
                    if Some(subscription_id) == sub_ids.person_entered_signal {
                        let chan = sig_chans.person_entered_sender.clone();

                        match serde_json::from_slice::<PersonEnteredSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.person);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into PersonEnteredSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    } // end person_entered signal handling

                    if subscription_id == sub_ids.school_property_value {
                        match serde_json::from_slice::<SchoolProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.school.write().await;

                                *guard = pl.name.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.school_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    } // end school property value update
                }
            }
        });

        Ok(())
    }
}
