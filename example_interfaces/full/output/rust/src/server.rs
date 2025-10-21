//! Server module for Full IPC
//!
//! This module is only available when the "server" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Full interface.
*/

use mqttier::{MqttierClient, PublishResult, ReceivedMessage};

#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};

use async_trait::async_trait;
use std::any::Any;
use std::sync::{Arc, Mutex};
use tokio::sync::Mutex as AsyncMutex;

use serde_json;
use tokio::sync::{mpsc, watch};

use std::future::Future;
use std::pin::Pin;
use tokio::task::JoinError;
type SentMessageFuture = Pin<Box<dyn Future<Output = Result<(), MethodReturnCode>> + Send>>;
#[cfg(feature = "server")]
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct FullServerSubscriptionIds {
    add_numbers_method_req: usize,
    do_something_method_req: usize,
    echo_method_req: usize,
    what_time_is_it_method_req: usize,
    set_the_time_method_req: usize,
    forward_time_method_req: usize,
    how_off_is_the_clock_method_req: usize,

    favorite_number_property_update: usize,

    favorite_foods_property_update: usize,

    lunch_menu_property_update: usize,

    family_name_property_update: usize,

    last_breakfast_time_property_update: usize,

    breakfast_length_property_update: usize,

    last_birthdays_property_update: usize,
}

#[derive(Clone)]
struct FullProperties {
    favorite_number_topic: Arc<String>,
    favorite_number: Arc<AsyncMutex<Option<FavoriteNumberProperty>>>,
    favorite_number_tx_channel: watch::Sender<Option<i32>>,
    favorite_foods_topic: Arc<String>,
    favorite_foods: Arc<AsyncMutex<Option<FavoriteFoodsProperty>>>,
    favorite_foods_tx_channel: watch::Sender<Option<FavoriteFoodsProperty>>,
    lunch_menu_topic: Arc<String>,
    lunch_menu: Arc<AsyncMutex<Option<LunchMenuProperty>>>,
    lunch_menu_tx_channel: watch::Sender<Option<LunchMenuProperty>>,
    family_name_topic: Arc<String>,
    family_name: Arc<AsyncMutex<Option<FamilyNameProperty>>>,
    family_name_tx_channel: watch::Sender<Option<String>>,
    last_breakfast_time_topic: Arc<String>,
    last_breakfast_time: Arc<AsyncMutex<Option<LastBreakfastTimeProperty>>>,
    last_breakfast_time_tx_channel: watch::Sender<Option<chrono::DateTime<chrono::Utc>>>,
    breakfast_length_topic: Arc<String>,
    breakfast_length: Arc<AsyncMutex<Option<BreakfastLengthProperty>>>,
    breakfast_length_tx_channel: watch::Sender<Option<chrono::Duration>>,
    last_birthdays_topic: Arc<String>,
    last_birthdays: Arc<AsyncMutex<Option<LastBirthdaysProperty>>>,
    last_birthdays_tx_channel: watch::Sender<Option<LastBirthdaysProperty>>,
}

#[derive(Clone)]
pub struct FullServer {
    mqttier_client: MqttierClient,

    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<mpsc::Receiver<ReceivedMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Struct contains all the method handlers.
    method_handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,

    /// Struct contains all the properties.
    properties: FullProperties,

    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: FullServerSubscriptionIds,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,

    pub instance_id: String,
}

