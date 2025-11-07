//! Client module for Full IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.

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
struct FullSubscriptionIds {
    add_numbers_method_resp: u32,
    do_something_method_resp: u32,
    echo_method_resp: u32,
    what_time_is_it_method_resp: u32,
    set_the_time_method_resp: u32,
    forward_time_method_resp: u32,
    how_off_is_the_clock_method_resp: u32,

    today_is_signal: Option<u32>,
    favorite_number_property_value: u32,
    favorite_foods_property_value: u32,
    lunch_menu_property_value: u32,
    family_name_property_value: u32,
    last_breakfast_time_property_value: u32,
    breakfast_length_property_value: u32,
    last_birthdays_property_value: u32,
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When FullClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct FullSignalChannels {
    today_is_sender: broadcast::Sender<TodayIsSignalPayload>,
}

#[derive(Clone)]
struct FullProperties {
    pub favorite_number: Arc<RwLockWatch<i32>>,
    pub favorite_number_version: Arc<AtomicU32>,

    pub favorite_foods: Arc<RwLockWatch<FavoriteFoodsProperty>>,
    pub favorite_foods_version: Arc<AtomicU32>,

    pub lunch_menu: Arc<RwLockWatch<LunchMenuProperty>>,
    pub lunch_menu_version: Arc<AtomicU32>,

    pub family_name: Arc<RwLockWatch<String>>,
    pub family_name_version: Arc<AtomicU32>,

    pub last_breakfast_time: Arc<RwLockWatch<chrono::DateTime<chrono::Utc>>>,
    pub last_breakfast_time_version: Arc<AtomicU32>,

    pub breakfast_length: Arc<RwLockWatch<chrono::Duration>>,
    pub breakfast_length_version: Arc<AtomicU32>,

    pub last_birthdays: Arc<RwLockWatch<LastBirthdaysProperty>>,
    pub last_birthdays_version: Arc<AtomicU32>,
}

/// This is the struct for our API client.
#[derive(Clone)]
pub struct FullClient<C: Mqtt5PubSub> {
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
    properties: FullProperties,

    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: FullSubscriptionIds,
    /// Holds the channels used for sending signals to the application.
    signal_channels: FullSignalChannels,

    /// Copy of MQTT Client ID
    pub client_id: String,

