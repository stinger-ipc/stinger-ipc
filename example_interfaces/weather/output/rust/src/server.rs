//! Server module for weather IPC
//!
//! This module is only available when the "server" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the weather interface.

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
struct WeatherServerSubscriptionIds {
    refresh_daily_forecast_method_req: u32,
    refresh_hourly_forecast_method_req: u32,
    refresh_current_conditions_method_req: u32,

    location_property_update: u32,

    current_condition_refresh_interval_property_update: u32,

    hourly_forecast_refresh_interval_property_update: u32,

    daily_forecast_refresh_interval_property_update: u32,
}

#[derive(Clone)]
struct WeatherProperties {
    location: Arc<AsyncMutex<Option<LocationProperty>>>,
    location_tx_channel: watch::Sender<Option<LocationProperty>>,
    location_version: Arc<AtomicU32>,
    current_temperature: Arc<AsyncMutex<Option<CurrentTemperatureProperty>>>,
    current_temperature_tx_channel: watch::Sender<Option<f32>>,
    current_temperature_version: Arc<AtomicU32>,
    current_condition: Arc<AsyncMutex<Option<CurrentConditionProperty>>>,
    current_condition_tx_channel: watch::Sender<Option<CurrentConditionProperty>>,
    current_condition_version: Arc<AtomicU32>,
    daily_forecast: Arc<AsyncMutex<Option<DailyForecastProperty>>>,
    daily_forecast_tx_channel: watch::Sender<Option<DailyForecastProperty>>,
    daily_forecast_version: Arc<AtomicU32>,
    hourly_forecast: Arc<AsyncMutex<Option<HourlyForecastProperty>>>,
    hourly_forecast_tx_channel: watch::Sender<Option<HourlyForecastProperty>>,
    hourly_forecast_version: Arc<AtomicU32>,
    current_condition_refresh_interval:
        Arc<AsyncMutex<Option<CurrentConditionRefreshIntervalProperty>>>,
    current_condition_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    current_condition_refresh_interval_version: Arc<AtomicU32>,
    hourly_forecast_refresh_interval:
        Arc<AsyncMutex<Option<HourlyForecastRefreshIntervalProperty>>>,
    hourly_forecast_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    hourly_forecast_refresh_interval_version: Arc<AtomicU32>,
    daily_forecast_refresh_interval: Arc<AsyncMutex<Option<DailyForecastRefreshIntervalProperty>>>,
    daily_forecast_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    daily_forecast_refresh_interval_version: Arc<AtomicU32>,
}

#[derive(Clone)]
pub struct WeatherServer<C: Mqtt5PubSub> {
    mqtt_client: C,

    /// Temporarily holds the receiver for the broadcast channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<broadcast::Receiver<MqttMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: broadcast::Sender<MqttMessage>,

    /// Struct contains all the method handlers.
    method_handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers<C>>>>,

    /// Struct contains all the properties.
    properties: WeatherProperties,

    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: WeatherServerSubscriptionIds,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,

    pub instance_id: String,
}

