//! Server module for weather IPC
//!
//! This module is only available when the "server" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the weather interface.
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
struct WeatherServerSubscriptionIds {
    refresh_daily_forecast_method_req: usize,
    refresh_hourly_forecast_method_req: usize,
    refresh_current_conditions_method_req: usize,

    location_property_update: usize,

    current_condition_refresh_interval_property_update: usize,

    hourly_forecast_refresh_interval_property_update: usize,

    daily_forecast_refresh_interval_property_update: usize,
}

#[derive(Clone)]
struct WeatherProperties {
    location_topic: Arc<String>,
    location: Arc<AsyncMutex<Option<LocationProperty>>>,
    location_tx_channel: watch::Sender<Option<LocationProperty>>,
    current_temperature_topic: Arc<String>,
    current_temperature: Arc<AsyncMutex<Option<CurrentTemperatureProperty>>>,
    current_temperature_tx_channel: watch::Sender<Option<f32>>,
    current_condition_topic: Arc<String>,
    current_condition: Arc<AsyncMutex<Option<CurrentConditionProperty>>>,
    current_condition_tx_channel: watch::Sender<Option<CurrentConditionProperty>>,
    daily_forecast_topic: Arc<String>,
    daily_forecast: Arc<AsyncMutex<Option<DailyForecastProperty>>>,
    daily_forecast_tx_channel: watch::Sender<Option<DailyForecastProperty>>,
    hourly_forecast_topic: Arc<String>,
    hourly_forecast: Arc<AsyncMutex<Option<HourlyForecastProperty>>>,
    hourly_forecast_tx_channel: watch::Sender<Option<HourlyForecastProperty>>,
    current_condition_refresh_interval_topic: Arc<String>,
    current_condition_refresh_interval:
        Arc<AsyncMutex<Option<CurrentConditionRefreshIntervalProperty>>>,
    current_condition_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    hourly_forecast_refresh_interval_topic: Arc<String>,
    hourly_forecast_refresh_interval:
        Arc<AsyncMutex<Option<HourlyForecastRefreshIntervalProperty>>>,
    hourly_forecast_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    daily_forecast_refresh_interval_topic: Arc<String>,
    daily_forecast_refresh_interval: Arc<AsyncMutex<Option<DailyForecastRefreshIntervalProperty>>>,
    daily_forecast_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
}

#[derive(Clone)]
pub struct WeatherServer {
    mqttier_client: MqttierClient,

    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<mpsc::Receiver<ReceivedMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Struct contains all the method handlers.
    method_handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers>>>,

    /// Struct contains all the properties.
    properties: WeatherProperties,

    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: WeatherServerSubscriptionIds,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,

    pub instance_id: String,
}