    /// Instance ID of the server
    service_instance_id: String,
}

impl<C: Mqtt5PubSub + Clone + Send + 'static> FullClient<C> {
    /// Creates a new FullClient that uses an Mqtt5PubSub.
    pub async fn new(mut connection: C, discovery_info: DiscoveredService) -> Self {
        // Create a channel for messages to get from the Connection object to this FullClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = broadcast::channel(64);

        let client_id = connection.get_client_id();

        let topic_add_numbers_method_resp = format!("client/{}/addNumbers/response", client_id);
        let subscription_id_add_numbers_method_resp = connection
            .subscribe(
                topic_add_numbers_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_add_numbers_method_resp =
            subscription_id_add_numbers_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_do_something_method_resp = format!("client/{}/doSomething/response", client_id);
        let subscription_id_do_something_method_resp = connection
            .subscribe(
                topic_do_something_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_do_something_method_resp =
            subscription_id_do_something_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_echo_method_resp = format!("client/{}/echo/response", client_id);
        let subscription_id_echo_method_resp = connection
            .subscribe(
                topic_echo_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_echo_method_resp =
            subscription_id_echo_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_what_time_is_it_method_resp =
            format!("client/{}/what_time_is_it/response", client_id);
        let subscription_id_what_time_is_it_method_resp = connection
            .subscribe(
                topic_what_time_is_it_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_what_time_is_it_method_resp =
            subscription_id_what_time_is_it_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_set_the_time_method_resp = format!("client/{}/set_the_time/response", client_id);
        let subscription_id_set_the_time_method_resp = connection
            .subscribe(
                topic_set_the_time_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_set_the_time_method_resp =
            subscription_id_set_the_time_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_forward_time_method_resp = format!("client/{}/forward_time/response", client_id);
        let subscription_id_forward_time_method_resp = connection
            .subscribe(
                topic_forward_time_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_forward_time_method_resp =
            subscription_id_forward_time_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_how_off_is_the_clock_method_resp =
            format!("client/{}/how_off_is_the_clock/response", client_id);
        let subscription_id_how_off_is_the_clock_method_resp = connection
            .subscribe(
                topic_how_off_is_the_clock_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_how_off_is_the_clock_method_resp =
            subscription_id_how_off_is_the_clock_method_resp.unwrap_or_else(|_| u32::MAX);

        // Subscribe to all the topics needed for signals.
        let topic_today_is_signal = format!(
            "full/{}/signal/todayIs",
            discovery_info.interface_info.instance
        );
        let subscription_id_today_is_signal = connection
            .subscribe(
                topic_today_is_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_today_is_signal =
            subscription_id_today_is_signal.unwrap_or_else(|_| u32::MAX);

        // Subscribe to all the topics needed for properties.

        let topic_favorite_number_property_value = format!(
            "full/{}/property/favoriteNumber/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_favorite_number_property_value = connection
            .subscribe(
                topic_favorite_number_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_number_property_value =
            subscription_id_favorite_number_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_favorite_foods_property_value = format!(
            "full/{}/property/favoriteFoods/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_favorite_foods_property_value = connection
            .subscribe(
                topic_favorite_foods_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_foods_property_value =
            subscription_id_favorite_foods_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_lunch_menu_property_value = format!(
            "full/{}/property/lunchMenu/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_lunch_menu_property_value = connection
            .subscribe(
                topic_lunch_menu_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_lunch_menu_property_value =
            subscription_id_lunch_menu_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_family_name_property_value = format!(
            "full/{}/property/familyName/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_family_name_property_value = connection
            .subscribe(
                topic_family_name_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_family_name_property_value =
            subscription_id_family_name_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_last_breakfast_time_property_value = format!(
            "full/{}/property/lastBreakfastTime/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_last_breakfast_time_property_value = connection
            .subscribe(
                topic_last_breakfast_time_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_last_breakfast_time_property_value =
            subscription_id_last_breakfast_time_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_breakfast_length_property_value = format!(
            "full/{}/property/breakfastLength/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_breakfast_length_property_value = connection
            .subscribe(
                topic_breakfast_length_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_breakfast_length_property_value =
            subscription_id_breakfast_length_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_last_birthdays_property_value = format!(
            "full/{}/property/lastBirthdays/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_last_birthdays_property_value = connection
            .subscribe(
                topic_last_birthdays_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_last_birthdays_property_value =
            subscription_id_last_birthdays_property_value.unwrap_or_else(|_| u32::MAX);

        let property_values = FullProperties {
            favorite_number: Arc::new(RwLockWatch::new(discovery_info.properties.favorite_number)),
            favorite_number_version: Arc::new(AtomicU32::new(
                discovery_info.properties.favorite_number_version,
            )),
            favorite_foods: Arc::new(RwLockWatch::new(discovery_info.properties.favorite_foods)),
            favorite_foods_version: Arc::new(AtomicU32::new(
                discovery_info.properties.favorite_foods_version,
            )),
            lunch_menu: Arc::new(RwLockWatch::new(discovery_info.properties.lunch_menu)),
            lunch_menu_version: Arc::new(AtomicU32::new(
                discovery_info.properties.lunch_menu_version,
            )),

            family_name: Arc::new(RwLockWatch::new(discovery_info.properties.family_name)),
            family_name_version: Arc::new(AtomicU32::new(
                discovery_info.properties.family_name_version,
            )),

            last_breakfast_time: Arc::new(RwLockWatch::new(
                discovery_info.properties.last_breakfast_time,
            )),
            last_breakfast_time_version: Arc::new(AtomicU32::new(
                discovery_info.properties.last_breakfast_time_version,
            )),

            breakfast_length: Arc::new(RwLockWatch::new(
                discovery_info.properties.breakfast_length,
            )),
            breakfast_length_version: Arc::new(AtomicU32::new(
                discovery_info.properties.breakfast_length_version,
            )),
            last_birthdays: Arc::new(RwLockWatch::new(discovery_info.properties.last_birthdays)),
            last_birthdays_version: Arc::new(AtomicU32::new(
                discovery_info.properties.last_birthdays_version,
            )),
        };

        // Create structure for subscription ids.
        let sub_ids = FullSubscriptionIds {
            add_numbers_method_resp: subscription_id_add_numbers_method_resp,
            do_something_method_resp: subscription_id_do_something_method_resp,
            echo_method_resp: subscription_id_echo_method_resp,
            what_time_is_it_method_resp: subscription_id_what_time_is_it_method_resp,
            set_the_time_method_resp: subscription_id_set_the_time_method_resp,
            forward_time_method_resp: subscription_id_forward_time_method_resp,
            how_off_is_the_clock_method_resp: subscription_id_how_off_is_the_clock_method_resp,
            today_is_signal: Some(subscription_id_today_is_signal),
            favorite_number_property_value: subscription_id_favorite_number_property_value,
            favorite_foods_property_value: subscription_id_favorite_foods_property_value,
            lunch_menu_property_value: subscription_id_lunch_menu_property_value,
            family_name_property_value: subscription_id_family_name_property_value,
            last_breakfast_time_property_value: subscription_id_last_breakfast_time_property_value,
            breakfast_length_property_value: subscription_id_breakfast_length_property_value,
            last_birthdays_property_value: subscription_id_last_birthdays_property_value,
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = FullSignalChannels {
            today_is_sender: broadcast::channel(64).0,
        };

        // Create FullClient structure.
        let inst = FullClient {
            mqtt_client: connection,
            pending_responses: Arc::new(Mutex::new(HashMap::new())),
            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,

            properties: property_values,

            subscription_ids: sub_ids,
            signal_channels: signal_channels,
            client_id: client_id,

            service_instance_id: discovery_info.interface_info.instance,
        };
        inst
    }

    /// Get the RX receiver side of the broadcast channel for the todayIs signal.
    /// The signal payload, `TodayIsSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_today_is_receiver(&self) -> broadcast::Receiver<TodayIsSignalPayload> {
        self.signal_channels.today_is_sender.subscribe()
    }

    async fn start_add_numbers(
        &mut self,
        first: i32,
        second: i32,
        third: Option<i32>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = AddNumbersRequestObject {
            first: first,
            second: second,
            third: third,
        };

        let response_topic: String = format!("client/{}/addNumbers/response", self.client_id);
        let msg = message::request(
            &format!("full/{}/method/addNumbers", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `addNumbers` method.
    /// Method arguments are packed into a AddNumbersRequestObject structure
    /// and published to the `full/{}/method/addNumbers` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn add_numbers(
        &mut self,
        first: i32,
        second: i32,
        third: Option<i32>,
    ) -> Result<i32, MethodReturnCode> {
        let receiver = self.start_add_numbers(first, second, third).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: AddNumbersReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.sum)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_do_something(
        &mut self,
        a_string: String,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = DoSomethingRequestObject { a_string: a_string };

        let response_topic: String = format!("client/{}/doSomething/response", self.client_id);
        let msg = message::request(
            &format!("full/{}/method/doSomething", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `doSomething` method.
    /// Method arguments are packed into a DoSomethingRequestObject structure
    /// and published to the `full/{}/method/doSomething` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn do_something(
        &mut self,
        a_string: String,
    ) -> Result<DoSomethingReturnValues, MethodReturnCode> {
        let receiver = self.start_do_something(a_string).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: DoSomethingReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_echo(&mut self, message: String) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = EchoRequestObject { message: message };

        let response_topic: String = format!("client/{}/echo/response", self.client_id);
        let msg = message::request(
            &format!("full/{}/method/echo", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `echo` method.
    /// Method arguments are packed into a EchoRequestObject structure
    /// and published to the `full/{}/method/echo` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn echo(&mut self, message: String) -> Result<String, MethodReturnCode> {
        let receiver = self.start_echo(message).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: EchoReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.message)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_what_time_is_it(
        &mut self,
        the_first_time: chrono::DateTime<chrono::Utc>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = WhatTimeIsItRequestObject {
            the_first_time: the_first_time,
        };

        let response_topic: String = format!("client/{}/what_time_is_it/response", self.client_id);
        let msg = message::request(
            &format!("full/{}/method/whatTimeIsIt", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `what_time_is_it` method.
    /// Method arguments are packed into a WhatTimeIsItRequestObject structure
    /// and published to the `full/{}/method/whatTimeIsIt` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn what_time_is_it(
        &mut self,
        the_first_time: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> {
        let receiver = self.start_what_time_is_it(the_first_time).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: WhatTimeIsItReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.timestamp)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_set_the_time(
        &mut self,
        the_first_time: chrono::DateTime<chrono::Utc>,
        the_second_time: chrono::DateTime<chrono::Utc>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = SetTheTimeRequestObject {
            the_first_time: the_first_time,
            the_second_time: the_second_time,
        };

        let response_topic: String = format!("client/{}/set_the_time/response", self.client_id);
        let msg = message::request(
            &format!("full/{}/method/setTheTime", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `set_the_time` method.
    /// Method arguments are packed into a SetTheTimeRequestObject structure
    /// and published to the `full/{}/method/setTheTime` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn set_the_time(
        &mut self,
        the_first_time: chrono::DateTime<chrono::Utc>,
        the_second_time: chrono::DateTime<chrono::Utc>,
    ) -> Result<SetTheTimeReturnValues, MethodReturnCode> {
        let receiver = self
            .start_set_the_time(the_first_time, the_second_time)
            .await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: SetTheTimeReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_forward_time(
        &mut self,
        adjustment: chrono::Duration,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = ForwardTimeRequestObject {
            adjustment: adjustment,
        };

        let response_topic: String = format!("client/{}/forward_time/response", self.client_id);
        let msg = message::request(
            &format!("full/{}/method/forwardTime", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `forward_time` method.
    /// Method arguments are packed into a ForwardTimeRequestObject structure
    /// and published to the `full/{}/method/forwardTime` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn forward_time(
        &mut self,
        adjustment: chrono::Duration,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> {
        let receiver = self.start_forward_time(adjustment).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: ForwardTimeReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.new_time)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_how_off_is_the_clock(
        &mut self,
        actual_time: chrono::DateTime<chrono::Utc>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = HowOffIsTheClockRequestObject {
            actual_time: actual_time,
        };

        let response_topic: String =
            format!("client/{}/how_off_is_the_clock/response", self.client_id);
        let msg = message::request(
            &format!("full/{}/method/howOffIsTheClock", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `how_off_is_the_clock` method.
    /// Method arguments are packed into a HowOffIsTheClockRequestObject structure
    /// and published to the `full/{}/method/howOffIsTheClock` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn how_off_is_the_clock(
        &mut self,
        actual_time: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::Duration, MethodReturnCode> {
        let receiver = self.start_how_off_is_the_clock(actual_time).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: HowOffIsTheClockReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.difference)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    /// Watch for changes to the `favorite_number` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_favorite_number(&self) -> watch::Receiver<i32> {
        self.properties.favorite_number.subscribe()
    }

    /// Sets the `favorite_number` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_favorite_number(&mut self, value: i32) -> MethodReturnCode {
        let data = FavoriteNumberProperty { number: value };
        let topic: String = format!("full/{}/property/favoriteNumber/setValue", self.client_id);
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .favorite_number_version
                .load(Ordering::Relaxed),
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

    pub fn get_favorite_number_handle(&self) -> Arc<WriteRequestLockWatch<i32>> {
        self.properties.favorite_number.write_request().into()
    }

    /// Watch for changes to the `favorite_foods` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_favorite_foods(&self) -> watch::Receiver<FavoriteFoodsProperty> {
        self.properties.favorite_foods.subscribe()
    }

    /// Sets the `favorite_foods` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_favorite_foods(&mut self, value: FavoriteFoodsProperty) -> MethodReturnCode {
        let data = value;
        let topic: String = format!("full/{}/property/favoriteFoods/setValue", self.client_id);
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .favorite_foods_version
                .load(Ordering::Relaxed),
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

    pub fn get_favorite_foods_handle(&self) -> Arc<WriteRequestLockWatch<FavoriteFoodsProperty>> {
        self.properties.favorite_foods.write_request().into()
    }

    /// Watch for changes to the `lunch_menu` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_lunch_menu(&self) -> watch::Receiver<LunchMenuProperty> {
        self.properties.lunch_menu.subscribe()
    }

    /// Sets the `lunch_menu` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_lunch_menu(&mut self, value: LunchMenuProperty) -> MethodReturnCode {
        let data = value;
        let topic: String = format!("full/{}/property/lunchMenu/setValue", self.client_id);
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties.lunch_menu_version.load(Ordering::Relaxed),
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

    pub fn get_lunch_menu_handle(&self) -> Arc<WriteRequestLockWatch<LunchMenuProperty>> {
        self.properties.lunch_menu.write_request().into()
    }

    /// Watch for changes to the `family_name` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_family_name(&self) -> watch::Receiver<String> {
        self.properties.family_name.subscribe()
    }

    /// Sets the `family_name` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_family_name(&mut self, value: String) -> MethodReturnCode {
        let data = FamilyNameProperty { family_name: value };
        let topic: String = format!("full/{}/property/familyName/setValue", self.client_id);
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties.family_name_version.load(Ordering::Relaxed),
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

    pub fn get_family_name_handle(&self) -> Arc<WriteRequestLockWatch<String>> {
        self.properties.family_name.write_request().into()
    }

    /// Watch for changes to the `last_breakfast_time` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_last_breakfast_time(&self) -> watch::Receiver<chrono::DateTime<chrono::Utc>> {
        self.properties.last_breakfast_time.subscribe()
    }

    /// Sets the `last_breakfast_time` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_last_breakfast_time(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> MethodReturnCode {
        let data = LastBreakfastTimeProperty { timestamp: value };
        let topic: String = format!(
            "full/{}/property/lastBreakfastTime/setValue",
            self.client_id
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
            self.properties
                .last_breakfast_time_version
                .load(Ordering::Relaxed),
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

    pub fn get_last_breakfast_time_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<chrono::DateTime<chrono::Utc>>> {
        self.properties.last_breakfast_time.write_request().into()
    }

    /// Watch for changes to the `breakfast_length` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_breakfast_length(&self) -> watch::Receiver<chrono::Duration> {
        self.properties.breakfast_length.subscribe()
    }

    /// Sets the `breakfast_length` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_breakfast_length(&mut self, value: chrono::Duration) -> MethodReturnCode {
        let data = BreakfastLengthProperty { length: value };
        let topic: String = format!("full/{}/property/breakfastLength/setValue", self.client_id);
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .breakfast_length_version
                .load(Ordering::Relaxed),
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

    pub fn get_breakfast_length_handle(&self) -> Arc<WriteRequestLockWatch<chrono::Duration>> {
        self.properties.breakfast_length.write_request().into()
    }

    /// Watch for changes to the `last_birthdays` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_last_birthdays(&self) -> watch::Receiver<LastBirthdaysProperty> {
        self.properties.last_birthdays.subscribe()
    }

    /// Sets the `last_birthdays` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_last_birthdays(&mut self, value: LastBirthdaysProperty) -> MethodReturnCode {
        let data = value;
        let topic: String = format!("full/{}/property/lastBirthdays/setValue", self.client_id);
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .last_birthdays_version
                .load(Ordering::Relaxed),
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

    pub fn get_last_birthdays_handle(&self) -> Arc<WriteRequestLockWatch<LastBirthdaysProperty>> {
        self.properties.last_birthdays.write_request().into()
    }

    fn get_return_code_from_message(msg: &MqttMessage) -> MethodReturnCode {
        let payload = String::from_utf8_lossy(&msg.payload).to_string();
        let mut return_code: MethodReturnCode = MethodReturnCode::Success(None);
        if let Some(retval) = msg.user_properties.get("ReturnCode") {
            let opt_dbg_info = msg.user_properties.get("DebugInfo").cloned();
            if let Ok(return_code_u32) = retval.parse::<u32>() {
                if return_code_u32 == 0 {
                    return_code = MethodReturnCode::from_code(return_code_u32, Some(payload));
                } else {
                    return_code = MethodReturnCode::from_code(return_code_u32, opt_dbg_info);
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
            let client_id_for_favorite_number_prop = self.client_id.clone();
            let mut publisher_for_favorite_number_prop = self.mqtt_client.clone();
            let favorite_number_prop_version = props.favorite_number_version.clone();
            if let Some(mut rx_for_favorite_number_prop) =
                props.favorite_number.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_favorite_number_prop.recv().await {
                        let topic: String = format!(
                            "full/{}/property/favoriteNumber/setValue",
                            client_id_for_favorite_number_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            favorite_number_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_favorite_number_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_favorite_foods_prop = self.client_id.clone();
            let mut publisher_for_favorite_foods_prop = self.mqtt_client.clone();
            let favorite_foods_prop_version = props.favorite_foods_version.clone();
            if let Some(mut rx_for_favorite_foods_prop) =
                props.favorite_foods.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_favorite_foods_prop.recv().await {
                        let topic: String = format!(
                            "full/{}/property/favoriteFoods/setValue",
                            client_id_for_favorite_foods_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            favorite_foods_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_favorite_foods_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_lunch_menu_prop = self.client_id.clone();
            let mut publisher_for_lunch_menu_prop = self.mqtt_client.clone();
            let lunch_menu_prop_version = props.lunch_menu_version.clone();
            if let Some(mut rx_for_lunch_menu_prop) = props.lunch_menu.take_request_receiver() {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_lunch_menu_prop.recv().await {
                        let topic: String = format!(
                            "full/{}/property/lunchMenu/setValue",
                            client_id_for_lunch_menu_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            lunch_menu_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_lunch_menu_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_family_name_prop = self.client_id.clone();
            let mut publisher_for_family_name_prop = self.mqtt_client.clone();
            let family_name_prop_version = props.family_name_version.clone();
            if let Some(mut rx_for_family_name_prop) = props.family_name.take_request_receiver() {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_family_name_prop.recv().await {
                        let topic: String = format!(
                            "full/{}/property/familyName/setValue",
                            client_id_for_family_name_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            family_name_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_family_name_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_last_breakfast_time_prop = self.client_id.clone();
            let mut publisher_for_last_breakfast_time_prop = self.mqtt_client.clone();
            let last_breakfast_time_prop_version = props.last_breakfast_time_version.clone();
            if let Some(mut rx_for_last_breakfast_time_prop) =
                props.last_breakfast_time.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_last_breakfast_time_prop.recv().await {
                        let topic: String = format!(
                            "full/{}/property/lastBreakfastTime/setValue",
                            client_id_for_last_breakfast_time_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            last_breakfast_time_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_last_breakfast_time_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_breakfast_length_prop = self.client_id.clone();
            let mut publisher_for_breakfast_length_prop = self.mqtt_client.clone();
            let breakfast_length_prop_version = props.breakfast_length_version.clone();
            if let Some(mut rx_for_breakfast_length_prop) =
                props.breakfast_length.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_breakfast_length_prop.recv().await {
                        let topic: String = format!(
                            "full/{}/property/breakfastLength/setValue",
                            client_id_for_breakfast_length_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            breakfast_length_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_breakfast_length_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_last_birthdays_prop = self.client_id.clone();
            let mut publisher_for_last_birthdays_prop = self.mqtt_client.clone();
            let last_birthdays_prop_version = props.last_birthdays_version.clone();
            if let Some(mut rx_for_last_birthdays_prop) =
                props.last_birthdays.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_last_birthdays_prop.recv().await {
                        let topic: String = format!(
                            "full/{}/property/lastBirthdays/setValue",
                            client_id_for_last_birthdays_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            last_birthdays_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_last_birthdays_prop.publish(msg).await;
                    }
                });
            }
        }

        let _loop_task = tokio::spawn(async move {
            while let Ok(msg) = message_receiver.recv().await {
                let opt_corr_data: Option<Vec<u8>> =
                    msg.correlation_data.clone().map(|b| b.to_vec());
                let opt_corr_id: Option<Uuid> =
                    opt_corr_data.and_then(|b| Uuid::from_slice(b.as_slice()).ok());

                if let Some(subscription_id) = msg.subscription_id {
                    let return_code = FullClient::<C>::get_return_code_from_message(&msg);
                    if subscription_id == sub_ids.add_numbers_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end addNumbers method response handling
                    else if subscription_id == sub_ids.do_something_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end doSomething method response handling
                    else if subscription_id == sub_ids.echo_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end echo method response handling
                    else if subscription_id == sub_ids.what_time_is_it_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end what_time_is_it method response handling
                    else if subscription_id == sub_ids.set_the_time_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end set_the_time method response handling
                    else if subscription_id == sub_ids.forward_time_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end forward_time method response handling
                    else if subscription_id == sub_ids.how_off_is_the_clock_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    } // end how_off_is_the_clock method response handling
                    if Some(subscription_id) == sub_ids.today_is_signal {
                        let chan = sig_chans.today_is_sender.clone();

                        match serde_json::from_slice::<TodayIsSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into TodayIsSignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    } // end todayIs signal handling

                    if subscription_id == sub_ids.favorite_number_property_value {
                        match serde_json::from_slice::<FavoriteNumberProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.favorite_number.write().await;

                                *guard = pl.number.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.favorite_number_version.store(
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
                    }
                    // end favorite_number property value update
                    else if subscription_id == sub_ids.favorite_foods_property_value {
                        match serde_json::from_slice::<FavoriteFoodsProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.favorite_foods.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.favorite_foods_version.store(
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
                    }
                    // end favorite_foods property value update
                    else if subscription_id == sub_ids.lunch_menu_property_value {
                        match serde_json::from_slice::<LunchMenuProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.lunch_menu.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.lunch_menu_version.store(
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
                    }
                    // end lunch_menu property value update
                    else if subscription_id == sub_ids.family_name_property_value {
                        match serde_json::from_slice::<FamilyNameProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.family_name.write().await;

                                *guard = pl.family_name.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.family_name_version.store(
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
                    }
                    // end family_name property value update
                    else if subscription_id == sub_ids.last_breakfast_time_property_value {
                        match serde_json::from_slice::<LastBreakfastTimeProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.last_breakfast_time.write().await;

                                *guard = pl.timestamp.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.last_breakfast_time_version.store(
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
                    }
                    // end last_breakfast_time property value update
                    else if subscription_id == sub_ids.breakfast_length_property_value {
                        match serde_json::from_slice::<BreakfastLengthProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.breakfast_length.write().await;

                                *guard = pl.length.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.breakfast_length_version.store(
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
                    }
                    // end breakfast_length property value update
                    else if subscription_id == sub_ids.last_birthdays_property_value {
                        match serde_json::from_slice::<LastBirthdaysProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.last_birthdays.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.last_birthdays_version.store(
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
                    } // end last_birthdays property value update
                }
            }
        });

        Ok(())
    }
}