impl<C: Mqtt5PubSub + Clone + Send> WeatherServer<C> {
    pub async fn new(
        mut connection: C,
        method_handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers<C>>>>,
        instance_id: String,
    ) -> Self {
        // Create a channel for messages to get from the Mqtt5PubSub object to this WeatherServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = broadcast::channel::<MqttMessage>(64);

        // Create method handler struct
        let subscription_id_refresh_daily_forecast_method_req = connection
            .subscribe(
                format!("weather/{}/method/refreshDailyForecast", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_daily_forecast_method_req =
            subscription_id_refresh_daily_forecast_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_refresh_hourly_forecast_method_req = connection
            .subscribe(
                format!("weather/{}/method/refreshHourlyForecast", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_hourly_forecast_method_req =
            subscription_id_refresh_hourly_forecast_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_refresh_current_conditions_method_req = connection
            .subscribe(
                format!("weather/{}/method/refreshCurrentConditions", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_current_conditions_method_req =
            subscription_id_refresh_current_conditions_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_location_property_update = connection
            .subscribe(
                format!("weather/{}/property/location/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_location_property_update =
            subscription_id_location_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_current_condition_refresh_interval_property_update = connection
            .subscribe(
                format!(
                    "weather/{}/property/currentConditionRefreshInterval/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_current_condition_refresh_interval_property_update =
            subscription_id_current_condition_refresh_interval_property_update
                .unwrap_or_else(|_| u32::MAX);

        let subscription_id_hourly_forecast_refresh_interval_property_update = connection
            .subscribe(
                format!(
                    "weather/{}/property/hourlyForecastRefreshInterval/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_hourly_forecast_refresh_interval_property_update =
            subscription_id_hourly_forecast_refresh_interval_property_update
                .unwrap_or_else(|_| u32::MAX);

        let subscription_id_daily_forecast_refresh_interval_property_update = connection
            .subscribe(
                format!(
                    "weather/{}/property/dailyForecastRefreshInterval/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_daily_forecast_refresh_interval_property_update =
            subscription_id_daily_forecast_refresh_interval_property_update
                .unwrap_or_else(|_| u32::MAX);

        // Create structure for subscription ids.
        let sub_ids = WeatherServerSubscriptionIds {
            refresh_daily_forecast_method_req: subscription_id_refresh_daily_forecast_method_req,
            refresh_hourly_forecast_method_req: subscription_id_refresh_hourly_forecast_method_req,
            refresh_current_conditions_method_req:
                subscription_id_refresh_current_conditions_method_req,

            location_property_update: subscription_id_location_property_update,
            current_condition_refresh_interval_property_update:
                subscription_id_current_condition_refresh_interval_property_update,
            hourly_forecast_refresh_interval_property_update:
                subscription_id_hourly_forecast_refresh_interval_property_update,
            daily_forecast_refresh_interval_property_update:
                subscription_id_daily_forecast_refresh_interval_property_update,
        };

        let property_values = WeatherProperties {
            location: Arc::new(AsyncMutex::new(None)),
            location_tx_channel: watch::channel(None).0,
            location_version: Arc::new(AtomicU32::new(0)),
            current_temperature: Arc::new(AsyncMutex::new(None)),
            current_temperature_tx_channel: watch::channel(None).0,
            current_temperature_version: Arc::new(AtomicU32::new(0)),
            current_condition: Arc::new(AsyncMutex::new(None)),
            current_condition_tx_channel: watch::channel(None).0,
            current_condition_version: Arc::new(AtomicU32::new(0)),
            daily_forecast: Arc::new(AsyncMutex::new(None)),
            daily_forecast_tx_channel: watch::channel(None).0,
            daily_forecast_version: Arc::new(AtomicU32::new(0)),
            hourly_forecast: Arc::new(AsyncMutex::new(None)),
            hourly_forecast_tx_channel: watch::channel(None).0,
            hourly_forecast_version: Arc::new(AtomicU32::new(0)),
            current_condition_refresh_interval: Arc::new(AsyncMutex::new(None)),
            current_condition_refresh_interval_tx_channel: watch::channel(None).0,
            current_condition_refresh_interval_version: Arc::new(AtomicU32::new(0)),
            hourly_forecast_refresh_interval: Arc::new(AsyncMutex::new(None)),
            hourly_forecast_refresh_interval_tx_channel: watch::channel(None).0,
            hourly_forecast_refresh_interval_version: Arc::new(AtomicU32::new(0)),
            daily_forecast_refresh_interval: Arc::new(AsyncMutex::new(None)),
            daily_forecast_refresh_interval_tx_channel: watch::channel(None).0,
            daily_forecast_refresh_interval_version: Arc::new(AtomicU32::new(0)),
        };

        WeatherServer {
            mqtt_client: connection.clone(),

            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,
            method_handlers: method_handlers,
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
    /// Emits the current_time signal with the given arguments.
    pub async fn emit_current_time(&mut self, current_time: String) -> SentMessageFuture {
        let data = CurrentTimeSignalPayload {
            current_time: current_time,
        };
        let topic = format!("weather/{}/signal/currentTime", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the current_time signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_current_time_nowait(
        &mut self,
        current_time: String,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = CurrentTimeSignalPayload {
            current_time: current_time,
        };
        let topic = format!("weather/{}/signal/currentTime", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }

    /// Handles a request message for the refresh_daily_forecast method.
    async fn handle_refresh_daily_forecast_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;

        // call the method handler
        let rc: Result<(), MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_refresh_daily_forecast().await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(_retval) => {
                    let empty_resp = RefreshDailyForecastReturnValues {};
                    let msg = message::response(&resp_topic, &empty_resp, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling refresh_daily_forecast: {:?}",
                        &err
                    );
                    WeatherServer::<C>::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `refresh_daily_forecast`.");
        }
    }

    /// Handles a request message for the refresh_hourly_forecast method.
    async fn handle_refresh_hourly_forecast_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;

        // call the method handler
        let rc: Result<(), MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_refresh_hourly_forecast().await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(_retval) => {
                    let empty_resp = RefreshHourlyForecastReturnValues {};
                    let msg = message::response(&resp_topic, &empty_resp, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling refresh_hourly_forecast: {:?}",
                        &err
                    );
                    WeatherServer::<C>::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `refresh_hourly_forecast`.");
        }
    }

    /// Handles a request message for the refresh_current_conditions method.
    async fn handle_refresh_current_conditions_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;

        // call the method handler
        let rc: Result<(), MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_refresh_current_conditions().await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(_retval) => {
                    let empty_resp = RefreshCurrentConditionsReturnValues {};
                    let msg = message::response(&resp_topic, &empty_resp, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling refresh_current_conditions: {:?}",
                        &err
                    );
                    WeatherServer::<C>::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `refresh_current_conditions`.");
        }
    }

    async fn publish_location_value(
        mut publisher: C,
        topic: String,
        data: LocationProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        WeatherServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_location_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<LocationProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<LocationProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: LocationProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'location' property: {:?}", e);
                    return WeatherServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'location' payload".to_string(),
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
                    "Failed to notify local watchers for 'location' property: {:?}",
                    e
                );
            }
        };

        WeatherServer::publish_location_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_location(&self) -> watch::Receiver<Option<LocationProperty>> {
        self.properties.location_tx_channel.subscribe()
    }

    /// Sets the values of the location property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_location(&mut self, data: LocationProperty) -> SentMessageFuture {
        let prop = self.properties.location.clone();

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
            .location_tx_channel
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
            debug!("Property 'location' value not changed, so not notifying watchers.");
            return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None))
                .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!("weather/{}/property/location/value", self.instance_id);
                let new_version = self
                    .properties
                    .location_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                WeatherServer::<C>::publish_location_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_current_temperature_value(
        mut publisher: C,
        topic: String,
        data: CurrentTemperatureProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        WeatherServer::<C>::oneshot_to_future(ch).await
    }

    /// Sets the value of the current_temperature property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_current_temperature(&mut self, data: f32) -> SentMessageFuture {
        let prop = self.properties.current_temperature.clone();

        let new_prop_obj = CurrentTemperatureProperty {
            temperature_f: data.clone(),
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
            .current_temperature_tx_channel
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
            debug!("Property 'current_temperature' value not changed, so not notifying watchers.");
            return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None))
                .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "weather/{}/property/currentTemperature/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .current_temperature_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                WeatherServer::<C>::publish_current_temperature_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_current_condition_value(
        mut publisher: C,
        topic: String,
        data: CurrentConditionProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        WeatherServer::<C>::oneshot_to_future(ch).await
    }

    /// Sets the values of the current_condition property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_current_condition(
        &mut self,
        data: CurrentConditionProperty,
    ) -> SentMessageFuture {
        let prop = self.properties.current_condition.clone();

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
            .current_condition_tx_channel
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
            debug!("Property 'current_condition' value not changed, so not notifying watchers.");
            return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None))
                .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "weather/{}/property/currentCondition/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .current_condition_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                WeatherServer::<C>::publish_current_condition_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_daily_forecast_value(
        mut publisher: C,
        topic: String,
        data: DailyForecastProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        WeatherServer::<C>::oneshot_to_future(ch).await
    }

    /// Sets the values of the daily_forecast property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_daily_forecast(&mut self, data: DailyForecastProperty) -> SentMessageFuture {
        let prop = self.properties.daily_forecast.clone();

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
                .daily_forecast_tx_channel
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
            debug!("Property 'daily_forecast' value not changed, so not notifying watchers.");
            return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None))
                .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!("weather/{}/property/dailyForecast/value", self.instance_id);
                let new_version = self
                    .properties
                    .daily_forecast_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                WeatherServer::<C>::publish_daily_forecast_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_hourly_forecast_value(
        mut publisher: C,
        topic: String,
        data: HourlyForecastProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        WeatherServer::<C>::oneshot_to_future(ch).await
    }

    /// Sets the values of the hourly_forecast property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_hourly_forecast(&mut self, data: HourlyForecastProperty) -> SentMessageFuture {
        let prop = self.properties.hourly_forecast.clone();

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
                .hourly_forecast_tx_channel
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
            debug!("Property 'hourly_forecast' value not changed, so not notifying watchers.");
            return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None))
                .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!("weather/{}/property/hourlyForecast/value", self.instance_id);
                let new_version = self
                    .properties
                    .hourly_forecast_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                WeatherServer::<C>::publish_hourly_forecast_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_current_condition_refresh_interval_value(
        mut publisher: C,
        topic: String,
        data: CurrentConditionRefreshIntervalProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        WeatherServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_current_condition_refresh_interval_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<CurrentConditionRefreshIntervalProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: CurrentConditionRefreshIntervalProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'current_condition_refresh_interval' property: {:?}", e);
                    return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::ServerDeserializationError("Failed to deserialize property 'current_condition_refresh_interval' payload".to_string())).await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.seconds.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'current_condition_refresh_interval' property: {:?}", e);
            }
        };

        WeatherServer::publish_current_condition_refresh_interval_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_current_condition_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .current_condition_refresh_interval_tx_channel
            .subscribe()
    }

