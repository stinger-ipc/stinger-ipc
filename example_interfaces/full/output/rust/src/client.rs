//! Client module for Full IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.
*/
use json::JsonValue;
#[cfg(feature = "client")]
use mqttier::{MqttierClient, ReceivedMessage};
use serde_json;
use std::collections::HashMap;
use uuid::Uuid;

#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
use iso8601_duration::Duration as IsoDuration;
use std::sync::{Arc, Mutex};
use tokio::sync::{broadcast, mpsc, oneshot, watch};
use tokio::task::JoinError;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct FullSubscriptionIds {
    add_numbers_method_resp: usize,
    do_something_method_resp: usize,
    echo_method_resp: usize,
    what_time_is_it_method_resp: usize,
    set_the_time_method_resp: usize,
    forward_time_method_resp: usize,
    how_off_is_the_clock_method_resp: usize,

    today_is_signal: Option<usize>,
    favorite_number_property_value: usize,
    favorite_foods_property_value: usize,
    lunch_menu_property_value: usize,
    family_name_property_value: usize,
    last_breakfast_time_property_value: usize,
    breakfast_length_property_value: usize,
    last_birthdays_property_value: usize,
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
pub struct FullProperties {
    pub favorite_number: Arc<Mutex<Option<i32>>>,

    favorite_number_tx_channel: watch::Sender<Option<i32>>,
    pub favorite_foods: Arc<Mutex<Option<FavoriteFoodsProperty>>>,
    favorite_foods_tx_channel: watch::Sender<Option<FavoriteFoodsProperty>>,
    pub lunch_menu: Arc<Mutex<Option<LunchMenuProperty>>>,
    lunch_menu_tx_channel: watch::Sender<Option<LunchMenuProperty>>,
    pub family_name: Arc<Mutex<Option<String>>>,

    family_name_tx_channel: watch::Sender<Option<String>>,
    pub last_breakfast_time: Arc<Mutex<Option<chrono::DateTime<chrono::Utc>>>>,

    last_breakfast_time_tx_channel: watch::Sender<Option<chrono::DateTime<chrono::Utc>>>,
    pub breakfast_length: Arc<Mutex<Option<chrono::Duration>>>,

    breakfast_length_tx_channel: watch::Sender<Option<chrono::Duration>>,
    pub last_birthdays: Arc<Mutex<Option<LastBirthdaysProperty>>>,
    last_birthdays_tx_channel: watch::Sender<Option<LastBirthdaysProperty>>,
}

/// This is the struct for our API client.
#[derive(Clone)]
pub struct FullClient {
    mqttier_client: MqttierClient,
    /// Temporarily holds oneshot channels for responses to method calls.
    pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>>,

    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<mpsc::Receiver<ReceivedMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Struct contains all the properties.
    pub properties: FullProperties,

    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: FullSubscriptionIds,
    /// Holds the channels used for sending signals to the application.
    signal_channels: FullSignalChannels,

    /// Copy of MQTT Client ID
    pub client_id: String,

    /// Instance ID of the server
    service_instance_id: String,
}

impl FullClient {
    /// Creates a new FullClient that uses an MqttierClient.
    pub async fn new(connection: &mut MqttierClient, service_id: String) -> Self {
        // Create a channel for messages to get from the Connection object to this FullClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        let topic_add_numbers_method_resp =
            format!("client/{}/addNumbers/response", connection.client_id);
        let subscription_id_add_numbers_method_resp = connection
            .subscribe(
                topic_add_numbers_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_add_numbers_method_resp =
            subscription_id_add_numbers_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_do_something_method_resp =
            format!("client/{}/doSomething/response", connection.client_id);
        let subscription_id_do_something_method_resp = connection
            .subscribe(
                topic_do_something_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_do_something_method_resp =
            subscription_id_do_something_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_echo_method_resp = format!("client/{}/echo/response", connection.client_id);
        let subscription_id_echo_method_resp = connection
            .subscribe(topic_echo_method_resp, 2, message_received_tx.clone())
            .await;
        let subscription_id_echo_method_resp =
            subscription_id_echo_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_what_time_is_it_method_resp =
            format!("client/{}/what_time_is_it/response", connection.client_id);
        let subscription_id_what_time_is_it_method_resp = connection
            .subscribe(
                topic_what_time_is_it_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_what_time_is_it_method_resp =
            subscription_id_what_time_is_it_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_set_the_time_method_resp =
            format!("client/{}/set_the_time/response", connection.client_id);
        let subscription_id_set_the_time_method_resp = connection
            .subscribe(
                topic_set_the_time_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_set_the_time_method_resp =
            subscription_id_set_the_time_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_forward_time_method_resp =
            format!("client/{}/forward_time/response", connection.client_id);
        let subscription_id_forward_time_method_resp = connection
            .subscribe(
                topic_forward_time_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_forward_time_method_resp =
            subscription_id_forward_time_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_how_off_is_the_clock_method_resp = format!(
            "client/{}/how_off_is_the_clock/response",
            connection.client_id
        );
        let subscription_id_how_off_is_the_clock_method_resp = connection
            .subscribe(
                topic_how_off_is_the_clock_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_how_off_is_the_clock_method_resp =
            subscription_id_how_off_is_the_clock_method_resp.unwrap_or_else(|_| usize::MAX);

        // Subscribe to all the topics needed for signals.
        let topic_today_is_signal = format!("full/{}/signal/todayIs", service_id);
        let subscription_id_today_is_signal = connection
            .subscribe(topic_today_is_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_today_is_signal =
            subscription_id_today_is_signal.unwrap_or_else(|_| usize::MAX);

        // Subscribe to all the topics needed for properties.

        let topic_favorite_number_property_value =
            format!("full/{}/property/favoriteNumber/value", service_id);
        let subscription_id_favorite_number_property_value = connection
            .subscribe(
                topic_favorite_number_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_number_property_value =
            subscription_id_favorite_number_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_favorite_foods_property_value =
            format!("full/{}/property/favoriteFoods/value", service_id);
        let subscription_id_favorite_foods_property_value = connection
            .subscribe(
                topic_favorite_foods_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_foods_property_value =
            subscription_id_favorite_foods_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_lunch_menu_property_value =
            format!("full/{}/property/lunchMenu/value", service_id);
        let subscription_id_lunch_menu_property_value = connection
            .subscribe(
                topic_lunch_menu_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_lunch_menu_property_value =
            subscription_id_lunch_menu_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_family_name_property_value =
            format!("full/{}/property/familyName/value", service_id);
        let subscription_id_family_name_property_value = connection
            .subscribe(
                topic_family_name_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_family_name_property_value =
            subscription_id_family_name_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_last_breakfast_time_property_value =
            format!("full/{}/property/lastBreakfastTime/value", service_id);
        let subscription_id_last_breakfast_time_property_value = connection
            .subscribe(
                topic_last_breakfast_time_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_last_breakfast_time_property_value =
            subscription_id_last_breakfast_time_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_breakfast_length_property_value =
            format!("full/{}/property/breakfastLength/value", service_id);
        let subscription_id_breakfast_length_property_value = connection
            .subscribe(
                topic_breakfast_length_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_breakfast_length_property_value =
            subscription_id_breakfast_length_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_last_birthdays_property_value =
            format!("full/{}/property/lastBirthdays/value", service_id);
        let subscription_id_last_birthdays_property_value = connection
            .subscribe(
                topic_last_birthdays_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_last_birthdays_property_value =
            subscription_id_last_birthdays_property_value.unwrap_or_else(|_| usize::MAX);

        let property_values = FullProperties {
            favorite_number: Arc::new(Mutex::new(None)),
            favorite_number_tx_channel: watch::channel(None).0,
            favorite_foods: Arc::new(Mutex::new(None)),
            favorite_foods_tx_channel: watch::channel(None).0,
            lunch_menu: Arc::new(Mutex::new(None)),
            lunch_menu_tx_channel: watch::channel(None).0,

            family_name: Arc::new(Mutex::new(None)),
            family_name_tx_channel: watch::channel(None).0,

            last_breakfast_time: Arc::new(Mutex::new(None)),
            last_breakfast_time_tx_channel: watch::channel(None).0,

            breakfast_length: Arc::new(Mutex::new(None)),
            breakfast_length_tx_channel: watch::channel(None).0,
            last_birthdays: Arc::new(Mutex::new(None)),
            last_birthdays_tx_channel: watch::channel(None).0,
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
            mqttier_client: connection.clone(),
            pending_responses: Arc::new(Mutex::new(HashMap::new())),
            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,

            properties: property_values,

            subscription_ids: sub_ids,
            signal_channels: signal_channels,
            client_id: connection.client_id.to_string(),
            service_instance_id: service_id,
        };
        inst
    }

    /// Get the RX receiver side of the broadcast channel for the todayIs signal.
    /// The signal payload, `TodayIsSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_today_is_receiver(&self) -> broadcast::Receiver<TodayIsSignalPayload> {
        self.signal_channels.today_is_sender.subscribe()
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
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
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
        let _ = self
            .mqttier_client
            .publish_request(
                format!("full/{}/method/addNumbers", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        let resp_obj = receiver.await.unwrap();

        Ok(resp_obj["sum"].as_i32().unwrap())
    }

    /// Handler for responses to `addNumbers` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_add_numbers_response(
        pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>>,
        payload: String,
        opt_correlation_id: Option<Uuid>,
    ) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.and_then(|uuid| {
                let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                hashmap.remove(&uuid)
            });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
    }
    /// The `doSomething` method.
    /// Method arguments are packed into a DoSomethingRequestObject structure
    /// and published to the `full/{}/method/doSomething` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn do_something(
        &mut self,
        a_string: String,
    ) -> Result<DoSomethingReturnValue, MethodReturnCode> {
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = DoSomethingRequestObject { aString: a_string };

        let response_topic: String = format!("client/{}/doSomething/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!("full/{}/method/doSomething", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        let resp_obj = receiver.await.unwrap();
        Ok(DoSomethingReturnValue {
            label: resp_obj["label"].as_str().unwrap().to_string(),

            identifier: resp_obj["identifier"].as_i32().unwrap(),

            day: DayOfTheWeek::from_u32(resp_obj["day"].as_u32().unwrap()).unwrap(),
        })
    }

    /// Handler for responses to `doSomething` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_do_something_response(
        pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>>,
        payload: String,
        opt_correlation_id: Option<Uuid>,
    ) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.and_then(|uuid| {
                let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                hashmap.remove(&uuid)
            });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
    }
    /// The `echo` method.
    /// Method arguments are packed into a EchoRequestObject structure
    /// and published to the `full/{}/method/echo` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn echo(&mut self, message: String) -> Result<String, MethodReturnCode> {
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = EchoRequestObject { message: message };

        let response_topic: String = format!("client/{}/echo/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!("full/{}/method/echo", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        let resp_obj = receiver.await.unwrap();

        Ok(resp_obj["message"].as_str().unwrap().to_string())
    }

    /// Handler for responses to `echo` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_echo_response(
        pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>>,
        payload: String,
        opt_correlation_id: Option<Uuid>,
    ) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.and_then(|uuid| {
                let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                hashmap.remove(&uuid)
            });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
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
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = WhatTimeIsItRequestObject {
            the_first_time: the_first_time,
        };

        let response_topic: String = format!("client/{}/what_time_is_it/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!("full/{}/method/whatTimeIsIt", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        let resp_obj = receiver.await.unwrap();
        {
            let dt_str = resp_obj["timestamp"].as_str().unwrap();
            let dt = chrono::DateTime::parse_from_rfc3339(dt_str)
                .map_err(|e| {
                    MethodReturnCode::DeserializationError(format!(
                        "Failed to parse datetime: {}",
                        e
                    ))
                })?
                .with_timezone(&chrono::Utc);
            Ok(dt)
        }
    }

    /// Handler for responses to `what_time_is_it` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_what_time_is_it_response(
        pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>>,
        payload: String,
        opt_correlation_id: Option<Uuid>,
    ) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.and_then(|uuid| {
                let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                hashmap.remove(&uuid)
            });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
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
    ) -> Result<SetTheTimeReturnValue, MethodReturnCode> {
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
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
        let _ = self
            .mqttier_client
            .publish_request(
                format!("full/{}/method/setTheTime", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        let resp_obj = receiver.await.unwrap();
        Ok(SetTheTimeReturnValue {
            timestamp: {
                let dt_str = resp_obj["timestamp"].as_str().unwrap();
                chrono::DateTime::parse_from_rfc3339(dt_str)
                    .map_err(|e| {
                        MethodReturnCode::DeserializationError(format!(
                            "Failed to parse datetime: {}",
                            e
                        ))
                    })?
                    .with_timezone(&chrono::Utc)
            },

            confirmation_message: resp_obj["confirmation_message"]
                .as_str()
                .unwrap()
                .to_string(),
        })
    }

    /// Handler for responses to `set_the_time` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_set_the_time_response(
        pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>>,
        payload: String,
        opt_correlation_id: Option<Uuid>,
    ) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.and_then(|uuid| {
                let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                hashmap.remove(&uuid)
            });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
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
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = ForwardTimeRequestObject {
            adjustment: adjustment,
        };

        let response_topic: String = format!("client/{}/forward_time/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!("full/{}/method/forwardTime", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        let resp_obj = receiver.await.unwrap();
        {
            let dt_str = resp_obj["new_time"].as_str().unwrap();
            let dt = chrono::DateTime::parse_from_rfc3339(dt_str)
                .map_err(|e| {
                    MethodReturnCode::DeserializationError(format!(
                        "Failed to parse datetime: {}",
                        e
                    ))
                })?
                .with_timezone(&chrono::Utc);
            Ok(dt)
        }
    }

    /// Handler for responses to `forward_time` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_forward_time_response(
        pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>>,
        payload: String,
        opt_correlation_id: Option<Uuid>,
    ) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.and_then(|uuid| {
                let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                hashmap.remove(&uuid)
            });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
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
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
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
        let _ = self
            .mqttier_client
            .publish_request(
                format!("full/{}/method/howOffIsTheClock", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        let resp_obj = receiver.await.unwrap();
        {
            let dur_str = resp_obj["difference"].as_str().unwrap();
            let iso_dur = dur_str.parse::<IsoDuration>().unwrap();
            let std_dur = iso_dur.to_std().unwrap();
            Ok(chrono::Duration::from_std(std_dur).unwrap())
        }
    }

    /// Handler for responses to `how_off_is_the_clock` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_how_off_is_the_clock_response(
        pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>>,
        payload: String,
        opt_correlation_id: Option<Uuid>,
    ) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.and_then(|uuid| {
                let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                hashmap.remove(&uuid)
            });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
    }

    /// Watch for changes to the `favorite_number` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_favorite_number(&self) -> watch::Receiver<Option<i32>> {
        self.properties.favorite_number_tx_channel.subscribe()
    }

    pub fn set_favorite_number(&mut self, value: i32) -> Result<(), MethodReturnCode> {
        let data = FavoriteNumberProperty { number: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "full/{}/property/favoriteNumber/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `favorite_foods` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_favorite_foods(&self) -> watch::Receiver<Option<FavoriteFoodsProperty>> {
        self.properties.favorite_foods_tx_channel.subscribe()
    }

    pub fn set_favorite_foods(
        &mut self,
        value: FavoriteFoodsProperty,
    ) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self
            .mqttier_client
            .publish_structure("full/{}/property/favoriteFoods/setValue".to_string(), &data);
        Ok(())
    }

    /// Watch for changes to the `lunch_menu` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_lunch_menu(&self) -> watch::Receiver<Option<LunchMenuProperty>> {
        self.properties.lunch_menu_tx_channel.subscribe()
    }

    pub fn set_lunch_menu(&mut self, value: LunchMenuProperty) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self
            .mqttier_client
            .publish_structure("full/{}/property/lunchMenu/setValue".to_string(), &data);
        Ok(())
    }

    /// Watch for changes to the `family_name` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_family_name(&self) -> watch::Receiver<Option<String>> {
        self.properties.family_name_tx_channel.subscribe()
    }

    pub fn set_family_name(&mut self, value: String) -> Result<(), MethodReturnCode> {
        let data = FamilyNameProperty { family_name: value };
        let _publish_result = self
            .mqttier_client
            .publish_structure("full/{}/property/familyName/setValue".to_string(), &data);
        Ok(())
    }

    /// Watch for changes to the `last_breakfast_time` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_last_breakfast_time(
        &self,
    ) -> watch::Receiver<Option<chrono::DateTime<chrono::Utc>>> {
        self.properties.last_breakfast_time_tx_channel.subscribe()
    }

    pub fn set_last_breakfast_time(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> Result<(), MethodReturnCode> {
        let data = LastBreakfastTimeProperty { timestamp: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "full/{}/property/lastBreakfastTime/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `breakfast_length` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_breakfast_length(&self) -> watch::Receiver<Option<chrono::Duration>> {
        self.properties.breakfast_length_tx_channel.subscribe()
    }

    pub fn set_breakfast_length(
        &mut self,
        value: chrono::Duration,
    ) -> Result<(), MethodReturnCode> {
        let data = BreakfastLengthProperty { length: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "full/{}/property/breakfastLength/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `last_birthdays` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_last_birthdays(&self) -> watch::Receiver<Option<LastBirthdaysProperty>> {
        self.properties.last_birthdays_tx_channel.subscribe()
    }

    pub fn set_last_birthdays(
        &mut self,
        value: LastBirthdaysProperty,
    ) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self
            .mqttier_client
            .publish_structure("full/{}/property/lastBirthdays/setValue".to_string(), &data);
        Ok(())
    }

    /// Starts the tasks that process messages received.
    pub async fn run_loop(&self) -> Result<(), JoinError> {
        // Make sure the MqttierClient is connected and running.
        let _ = self.mqttier_client.run_loop().await;

        // Clone the Arc pointer to the map.  This will be moved into the loop_task.
        let resp_map: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>> =
            self.pending_responses.clone();

        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = {
            let mut guard = self.msg_streamer_rx.lock().expect("Mutex was poisoned");
            guard.take().expect("msg_streamer_rx should be Some")
        };

        let sig_chans = self.signal_channels.clone();

        let sub_ids = self.subscription_ids.clone();
        let props = self.properties.clone();

        let _loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                let opt_corr_data: Option<Vec<u8>> = msg.correlation_data.clone();
                let opt_corr_id: Option<Uuid> =
                    opt_corr_data.and_then(|b| Uuid::from_slice(b.as_slice()).ok());

                let payload = String::from_utf8_lossy(&msg.payload).to_string();
                if msg.subscription_id == sub_ids.add_numbers_method_resp {
                    FullClient::handle_add_numbers_response(resp_map.clone(), payload, opt_corr_id);
                } else if msg.subscription_id == sub_ids.do_something_method_resp {
                    FullClient::handle_do_something_response(
                        resp_map.clone(),
                        payload,
                        opt_corr_id,
                    );
                } else if msg.subscription_id == sub_ids.echo_method_resp {
                    FullClient::handle_echo_response(resp_map.clone(), payload, opt_corr_id);
                } else if msg.subscription_id == sub_ids.what_time_is_it_method_resp {
                    FullClient::handle_what_time_is_it_response(
                        resp_map.clone(),
                        payload,
                        opt_corr_id,
                    );
                } else if msg.subscription_id == sub_ids.set_the_time_method_resp {
                    FullClient::handle_set_the_time_response(
                        resp_map.clone(),
                        payload,
                        opt_corr_id,
                    );
                } else if msg.subscription_id == sub_ids.forward_time_method_resp {
                    FullClient::handle_forward_time_response(
                        resp_map.clone(),
                        payload,
                        opt_corr_id,
                    );
                } else if msg.subscription_id == sub_ids.how_off_is_the_clock_method_resp {
                    FullClient::handle_how_off_is_the_clock_response(
                        resp_map.clone(),
                        payload,
                        opt_corr_id,
                    );
                }

                if msg.subscription_id == sub_ids.today_is_signal.unwrap_or_default() {
                    let chan = sig_chans.today_is_sender.clone();
                    let pl: TodayIsSignalPayload =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let _send_result = chan.send(pl);
                }

                if msg.subscription_id == sub_ids.favorite_number_property_value {
                    let deserialized_data: FavoriteNumberProperty =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let pl = deserialized_data.number;

                    let mut guard = props.favorite_number.lock().expect("Mutex was poisoned");
                    *guard = Some(pl.clone());
                    // Notify any watchers of the property that it has changed.
                    let _ = props.favorite_number_tx_channel.send(Some(pl));
                } else if msg.subscription_id == sub_ids.favorite_foods_property_value {
                    let pl: FavoriteFoodsProperty =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");

                    let mut guard = props.favorite_foods.lock().expect("Mutex was poisoned");
                    *guard = Some(pl.clone());
                    // Notify any watchers of the property that it has changed.
                    let _ = props.favorite_foods_tx_channel.send(Some(pl));
                } else if msg.subscription_id == sub_ids.lunch_menu_property_value {
                    let pl: LunchMenuProperty =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");

                    let mut guard = props.lunch_menu.lock().expect("Mutex was poisoned");
                    *guard = Some(pl.clone());
                    // Notify any watchers of the property that it has changed.
                    let _ = props.lunch_menu_tx_channel.send(Some(pl));
                } else if msg.subscription_id == sub_ids.family_name_property_value {
                    let deserialized_data: FamilyNameProperty =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let pl = deserialized_data.family_name;

                    let mut guard = props.family_name.lock().expect("Mutex was poisoned");
                    *guard = Some(pl.clone());
                    // Notify any watchers of the property that it has changed.
                    let _ = props.family_name_tx_channel.send(Some(pl));
                } else if msg.subscription_id == sub_ids.last_breakfast_time_property_value {
                    let deserialized_data: LastBreakfastTimeProperty =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let pl = deserialized_data.timestamp;

                    let mut guard = props
                        .last_breakfast_time
                        .lock()
                        .expect("Mutex was poisoned");
                    *guard = Some(pl.clone());
                    // Notify any watchers of the property that it has changed.
                    let _ = props.last_breakfast_time_tx_channel.send(Some(pl));
                } else if msg.subscription_id == sub_ids.breakfast_length_property_value {
                    let deserialized_data: BreakfastLengthProperty =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let pl = deserialized_data.length;

                    let mut guard = props.breakfast_length.lock().expect("Mutex was poisoned");
                    *guard = Some(pl.clone());
                    // Notify any watchers of the property that it has changed.
                    let _ = props.breakfast_length_tx_channel.send(Some(pl));
                } else if msg.subscription_id == sub_ids.last_birthdays_property_value {
                    let pl: LastBirthdaysProperty =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");

                    let mut guard = props.last_birthdays.lock().expect("Mutex was poisoned");
                    *guard = Some(pl.clone());
                    // Notify any watchers of the property that it has changed.
                    let _ = props.last_birthdays_tx_channel.send(Some(pl));
                }
            }
        });

        println!("Started client receive task");
        Ok(())
    }
}
