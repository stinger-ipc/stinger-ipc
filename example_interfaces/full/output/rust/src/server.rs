//! Server module for Full IPC
//!
//! This module is only available when the "server" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Full interface.

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
struct FullServerSubscriptionIds {
    add_numbers_method_req: u32,
    do_something_method_req: u32,
    echo_method_req: u32,
    what_time_is_it_method_req: u32,
    set_the_time_method_req: u32,
    forward_time_method_req: u32,
    how_off_is_the_clock_method_req: u32,

    favorite_number_property_update: u32,

    favorite_foods_property_update: u32,

    lunch_menu_property_update: u32,

    family_name_property_update: u32,

    last_breakfast_time_property_update: u32,

    breakfast_length_property_update: u32,

    last_birthdays_property_update: u32,
}

#[derive(Clone)]
struct FullProperties {
    favorite_number: Arc<AsyncMutex<Option<FavoriteNumberProperty>>>,
    favorite_number_tx_channel: watch::Sender<Option<i32>>,
    favorite_number_version: Arc<AtomicU32>,
    favorite_foods: Arc<AsyncMutex<Option<FavoriteFoodsProperty>>>,
    favorite_foods_tx_channel: watch::Sender<Option<FavoriteFoodsProperty>>,
    favorite_foods_version: Arc<AtomicU32>,
    lunch_menu: Arc<AsyncMutex<Option<LunchMenuProperty>>>,
    lunch_menu_tx_channel: watch::Sender<Option<LunchMenuProperty>>,
    lunch_menu_version: Arc<AtomicU32>,
    family_name: Arc<AsyncMutex<Option<FamilyNameProperty>>>,
    family_name_tx_channel: watch::Sender<Option<String>>,
    family_name_version: Arc<AtomicU32>,
    last_breakfast_time: Arc<AsyncMutex<Option<LastBreakfastTimeProperty>>>,
    last_breakfast_time_tx_channel: watch::Sender<Option<chrono::DateTime<chrono::Utc>>>,
    last_breakfast_time_version: Arc<AtomicU32>,
    breakfast_length: Arc<AsyncMutex<Option<BreakfastLengthProperty>>>,
    breakfast_length_tx_channel: watch::Sender<Option<chrono::Duration>>,
    breakfast_length_version: Arc<AtomicU32>,
    last_birthdays: Arc<AsyncMutex<Option<LastBirthdaysProperty>>>,
    last_birthdays_tx_channel: watch::Sender<Option<LastBirthdaysProperty>>,
    last_birthdays_version: Arc<AtomicU32>,
}

#[derive(Clone)]
pub struct FullServer<C: Mqtt5PubSub> {
    mqtt_client: C,

    /// Temporarily holds the receiver for the broadcast channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<broadcast::Receiver<MqttMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: broadcast::Sender<MqttMessage>,

    /// Struct contains all the method handlers.
    method_handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,

    /// Struct contains all the properties.
    properties: FullProperties,

    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: FullServerSubscriptionIds,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,

    pub instance_id: String,
}

