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
use std::any::Any;

use async_trait::async_trait;
use std::sync::{Arc, Mutex};
use tokio::sync::Mutex as AsyncMutex;

use serde_json;
use tokio::sync::{mpsc, watch};

use std::future::Future;
use std::pin::Pin;
use tokio::task::JoinError;
type SentMessageFuture = Pin<Box<dyn Future<Output = Result<(), MethodReturnCode>> + Send>>;
#[cfg(feature = "server")]
use tracing::{debug, error, info, warn};

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct FullServerSubscriptionIds {
    add_numbers_method_req: usize,
    do_something_method_req: usize,
    echo_method_req: usize,

    favorite_number_property_update: usize,

    favorite_foods_property_update: usize,

    lunch_menu_property_update: usize,

    family_name_property_update: usize,
}

#[derive(Clone)]
struct FullProperties {
    favorite_number_topic: Arc<String>,
    favorite_number: Arc<Mutex<Option<i32>>>,
    favorite_number_tx_channel: watch::Sender<Option<i32>>,
    favorite_foods_topic: Arc<String>,
    favorite_foods: Arc<Mutex<Option<FavoriteFoodsProperty>>>,
    favorite_foods_tx_channel: watch::Sender<Option<FavoriteFoodsProperty>>,
    lunch_menu_topic: Arc<String>,
    lunch_menu: Arc<Mutex<Option<LunchMenuProperty>>>,
    lunch_menu_tx_channel: watch::Sender<Option<LunchMenuProperty>>,
    family_name_topic: Arc<String>,
    family_name: Arc<Mutex<Option<String>>>,
    family_name_tx_channel: watch::Sender<Option<String>>,
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
}

