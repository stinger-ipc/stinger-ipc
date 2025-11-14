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

use crate::property::WeatherInitialPropertyValues;
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
    pub location: Arc<RwLockWatch<LocationProperty>>,
    location_version: Arc<AtomicU32>,
    pub current_temperature: Arc<RwLockWatch<f32>>,
    current_temperature_version: Arc<AtomicU32>,
    pub current_condition: Arc<RwLockWatch<CurrentConditionProperty>>,
    current_condition_version: Arc<AtomicU32>,
    pub daily_forecast: Arc<RwLockWatch<DailyForecastProperty>>,
    daily_forecast_version: Arc<AtomicU32>,
    pub hourly_forecast: Arc<RwLockWatch<HourlyForecastProperty>>,
    hourly_forecast_version: Arc<AtomicU32>,
    pub current_condition_refresh_interval: Arc<RwLockWatch<i32>>,
    current_condition_refresh_interval_version: Arc<AtomicU32>,
    pub hourly_forecast_refresh_interval: Arc<RwLockWatch<i32>>,
    hourly_forecast_refresh_interval_version: Arc<AtomicU32>,
    pub daily_forecast_refresh_interval: Arc<RwLockWatch<i32>>,
    daily_forecast_refresh_interval_version: Arc<AtomicU32>,
}

#[cfg(feature = "metrics")]
#[derive(Debug, Serialize)]
pub struct WeatherServerMetrics {
    pub refresh_daily_forecast_calls: u64,
    pub refresh_daily_forecast_errors: u64,
    pub refresh_hourly_forecast_calls: u64,
    pub refresh_hourly_forecast_errors: u64,
    pub refresh_current_conditions_calls: u64,
    pub refresh_current_conditions_errors: u64,

    pub initial_property_publish_time: std::time::Duration,
}

#[cfg(feature = "metrics")]
impl Default for WeatherServerMetrics {
    fn default() -> Self {
        WeatherServerMetrics {
            refresh_daily_forecast_calls: 0,
            refresh_daily_forecast_errors: 0,
            refresh_hourly_forecast_calls: 0,
            refresh_hourly_forecast_errors: 0,
            refresh_current_conditions_calls: 0,
            refresh_current_conditions_errors: 0,

            initial_property_publish_time: std::time::Duration::from_secs(0),
        }
    }
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

    #[cfg(feature = "metrics")]
    metrics: Arc<AsyncMutex<WeatherServerMetrics>>,
}