impl<C: Mqtt5PubSub + Clone + Send> FullServer<C> {
    pub async fn new(
        mut connection: C,
        method_handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        instance_id: String,
    ) -> Self {
        // Create a channel for messages to get from the Mqtt5PubSub object to this FullServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = broadcast::channel::<MqttMessage>(64);

        // Create method handler struct
        let subscription_id_add_numbers_method_req = connection
            .subscribe(
                format!("full/{}/method/addNumbers", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_add_numbers_method_req =
            subscription_id_add_numbers_method_req.unwrap_or(u32::MAX);

        let subscription_id_do_something_method_req = connection
            .subscribe(
                format!("full/{}/method/doSomething", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_do_something_method_req =
            subscription_id_do_something_method_req.unwrap_or(u32::MAX);

        let subscription_id_echo_method_req = connection
            .subscribe(
                format!("full/{}/method/echo", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_echo_method_req = subscription_id_echo_method_req.unwrap_or(u32::MAX);

        let subscription_id_what_time_is_it_method_req = connection
            .subscribe(
                format!("full/{}/method/whatTimeIsIt", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_what_time_is_it_method_req =
            subscription_id_what_time_is_it_method_req.unwrap_or(u32::MAX);

        let subscription_id_set_the_time_method_req = connection
            .subscribe(
                format!("full/{}/method/setTheTime", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_set_the_time_method_req =
            subscription_id_set_the_time_method_req.unwrap_or(u32::MAX);

        let subscription_id_forward_time_method_req = connection
            .subscribe(
                format!("full/{}/method/forwardTime", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_forward_time_method_req =
            subscription_id_forward_time_method_req.unwrap_or(u32::MAX);

        let subscription_id_how_off_is_the_clock_method_req = connection
            .subscribe(
                format!("full/{}/method/howOffIsTheClock", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_how_off_is_the_clock_method_req =
            subscription_id_how_off_is_the_clock_method_req.unwrap_or(u32::MAX);

        let subscription_id_favorite_number_property_update = connection
            .subscribe(
                format!("full/{}/property/favoriteNumber/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_number_property_update =
            subscription_id_favorite_number_property_update.unwrap_or(u32::MAX);

        let subscription_id_favorite_foods_property_update = connection
            .subscribe(
                format!("full/{}/property/favoriteFoods/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_foods_property_update =
            subscription_id_favorite_foods_property_update.unwrap_or(u32::MAX);

        let subscription_id_lunch_menu_property_update = connection
            .subscribe(
                format!("full/{}/property/lunchMenu/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_lunch_menu_property_update =
            subscription_id_lunch_menu_property_update.unwrap_or(u32::MAX);

        let subscription_id_family_name_property_update = connection
            .subscribe(
                format!("full/{}/property/familyName/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_family_name_property_update =
            subscription_id_family_name_property_update.unwrap_or(u32::MAX);

        let subscription_id_last_breakfast_time_property_update = connection
            .subscribe(
                format!("full/{}/property/lastBreakfastTime/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_last_breakfast_time_property_update =
            subscription_id_last_breakfast_time_property_update.unwrap_or(u32::MAX);

        let subscription_id_breakfast_length_property_update = connection
            .subscribe(
                format!("full/{}/property/breakfastLength/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_breakfast_length_property_update =
            subscription_id_breakfast_length_property_update.unwrap_or(u32::MAX);

        let subscription_id_last_birthdays_property_update = connection
            .subscribe(
                format!("full/{}/property/lastBirthdays/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_last_birthdays_property_update =
            subscription_id_last_birthdays_property_update.unwrap_or(u32::MAX);

        // Create structure for subscription ids.
        let sub_ids = FullServerSubscriptionIds {
            add_numbers_method_req: subscription_id_add_numbers_method_req,
            do_something_method_req: subscription_id_do_something_method_req,
            echo_method_req: subscription_id_echo_method_req,
            what_time_is_it_method_req: subscription_id_what_time_is_it_method_req,
            set_the_time_method_req: subscription_id_set_the_time_method_req,
            forward_time_method_req: subscription_id_forward_time_method_req,
            how_off_is_the_clock_method_req: subscription_id_how_off_is_the_clock_method_req,

            favorite_number_property_update: subscription_id_favorite_number_property_update,
            favorite_foods_property_update: subscription_id_favorite_foods_property_update,
            lunch_menu_property_update: subscription_id_lunch_menu_property_update,
            family_name_property_update: subscription_id_family_name_property_update,
            last_breakfast_time_property_update:
                subscription_id_last_breakfast_time_property_update,
            breakfast_length_property_update: subscription_id_breakfast_length_property_update,
            last_birthdays_property_update: subscription_id_last_birthdays_property_update,
        };

        let property_values = FullProperties {
            favorite_number: Arc::new(AsyncMutex::new(None)),
            favorite_number_tx_channel: watch::channel(None).0,
            favorite_number_version: Arc::new(AtomicU32::new(0)),
            favorite_foods: Arc::new(AsyncMutex::new(None)),
            favorite_foods_tx_channel: watch::channel(None).0,
            favorite_foods_version: Arc::new(AtomicU32::new(0)),
            lunch_menu: Arc::new(AsyncMutex::new(None)),
            lunch_menu_tx_channel: watch::channel(None).0,
            lunch_menu_version: Arc::new(AtomicU32::new(0)),
            family_name: Arc::new(AsyncMutex::new(None)),
            family_name_tx_channel: watch::channel(None).0,
            family_name_version: Arc::new(AtomicU32::new(0)),
            last_breakfast_time: Arc::new(AsyncMutex::new(None)),
            last_breakfast_time_tx_channel: watch::channel(None).0,
            last_breakfast_time_version: Arc::new(AtomicU32::new(0)),
            breakfast_length: Arc::new(AsyncMutex::new(None)),
            breakfast_length_tx_channel: watch::channel(None).0,
            breakfast_length_version: Arc::new(AtomicU32::new(0)),
            last_birthdays: Arc::new(AsyncMutex::new(None)),
            last_birthdays_tx_channel: watch::channel(None).0,
            last_birthdays_version: Arc::new(AtomicU32::new(0)),
        };

        FullServer {
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
    /// Emits the todayIs signal with the given arguments.
    pub async fn emit_today_is(
        &mut self,
        day_of_month: i32,
        day_of_week: Option<DayOfTheWeek>,
        timestamp: chrono::DateTime<chrono::Utc>,
        process_time: chrono::Duration,
        memory_segment: Vec<u8>,
    ) -> SentMessageFuture {
        let data = TodayIsSignalPayload {
            day_of_month,

            day_of_week,

            timestamp,

            process_time,

            memory_segment,
        };
        let topic = format!("full/{}/signal/todayIs", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the todayIs signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_today_is_nowait(
        &mut self,
        day_of_month: i32,
        day_of_week: Option<DayOfTheWeek>,
        timestamp: chrono::DateTime<chrono::Utc>,
        process_time: chrono::Duration,
        memory_segment: Vec<u8>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = TodayIsSignalPayload {
            day_of_month,

            day_of_week,

            timestamp,

            process_time,

            memory_segment,
        };
        let topic = format!("full/{}/signal/todayIs", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }

    /// Handles a request message for the addNumbers method.
    async fn handle_add_numbers_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<AddNumbersRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for addNumbers: {:?}",
                payload_obj.err()
            );
            FullServer::<C>::publish_error_response(
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
                .handle_add_numbers(payload.first, payload.second, payload.third)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = AddNumbersReturnValues { sum: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling addNumbers: {:?}", &err);
                    FullServer::<C>::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `addNumbers`.");
        }
    }

    /// Handles a request message for the doSomething method.
    async fn handle_do_something_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<DoSomethingRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for doSomething: {:?}",
                payload_obj.err()
            );
            FullServer::<C>::publish_error_response(
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
        let rc: Result<DoSomethingReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_do_something(payload.a_string).await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling doSomething: {:?}", &err);
                    FullServer::<C>::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `doSomething`.");
        }
    }

    /// Handles a request message for the echo method.
    async fn handle_echo_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<EchoRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for echo: {:?}",
                payload_obj.err()
            );
            FullServer::<C>::publish_error_response(
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
        let rc: Result<String, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_echo(payload.message).await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = EchoReturnValues { message: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling echo: {:?}", &err);
                    FullServer::<C>::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `echo`.");
        }
    }

    /// Handles a request message for the what_time_is_it method.
    async fn handle_what_time_is_it_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<WhatTimeIsItRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for what_time_is_it: {:?}",
                payload_obj.err()
            );
            FullServer::<C>::publish_error_response(
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
        let rc: Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_what_time_is_it(payload.the_first_time)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = WhatTimeIsItReturnValues { timestamp: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling what_time_is_it: {:?}", &err);
                    FullServer::<C>::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `what_time_is_it`.");
        }
    }

    /// Handles a request message for the set_the_time method.
    async fn handle_set_the_time_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<SetTheTimeRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for set_the_time: {:?}",
                payload_obj.err()
            );
            FullServer::<C>::publish_error_response(
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
        let rc: Result<SetTheTimeReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_set_the_time(payload.the_first_time, payload.the_second_time)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling set_the_time: {:?}", &err);
                    FullServer::<C>::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `set_the_time`.");
        }
    }

    /// Handles a request message for the forward_time method.
    async fn handle_forward_time_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<ForwardTimeRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for forward_time: {:?}",
                payload_obj.err()
            );
            FullServer::<C>::publish_error_response(
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
        let rc: Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_forward_time(payload.adjustment).await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = ForwardTimeReturnValues { new_time: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling forward_time: {:?}", &err);
                    FullServer::<C>::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `forward_time`.");
        }
    }

    /// Handles a request message for the how_off_is_the_clock method.
    async fn handle_how_off_is_the_clock_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<HowOffIsTheClockRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for how_off_is_the_clock: {:?}",
                payload_obj.err()
            );
            FullServer::<C>::publish_error_response(
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
        let rc: Result<chrono::Duration, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_how_off_is_the_clock(payload.actual_time)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = HowOffIsTheClockReturnValues { difference: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling how_off_is_the_clock: {:?}",
                        &err
                    );
                    FullServer::<C>::publish_error_response(
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
            info!(
                "No response topic provided, so no publishing response to `how_off_is_the_clock`."
            );
        }
    }

    async fn publish_favorite_number_value(
        mut publisher: C,
        topic: String,
        data: FavoriteNumberProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        FullServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_favorite_number_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<FavoriteNumberProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: FavoriteNumberProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'favorite_number' property: {:?}", e);
                    return FullServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'favorite_number' payload".to_string(),
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
        let data_to_send_to_watchers = new_property_structure.number.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'favorite_number' property: {:?}",
                    e
                );
            }
        };

        FullServer::publish_favorite_number_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_favorite_number(&self) -> watch::Receiver<Option<i32>> {
        self.properties.favorite_number_tx_channel.subscribe()
    }

    /// Sets the value of the favorite_number property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_favorite_number(&mut self, data: i32) -> SentMessageFuture {
        let prop = self.properties.favorite_number.clone();

        let new_prop_obj = FavoriteNumberProperty {
            number: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result =
            self.properties
                .favorite_number_tx_channel
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
            debug!("Property 'favorite_number' value not changed, so not notifying watchers.");
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None)).await
        } else if let Some(prop_obj) = property_obj {
            let publisher2 = self.mqtt_client.clone();
            let topic2 = format!("full/{}/property/favoriteNumber/value", self.instance_id);
            let new_version = self
                .properties
                .favorite_number_version
                .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            FullServer::<C>::publish_favorite_number_value(
                publisher2,
                topic2,
                prop_obj,
                new_version,
            )
            .await
        } else {
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                "Could not find property object".to_string(),
            ))
            .await
        }
    }

    async fn publish_favorite_foods_value(
        mut publisher: C,
        topic: String,
        data: FavoriteFoodsProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        FullServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_favorite_foods_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<FavoriteFoodsProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<FavoriteFoodsProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: FavoriteFoodsProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'favorite_foods' property: {:?}", e);
                    return FullServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'favorite_foods' payload".to_string(),
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
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'favorite_foods' property: {:?}",
                    e
                );
            }
        };

        FullServer::publish_favorite_foods_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_favorite_foods(&self) -> watch::Receiver<Option<FavoriteFoodsProperty>> {
        self.properties.favorite_foods_tx_channel.subscribe()
    }

    /// Sets the values of the favorite_foods property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_favorite_foods(&mut self, data: FavoriteFoodsProperty) -> SentMessageFuture {
        let prop = self.properties.favorite_foods.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result =
            self.properties
                .favorite_foods_tx_channel
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
            debug!("Property 'favorite_foods' value not changed, so not notifying watchers.");
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None)).await
        } else if let Some(prop_obj) = property_obj {
            let publisher2 = self.mqtt_client.clone();
            let topic2 = format!("full/{}/property/favoriteFoods/value", self.instance_id);
            let new_version = self
                .properties
                .favorite_foods_version
                .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            FullServer::<C>::publish_favorite_foods_value(publisher2, topic2, prop_obj, new_version)
                .await
        } else {
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                "Could not find property object".to_string(),
            ))
            .await
        }
    }

    async fn publish_lunch_menu_value(
        mut publisher: C,
        topic: String,
        data: LunchMenuProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        FullServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_lunch_menu_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<LunchMenuProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<LunchMenuProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: LunchMenuProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'lunch_menu' property: {:?}", e);
                    return FullServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'lunch_menu' payload".to_string(),
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
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'lunch_menu' property: {:?}",
                    e
                );
            }
        };

        FullServer::publish_lunch_menu_value(publisher, topic2, new_property_structure, new_version)
            .await
    }

    pub async fn watch_lunch_menu(&self) -> watch::Receiver<Option<LunchMenuProperty>> {
        self.properties.lunch_menu_tx_channel.subscribe()
    }

    /// Sets the values of the lunch_menu property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_lunch_menu(&mut self, data: LunchMenuProperty) -> SentMessageFuture {
        let prop = self.properties.lunch_menu.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result = self
            .properties
            .lunch_menu_tx_channel
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
            debug!("Property 'lunch_menu' value not changed, so not notifying watchers.");
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None)).await
        } else if let Some(prop_obj) = property_obj {
            let publisher2 = self.mqtt_client.clone();
            let topic2 = format!("full/{}/property/lunchMenu/value", self.instance_id);
            let new_version = self
                .properties
                .lunch_menu_version
                .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            FullServer::<C>::publish_lunch_menu_value(publisher2, topic2, prop_obj, new_version)
                .await
        } else {
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                "Could not find property object".to_string(),
            ))
            .await
        }
    }

