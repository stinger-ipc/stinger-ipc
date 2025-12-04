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

use crate::property::FullInitialPropertyValues;
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
struct FullServerSubscriptionIds {
    add_numbers_method_req: u32,
    do_something_method_req: u32,
    what_time_is_it_method_req: u32,
    hold_temperature_method_req: u32,

    favorite_number_property_update: u32,

    favorite_foods_property_update: u32,

    family_name_property_update: u32,

    last_breakfast_time_property_update: u32,

    last_birthdays_property_update: u32,
}

#[derive(Clone)]
struct FullProperties {
    pub favorite_number: Arc<RwLockWatch<i32>>,
    favorite_number_version: Arc<AtomicU32>,
    pub favorite_foods: Arc<RwLockWatch<FavoriteFoodsProperty>>,
    favorite_foods_version: Arc<AtomicU32>,
    pub lunch_menu: Arc<RwLockWatch<LunchMenuProperty>>,
    lunch_menu_version: Arc<AtomicU32>,
    pub family_name: Arc<RwLockWatch<String>>,
    family_name_version: Arc<AtomicU32>,
    pub last_breakfast_time: Arc<RwLockWatch<chrono::DateTime<chrono::Utc>>>,
    last_breakfast_time_version: Arc<AtomicU32>,
    pub last_birthdays: Arc<RwLockWatch<LastBirthdaysProperty>>,
    last_birthdays_version: Arc<AtomicU32>,
}

#[cfg(feature = "metrics")]
#[derive(Debug, Serialize)]
pub struct FullServerMetrics {
    pub add_numbers_calls: u64,
    pub add_numbers_errors: u64,
    pub do_something_calls: u64,
    pub do_something_errors: u64,
    pub what_time_is_it_calls: u64,
    pub what_time_is_it_errors: u64,
    pub hold_temperature_calls: u64,
    pub hold_temperature_errors: u64,

    pub initial_property_publish_time: std::time::Duration,
}

#[cfg(feature = "metrics")]
impl Default for FullServerMetrics {
    fn default() -> Self {
        FullServerMetrics {
            add_numbers_calls: 0,
            add_numbers_errors: 0,
            do_something_calls: 0,
            do_something_errors: 0,
            what_time_is_it_calls: 0,
            what_time_is_it_errors: 0,
            hold_temperature_calls: 0,
            hold_temperature_errors: 0,

            initial_property_publish_time: std::time::Duration::from_secs(0),
        }
    }
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

    #[cfg(feature = "metrics")]
    metrics: Arc<AsyncMutex<FullServerMetrics>>,
}