impl<C: Mqtt5PubSub + Clone + Send> WeatherServer<C> {
    pub async fn new(
        mut connection: C,
        method_handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers<C>>>>,
        instance_id: String,
        initial_property_values: WeatherInitialPropertyValues,
    ) -> Self {
        #[cfg(feature = "metrics")]
        let mut metrics = WeatherServerMetrics::default();

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
            subscription_id_refresh_daily_forecast_method_req.unwrap_or(u32::MAX);

        let subscription_id_refresh_hourly_forecast_method_req = connection
            .subscribe(
                format!("weather/{}/method/refreshHourlyForecast", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_hourly_forecast_method_req =
            subscription_id_refresh_hourly_forecast_method_req.unwrap_or(u32::MAX);

        let subscription_id_refresh_current_conditions_method_req = connection
            .subscribe(
                format!("weather/{}/method/refreshCurrentConditions", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_current_conditions_method_req =
            subscription_id_refresh_current_conditions_method_req.unwrap_or(u32::MAX);

        let subscription_id_location_property_update = connection
            .subscribe(
                format!("weather/{}/property/location/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_location_property_update =
            subscription_id_location_property_update.unwrap_or(u32::MAX);

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
            subscription_id_current_condition_refresh_interval_property_update.unwrap_or(u32::MAX);

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
            subscription_id_hourly_forecast_refresh_interval_property_update.unwrap_or(u32::MAX);

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
            subscription_id_daily_forecast_refresh_interval_property_update.unwrap_or(u32::MAX);

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
            location: Arc::new(RwLockWatch::new(initial_property_values.location.clone())),
            location_version: Arc::new(AtomicU32::new(initial_property_values.location_version)),

            current_temperature: Arc::new(RwLockWatch::new(
                initial_property_values.current_temperature.clone(),
            )),
            current_temperature_version: Arc::new(AtomicU32::new(
                initial_property_values.current_temperature_version,
            )),
            current_condition: Arc::new(RwLockWatch::new(
                initial_property_values.current_condition.clone(),
            )),
            current_condition_version: Arc::new(AtomicU32::new(
                initial_property_values.current_condition_version,
            )),
            daily_forecast: Arc::new(RwLockWatch::new(
                initial_property_values.daily_forecast.clone(),
            )),
            daily_forecast_version: Arc::new(AtomicU32::new(
                initial_property_values.daily_forecast_version,
            )),
            hourly_forecast: Arc::new(RwLockWatch::new(
                initial_property_values.hourly_forecast.clone(),
            )),
            hourly_forecast_version: Arc::new(AtomicU32::new(
                initial_property_values.hourly_forecast_version,
            )),

            current_condition_refresh_interval: Arc::new(RwLockWatch::new(
                initial_property_values
                    .current_condition_refresh_interval
                    .clone(),
            )),
            current_condition_refresh_interval_version: Arc::new(AtomicU32::new(
                initial_property_values.current_condition_refresh_interval_version,
            )),

            hourly_forecast_refresh_interval: Arc::new(RwLockWatch::new(
                initial_property_values
                    .hourly_forecast_refresh_interval
                    .clone(),
            )),
            hourly_forecast_refresh_interval_version: Arc::new(AtomicU32::new(
                initial_property_values.hourly_forecast_refresh_interval_version,
            )),

            daily_forecast_refresh_interval: Arc::new(RwLockWatch::new(
                initial_property_values
                    .daily_forecast_refresh_interval
                    .clone(),
            )),
            daily_forecast_refresh_interval_version: Arc::new(AtomicU32::new(
                initial_property_values.daily_forecast_refresh_interval_version,
            )),
        };

        // Publish the initial property values for all the properties.
        #[cfg(feature = "metrics")]
        let start_prop_publish_time = std::time::Instant::now();
        {
            let topic = format!("weather/{}/property/location/value", instance_id);
            let msg = message::property_value(
                &topic,
                &initial_property_values.location,
                initial_property_values.location_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("weather/{}/property/currentTemperature/value", instance_id);

            let payload_obj = CurrentTemperatureProperty {
                temperature_f: initial_property_values.current_temperature,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.current_temperature_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("weather/{}/property/currentCondition/value", instance_id);
            let msg = message::property_value(
                &topic,
                &initial_property_values.current_condition,
                initial_property_values.current_condition_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("weather/{}/property/dailyForecast/value", instance_id);
            let msg = message::property_value(
                &topic,
                &initial_property_values.daily_forecast,
                initial_property_values.daily_forecast_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("weather/{}/property/hourlyForecast/value", instance_id);
            let msg = message::property_value(
                &topic,
                &initial_property_values.hourly_forecast,
                initial_property_values.hourly_forecast_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "weather/{}/property/currentConditionRefreshInterval/value",
                instance_id
            );

            let payload_obj = CurrentConditionRefreshIntervalProperty {
                seconds: initial_property_values.current_condition_refresh_interval,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.current_condition_refresh_interval_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "weather/{}/property/hourlyForecastRefreshInterval/value",
                instance_id
            );

            let payload_obj = HourlyForecastRefreshIntervalProperty {
                seconds: initial_property_values.hourly_forecast_refresh_interval,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.hourly_forecast_refresh_interval_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "weather/{}/property/dailyForecastRefreshInterval/value",
                instance_id
            );

            let payload_obj = DailyForecastRefreshIntervalProperty {
                seconds: initial_property_values.daily_forecast_refresh_interval,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.daily_forecast_refresh_interval_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        #[cfg(feature = "metrics")]
        {
            metrics.initial_property_publish_time = start_prop_publish_time.elapsed();
            debug!(
                "Published 8 initial property values in {:?}",
                metrics.initial_property_publish_time
            );
        }

        WeatherServer {
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
    pub fn get_metrics(&self) -> Arc<AsyncMutex<WeatherServerMetrics>> {
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
    /// Emits the current_time signal with the given arguments.
    pub async fn emit_current_time(&mut self, current_time: String) -> SentMessageFuture {
        let data = CurrentTimeSignalPayload { current_time };
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
        let data = CurrentTimeSignalPayload { current_time };
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

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_location_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<LocationProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 2 fields.
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
                match serde_json::from_str::<LocationProperty>(&payload_str) {
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
                        error!("Failed to parse JSON received over MQTT to update 'location' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'location' payload".to_string(),
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
                        "Error occurred while handling property update for 'location': {:?}",
                        &err
                    );
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'location'.");
        }
    }

    /// Watch for changes to the `location` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_location(&self) -> watch::Receiver<LocationProperty> {
        self.properties.location.subscribe()
    }

    pub fn get_location_handle(&self) -> WriteRequestLockWatch<LocationProperty> {
        self.properties.location.write_request()
    }

    /// Sets the values of the location property.
    pub async fn set_location(&mut self, value: LocationProperty) -> SentMessageFuture {
        let write_request_lock = self.get_location_handle();
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

    /// Watch for changes to the `current_temperature` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_current_temperature(&self) -> watch::Receiver<f32> {
        self.properties.current_temperature.subscribe()
    }

    pub fn get_current_temperature_handle(&self) -> WriteRequestLockWatch<f32> {
        self.properties.current_temperature.write_request()
    }

    /// Sets the value of the current_temperature property.
    pub async fn set_current_temperature(&mut self, value: f32) -> SentMessageFuture {
        let write_request_lock = self.get_current_temperature_handle();
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

    /// Watch for changes to the `current_condition` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_current_condition(&self) -> watch::Receiver<CurrentConditionProperty> {
        self.properties.current_condition.subscribe()
    }

    pub fn get_current_condition_handle(&self) -> WriteRequestLockWatch<CurrentConditionProperty> {
        self.properties.current_condition.write_request()
    }

    /// Sets the values of the current_condition property.
    pub async fn set_current_condition(
        &mut self,
        value: CurrentConditionProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_current_condition_handle();
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

    /// Watch for changes to the `daily_forecast` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_daily_forecast(&self) -> watch::Receiver<DailyForecastProperty> {
        self.properties.daily_forecast.subscribe()
    }

    pub fn get_daily_forecast_handle(&self) -> WriteRequestLockWatch<DailyForecastProperty> {
        self.properties.daily_forecast.write_request()
    }

    /// Sets the values of the daily_forecast property.
    pub async fn set_daily_forecast(&mut self, value: DailyForecastProperty) -> SentMessageFuture {
        let write_request_lock = self.get_daily_forecast_handle();
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

    /// Watch for changes to the `hourly_forecast` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_hourly_forecast(&self) -> watch::Receiver<HourlyForecastProperty> {
        self.properties.hourly_forecast.subscribe()
    }

    pub fn get_hourly_forecast_handle(&self) -> WriteRequestLockWatch<HourlyForecastProperty> {
        self.properties.hourly_forecast.write_request()
    }

    /// Sets the values of the hourly_forecast property.
    pub async fn set_hourly_forecast(
        &mut self,
        value: HourlyForecastProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_hourly_forecast_handle();
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
    async fn update_current_condition_refresh_interval_value(
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
                match serde_json::from_str::<CurrentConditionRefreshIntervalProperty>(&payload_str)
                {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the seconds field of the struct.
                        *write_request = new_property_structure.seconds.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'current_condition_refresh_interval' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError("Failed to deserialize property 'current_condition_refresh_interval' payload".to_string());
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
                    CurrentConditionRefreshIntervalProperty { seconds: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    CurrentConditionRefreshIntervalProperty {
                        seconds: (*prop_lock).clone(),
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
                    error!("Error occurred while handling property update for 'current_condition_refresh_interval': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'current_condition_refresh_interval'.");
        }
    }

    /// Watch for changes to the `current_condition_refresh_interval` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_current_condition_refresh_interval(&self) -> watch::Receiver<i32> {
        self.properties
            .current_condition_refresh_interval
            .subscribe()
    }

    pub fn get_current_condition_refresh_interval_handle(&self) -> WriteRequestLockWatch<i32> {
        self.properties
            .current_condition_refresh_interval
            .write_request()
    }

    /// Sets the value of the current_condition_refresh_interval property.
    pub async fn set_current_condition_refresh_interval(
        &mut self,
        value: i32,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_current_condition_refresh_interval_handle();
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
    async fn update_hourly_forecast_refresh_interval_value(
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
                match serde_json::from_str::<HourlyForecastRefreshIntervalProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the seconds field of the struct.
                        *write_request = new_property_structure.seconds.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'hourly_forecast_refresh_interval' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError("Failed to deserialize property 'hourly_forecast_refresh_interval' payload".to_string());
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
                    HourlyForecastRefreshIntervalProperty { seconds: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    HourlyForecastRefreshIntervalProperty {
                        seconds: (*prop_lock).clone(),
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
                    error!("Error occurred while handling property update for 'hourly_forecast_refresh_interval': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'hourly_forecast_refresh_interval'.");
        }
    }

    /// Watch for changes to the `hourly_forecast_refresh_interval` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_hourly_forecast_refresh_interval(&self) -> watch::Receiver<i32> {
        self.properties.hourly_forecast_refresh_interval.subscribe()
    }

    pub fn get_hourly_forecast_refresh_interval_handle(&self) -> WriteRequestLockWatch<i32> {
        self.properties
            .hourly_forecast_refresh_interval
            .write_request()
    }

    /// Sets the value of the hourly_forecast_refresh_interval property.
    pub async fn set_hourly_forecast_refresh_interval(&mut self, value: i32) -> SentMessageFuture {
        let write_request_lock = self.get_hourly_forecast_refresh_interval_handle();
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
    async fn update_daily_forecast_refresh_interval_value(
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
                match serde_json::from_str::<DailyForecastRefreshIntervalProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the seconds field of the struct.
                        *write_request = new_property_structure.seconds.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'daily_forecast_refresh_interval' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError("Failed to deserialize property 'daily_forecast_refresh_interval' payload".to_string());
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
                    DailyForecastRefreshIntervalProperty { seconds: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    DailyForecastRefreshIntervalProperty {
                        seconds: (*prop_lock).clone(),
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
                    error!("Error occurred while handling property update for 'daily_forecast_refresh_interval': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'daily_forecast_refresh_interval'.");
        }
    }

    /// Watch for changes to the `daily_forecast_refresh_interval` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_daily_forecast_refresh_interval(&self) -> watch::Receiver<i32> {
        self.properties.daily_forecast_refresh_interval.subscribe()
    }

    pub fn get_daily_forecast_refresh_interval_handle(&self) -> WriteRequestLockWatch<i32> {
        self.properties
            .daily_forecast_refresh_interval
            .write_request()
    }

    /// Sets the value of the daily_forecast_refresh_interval property.
    pub async fn set_daily_forecast_refresh_interval(&mut self, value: i32) -> SentMessageFuture {
        let write_request_lock = self.get_daily_forecast_refresh_interval_handle();
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
            let instance_id_for_location_prop = self.instance_id.clone();
            let mut publisher_for_location_prop = self.mqtt_client.clone();
            let location_prop_version = props.location_version.clone();
            if let Some(mut rx_for_location_prop) = props.location.take_request_receiver() {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) = rx_for_location_prop.recv().await {
                        let payload_obj = request.clone();

                        let version_value = location_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "weather/{}/property/location/value",
                            instance_id_for_location_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_location_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'location' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'location' property: {:?}", e);
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
            let instance_id_for_current_temperature_prop = self.instance_id.clone();
            let mut publisher_for_current_temperature_prop = self.mqtt_client.clone();
            let current_temperature_prop_version = props.current_temperature_version.clone();
            if let Some(mut rx_for_current_temperature_prop) =
                props.current_temperature.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_current_temperature_prop.recv().await
                    {
                        let payload_obj = CurrentTemperatureProperty {
                            temperature_f: request.clone(),
                        };

                        let version_value = current_temperature_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "weather/{}/property/currentTemperature/value",
                            instance_id_for_current_temperature_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_current_temperature_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'current_temperature' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'current_temperature' property: {:?}", e);
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
            let instance_id_for_current_condition_prop = self.instance_id.clone();
            let mut publisher_for_current_condition_prop = self.mqtt_client.clone();
            let current_condition_prop_version = props.current_condition_version.clone();
            if let Some(mut rx_for_current_condition_prop) =
                props.current_condition.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_current_condition_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = current_condition_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "weather/{}/property/currentCondition/value",
                            instance_id_for_current_condition_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_current_condition_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'current_condition' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'current_condition' property: {:?}", e);
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
            let instance_id_for_daily_forecast_prop = self.instance_id.clone();
            let mut publisher_for_daily_forecast_prop = self.mqtt_client.clone();
            let daily_forecast_prop_version = props.daily_forecast_version.clone();
            if let Some(mut rx_for_daily_forecast_prop) =
                props.daily_forecast.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_daily_forecast_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = daily_forecast_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "weather/{}/property/dailyForecast/value",
                            instance_id_for_daily_forecast_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_daily_forecast_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'daily_forecast' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'daily_forecast' property: {:?}", e);
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
            let instance_id_for_hourly_forecast_prop = self.instance_id.clone();
            let mut publisher_for_hourly_forecast_prop = self.mqtt_client.clone();
            let hourly_forecast_prop_version = props.hourly_forecast_version.clone();
            if let Some(mut rx_for_hourly_forecast_prop) =
                props.hourly_forecast.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_hourly_forecast_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = hourly_forecast_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "weather/{}/property/hourlyForecast/value",
                            instance_id_for_hourly_forecast_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_hourly_forecast_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'hourly_forecast' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'hourly_forecast' property: {:?}", e);
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
            let instance_id_for_current_condition_refresh_interval_prop = self.instance_id.clone();
            let mut publisher_for_current_condition_refresh_interval_prop =
                self.mqtt_client.clone();
            let current_condition_refresh_interval_prop_version =
                props.current_condition_refresh_interval_version.clone();
            if let Some(mut rx_for_current_condition_refresh_interval_prop) = props
                .current_condition_refresh_interval
                .take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_current_condition_refresh_interval_prop.recv().await
                    {
                        let payload_obj = CurrentConditionRefreshIntervalProperty {
                            seconds: request.clone(),
                        };

                        let version_value = current_condition_refresh_interval_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "weather/{}/property/currentConditionRefreshInterval/value",
                            instance_id_for_current_condition_refresh_interval_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_current_condition_refresh_interval_prop
                                        .publish(msg)
                                        .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'current_condition_refresh_interval' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'current_condition_refresh_interval' property: {:?}", e);
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
            let instance_id_for_hourly_forecast_refresh_interval_prop = self.instance_id.clone();
            let mut publisher_for_hourly_forecast_refresh_interval_prop = self.mqtt_client.clone();
            let hourly_forecast_refresh_interval_prop_version =
                props.hourly_forecast_refresh_interval_version.clone();
            if let Some(mut rx_for_hourly_forecast_refresh_interval_prop) = props
                .hourly_forecast_refresh_interval
                .take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_hourly_forecast_refresh_interval_prop.recv().await
                    {
                        let payload_obj = HourlyForecastRefreshIntervalProperty {
                            seconds: request.clone(),
                        };

                        let version_value = hourly_forecast_refresh_interval_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "weather/{}/property/hourlyForecastRefreshInterval/value",
                            instance_id_for_hourly_forecast_refresh_interval_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_hourly_forecast_refresh_interval_prop
                                        .publish(msg)
                                        .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'hourly_forecast_refresh_interval' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'hourly_forecast_refresh_interval' property: {:?}", e);
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
            let instance_id_for_daily_forecast_refresh_interval_prop = self.instance_id.clone();
            let mut publisher_for_daily_forecast_refresh_interval_prop = self.mqtt_client.clone();
            let daily_forecast_refresh_interval_prop_version =
                props.daily_forecast_refresh_interval_version.clone();
            if let Some(mut rx_for_daily_forecast_refresh_interval_prop) = props
                .daily_forecast_refresh_interval
                .take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_daily_forecast_refresh_interval_prop.recv().await
                    {
                        let payload_obj = DailyForecastRefreshIntervalProperty {
                            seconds: request.clone(),
                        };

                        let version_value = daily_forecast_refresh_interval_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "weather/{}/property/dailyForecastRefreshInterval/value",
                            instance_id_for_daily_forecast_refresh_interval_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_daily_forecast_refresh_interval_prop
                                        .publish(msg)
                                        .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'daily_forecast_refresh_interval' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'daily_forecast_refresh_interval' property: {:?}", e);
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
                let topic = format!("weather/{}/interface", instance_id);
                let info = crate::interface::InterfaceInfoBuilder::default()
                    .interface_name("weather".to_string())
                    .title("NWS weather forecast".to_string())
                    .version("0.1.2".to_string())
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
                                _i if _i == sub_ids.refresh_daily_forecast_method_req => {
                                    debug!("Received refresh_daily_forecast method invocation message.");
                                    WeatherServer::<C>::handle_refresh_daily_forecast_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.refresh_hourly_forecast_method_req => {
                                    debug!("Received refresh_hourly_forecast method invocation message.");
                                    WeatherServer::<C>::handle_refresh_hourly_forecast_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.refresh_current_conditions_method_req => {
                                    debug!("Received refresh_current_conditions method invocation message.");
                                    WeatherServer::<C>::handle_refresh_current_conditions_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.location_property_update => {
                                    debug!("Received location property update request message.");
                                    WeatherServer::<C>::update_location_value(
                                        publisher.clone(),
                                        properties.location.clone(),
                                        properties.location_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i
                                    == sub_ids
                                        .current_condition_refresh_interval_property_update =>
                                {
                                    debug!("Received current_condition_refresh_interval property update request message.");
                                    WeatherServer::<C>::update_current_condition_refresh_interval_value(
                                            publisher.clone(),
                                            properties.current_condition_refresh_interval.clone(),
                                            properties.current_condition_refresh_interval_version.clone(),
                                            msg
                                    ).await;
                                }

                                _i if _i
                                    == sub_ids.hourly_forecast_refresh_interval_property_update =>
                                {
                                    debug!("Received hourly_forecast_refresh_interval property update request message.");
                                    WeatherServer::<C>::update_hourly_forecast_refresh_interval_value(
                                            publisher.clone(),
                                            properties.hourly_forecast_refresh_interval.clone(),
                                            properties.hourly_forecast_refresh_interval_version.clone(),
                                            msg
                                    ).await;
                                }

                                _i if _i
                                    == sub_ids.daily_forecast_refresh_interval_property_update =>
                                {
                                    debug!("Received daily_forecast_refresh_interval property update request message.");
                                    WeatherServer::<C>::update_daily_forecast_refresh_interval_value(
                                            publisher.clone(),
                                            properties.daily_forecast_refresh_interval.clone(),
                                            properties.daily_forecast_refresh_interval_version.clone(),
                                            msg
                                    ).await;
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