impl FullServer {
    pub async fn new(
        connection: &mut MqttierClient,
        method_handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,
        instance_id: String,
    ) -> Self {
        // Create a channel for messages to get from the MqttierClient object to this FullServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel::<ReceivedMessage>(64);

        // Create method handler struct
        let subscription_id_add_numbers_method_req = connection
            .subscribe(
                format!("full/{}/method/addNumbers", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_add_numbers_method_req =
            subscription_id_add_numbers_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_do_something_method_req = connection
            .subscribe(
                format!("full/{}/method/doSomething", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_do_something_method_req =
            subscription_id_do_something_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_echo_method_req = connection
            .subscribe(
                format!("full/{}/method/echo", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_echo_method_req =
            subscription_id_echo_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_what_time_is_it_method_req = connection
            .subscribe(
                format!("full/{}/method/whatTimeIsIt", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_what_time_is_it_method_req =
            subscription_id_what_time_is_it_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_set_the_time_method_req = connection
            .subscribe(
                format!("full/{}/method/setTheTime", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_set_the_time_method_req =
            subscription_id_set_the_time_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_forward_time_method_req = connection
            .subscribe(
                format!("full/{}/method/forwardTime", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_forward_time_method_req =
            subscription_id_forward_time_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_how_off_is_the_clock_method_req = connection
            .subscribe(
                format!("full/{}/method/howOffIsTheClock", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_how_off_is_the_clock_method_req =
            subscription_id_how_off_is_the_clock_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_favorite_number_property_update = connection
            .subscribe(
                format!("full/{}/property/favoriteNumber/setValue", instance_id),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_number_property_update =
            subscription_id_favorite_number_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_favorite_foods_property_update = connection
            .subscribe(
                format!("full/{}/property/favoriteFoods/setValue", instance_id),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_foods_property_update =
            subscription_id_favorite_foods_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_lunch_menu_property_update = connection
            .subscribe(
                format!("full/{}/property/lunchMenu/setValue", instance_id),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_lunch_menu_property_update =
            subscription_id_lunch_menu_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_family_name_property_update = connection
            .subscribe(
                format!("full/{}/property/familyName/setValue", instance_id),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_family_name_property_update =
            subscription_id_family_name_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_last_breakfast_time_property_update = connection
            .subscribe(
                format!("full/{}/property/lastBreakfastTime/setValue", instance_id),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_last_breakfast_time_property_update =
            subscription_id_last_breakfast_time_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_breakfast_length_property_update = connection
            .subscribe(
                format!("full/{}/property/breakfastLength/setValue", instance_id),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_breakfast_length_property_update =
            subscription_id_breakfast_length_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_last_birthdays_property_update = connection
            .subscribe(
                format!("full/{}/property/lastBirthdays/setValue", instance_id),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_last_birthdays_property_update =
            subscription_id_last_birthdays_property_update.unwrap_or_else(|_| usize::MAX);

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
            favorite_number_topic: Arc::new(format!(
                "full/{}/property/favoriteNumber/value",
                instance_id
            )),
            favorite_number: Arc::new(AsyncMutex::new(None)),
            favorite_number_tx_channel: watch::channel(None).0,
            favorite_foods_topic: Arc::new(format!(
                "full/{}/property/favoriteFoods/value",
                instance_id
            )),
            favorite_foods: Arc::new(AsyncMutex::new(None)),
            favorite_foods_tx_channel: watch::channel(None).0,
            lunch_menu_topic: Arc::new(format!("full/{}/property/lunchMenu/value", instance_id)),
            lunch_menu: Arc::new(AsyncMutex::new(None)),
            lunch_menu_tx_channel: watch::channel(None).0,
            family_name_topic: Arc::new(format!("full/{}/property/familyName/value", instance_id)),
            family_name: Arc::new(AsyncMutex::new(None)),
            family_name_tx_channel: watch::channel(None).0,
            last_breakfast_time_topic: Arc::new(format!(
                "full/{}/property/lastBreakfastTime/value",
                instance_id
            )),
            last_breakfast_time: Arc::new(AsyncMutex::new(None)),
            last_breakfast_time_tx_channel: watch::channel(None).0,
            breakfast_length_topic: Arc::new(format!(
                "full/{}/property/breakfastLength/value",
                instance_id
            )),
            breakfast_length: Arc::new(AsyncMutex::new(None)),
            breakfast_length_tx_channel: watch::channel(None).0,
            last_birthdays_topic: Arc::new(format!(
                "full/{}/property/lastBirthdays/value",
                instance_id
            )),
            last_birthdays: Arc::new(AsyncMutex::new(None)),
            last_birthdays_tx_channel: watch::channel(None).0,
        };

        FullServer {
            mqttier_client: connection.clone(),

            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,
            method_handlers: method_handlers,
            properties: property_values,
            subscription_ids: sub_ids,

            client_id: connection.client_id.to_string(),
            instance_id,
        }
    }

    /// Converts a oneshot receiver for the publish result into a Future that resolves to
    pub async fn oneshot_to_future(
        publish_oneshot: tokio::sync::oneshot::Receiver<PublishResult>,
    ) -> SentMessageFuture {
        Box::pin(async move {
            let publish_result = publish_oneshot.await;
            match publish_result {
                Ok(PublishResult::Acknowledged(_))
                | Ok(PublishResult::Completed(_))
                | Ok(PublishResult::Sent(_)) => Ok(()),

                Ok(PublishResult::TimedOut) => Err(MethodReturnCode::Timeout(
                    "Timed out publishing signal".to_string(),
                )),

                Ok(PublishResult::SerializationError(s)) => {
                    Err(MethodReturnCode::ServerSerializationError(s))
                }

                Ok(PublishResult::Error(s)) => Err(MethodReturnCode::TransportError(s)),

                Err(_) => Err(MethodReturnCode::UnknownError(
                    "Error publishing signal".to_string(),
                )),
            }
        })
    }

    pub async fn wrap_return_code_in_future(rc: MethodReturnCode) -> SentMessageFuture {
        Box::pin(async move {
            match rc {
                MethodReturnCode::Success => Ok(()),
                _ => Err(rc),
            }
        })
    }

    /// Publishes an error response to the given response topic with the given correlation data.
    async fn publish_error_response(
        publisher: MqttierClient,
        response_topic: Option<String>,
        correlation_data: Option<Vec<u8>>,
        err: &MethodReturnCode,
    ) {
        if let Some(resp_topic) = response_topic {
            let corr_data = correlation_data.unwrap_or_default();
            let (return_code, debug_message) = err.to_code();
            let _ = publisher
                .publish_error_response(
                    resp_topic,
                    debug_message.unwrap_or_default(),
                    corr_data,
                    return_code,
                )
                .await;
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
            day_of_month: day_of_month,

            day_of_week: day_of_week,

            timestamp: timestamp,

            process_time: process_time,

            memory_segment: memory_segment,
        };
        let published_oneshot = self
            .mqttier_client
            .publish_structure(format!("full/{}/signal/todayIs", self.instance_id), &data)
            .await;
        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// Handles a request message for the addNumbers method.
    async fn handle_add_numbers_request(
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,
        msg: ReceivedMessage,
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
            FullServer::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                &MethodReturnCode::ServerDeserializationError(
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &resp_obj, corr_data)
                        .await;
                }
                Err(err) => {
                    info!("Error occurred while handling addNumbers: {:?}", &err);
                    FullServer::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        &err,
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
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,
        msg: ReceivedMessage,
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
            FullServer::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                &MethodReturnCode::ServerDeserializationError(
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &retval, corr_data)
                        .await;
                }
                Err(err) => {
                    info!("Error occurred while handling doSomething: {:?}", &err);
                    FullServer::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        &err,
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
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,
        msg: ReceivedMessage,
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
            FullServer::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                &MethodReturnCode::ServerDeserializationError(
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &resp_obj, corr_data)
                        .await;
                }
                Err(err) => {
                    info!("Error occurred while handling echo: {:?}", &err);
                    FullServer::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        &err,
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
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,
        msg: ReceivedMessage,
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
            FullServer::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                &MethodReturnCode::ServerDeserializationError(
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &resp_obj, corr_data)
                        .await;
                }
                Err(err) => {
                    info!("Error occurred while handling what_time_is_it: {:?}", &err);
                    FullServer::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        &err,
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
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,
        msg: ReceivedMessage,
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
            FullServer::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                &MethodReturnCode::ServerDeserializationError(
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &retval, corr_data)
                        .await;
                }
                Err(err) => {
                    info!("Error occurred while handling set_the_time: {:?}", &err);
                    FullServer::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        &err,
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
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,
        msg: ReceivedMessage,
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
            FullServer::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                &MethodReturnCode::ServerDeserializationError(
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &resp_obj, corr_data)
                        .await;
                }
                Err(err) => {
                    info!("Error occurred while handling forward_time: {:?}", &err);
                    FullServer::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        &err,
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
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,
        msg: ReceivedMessage,
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
            FullServer::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                &MethodReturnCode::ServerDeserializationError(
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &resp_obj, corr_data)
                        .await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling how_off_is_the_clock: {:?}",
                        &err
                    );
                    FullServer::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        &err,
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
        publisher: MqttierClient,
        topic: String,
        data: FavoriteNumberProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_favorite_number_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<FavoriteNumberProperty>>>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: FavoriteNumberProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'favorite_number' property: {:?}", e);
                    return FullServer::wrap_return_code_in_future(
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

        let topic2: String = topic.as_ref().clone();
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
        FullServer::publish_favorite_number_value(publisher, topic2, new_property_structure).await
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
            return FullServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.favorite_number_topic.as_ref().clone();
                FullServer::publish_favorite_number_value(publisher2, topic2, prop_obj).await
            } else {
                FullServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_favorite_foods_value(
        publisher: MqttierClient,
        topic: String,
        data: FavoriteFoodsProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_favorite_foods_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<FavoriteFoodsProperty>>>,
        watch_sender: watch::Sender<Option<FavoriteFoodsProperty>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: FavoriteFoodsProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'favorite_foods' property: {:?}", e);
                    return FullServer::wrap_return_code_in_future(
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

        let topic2: String = topic.as_ref().clone();
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
        FullServer::publish_favorite_foods_value(publisher, topic2, new_property_structure).await
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
            return FullServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.favorite_foods_topic.as_ref().clone();
                FullServer::publish_favorite_foods_value(publisher2, topic2, prop_obj).await
            } else {
                FullServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_lunch_menu_value(
        publisher: MqttierClient,
        topic: String,
        data: LunchMenuProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_lunch_menu_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<LunchMenuProperty>>>,
        watch_sender: watch::Sender<Option<LunchMenuProperty>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: LunchMenuProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'lunch_menu' property: {:?}", e);
                    return FullServer::wrap_return_code_in_future(
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

        let topic2: String = topic.as_ref().clone();
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
        FullServer::publish_lunch_menu_value(publisher, topic2, new_property_structure).await
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
            return FullServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.lunch_menu_topic.as_ref().clone();
                FullServer::publish_lunch_menu_value(publisher2, topic2, prop_obj).await
            } else {
                FullServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_family_name_value(
        publisher: MqttierClient,
        topic: String,
        data: FamilyNameProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_family_name_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<FamilyNameProperty>>>,
        watch_sender: watch::Sender<Option<String>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: FamilyNameProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'family_name' property: {:?}", e);
                    return FullServer::wrap_return_code_in_future(
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

        let topic2: String = topic.as_ref().clone();
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
        FullServer::publish_family_name_value(publisher, topic2, new_property_structure).await
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
            return FullServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.family_name_topic.as_ref().clone();
                FullServer::publish_family_name_value(publisher2, topic2, prop_obj).await
            } else {
                FullServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_last_breakfast_time_value(
        publisher: MqttierClient,
        topic: String,
        data: LastBreakfastTimeProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_last_breakfast_time_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<LastBreakfastTimeProperty>>>,
        watch_sender: watch::Sender<Option<chrono::DateTime<chrono::Utc>>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: LastBreakfastTimeProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'last_breakfast_time' property: {:?}", e);
                    return FullServer::wrap_return_code_in_future(
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

        let topic2: String = topic.as_ref().clone();
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
        FullServer::publish_last_breakfast_time_value(publisher, topic2, new_property_structure)
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
            return FullServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.last_breakfast_time_topic.as_ref().clone();
                FullServer::publish_last_breakfast_time_value(publisher2, topic2, prop_obj).await
            } else {
                FullServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_breakfast_length_value(
        publisher: MqttierClient,
        topic: String,
        data: BreakfastLengthProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_breakfast_length_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<BreakfastLengthProperty>>>,
        watch_sender: watch::Sender<Option<chrono::Duration>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: BreakfastLengthProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'breakfast_length' property: {:?}", e);
                    return FullServer::wrap_return_code_in_future(
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

        let topic2: String = topic.as_ref().clone();
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
        FullServer::publish_breakfast_length_value(publisher, topic2, new_property_structure).await
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
            return FullServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.breakfast_length_topic.as_ref().clone();
                FullServer::publish_breakfast_length_value(publisher2, topic2, prop_obj).await
            } else {
                FullServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_last_birthdays_value(
        publisher: MqttierClient,
        topic: String,
        data: LastBirthdaysProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_last_birthdays_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<LastBirthdaysProperty>>>,
        watch_sender: watch::Sender<Option<LastBirthdaysProperty>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: LastBirthdaysProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'last_birthdays' property: {:?}", e);
                    return FullServer::wrap_return_code_in_future(
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

        let topic2: String = topic.as_ref().clone();
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
        FullServer::publish_last_birthdays_value(publisher, topic2, new_property_structure).await
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
            return FullServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.last_birthdays_topic.as_ref().clone();
                FullServer::publish_last_birthdays_value(publisher2, topic2, prop_obj).await
            } else {
                FullServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    /// Starts the tasks that process messages received.
    /// In the task, it loops over messages received from the rx side of the message_receiver channel.
    /// Based on the subscription id of the received message, it will call a function to handle the
    /// received message.
    pub async fn run_loop(&mut self) -> Result<(), JoinError> {
        // Make sure the MqttierClient is connected and running.
        let _ = self.mqttier_client.run_loop().await;

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
        let publisher = self.mqttier_client.clone();

        let properties = self.properties.clone();

        let interface_publisher = self.mqttier_client.clone();
        let instance_id = self.instance_id.clone();
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(std::time::Duration::from_secs(120));
            loop {
                interval.tick().await;
                let info = crate::interface::InterfaceInfo::new()
                    .interface_name("Full".to_string())
                    .title("Fully Featured Example Interface".to_string())
                    .version("0.0.1".to_string())
                    .instance(instance_id.clone())
                    .connection_topic(format!("client/{}/online", interface_publisher.client_id))
                    .build();
                let _ = interface_publisher
                    .publish_status(format!("full/{}/interface", instance_id), &info, 150)
                    .await;
            }
        });
        let loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                let opt_resp_topic = msg.response_topic.clone();
                let opt_corr_data = msg.correlation_data.clone();

                if msg.subscription_id == sub_ids.add_numbers_method_req {
                    FullServer::handle_add_numbers_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.do_something_method_req {
                    FullServer::handle_do_something_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.echo_method_req {
                    FullServer::handle_echo_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.what_time_is_it_method_req {
                    FullServer::handle_what_time_is_it_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.set_the_time_method_req {
                    FullServer::handle_set_the_time_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.forward_time_method_req {
                    FullServer::handle_forward_time_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.how_off_is_the_clock_method_req {
                    FullServer::handle_how_off_is_the_clock_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else {
                    let update_prop_future = {
                        if msg.subscription_id == sub_ids.favorite_number_property_update {
                            FullServer::update_favorite_number_value(
                                publisher.clone(),
                                properties.favorite_number_topic.clone(),
                                properties.favorite_number.clone(),
                                properties.favorite_number_tx_channel.clone(),
                                msg,
                            )
                            .await
                        } else if msg.subscription_id == sub_ids.favorite_foods_property_update {
                            FullServer::update_favorite_foods_value(
                                publisher.clone(),
                                properties.favorite_foods_topic.clone(),
                                properties.favorite_foods.clone(),
                                properties.favorite_foods_tx_channel.clone(),
                                msg,
                            )
                            .await
                        } else if msg.subscription_id == sub_ids.lunch_menu_property_update {
                            FullServer::update_lunch_menu_value(
                                publisher.clone(),
                                properties.lunch_menu_topic.clone(),
                                properties.lunch_menu.clone(),
                                properties.lunch_menu_tx_channel.clone(),
                                msg,
                            )
                            .await
                        } else if msg.subscription_id == sub_ids.family_name_property_update {
                            FullServer::update_family_name_value(
                                publisher.clone(),
                                properties.family_name_topic.clone(),
                                properties.family_name.clone(),
                                properties.family_name_tx_channel.clone(),
                                msg,
                            )
                            .await
                        } else if msg.subscription_id == sub_ids.last_breakfast_time_property_update
                        {
                            FullServer::update_last_breakfast_time_value(
                                publisher.clone(),
                                properties.last_breakfast_time_topic.clone(),
                                properties.last_breakfast_time.clone(),
                                properties.last_breakfast_time_tx_channel.clone(),
                                msg,
                            )
                            .await
                        } else if msg.subscription_id == sub_ids.breakfast_length_property_update {
                            FullServer::update_breakfast_length_value(
                                publisher.clone(),
                                properties.breakfast_length_topic.clone(),
                                properties.breakfast_length.clone(),
                                properties.breakfast_length_tx_channel.clone(),
                                msg,
                            )
                            .await
                        } else if msg.subscription_id == sub_ids.last_birthdays_property_update {
                            FullServer::update_last_birthdays_value(
                                publisher.clone(),
                                properties.last_birthdays_topic.clone(),
                                properties.last_birthdays.clone(),
                                properties.last_birthdays_tx_channel.clone(),
                                msg,
                            )
                            .await
                        } else {
                            FullServer::wrap_return_code_in_future(
                                MethodReturnCode::NotImplemented(
                                    "Could not find a property matching the request".to_string(),
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
                                FullServer::publish_error_response(
                                    publisher.clone(),
                                    Some(resp_topic),
                                    opt_corr_data,
                                    &e,
                                )
                                .await;
                            } else {
                                warn!("No response topic found in message properties; cannot send error response.");
                            }
                        }
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
pub trait FullMethodHandlers: Send + Sync {
    async fn initialize(&mut self, server: FullServer) -> Result<(), MethodReturnCode>;

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