    /// Sets the value of the current_condition_refresh_interval property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_current_condition_refresh_interval(&mut self, data: i32) -> SentMessageFuture {
        let prop = self.properties.current_condition_refresh_interval.clone();

        let new_prop_obj = CurrentConditionRefreshIntervalProperty {
            seconds: data.clone(),
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
            .current_condition_refresh_interval_tx_channel
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
            debug!("Property 'current_condition_refresh_interval' value not changed, so not notifying watchers.");
            return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None))
                .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "weather/{}/property/currentConditionRefreshInterval/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .current_condition_refresh_interval_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                WeatherServer::<C>::publish_current_condition_refresh_interval_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_hourly_forecast_refresh_interval_value(
        mut publisher: C,
        topic: String,
        data: HourlyForecastRefreshIntervalProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        WeatherServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_hourly_forecast_refresh_interval_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<HourlyForecastRefreshIntervalProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: HourlyForecastRefreshIntervalProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'hourly_forecast_refresh_interval' property: {:?}", e);
                    return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::ServerDeserializationError("Failed to deserialize property 'hourly_forecast_refresh_interval' payload".to_string())).await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.seconds.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'hourly_forecast_refresh_interval' property: {:?}", e);
            }
        };

        WeatherServer::publish_hourly_forecast_refresh_interval_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_hourly_forecast_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .hourly_forecast_refresh_interval_tx_channel
            .subscribe()
    }

    /// Sets the value of the hourly_forecast_refresh_interval property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_hourly_forecast_refresh_interval(&mut self, data: i32) -> SentMessageFuture {
        let prop = self.properties.hourly_forecast_refresh_interval.clone();

        let new_prop_obj = HourlyForecastRefreshIntervalProperty {
            seconds: data.clone(),
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
            .hourly_forecast_refresh_interval_tx_channel
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
            debug!("Property 'hourly_forecast_refresh_interval' value not changed, so not notifying watchers.");
            return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None))
                .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "weather/{}/property/hourlyForecastRefreshInterval/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .hourly_forecast_refresh_interval_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                WeatherServer::<C>::publish_hourly_forecast_refresh_interval_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_daily_forecast_refresh_interval_value(
        mut publisher: C,
        topic: String,
        data: DailyForecastRefreshIntervalProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        WeatherServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_daily_forecast_refresh_interval_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<DailyForecastRefreshIntervalProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: DailyForecastRefreshIntervalProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'daily_forecast_refresh_interval' property: {:?}", e);
                    return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::ServerDeserializationError("Failed to deserialize property 'daily_forecast_refresh_interval' payload".to_string())).await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.seconds.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'daily_forecast_refresh_interval' property: {:?}", e);
            }
        };

        WeatherServer::publish_daily_forecast_refresh_interval_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_daily_forecast_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .daily_forecast_refresh_interval_tx_channel
            .subscribe()
    }

    /// Sets the value of the daily_forecast_refresh_interval property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_daily_forecast_refresh_interval(&mut self, data: i32) -> SentMessageFuture {
        let prop = self.properties.daily_forecast_refresh_interval.clone();

        let new_prop_obj = DailyForecastRefreshIntervalProperty {
            seconds: data.clone(),
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
            .daily_forecast_refresh_interval_tx_channel
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
            debug!("Property 'daily_forecast_refresh_interval' value not changed, so not notifying watchers.");
            return WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(None))
                .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "weather/{}/property/dailyForecastRefreshInterval/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .daily_forecast_refresh_interval_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                WeatherServer::<C>::publish_daily_forecast_refresh_interval_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                WeatherServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
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
                let topic = format!("weather/{}/interface", instance_id);
                let info = crate::interface::InterfaceInfo::new()
                    .interface_name("weather".to_string())
                    .title("NWS weather forecast".to_string())
                    .version("0.1.2".to_string())
                    .instance(instance_id.clone())
                    .connection_topic(topic.clone())
                    .build();
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
                            if subscription_id == sub_ids.refresh_daily_forecast_method_req {
                                WeatherServer::<C>::handle_refresh_daily_forecast_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.refresh_hourly_forecast_method_req
                            {
                                WeatherServer::<C>::handle_refresh_hourly_forecast_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id
                                == sub_ids.refresh_current_conditions_method_req
                            {
                                WeatherServer::<C>::handle_refresh_current_conditions_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else {
                                let update_prop_future = {
                                    if subscription_id == sub_ids.location_property_update {
                                        let prop_topic = format!(
                                            "weather/{}/property/location/value",
                                            instance_id
                                        );
                                        WeatherServer::<C>::update_location_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.location.clone(),
                                            properties.location_version.clone(),
                                            properties.location_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids
                                            .current_condition_refresh_interval_property_update
                                    {
                                        let prop_topic = format!("weather/{}/property/currentConditionRefreshInterval/value", instance_id);
                                        WeatherServer::<C>::update_current_condition_refresh_interval_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.current_condition_refresh_interval.clone(),
                                                    properties.current_condition_refresh_interval_version.clone(),
                                                    properties.current_condition_refresh_interval_tx_channel.clone(),
                                                    msg).await
                                    } else if subscription_id
                                        == sub_ids.hourly_forecast_refresh_interval_property_update
                                    {
                                        let prop_topic = format!("weather/{}/property/hourlyForecastRefreshInterval/value", instance_id);
                                        WeatherServer::<C>::update_hourly_forecast_refresh_interval_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.hourly_forecast_refresh_interval.clone(),
                                                    properties.hourly_forecast_refresh_interval_version.clone(),
                                                    properties.hourly_forecast_refresh_interval_tx_channel.clone(),
                                                    msg).await
                                    } else if subscription_id
                                        == sub_ids.daily_forecast_refresh_interval_property_update
                                    {
                                        let prop_topic = format!("weather/{}/property/dailyForecastRefreshInterval/value", instance_id);
                                        WeatherServer::<C>::update_daily_forecast_refresh_interval_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.daily_forecast_refresh_interval.clone(),
                                                    properties.daily_forecast_refresh_interval_version.clone(),
                                                    properties.daily_forecast_refresh_interval_tx_channel.clone(),
                                                    msg).await
                                    } else {
                                        WeatherServer::<C>::wrap_return_code_in_future(
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
                                            WeatherServer::<C>::publish_error_response(
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
pub trait WeatherMethodHandlers<C: Mqtt5PubSub>: Send + Sync {
    async fn initialize(&mut self, server: WeatherServer<C>) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the refresh_daily_forecast method request.
    async fn handle_refresh_daily_forecast(&self) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the refresh_hourly_forecast method request.
    async fn handle_refresh_hourly_forecast(&self) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the refresh_current_conditions method request.
    async fn handle_refresh_current_conditions(&self) -> Result<(), MethodReturnCode>;

    fn as_any(&self) -> &dyn Any;
}