    async fn publish_family_name_value(
        mut publisher: C,
        topic: String,
        data: FamilyNameProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        FullServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_family_name_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<FamilyNameProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<String>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: FamilyNameProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'family_name' property: {:?}", e);
                    return FullServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'family_name' payload".to_string(),
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
        let data_to_send_to_watchers = new_property_structure.family_name.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'family_name' property: {:?}",
                    e
                );
            }
        };

        FullServer::publish_family_name_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_family_name(&self) -> watch::Receiver<Option<String>> {
        self.properties.family_name_tx_channel.subscribe()
    }

    /// Sets the value of the family_name property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_family_name(&mut self, data: String) -> SentMessageFuture {
        let prop = self.properties.family_name.clone();

        let new_prop_obj = FamilyNameProperty {
            family_name: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .family_name_tx_channel
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
            debug!("Property 'family_name' value not changed, so not notifying watchers.");
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None)).await
        } else if let Some(prop_obj) = property_obj {
            let publisher2 = self.mqtt_client.clone();
            let topic2 = format!("full/{}/property/familyName/value", self.instance_id);
            let new_version = self
                .properties
                .family_name_version
                .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            FullServer::<C>::publish_family_name_value(publisher2, topic2, prop_obj, new_version)
                .await
        } else {
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                "Could not find property object".to_string(),
            ))
            .await
        }
    }

    async fn publish_last_breakfast_time_value(
        mut publisher: C,
        topic: String,
        data: LastBreakfastTimeProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        FullServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_last_breakfast_time_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<LastBreakfastTimeProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<chrono::DateTime<chrono::Utc>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: LastBreakfastTimeProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'last_breakfast_time' property: {:?}", e);
                    return FullServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'last_breakfast_time' payload"
                                .to_string(),
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
        let data_to_send_to_watchers = new_property_structure.timestamp.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'last_breakfast_time' property: {:?}",
                    e
                );
            }
        };

        FullServer::publish_last_breakfast_time_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_last_breakfast_time(
        &self,
    ) -> watch::Receiver<Option<chrono::DateTime<chrono::Utc>>> {
        self.properties.last_breakfast_time_tx_channel.subscribe()
    }

    /// Sets the value of the last_breakfast_time property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_last_breakfast_time(
        &mut self,
        data: chrono::DateTime<chrono::Utc>,
    ) -> SentMessageFuture {
        let prop = self.properties.last_breakfast_time.clone();

        let new_prop_obj = LastBreakfastTimeProperty {
            timestamp: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .last_breakfast_time_tx_channel
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
            debug!("Property 'last_breakfast_time' value not changed, so not notifying watchers.");
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None)).await
        } else if let Some(prop_obj) = property_obj {
            let publisher2 = self.mqtt_client.clone();
            let topic2 = format!("full/{}/property/lastBreakfastTime/value", self.instance_id);
            let new_version = self
                .properties
                .last_breakfast_time_version
                .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            FullServer::<C>::publish_last_breakfast_time_value(
                publisher2,
                topic2,
                prop_obj,
                new_version,
            )
            .await
        } else {
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                "Could not find property object".to_string(),
            ))
            .await
        }
    }

    async fn publish_breakfast_length_value(
        mut publisher: C,
        topic: String,
        data: BreakfastLengthProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        FullServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_breakfast_length_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<BreakfastLengthProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<chrono::Duration>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: BreakfastLengthProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'breakfast_length' property: {:?}", e);
                    return FullServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'breakfast_length' payload".to_string(),
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
        let data_to_send_to_watchers = new_property_structure.length.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'breakfast_length' property: {:?}",
                    e
                );
            }
        };

        FullServer::publish_breakfast_length_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_breakfast_length(&self) -> watch::Receiver<Option<chrono::Duration>> {
        self.properties.breakfast_length_tx_channel.subscribe()
    }

    /// Sets the value of the breakfast_length property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_breakfast_length(&mut self, data: chrono::Duration) -> SentMessageFuture {
        let prop = self.properties.breakfast_length.clone();

        let new_prop_obj = BreakfastLengthProperty {
            length: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .breakfast_length_tx_channel
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
            debug!("Property 'breakfast_length' value not changed, so not notifying watchers.");
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None)).await
        } else if let Some(prop_obj) = property_obj {
            let publisher2 = self.mqtt_client.clone();
            let topic2 = format!("full/{}/property/breakfastLength/value", self.instance_id);
            let new_version = self
                .properties
                .breakfast_length_version
                .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            FullServer::<C>::publish_breakfast_length_value(
                publisher2,
                topic2,
                prop_obj,
                new_version,
            )
            .await
        } else {
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                "Could not find property object".to_string(),
            ))
            .await
        }
    }

    async fn publish_last_birthdays_value(
        mut publisher: C,
        topic: String,
        data: LastBirthdaysProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        FullServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_last_birthdays_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<LastBirthdaysProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<LastBirthdaysProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: LastBirthdaysProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'last_birthdays' property: {:?}", e);
                    return FullServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'last_birthdays' payload".to_string(),
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
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'last_birthdays' property: {:?}",
                    e
                );
            }
        };

        FullServer::publish_last_birthdays_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_last_birthdays(&self) -> watch::Receiver<Option<LastBirthdaysProperty>> {
        self.properties.last_birthdays_tx_channel.subscribe()
    }

    /// Sets the values of the last_birthdays property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_last_birthdays(&mut self, data: LastBirthdaysProperty) -> SentMessageFuture {
        let prop = self.properties.last_birthdays.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result =
            self.properties
                .last_birthdays_tx_channel
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
            debug!("Property 'last_birthdays' value not changed, so not notifying watchers.");
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None)).await
        } else if let Some(prop_obj) = property_obj {
            let publisher2 = self.mqtt_client.clone();
            let topic2 = format!("full/{}/property/lastBirthdays/value", self.instance_id);
            let new_version = self
                .properties
                .last_birthdays_version
                .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            FullServer::<C>::publish_last_birthdays_value(publisher2, topic2, prop_obj, new_version)
                .await
        } else {
            FullServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
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
                let topic = format!("full/{}/interface", instance_id);
                let info = crate::interface::InterfaceInfoBuilder::default()
                    .interface_name("Full".to_string())
                    .title("Fully Featured Example Interface".to_string())
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
                            if subscription_id == sub_ids.add_numbers_method_req {
                                FullServer::<C>::handle_add_numbers_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.do_something_method_req {
                                FullServer::<C>::handle_do_something_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.echo_method_req {
                                FullServer::<C>::handle_echo_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.what_time_is_it_method_req {
                                FullServer::<C>::handle_what_time_is_it_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.set_the_time_method_req {
                                FullServer::<C>::handle_set_the_time_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.forward_time_method_req {
                                FullServer::<C>::handle_forward_time_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.how_off_is_the_clock_method_req {
                                FullServer::<C>::handle_how_off_is_the_clock_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else {
                                let update_prop_future = {
                                    if subscription_id == sub_ids.favorite_number_property_update {
                                        let prop_topic = format!(
                                            "full/{}/property/favoriteNumber/value",
                                            instance_id
                                        );
                                        FullServer::<C>::update_favorite_number_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.favorite_number.clone(),
                                            properties.favorite_number_version.clone(),
                                            properties.favorite_number_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.favorite_foods_property_update
                                    {
                                        let prop_topic = format!(
                                            "full/{}/property/favoriteFoods/value",
                                            instance_id
                                        );
                                        FullServer::<C>::update_favorite_foods_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.favorite_foods.clone(),
                                            properties.favorite_foods_version.clone(),
                                            properties.favorite_foods_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id == sub_ids.lunch_menu_property_update
                                    {
                                        let prop_topic = format!(
                                            "full/{}/property/lunchMenu/value",
                                            instance_id
                                        );
                                        FullServer::<C>::update_lunch_menu_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.lunch_menu.clone(),
                                            properties.lunch_menu_version.clone(),
                                            properties.lunch_menu_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id == sub_ids.family_name_property_update
                                    {
                                        let prop_topic = format!(
                                            "full/{}/property/familyName/value",
                                            instance_id
                                        );
                                        FullServer::<C>::update_family_name_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.family_name.clone(),
                                            properties.family_name_version.clone(),
                                            properties.family_name_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.last_breakfast_time_property_update
                                    {
                                        let prop_topic = format!(
                                            "full/{}/property/lastBreakfastTime/value",
                                            instance_id
                                        );
                                        FullServer::<C>::update_last_breakfast_time_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.last_breakfast_time.clone(),
                                            properties.last_breakfast_time_version.clone(),
                                            properties.last_breakfast_time_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.breakfast_length_property_update
                                    {
                                        let prop_topic = format!(
                                            "full/{}/property/breakfastLength/value",
                                            instance_id
                                        );
                                        FullServer::<C>::update_breakfast_length_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.breakfast_length.clone(),
                                            properties.breakfast_length_version.clone(),
                                            properties.breakfast_length_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.last_birthdays_property_update
                                    {
                                        let prop_topic = format!(
                                            "full/{}/property/lastBirthdays/value",
                                            instance_id
                                        );
                                        FullServer::<C>::update_last_birthdays_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.last_birthdays.clone(),
                                            properties.last_birthdays_version.clone(),
                                            properties.last_birthdays_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else {
                                        FullServer::<C>::wrap_return_code_in_future(
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
                                            FullServer::<C>::publish_error_response(
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
pub trait FullMethodHandlers<C: Mqtt5PubSub>: Send + Sync {
    async fn initialize(&mut self, server: FullServer<C>) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the addNumbers method request.
    async fn handle_add_numbers(
        &self,
        first: i32,
        second: i32,
        third: Option<i32>,
    ) -> Result<i32, MethodReturnCode>;

    /// Pointer to a function to handle the doSomething method request.
    async fn handle_do_something(
        &self,
        a_string: String,
    ) -> Result<DoSomethingReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the echo method request.
    async fn handle_echo(&self, message: String) -> Result<String, MethodReturnCode>;

    /// Pointer to a function to handle the what_time_is_it method request.
    async fn handle_what_time_is_it(
        &self,
        the_first_time: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode>;

    /// Pointer to a function to handle the set_the_time method request.
    async fn handle_set_the_time(
        &self,
        the_first_time: chrono::DateTime<chrono::Utc>,
        the_second_time: chrono::DateTime<chrono::Utc>,
    ) -> Result<SetTheTimeReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the forward_time method request.
    async fn handle_forward_time(
        &self,
        adjustment: chrono::Duration,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode>;

    /// Pointer to a function to handle the how_off_is_the_clock method request.
    async fn handle_how_off_is_the_clock(
        &self,
        actual_time: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::Duration, MethodReturnCode>;

    fn as_any(&self) -> &dyn Any;
}