impl FullServer {
    pub async fn new(
        connection: &mut MqttierClient,
        method_handlers: Arc<AsyncMutex<Box<dyn FullMethodHandlers>>>,
    ) -> Self {
        // Create a channel for messages to get from the MqttierClient object to this FullServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel::<ReceivedMessage>(64);

        // Create method handler struct
        let subscription_id_add_numbers_method_req = connection
            .subscribe(
                "full/method/addNumbers".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_add_numbers_method_req =
            subscription_id_add_numbers_method_req.unwrap_or_else(|_| usize::MAX);
        let subscription_id_do_something_method_req = connection
            .subscribe(
                "full/method/doSomething".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_do_something_method_req =
            subscription_id_do_something_method_req.unwrap_or_else(|_| usize::MAX);
        let subscription_id_echo_method_req = connection
            .subscribe(
                "full/method/echo".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_echo_method_req =
            subscription_id_echo_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_favorite_number_property_update = connection
            .subscribe(
                "full/property/favoriteNumber/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_number_property_update =
            subscription_id_favorite_number_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_favorite_foods_property_update = connection
            .subscribe(
                "full/property/favoriteFoods/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_favorite_foods_property_update =
            subscription_id_favorite_foods_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_lunch_menu_property_update = connection
            .subscribe(
                "full/property/lunchMenu/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_lunch_menu_property_update =
            subscription_id_lunch_menu_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_family_name_property_update = connection
            .subscribe(
                "full/property/familyName/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_family_name_property_update =
            subscription_id_family_name_property_update.unwrap_or_else(|_| usize::MAX);

        // Create structure for subscription ids.
        let sub_ids = FullServerSubscriptionIds {
            add_numbers_method_req: subscription_id_add_numbers_method_req,
            do_something_method_req: subscription_id_do_something_method_req,
            echo_method_req: subscription_id_echo_method_req,

            favorite_number_property_update: subscription_id_favorite_number_property_update,

            favorite_foods_property_update: subscription_id_favorite_foods_property_update,

            lunch_menu_property_update: subscription_id_lunch_menu_property_update,

            family_name_property_update: subscription_id_family_name_property_update,
        };

        let property_values = FullProperties {
            favorite_number_topic: Arc::new(String::from("full/property/favoriteNumber/value")),

            favorite_number: Arc::new(Mutex::new(None)),
            favorite_number_tx_channel: watch::channel(None).0,
            favorite_foods_topic: Arc::new(String::from("full/property/favoriteFoods/value")),

            favorite_foods: Arc::new(Mutex::new(None)),
            favorite_foods_tx_channel: watch::channel(None).0,
            lunch_menu_topic: Arc::new(String::from("full/property/lunchMenu/value")),

            lunch_menu: Arc::new(Mutex::new(None)),
            lunch_menu_tx_channel: watch::channel(None).0,
            family_name_topic: Arc::new(String::from("full/property/familyName/value")),

            family_name: Arc::new(Mutex::new(None)),
            family_name_tx_channel: watch::channel(None).0,
        };

        FullServer {
            mqttier_client: connection.clone(),

            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,
            method_handlers: method_handlers,
            properties: property_values,
            subscription_ids: sub_ids,

            client_id: connection.client_id.to_string(),
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
                    Err(MethodReturnCode::SerializationError(s))
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
    ) -> SentMessageFuture {
        let data = TodayIsSignalPayload {
            dayOfMonth: day_of_month,

            dayOfWeek: day_of_week,
        };
        let published_oneshot = self
            .mqttier_client
            .publish_structure("full/signal/todayIs".to_string(), &data)
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
                &MethodReturnCode::DeserializationError(
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
                    let retval = AddNumbersReturnValue { sum: retval };

                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &retval, corr_data)
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
                &MethodReturnCode::DeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<DoSomethingReturnValue, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_do_something(payload.aString).await
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
                &MethodReturnCode::DeserializationError(
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
                    let retval = EchoReturnValue { message: retval };

                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &retval, corr_data)
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

    async fn publish_favorite_number_value(
        publisher: MqttierClient,
        topic: String,
        data: i32,
    ) -> SentMessageFuture {
        let new_data = FavoriteNumberProperty { number: data };
        debug!(
            "Publishing 'favorite_number' property value to topic {}",
            topic
        );
        let published_oneshot = publisher.publish_state(topic, &new_data, 1).await;

        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_favorite_number_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        data: Arc<Mutex<Option<i32>>>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_data: FavoriteNumberProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(data) => data,
                Err(e) => {
                    error!(
                        "Failed to parse JSON received over MQTT to update 'favorite_number' property: {:?}",
                        e
                    );
                    return FullServer::wrap_return_code_in_future(
                        MethodReturnCode::DeserializationError(
                            "Failed to deserialize property 'favorite_number' payload".to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let assignment_result = match data.lock() {
            Ok(mut guard) => {
                *guard = Some(new_data.number);

                Ok(())
            }
            Err(_e) => Err(()),
        };
        // Since the lock is not Send, we need to be completely removed from it before calling the async method.
        if let Err(()) = assignment_result {
            return FullServer::wrap_return_code_in_future(MethodReturnCode::ServerError(format!(
                "Failed to lock mutex for updating property 'favorite_number'"
            )))
            .await;
        }
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.number;
        let data_to_send_to_watchers = data2.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'favorite_number' property: {:?}",
                    e
                );
            }
        };
        FullServer::publish_favorite_number_value(publisher, topic2, data2).await
    }

    pub async fn watch_favorite_number(&self) -> watch::Receiver<Option<i32>> {
        self.properties.favorite_number_tx_channel.subscribe()
    }

    pub async fn set_favorite_number(&mut self, data: i32) -> SentMessageFuture {
        println!("Setting favorite_number of type i32");
        let prop = self.properties.favorite_number.clone();
        {
            if let mut locked_data = prop.lock().unwrap() {
                *locked_data = Some(data.clone());
            } else {
                return FullServer::wrap_return_code_in_future(MethodReturnCode::ServerError(
                    format!("Failed to lock mutex for setting property 'favorite_number'"),
                ))
                .await;
            }
        }

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
        if !send_result {
            debug!("Property 'favorite_number' value not changed, so not notifying watchers.");
        }

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.favorite_number_topic.as_ref().clone();
        FullServer::publish_favorite_number_value(publisher2, topic2, data).await
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
        data: Arc<Mutex<Option<FavoriteFoodsProperty>>>,
        watch_sender: watch::Sender<Option<FavoriteFoodsProperty>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_data: FavoriteFoodsProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(data) => data,
                Err(e) => {
                    error!(
                        "Failed to parse JSON received over MQTT to update 'favorite_foods' property: {:?}",
                        e
                    );
                    return FullServer::wrap_return_code_in_future(
                        MethodReturnCode::DeserializationError(
                            "Failed to deserialize property 'favorite_foods' payload".to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let assignment_result = match data.lock() {
            Ok(mut guard) => {
                *guard = Some(new_data.clone());

                Ok(())
            }
            Err(_e) => Err(()),
        };
        // Since the lock is not Send, we need to be completely removed from it before calling the async method.
        if let Err(()) = assignment_result {
            return FullServer::wrap_return_code_in_future(MethodReturnCode::ServerError(format!(
                "Failed to lock mutex for updating property 'favorite_foods'"
            )))
            .await;
        }
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data;

        let data_to_send_to_watchers = data2.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'favorite_foods' property: {:?}",
                    e
                );
            }
        };
        FullServer::publish_favorite_foods_value(publisher, topic2, data2).await
    }

    pub async fn watch_favorite_foods(&self) -> watch::Receiver<Option<FavoriteFoodsProperty>> {
        self.properties.favorite_foods_tx_channel.subscribe()
    }

    pub async fn set_favorite_foods(&mut self, data: FavoriteFoodsProperty) -> SentMessageFuture {
        println!("Setting favorite_foods of type FavoriteFoodsProperty");
        let prop = self.properties.favorite_foods.clone();
        {
            if let mut locked_data = prop.lock().unwrap() {
                *locked_data = Some(data.clone());
            } else {
                return FullServer::wrap_return_code_in_future(MethodReturnCode::ServerError(
                    format!("Failed to lock mutex for setting property 'favorite_foods'"),
                ))
                .await;
            }
        }

        let data_to_send_to_watchers = Some(data.clone());
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
        if !send_result {
            debug!("Property 'favorite_foods' value not changed, so not notifying watchers.");
        }

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.favorite_foods_topic.as_ref().clone();
        FullServer::publish_favorite_foods_value(publisher2, topic2, data).await
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
        data: Arc<Mutex<Option<LunchMenuProperty>>>,
        watch_sender: watch::Sender<Option<LunchMenuProperty>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_data: LunchMenuProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(data) => data,
                Err(e) => {
                    error!(
                        "Failed to parse JSON received over MQTT to update 'lunch_menu' property: {:?}",
                        e
                    );
                    return FullServer::wrap_return_code_in_future(
                        MethodReturnCode::DeserializationError(
                            "Failed to deserialize property 'lunch_menu' payload".to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let assignment_result = match data.lock() {
            Ok(mut guard) => {
                *guard = Some(new_data.clone());

                Ok(())
            }
            Err(_e) => Err(()),
        };
        // Since the lock is not Send, we need to be completely removed from it before calling the async method.
        if let Err(()) = assignment_result {
            return FullServer::wrap_return_code_in_future(MethodReturnCode::ServerError(format!(
                "Failed to lock mutex for updating property 'lunch_menu'"
            )))
            .await;
        }
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data;

        let data_to_send_to_watchers = data2.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'lunch_menu' property: {:?}",
                    e
                );
            }
        };
        FullServer::publish_lunch_menu_value(publisher, topic2, data2).await
    }

    pub async fn watch_lunch_menu(&self) -> watch::Receiver<Option<LunchMenuProperty>> {
        self.properties.lunch_menu_tx_channel.subscribe()
    }

    pub async fn set_lunch_menu(&mut self, data: LunchMenuProperty) -> SentMessageFuture {
        println!("Setting lunch_menu of type LunchMenuProperty");
        let prop = self.properties.lunch_menu.clone();
        {
            if let mut locked_data = prop.lock().unwrap() {
                *locked_data = Some(data.clone());
            } else {
                return FullServer::wrap_return_code_in_future(MethodReturnCode::ServerError(
                    format!("Failed to lock mutex for setting property 'lunch_menu'"),
                ))
                .await;
            }
        }

        let data_to_send_to_watchers = Some(data.clone());
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
        if !send_result {
            debug!("Property 'lunch_menu' value not changed, so not notifying watchers.");
        }

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.lunch_menu_topic.as_ref().clone();
        FullServer::publish_lunch_menu_value(publisher2, topic2, data).await
    }

    async fn publish_family_name_value(
        publisher: MqttierClient,
        topic: String,
        data: String,
    ) -> SentMessageFuture {
        let new_data = FamilyNameProperty { family_name: data };
        debug!("Publishing 'family_name' property value to topic {}", topic);
        let published_oneshot = publisher.publish_state(topic, &new_data, 1).await;

        FullServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_family_name_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        data: Arc<Mutex<Option<String>>>,
        watch_sender: watch::Sender<Option<String>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_data: FamilyNameProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(data) => data,
                Err(e) => {
                    error!(
                        "Failed to parse JSON received over MQTT to update 'family_name' property: {:?}",
                        e
                    );
                    return FullServer::wrap_return_code_in_future(
                        MethodReturnCode::DeserializationError(
                            "Failed to deserialize property 'family_name' payload".to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let assignment_result = match data.lock() {
            Ok(mut guard) => {
                *guard = Some(new_data.family_name.clone());

                Ok(())
            }
            Err(_e) => Err(()),
        };
        // Since the lock is not Send, we need to be completely removed from it before calling the async method.
        if let Err(()) = assignment_result {
            return FullServer::wrap_return_code_in_future(MethodReturnCode::ServerError(format!(
                "Failed to lock mutex for updating property 'family_name'"
            )))
            .await;
        }
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.family_name.clone();
        let data_to_send_to_watchers = data2.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'family_name' property: {:?}",
                    e
                );
            }
        };
        FullServer::publish_family_name_value(publisher, topic2, data2).await
    }

    pub async fn watch_family_name(&self) -> watch::Receiver<Option<String>> {
        self.properties.family_name_tx_channel.subscribe()
    }

    pub async fn set_family_name(&mut self, data: String) -> SentMessageFuture {
        println!("Setting family_name of type String");
        let prop = self.properties.family_name.clone();
        {
            if let mut locked_data = prop.lock().unwrap() {
                *locked_data = Some(data.clone());
            } else {
                return FullServer::wrap_return_code_in_future(MethodReturnCode::ServerError(
                    format!("Failed to lock mutex for setting property 'family_name'"),
                ))
                .await;
            }
        }

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
        if !send_result {
            debug!("Property 'family_name' value not changed, so not notifying watchers.");
        }

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.family_name_topic.as_ref().clone();
        FullServer::publish_family_name_value(publisher2, topic2, data).await
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

        let loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                let opt_resp_topic = msg.response_topic.clone();
                let opt_corr_data = msg.correlation_data.clone();
                let topic = msg.topic.clone();

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
                        Err(e) => error!("Error processing update  property: {:?}", e),
                    }
                }
            }
            println!("No more messages from message_receiver channel");
        });
        let _ = tokio::join!(loop_task);

        println!("Server receive loop completed [error?]");
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
    ) -> Result<DoSomethingReturnValue, MethodReturnCode>;

    /// Pointer to a function to handle the echo method request.
    async fn handle_echo(&self, message: String) -> Result<String, MethodReturnCode>;

    fn as_any(&self) -> &dyn Any;
}