impl WeatherServer {
    pub async fn new(
        connection: &mut MqttierClient,
        method_handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers>>>,
        instance_id: String,
    ) -> Self {
        // Create a channel for messages to get from the MqttierClient object to this WeatherServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel::<ReceivedMessage>(64);

        // Create method handler struct
        let subscription_id_refresh_daily_forecast_method_req = connection
            .subscribe(
                format!("weather/{}/method/refreshDailyForecast", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_daily_forecast_method_req =
            subscription_id_refresh_daily_forecast_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_refresh_hourly_forecast_method_req = connection
            .subscribe(
                format!("weather/{}/method/refreshHourlyForecast", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_hourly_forecast_method_req =
            subscription_id_refresh_hourly_forecast_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_refresh_current_conditions_method_req = connection
            .subscribe(
                format!("weather/{}/method/refreshCurrentConditions", instance_id),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_current_conditions_method_req =
            subscription_id_refresh_current_conditions_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_location_property_update = connection
            .subscribe(
                format!("weather/{}/property/location/setValue", instance_id),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_location_property_update =
            subscription_id_location_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_current_condition_refresh_interval_property_update = connection
            .subscribe(
                format!(
                    "weather/{}/property/currentConditionRefreshInterval/setValue",
                    instance_id
                ),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_current_condition_refresh_interval_property_update =
            subscription_id_current_condition_refresh_interval_property_update
                .unwrap_or_else(|_| usize::MAX);

        let subscription_id_hourly_forecast_refresh_interval_property_update = connection
            .subscribe(
                format!(
                    "weather/{}/property/hourlyForecastRefreshInterval/setValue",
                    instance_id
                ),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_hourly_forecast_refresh_interval_property_update =
            subscription_id_hourly_forecast_refresh_interval_property_update
                .unwrap_or_else(|_| usize::MAX);

        let subscription_id_daily_forecast_refresh_interval_property_update = connection
            .subscribe(
                format!(
                    "weather/{}/property/dailyForecastRefreshInterval/setValue",
                    instance_id
                ),
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_daily_forecast_refresh_interval_property_update =
            subscription_id_daily_forecast_refresh_interval_property_update
                .unwrap_or_else(|_| usize::MAX);

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
            location_topic: Arc::new(format!("weather/{}/property/location/value", instance_id)),
            location: Arc::new(AsyncMutex::new(None)),
            location_tx_channel: watch::channel(None).0,
            current_temperature_topic: Arc::new(format!(
                "weather/{}/property/currentTemperature/value",
                instance_id
            )),
            current_temperature: Arc::new(AsyncMutex::new(None)),
            current_temperature_tx_channel: watch::channel(None).0,
            current_condition_topic: Arc::new(format!(
                "weather/{}/property/currentCondition/value",
                instance_id
            )),
            current_condition: Arc::new(AsyncMutex::new(None)),
            current_condition_tx_channel: watch::channel(None).0,
            daily_forecast_topic: Arc::new(format!(
                "weather/{}/property/dailyForecast/value",
                instance_id
            )),
            daily_forecast: Arc::new(AsyncMutex::new(None)),
            daily_forecast_tx_channel: watch::channel(None).0,
            hourly_forecast_topic: Arc::new(format!(
                "weather/{}/property/hourlyForecast/value",
                instance_id
            )),
            hourly_forecast: Arc::new(AsyncMutex::new(None)),
            hourly_forecast_tx_channel: watch::channel(None).0,
            current_condition_refresh_interval_topic: Arc::new(format!(
                "weather/{}/property/currentConditionRefreshInterval/value",
                instance_id
            )),
            current_condition_refresh_interval: Arc::new(AsyncMutex::new(None)),
            current_condition_refresh_interval_tx_channel: watch::channel(None).0,
            hourly_forecast_refresh_interval_topic: Arc::new(format!(
                "weather/{}/property/hourlyForecastRefreshInterval/value",
                instance_id
            )),
            hourly_forecast_refresh_interval: Arc::new(AsyncMutex::new(None)),
            hourly_forecast_refresh_interval_tx_channel: watch::channel(None).0,
            daily_forecast_refresh_interval_topic: Arc::new(format!(
                "weather/{}/property/dailyForecastRefreshInterval/value",
                instance_id
            )),
            daily_forecast_refresh_interval: Arc::new(AsyncMutex::new(None)),
            daily_forecast_refresh_interval_tx_channel: watch::channel(None).0,
        };

        WeatherServer {
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
    /// Emits the current_time signal with the given arguments.
    pub async fn emit_current_time(&mut self, current_time: String) -> SentMessageFuture {
        let data = CurrentTimeSignalPayload {
            current_time: current_time,
        };
        let published_oneshot = self
            .mqttier_client
            .publish_structure(
                format!("weather/{}/signal/currentTime", self.instance_id),
                &data,
            )
            .await;
        WeatherServer::oneshot_to_future(published_oneshot).await
    }

    /// Handles a request message for the refresh_daily_forecast method.
    async fn handle_refresh_daily_forecast_request(
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers>>>,
        msg: ReceivedMessage,
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &empty_resp, corr_data)
                        .await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling refresh_daily_forecast: {:?}",
                        &err
                    );
                    WeatherServer::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `refresh_daily_forecast`.");
        }
    }

    /// Handles a request message for the refresh_hourly_forecast method.
    async fn handle_refresh_hourly_forecast_request(
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers>>>,
        msg: ReceivedMessage,
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &empty_resp, corr_data)
                        .await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling refresh_hourly_forecast: {:?}",
                        &err
                    );
                    WeatherServer::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `refresh_hourly_forecast`.");
        }
    }

    /// Handles a request message for the refresh_current_conditions method.
    async fn handle_refresh_current_conditions_request(
        publisher: MqttierClient,
        handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers>>>,
        msg: ReceivedMessage,
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
                    let _fut_publish_result = publisher
                        .publish_response(resp_topic, &empty_resp, corr_data)
                        .await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling refresh_current_conditions: {:?}",
                        &err
                    );
                    WeatherServer::publish_error_response(
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
            info!("No response topic provided, so no publishing response to `refresh_current_conditions`.");
        }
    }

    async fn publish_location_value(
        publisher: MqttierClient,
        topic: String,
        data: LocationProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        WeatherServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_location_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<LocationProperty>>>,
        watch_sender: watch::Sender<Option<LocationProperty>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: LocationProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'location' property: {:?}", e);
                    return WeatherServer::wrap_return_code_in_future(
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

        let topic2: String = topic.as_ref().clone();
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
        WeatherServer::publish_location_value(publisher, topic2, new_property_structure).await
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
            return WeatherServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.location_topic.as_ref().clone();
                WeatherServer::publish_location_value(publisher2, topic2, prop_obj).await
            } else {
                WeatherServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_current_temperature_value(
        publisher: MqttierClient,
        topic: String,
        data: CurrentTemperatureProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        WeatherServer::oneshot_to_future(published_oneshot).await
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
            return WeatherServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.current_temperature_topic.as_ref().clone();
                WeatherServer::publish_current_temperature_value(publisher2, topic2, prop_obj).await
            } else {
                WeatherServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_current_condition_value(
        publisher: MqttierClient,
        topic: String,
        data: CurrentConditionProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        WeatherServer::oneshot_to_future(published_oneshot).await
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
            return WeatherServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.current_condition_topic.as_ref().clone();
                WeatherServer::publish_current_condition_value(publisher2, topic2, prop_obj).await
            } else {
                WeatherServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_daily_forecast_value(
        publisher: MqttierClient,
        topic: String,
        data: DailyForecastProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        WeatherServer::oneshot_to_future(published_oneshot).await
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
            return WeatherServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.daily_forecast_topic.as_ref().clone();
                WeatherServer::publish_daily_forecast_value(publisher2, topic2, prop_obj).await
            } else {
                WeatherServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_hourly_forecast_value(
        publisher: MqttierClient,
        topic: String,
        data: HourlyForecastProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        WeatherServer::oneshot_to_future(published_oneshot).await
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
            return WeatherServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self.properties.hourly_forecast_topic.as_ref().clone();
                WeatherServer::publish_hourly_forecast_value(publisher2, topic2, prop_obj).await
            } else {
                WeatherServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_current_condition_refresh_interval_value(
        publisher: MqttierClient,
        topic: String,
        data: CurrentConditionRefreshIntervalProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        WeatherServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_current_condition_refresh_interval_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<CurrentConditionRefreshIntervalProperty>>>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: CurrentConditionRefreshIntervalProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'current_condition_refresh_interval' property: {:?}", e);
                    return WeatherServer::wrap_return_code_in_future(MethodReturnCode::ServerDeserializationError("Failed to deserialize property 'current_condition_refresh_interval' payload".to_string())).await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.as_ref().clone();
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
            return WeatherServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self
                    .properties
                    .current_condition_refresh_interval_topic
                    .as_ref()
                    .clone();
                WeatherServer::publish_current_condition_refresh_interval_value(
                    publisher2, topic2, prop_obj,
                )
                .await
            } else {
                WeatherServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_hourly_forecast_refresh_interval_value(
        publisher: MqttierClient,
        topic: String,
        data: HourlyForecastRefreshIntervalProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        WeatherServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_hourly_forecast_refresh_interval_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<HourlyForecastRefreshIntervalProperty>>>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: HourlyForecastRefreshIntervalProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'hourly_forecast_refresh_interval' property: {:?}", e);
                    return WeatherServer::wrap_return_code_in_future(MethodReturnCode::ServerDeserializationError("Failed to deserialize property 'hourly_forecast_refresh_interval' payload".to_string())).await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.as_ref().clone();
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
            return WeatherServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self
                    .properties
                    .hourly_forecast_refresh_interval_topic
                    .as_ref()
                    .clone();
                WeatherServer::publish_hourly_forecast_refresh_interval_value(
                    publisher2, topic2, prop_obj,
                )
                .await
            } else {
                WeatherServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_daily_forecast_refresh_interval_value(
        publisher: MqttierClient,
        topic: String,
        data: DailyForecastRefreshIntervalProperty,
    ) -> SentMessageFuture {
        let published_oneshot = publisher.publish_state(topic, &data, 1).await;
        WeatherServer::oneshot_to_future(published_oneshot).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_daily_forecast_refresh_interval_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        property_pointer: Arc<AsyncMutex<Option<DailyForecastRefreshIntervalProperty>>>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: ReceivedMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let new_property_structure: DailyForecastRefreshIntervalProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'daily_forecast_refresh_interval' property: {:?}", e);
                    return WeatherServer::wrap_return_code_in_future(MethodReturnCode::ServerDeserializationError("Failed to deserialize property 'daily_forecast_refresh_interval' payload".to_string())).await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.as_ref().clone();
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
            return WeatherServer::wrap_return_code_in_future(MethodReturnCode::Success).await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqttier_client.clone();
                let topic2 = self
                    .properties
                    .daily_forecast_refresh_interval_topic
                    .as_ref()
                    .clone();
                WeatherServer::publish_daily_forecast_refresh_interval_value(
                    publisher2, topic2, prop_obj,
                )
                .await
            } else {
                WeatherServer::wrap_return_code_in_future(MethodReturnCode::UnknownError(
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
                    .interface_name("weather".to_string())
                    .title("NWS weather forecast".to_string())
                    .version("0.1.2".to_string())
                    .instance(instance_id.clone())
                    .connection_topic(format!("client/{}/online", interface_publisher.client_id))
                    .build();
                let _ = interface_publisher
                    .publish_status(format!("weather/{}/interface", instance_id), &info, 150)
                    .await;
            }
        });
        let loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                let opt_resp_topic = msg.response_topic.clone();
                let opt_corr_data = msg.correlation_data.clone();

                if msg.subscription_id == sub_ids.refresh_daily_forecast_method_req {
                    WeatherServer::handle_refresh_daily_forecast_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.refresh_hourly_forecast_method_req {
                    WeatherServer::handle_refresh_hourly_forecast_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else if msg.subscription_id == sub_ids.refresh_current_conditions_method_req {
                    WeatherServer::handle_refresh_current_conditions_request(
                        publisher.clone(),
                        method_handlers.clone(),
                        msg,
                    )
                    .await;
                } else {
                    let update_prop_future = {
                        if msg.subscription_id == sub_ids.location_property_update {
                            WeatherServer::update_location_value(
                                publisher.clone(),
                                properties.location_topic.clone(),
                                properties.location.clone(),
                                properties.location_tx_channel.clone(),
                                msg,
                            )
                            .await
                        } else if msg.subscription_id
                            == sub_ids.current_condition_refresh_interval_property_update
                        {
                            WeatherServer::update_current_condition_refresh_interval_value(
                                publisher.clone(),
                                properties.current_condition_refresh_interval_topic.clone(),
                                properties.current_condition_refresh_interval.clone(),
                                properties
                                    .current_condition_refresh_interval_tx_channel
                                    .clone(),
                                msg,
                            )
                            .await
                        } else if msg.subscription_id
                            == sub_ids.hourly_forecast_refresh_interval_property_update
                        {
                            WeatherServer::update_hourly_forecast_refresh_interval_value(
                                publisher.clone(),
                                properties.hourly_forecast_refresh_interval_topic.clone(),
                                properties.hourly_forecast_refresh_interval.clone(),
                                properties
                                    .hourly_forecast_refresh_interval_tx_channel
                                    .clone(),
                                msg,
                            )
                            .await
                        } else if msg.subscription_id
                            == sub_ids.daily_forecast_refresh_interval_property_update
                        {
                            WeatherServer::update_daily_forecast_refresh_interval_value(
                                publisher.clone(),
                                properties.daily_forecast_refresh_interval_topic.clone(),
                                properties.daily_forecast_refresh_interval.clone(),
                                properties
                                    .daily_forecast_refresh_interval_tx_channel
                                    .clone(),
                                msg,
                            )
                            .await
                        } else {
                            WeatherServer::wrap_return_code_in_future(
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
                                WeatherServer::publish_error_response(
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
pub trait WeatherMethodHandlers: Send + Sync {
    async fn initialize(&mut self, server: WeatherServer) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the refresh_daily_forecast method request.
    async fn handle_refresh_daily_forecast(&self) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the refresh_hourly_forecast method request.
    async fn handle_refresh_hourly_forecast(&self) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the refresh_current_conditions method request.
    async fn handle_refresh_current_conditions(&self) -> Result<(), MethodReturnCode>;

    fn as_any(&self) -> &dyn Any;
}