impl<C: Mqtt5PubSub + Clone + Send> FullServer<C> {
    pub async fn new(
        mut connection: C,
        method_handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        instance_id: String,
        initial_property_values: FullInitialPropertyValues,
    ) -> Self {
        #[cfg(feature = "metrics")]
        let mut metrics = FullServerMetrics::default();

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

        let subscription_id_what_time_is_it_method_req = connection
            .subscribe(
                format!("full/{}/method/whatTimeIsIt", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_what_time_is_it_method_req =
            subscription_id_what_time_is_it_method_req.unwrap_or(u32::MAX);

        let subscription_id_hold_temperature_method_req = connection
            .subscribe(
                format!("full/{}/method/holdTemperature", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_hold_temperature_method_req =
            subscription_id_hold_temperature_method_req.unwrap_or(u32::MAX);

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
            what_time_is_it_method_req: subscription_id_what_time_is_it_method_req,
            hold_temperature_method_req: subscription_id_hold_temperature_method_req,

            favorite_number_property_update: subscription_id_favorite_number_property_update,
            favorite_foods_property_update: subscription_id_favorite_foods_property_update,
            family_name_property_update: subscription_id_family_name_property_update,
            last_breakfast_time_property_update:
                subscription_id_last_breakfast_time_property_update,
            last_birthdays_property_update: subscription_id_last_birthdays_property_update,
        };

        let property_values = FullProperties {
            favorite_number: Arc::new(RwLockWatch::new(
                initial_property_values.favorite_number.clone(),
            )),
            favorite_number_version: Arc::new(AtomicU32::new(
                initial_property_values.favorite_number_version,
            )),
            favorite_foods: Arc::new(RwLockWatch::new(
                initial_property_values.favorite_foods.clone(),
            )),
            favorite_foods_version: Arc::new(AtomicU32::new(
                initial_property_values.favorite_foods_version,
            )),
            lunch_menu: Arc::new(RwLockWatch::new(initial_property_values.lunch_menu.clone())),
            lunch_menu_version: Arc::new(AtomicU32::new(
                initial_property_values.lunch_menu_version,
            )),

            family_name: Arc::new(RwLockWatch::new(
                initial_property_values.family_name.clone(),
            )),
            family_name_version: Arc::new(AtomicU32::new(
                initial_property_values.family_name_version,
            )),

            last_breakfast_time: Arc::new(RwLockWatch::new(
                initial_property_values.last_breakfast_time.clone(),
            )),
            last_breakfast_time_version: Arc::new(AtomicU32::new(
                initial_property_values.last_breakfast_time_version,
            )),
            last_birthdays: Arc::new(RwLockWatch::new(
                initial_property_values.last_birthdays.clone(),
            )),
            last_birthdays_version: Arc::new(AtomicU32::new(
                initial_property_values.last_birthdays_version,
            )),
        };

        // Publish the initial property values for all the properties.
        #[cfg(feature = "metrics")]
        let start_prop_publish_time = std::time::Instant::now();
        {
            let topic = format!("full/{}/property/favoriteNumber/value", instance_id);

            let payload_obj = FavoriteNumberProperty {
                number: initial_property_values.favorite_number,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.favorite_number_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("full/{}/property/favoriteFoods/value", instance_id);
            let msg = message::property_value(
                &topic,
                &initial_property_values.favorite_foods,
                initial_property_values.favorite_foods_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("full/{}/property/lunchMenu/value", instance_id);
            let msg = message::property_value(
                &topic,
                &initial_property_values.lunch_menu,
                initial_property_values.lunch_menu_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("full/{}/property/familyName/value", instance_id);

            let payload_obj = FamilyNameProperty {
                family_name: initial_property_values.family_name,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.family_name_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("full/{}/property/lastBreakfastTime/value", instance_id);

            let payload_obj = LastBreakfastTimeProperty {
                timestamp: initial_property_values.last_breakfast_time,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.last_breakfast_time_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("full/{}/property/lastBirthdays/value", instance_id);
            let msg = message::property_value(
                &topic,
                &initial_property_values.last_birthdays,
                initial_property_values.last_birthdays_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        #[cfg(feature = "metrics")]
        {
            metrics.initial_property_publish_time = start_prop_publish_time.elapsed();
            debug!(
                "Published 6 initial property values in {:?}",
                metrics.initial_property_publish_time
            );
        }

        FullServer {
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
    pub fn get_metrics(&self) -> Arc<AsyncMutex<FullServerMetrics>> {
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
    /// Emits the todayIs signal with the given arguments.
    pub async fn emit_today_is(
        &mut self,
        day_of_month: i32,
        day_of_week: DayOfTheWeek,
    ) -> SentMessageFuture {
        let data = TodayIsSignalPayload {
            day_of_month,

            day_of_week,
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
        day_of_week: DayOfTheWeek,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = TodayIsSignalPayload {
            day_of_month,

            day_of_week,
        };
        let topic = format!("full/{}/signal/todayIs", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the randomWord signal with the given arguments.
    pub async fn emit_random_word(
        &mut self,
        word: String,
        time: chrono::DateTime<chrono::Utc>,
    ) -> SentMessageFuture {
        let data = RandomWordSignalPayload { word, time };
        let topic = format!("full/{}/signal/randomWord", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the randomWord signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_random_word_nowait(
        &mut self,
        word: String,
        time: chrono::DateTime<chrono::Utc>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = RandomWordSignalPayload { word, time };
        let topic = format!("full/{}/signal/randomWord", self.instance_id);
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
            handler_guard.handle_do_something(payload.task_to_do).await
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

    /// Handles a request message for the what_time_is_it method.
    async fn handle_what_time_is_it_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;

        // call the method handler
        let rc: Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_what_time_is_it().await
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

    /// Handles a request message for the hold_temperature method.
    async fn handle_hold_temperature_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<HoldTemperatureRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for hold_temperature: {:?}",
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
        let rc: Result<bool, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_hold_temperature(payload.temperature_celsius)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = HoldTemperatureReturnValues { success: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling hold_temperature: {:?}", &err);
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
            info!("No response topic provided, so no publishing response to `hold_temperature`.");
        }
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_favorite_number_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<i32>>, // Arc to the property value
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
                match serde_json::from_str::<FavoriteNumberProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the number field of the struct.
                        *write_request = new_property_structure.number.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'favorite_number' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'favorite_number' payload".to_string(),
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
                    FavoriteNumberProperty { number: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    FavoriteNumberProperty {
                        number: (*prop_lock).clone(),
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
                        "Error occurred while handling property update for 'favorite_number': {:?}",
                        &err
                    );
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'favorite_number'.");
        }
    }

    /// Watch for changes to the `favorite_number` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_favorite_number(&self) -> watch::Receiver<i32> {
        self.properties.favorite_number.subscribe()
    }

    pub fn get_favorite_number_handle(&self) -> WriteRequestLockWatch<i32> {
        self.properties.favorite_number.write_request()
    }

    /// Sets the value of the favorite_number property.
    pub async fn set_favorite_number(&mut self, value: i32) -> SentMessageFuture {
        let write_request_lock = self.get_favorite_number_handle();
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

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_favorite_foods_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<FavoriteFoodsProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 3 fields.
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
                match serde_json::from_str::<FavoriteFoodsProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'favorite_foods' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'favorite_foods' payload".to_string(),
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
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
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
                        "Error occurred while handling property update for 'favorite_foods': {:?}",
                        &err
                    );
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'favorite_foods'.");
        }
    }

    /// Watch for changes to the `favorite_foods` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_favorite_foods(&self) -> watch::Receiver<FavoriteFoodsProperty> {
        self.properties.favorite_foods.subscribe()
    }

    pub fn get_favorite_foods_handle(&self) -> WriteRequestLockWatch<FavoriteFoodsProperty> {
        self.properties.favorite_foods.write_request()
    }

    /// Sets the values of the favorite_foods property.
    pub async fn set_favorite_foods(&mut self, value: FavoriteFoodsProperty) -> SentMessageFuture {
        let write_request_lock = self.get_favorite_foods_handle();
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

    /// Watch for changes to the `lunch_menu` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_lunch_menu(&self) -> watch::Receiver<LunchMenuProperty> {
        self.properties.lunch_menu.subscribe()
    }

    pub fn get_lunch_menu_handle(&self) -> WriteRequestLockWatch<LunchMenuProperty> {
        self.properties.lunch_menu.write_request()
    }

    /// Sets the values of the lunch_menu property.
    pub async fn set_lunch_menu(&mut self, value: LunchMenuProperty) -> SentMessageFuture {
        let write_request_lock = self.get_lunch_menu_handle();
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

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_family_name_value(
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
                match serde_json::from_str::<FamilyNameProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the family_name field of the struct.
                        *write_request = new_property_structure.family_name.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'family_name' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'family_name' payload".to_string(),
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
                    FamilyNameProperty {
                        family_name: new_value,
                    }
                } else {
                    let prop_lock = property_pointer.read().await;

                    FamilyNameProperty {
                        family_name: (*prop_lock).clone(),
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
                        "Error occurred while handling property update for 'family_name': {:?}",
                        &err
                    );
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'family_name'.");
        }
    }

    /// Watch for changes to the `family_name` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_family_name(&self) -> watch::Receiver<String> {
        self.properties.family_name.subscribe()
    }

    pub fn get_family_name_handle(&self) -> WriteRequestLockWatch<String> {
        self.properties.family_name.write_request()
    }

    /// Sets the value of the family_name property.
    pub async fn set_family_name(&mut self, value: String) -> SentMessageFuture {
        let write_request_lock = self.get_family_name_handle();
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

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_last_breakfast_time_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<chrono::DateTime<chrono::Utc>>>, // Arc to the property value
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
                match serde_json::from_str::<LastBreakfastTimeProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the timestamp field of the struct.
                        *write_request = new_property_structure.timestamp.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'last_breakfast_time' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'last_breakfast_time' payload"
                                .to_string(),
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
                    LastBreakfastTimeProperty {
                        timestamp: new_value,
                    }
                } else {
                    let prop_lock = property_pointer.read().await;

                    LastBreakfastTimeProperty {
                        timestamp: (*prop_lock).clone(),
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
                    error!("Error occurred while handling property update for 'last_breakfast_time': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'last_breakfast_time'.");
        }
    }

    /// Watch for changes to the `last_breakfast_time` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_last_breakfast_time(&self) -> watch::Receiver<chrono::DateTime<chrono::Utc>> {
        self.properties.last_breakfast_time.subscribe()
    }

    pub fn get_last_breakfast_time_handle(
        &self,
    ) -> WriteRequestLockWatch<chrono::DateTime<chrono::Utc>> {
        self.properties.last_breakfast_time.write_request()
    }

    /// Sets the value of the last_breakfast_time property.
    pub async fn set_last_breakfast_time(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_last_breakfast_time_handle();
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

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_last_birthdays_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<LastBirthdaysProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 4 fields.
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
                match serde_json::from_str::<LastBirthdaysProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'last_birthdays' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'last_birthdays' payload".to_string(),
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
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
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
                        "Error occurred while handling property update for 'last_birthdays': {:?}",
                        &err
                    );
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'last_birthdays'.");
        }
    }

    /// Watch for changes to the `last_birthdays` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_last_birthdays(&self) -> watch::Receiver<LastBirthdaysProperty> {
        self.properties.last_birthdays.subscribe()
    }

    pub fn get_last_birthdays_handle(&self) -> WriteRequestLockWatch<LastBirthdaysProperty> {
        self.properties.last_birthdays.write_request()
    }

    /// Sets the values of the last_birthdays property.
    pub async fn set_last_birthdays(&mut self, value: LastBirthdaysProperty) -> SentMessageFuture {
        let write_request_lock = self.get_last_birthdays_handle();
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
            let instance_id_for_favorite_number_prop = self.instance_id.clone();
            let mut publisher_for_favorite_number_prop = self.mqtt_client.clone();
            let favorite_number_prop_version = props.favorite_number_version.clone();
            if let Some(mut rx_for_favorite_number_prop) =
                props.favorite_number.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_favorite_number_prop.recv().await
                    {
                        let payload_obj = FavoriteNumberProperty {
                            number: request.clone(),
                        };

                        let version_value = favorite_number_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "full/{}/property/favoriteNumber/value",
                            instance_id_for_favorite_number_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_favorite_number_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'favorite_number' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'favorite_number' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_favorite_foods_prop = self.instance_id.clone();
            let mut publisher_for_favorite_foods_prop = self.mqtt_client.clone();
            let favorite_foods_prop_version = props.favorite_foods_version.clone();
            if let Some(mut rx_for_favorite_foods_prop) =
                props.favorite_foods.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_favorite_foods_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = favorite_foods_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "full/{}/property/favoriteFoods/value",
                            instance_id_for_favorite_foods_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_favorite_foods_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'favorite_foods' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'favorite_foods' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_lunch_menu_prop = self.instance_id.clone();
            let mut publisher_for_lunch_menu_prop = self.mqtt_client.clone();
            let lunch_menu_prop_version = props.lunch_menu_version.clone();
            if let Some(mut rx_for_lunch_menu_prop) = props.lunch_menu.take_request_receiver() {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) = rx_for_lunch_menu_prop.recv().await {
                        let payload_obj = request.clone();

                        let version_value = lunch_menu_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "full/{}/property/lunchMenu/value",
                            instance_id_for_lunch_menu_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_lunch_menu_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'lunch_menu' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'lunch_menu' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_family_name_prop = self.instance_id.clone();
            let mut publisher_for_family_name_prop = self.mqtt_client.clone();
            let family_name_prop_version = props.family_name_version.clone();
            if let Some(mut rx_for_family_name_prop) = props.family_name.take_request_receiver() {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) = rx_for_family_name_prop.recv().await
                    {
                        let payload_obj = FamilyNameProperty {
                            family_name: request.clone(),
                        };

                        let version_value = family_name_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "full/{}/property/familyName/value",
                            instance_id_for_family_name_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_family_name_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'family_name' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'family_name' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_last_breakfast_time_prop = self.instance_id.clone();
            let mut publisher_for_last_breakfast_time_prop = self.mqtt_client.clone();
            let last_breakfast_time_prop_version = props.last_breakfast_time_version.clone();
            if let Some(mut rx_for_last_breakfast_time_prop) =
                props.last_breakfast_time.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_last_breakfast_time_prop.recv().await
                    {
                        let payload_obj = LastBreakfastTimeProperty {
                            timestamp: request.clone(),
                        };

                        let version_value = last_breakfast_time_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "full/{}/property/lastBreakfastTime/value",
                            instance_id_for_last_breakfast_time_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_last_breakfast_time_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'last_breakfast_time' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'last_breakfast_time' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_last_birthdays_prop = self.instance_id.clone();
            let mut publisher_for_last_birthdays_prop = self.mqtt_client.clone();
            let last_birthdays_prop_version = props.last_birthdays_version.clone();
            if let Some(mut rx_for_last_birthdays_prop) =
                props.last_birthdays.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_last_birthdays_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = last_birthdays_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "full/{}/property/lastBirthdays/value",
                            instance_id_for_last_birthdays_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_last_birthdays_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'last_birthdays' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'last_birthdays' property: {:?}", e);
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
                let topic = format!("full/{}/interface", instance_id);
                let info = crate::interface::InterfaceInfoBuilder::default()
                    .interface_name("Full".to_string())
                    .title("Example Interface".to_string())
                    .version("0.0.2".to_string())
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
                                _i if _i == sub_ids.add_numbers_method_req => {
                                    debug!("Received addNumbers method invocation message.");
                                    FullServer::<C>::handle_add_numbers_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.do_something_method_req => {
                                    debug!("Received doSomething method invocation message.");
                                    FullServer::<C>::handle_do_something_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.what_time_is_it_method_req => {
                                    debug!("Received what_time_is_it method invocation message.");
                                    FullServer::<C>::handle_what_time_is_it_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.hold_temperature_method_req => {
                                    debug!("Received hold_temperature method invocation message.");
                                    FullServer::<C>::handle_hold_temperature_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.favorite_number_property_update => {
                                    debug!(
                                        "Received favorite_number property update request message."
                                    );
                                    FullServer::<C>::update_favorite_number_value(
                                        publisher.clone(),
                                        properties.favorite_number.clone(),
                                        properties.favorite_number_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.favorite_foods_property_update => {
                                    debug!(
                                        "Received favorite_foods property update request message."
                                    );
                                    FullServer::<C>::update_favorite_foods_value(
                                        publisher.clone(),
                                        properties.favorite_foods.clone(),
                                        properties.favorite_foods_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.family_name_property_update => {
                                    debug!("Received family_name property update request message.");
                                    FullServer::<C>::update_family_name_value(
                                        publisher.clone(),
                                        properties.family_name.clone(),
                                        properties.family_name_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.last_breakfast_time_property_update => {
                                    debug!("Received last_breakfast_time property update request message.");
                                    FullServer::<C>::update_last_breakfast_time_value(
                                        publisher.clone(),
                                        properties.last_breakfast_time.clone(),
                                        properties.last_breakfast_time_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.last_birthdays_property_update => {
                                    debug!(
                                        "Received last_birthdays property update request message."
                                    );
                                    FullServer::<C>::update_last_birthdays_value(
                                        publisher.clone(),
                                        properties.last_birthdays.clone(),
                                        properties.last_birthdays_version.clone(),
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
        task_to_do: String,
    ) -> Result<DoSomethingReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the what_time_is_it method request.
    async fn handle_what_time_is_it(
        &self,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode>;

    /// Pointer to a function to handle the hold_temperature method request.
    async fn handle_hold_temperature(
        &self,
        temperature_celsius: f32,
    ) -> Result<bool, MethodReturnCode>;

    fn as_any(&self) -> &dyn Any;
}
