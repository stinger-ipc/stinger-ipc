//! Client module for weather IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the weather interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/
use crate::message;
use serde_json;
use std::collections::HashMap;
use stinger_mqtt_trait::message::{MqttMessage, QoS};
#[cfg(feature = "client")]
use stinger_mqtt_trait::Mqtt5PubSub;
use uuid::Uuid;

#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
#[allow(unused_imports)]
use iso8601_duration::Duration as IsoDuration;
use std::sync::{Arc, Mutex};
use tokio::sync::{broadcast, oneshot, watch};
use tokio::task::JoinError;
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};

use std::sync::atomic::{AtomicU32, Ordering};
#[allow(unused_imports)]
use stinger_rwlock_watch::ReadOnlyLockWatch;
use stinger_rwlock_watch::RwLockWatch;
#[allow(unused_imports)]
use stinger_rwlock_watch::WriteRequestLockWatch;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct WeatherSubscriptionIds {
    refresh_daily_forecast_method_resp: u32,
    refresh_hourly_forecast_method_resp: u32,
    refresh_current_conditions_method_resp: u32,

    current_time_signal: Option<u32>,
    location_property_value: u32,
    current_temperature_property_value: u32,
    current_condition_property_value: u32,
    daily_forecast_property_value: u32,
    hourly_forecast_property_value: u32,
    current_condition_refresh_interval_property_value: u32,
    hourly_forecast_refresh_interval_property_value: u32,
    daily_forecast_refresh_interval_property_value: u32,
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When WeatherClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct WeatherSignalChannels {
    current_time_sender: broadcast::Sender<String>,
}

#[derive(Clone)]
pub struct WeatherProperties {
    pub location: Arc<RwLockWatch<Option<LocationProperty>>>,
    pub location_version: Arc<AtomicU32>,

    pub current_temperature: Arc<RwLockWatch<Option<f32>>>,
    pub current_temperature_version: Arc<AtomicU32>,

    pub current_condition: Arc<RwLockWatch<Option<CurrentConditionProperty>>>,
    pub current_condition_version: Arc<AtomicU32>,

    pub daily_forecast: Arc<RwLockWatch<Option<DailyForecastProperty>>>,
    pub daily_forecast_version: Arc<AtomicU32>,

    pub hourly_forecast: Arc<RwLockWatch<Option<HourlyForecastProperty>>>,
    pub hourly_forecast_version: Arc<AtomicU32>,

    pub current_condition_refresh_interval: Arc<RwLockWatch<Option<i32>>>,
    pub current_condition_refresh_interval_version: Arc<AtomicU32>,

    pub hourly_forecast_refresh_interval: Arc<RwLockWatch<Option<i32>>>,
    pub hourly_forecast_refresh_interval_version: Arc<AtomicU32>,

    pub daily_forecast_refresh_interval: Arc<RwLockWatch<Option<i32>>>,
    pub daily_forecast_refresh_interval_version: Arc<AtomicU32>,
}

/// This is the struct for our API client.
#[derive(Clone)]
pub struct WeatherClient<C: Mqtt5PubSub> {
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
    pub properties: WeatherProperties,

    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: WeatherSubscriptionIds,
    /// Holds the channels used for sending signals to the application.
    signal_channels: WeatherSignalChannels,

    /// Copy of MQTT Client ID
    pub client_id: String,

    /// Instance ID of the server
    service_instance_id: String,
}

impl<C: Mqtt5PubSub + Clone + Send + 'static> WeatherClient<C> {
    /// Creates a new WeatherClient that uses an Mqtt5PubSub.
    pub async fn new(mut connection: C, service_id: String) -> Self {
        // Create a channel for messages to get from the Connection object to this WeatherClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = broadcast::channel(64);

        let client_id = connection.get_client_id();

        let topic_refresh_daily_forecast_method_resp =
            format!("client/{}/refresh_daily_forecast/response", client_id);
        let subscription_id_refresh_daily_forecast_method_resp = connection
            .subscribe(
                topic_refresh_daily_forecast_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_daily_forecast_method_resp =
            subscription_id_refresh_daily_forecast_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_refresh_hourly_forecast_method_resp =
            format!("client/{}/refresh_hourly_forecast/response", client_id);
        let subscription_id_refresh_hourly_forecast_method_resp = connection
            .subscribe(
                topic_refresh_hourly_forecast_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_hourly_forecast_method_resp =
            subscription_id_refresh_hourly_forecast_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_refresh_current_conditions_method_resp =
            format!("client/{}/refresh_current_conditions/response", client_id);
        let subscription_id_refresh_current_conditions_method_resp = connection
            .subscribe(
                topic_refresh_current_conditions_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_current_conditions_method_resp =
            subscription_id_refresh_current_conditions_method_resp.unwrap_or_else(|_| u32::MAX);

        // Subscribe to all the topics needed for signals.
        let topic_current_time_signal = format!("weather/{}/signal/currentTime", service_id);
        let subscription_id_current_time_signal = connection
            .subscribe(
                topic_current_time_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_current_time_signal =
            subscription_id_current_time_signal.unwrap_or_else(|_| u32::MAX);

        // Subscribe to all the topics needed for properties.

        let topic_location_property_value =
            format!("weather/{}/property/location/value", service_id);
        let subscription_id_location_property_value = connection
            .subscribe(
                topic_location_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_location_property_value =
            subscription_id_location_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_current_temperature_property_value =
            format!("weather/{}/property/currentTemperature/value", service_id);
        let subscription_id_current_temperature_property_value = connection
            .subscribe(
                topic_current_temperature_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_current_temperature_property_value =
            subscription_id_current_temperature_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_current_condition_property_value =
            format!("weather/{}/property/currentCondition/value", service_id);
        let subscription_id_current_condition_property_value = connection
            .subscribe(
                topic_current_condition_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_current_condition_property_value =
            subscription_id_current_condition_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_daily_forecast_property_value =
            format!("weather/{}/property/dailyForecast/value", service_id);
        let subscription_id_daily_forecast_property_value = connection
            .subscribe(
                topic_daily_forecast_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_daily_forecast_property_value =
            subscription_id_daily_forecast_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_hourly_forecast_property_value =
            format!("weather/{}/property/hourlyForecast/value", service_id);
        let subscription_id_hourly_forecast_property_value = connection
            .subscribe(
                topic_hourly_forecast_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_hourly_forecast_property_value =
            subscription_id_hourly_forecast_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_current_condition_refresh_interval_property_value = format!(
            "weather/{}/property/currentConditionRefreshInterval/value",
            service_id
        );
        let subscription_id_current_condition_refresh_interval_property_value = connection
            .subscribe(
                topic_current_condition_refresh_interval_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_current_condition_refresh_interval_property_value =
            subscription_id_current_condition_refresh_interval_property_value
                .unwrap_or_else(|_| u32::MAX);

        let topic_hourly_forecast_refresh_interval_property_value = format!(
            "weather/{}/property/hourlyForecastRefreshInterval/value",
            service_id
        );
        let subscription_id_hourly_forecast_refresh_interval_property_value = connection
            .subscribe(
                topic_hourly_forecast_refresh_interval_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_hourly_forecast_refresh_interval_property_value =
            subscription_id_hourly_forecast_refresh_interval_property_value
                .unwrap_or_else(|_| u32::MAX);

        let topic_daily_forecast_refresh_interval_property_value = format!(
            "weather/{}/property/dailyForecastRefreshInterval/value",
            service_id
        );
        let subscription_id_daily_forecast_refresh_interval_property_value = connection
            .subscribe(
                topic_daily_forecast_refresh_interval_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_daily_forecast_refresh_interval_property_value =
            subscription_id_daily_forecast_refresh_interval_property_value
                .unwrap_or_else(|_| u32::MAX);

        let property_values = WeatherProperties {
            location: Arc::new(RwLockWatch::new(None)),
            location_version: Arc::new(AtomicU32::new(0)),

            current_temperature: Arc::new(RwLockWatch::new(None)),
            current_temperature_version: Arc::new(AtomicU32::new(0)),
            current_condition: Arc::new(RwLockWatch::new(None)),
            current_condition_version: Arc::new(AtomicU32::new(0)),
            daily_forecast: Arc::new(RwLockWatch::new(None)),
            daily_forecast_version: Arc::new(AtomicU32::new(0)),
            hourly_forecast: Arc::new(RwLockWatch::new(None)),
            hourly_forecast_version: Arc::new(AtomicU32::new(0)),

            current_condition_refresh_interval: Arc::new(RwLockWatch::new(None)),
            current_condition_refresh_interval_version: Arc::new(AtomicU32::new(0)),

            hourly_forecast_refresh_interval: Arc::new(RwLockWatch::new(None)),
            hourly_forecast_refresh_interval_version: Arc::new(AtomicU32::new(0)),

            daily_forecast_refresh_interval: Arc::new(RwLockWatch::new(None)),
            daily_forecast_refresh_interval_version: Arc::new(AtomicU32::new(0)),
        };

        // Create structure for subscription ids.
        let sub_ids = WeatherSubscriptionIds {
            refresh_daily_forecast_method_resp: subscription_id_refresh_daily_forecast_method_resp,
            refresh_hourly_forecast_method_resp:
                subscription_id_refresh_hourly_forecast_method_resp,
            refresh_current_conditions_method_resp:
                subscription_id_refresh_current_conditions_method_resp,
            current_time_signal: Some(subscription_id_current_time_signal),
            location_property_value: subscription_id_location_property_value,
            current_temperature_property_value: subscription_id_current_temperature_property_value,
            current_condition_property_value: subscription_id_current_condition_property_value,
            daily_forecast_property_value: subscription_id_daily_forecast_property_value,
            hourly_forecast_property_value: subscription_id_hourly_forecast_property_value,
            current_condition_refresh_interval_property_value:
                subscription_id_current_condition_refresh_interval_property_value,
            hourly_forecast_refresh_interval_property_value:
                subscription_id_hourly_forecast_refresh_interval_property_value,
            daily_forecast_refresh_interval_property_value:
                subscription_id_daily_forecast_refresh_interval_property_value,
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = WeatherSignalChannels {
            current_time_sender: broadcast::channel(64).0,
        };

        // Create WeatherClient structure.
        let inst = WeatherClient {
            mqtt_client: connection,
            pending_responses: Arc::new(Mutex::new(HashMap::new())),
            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,

            properties: property_values,

            subscription_ids: sub_ids,
            signal_channels: signal_channels,
            client_id: client_id,

            service_instance_id: service_id,
        };
        inst
    }

    /// Get the RX receiver side of the broadcast channel for the current_time signal.
    /// The signal payload, `CurrentTimeSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_current_time_receiver(&self) -> broadcast::Receiver<String> {
        self.signal_channels.current_time_sender.subscribe()
    }

    async fn start_refresh_daily_forecast(&mut self) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = RefreshDailyForecastRequestObject {};

        let response_topic: String =
            format!("client/{}/refresh_daily_forecast/response", self.client_id);
        let msg = message::request(
            &format!(
                "weather/{}/method/refreshDailyForecast",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `refresh_daily_forecast` method.
    /// Method arguments are packed into a RefreshDailyForecastRequestObject structure
    /// and published to the `weather/{}/method/refreshDailyForecast` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn refresh_daily_forecast(&mut self) -> Result<(), MethodReturnCode> {
        let receiver = self.start_refresh_daily_forecast().await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(_) => Ok(()),
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_refresh_hourly_forecast(&mut self) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = RefreshHourlyForecastRequestObject {};

        let response_topic: String =
            format!("client/{}/refresh_hourly_forecast/response", self.client_id);
        let msg = message::request(
            &format!(
                "weather/{}/method/refreshHourlyForecast",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `refresh_hourly_forecast` method.
    /// Method arguments are packed into a RefreshHourlyForecastRequestObject structure
    /// and published to the `weather/{}/method/refreshHourlyForecast` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn refresh_hourly_forecast(&mut self) -> Result<(), MethodReturnCode> {
        let receiver = self.start_refresh_hourly_forecast().await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(_) => Ok(()),
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_refresh_current_conditions(&mut self) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = RefreshCurrentConditionsRequestObject {};

        let response_topic: String = format!(
            "client/{}/refresh_current_conditions/response",
            self.client_id
        );
        let msg = message::request(
            &format!(
                "weather/{}/method/refreshCurrentConditions",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `refresh_current_conditions` method.
    /// Method arguments are packed into a RefreshCurrentConditionsRequestObject structure
    /// and published to the `weather/{}/method/refreshCurrentConditions` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn refresh_current_conditions(&mut self) -> Result<(), MethodReturnCode> {
        let receiver = self.start_refresh_current_conditions().await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(_) => Ok(()),
            _ => {
                return Err(return_code);
            }
        }
    }

    /// Watch for changes to the `location` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_location(&self) -> watch::Receiver<Option<LocationProperty>> {
        self.properties.location.subscribe()
    }

    /// Sets the `location` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_location(&mut self, value: LocationProperty) -> MethodReturnCode {
        let data = value;
        let topic: String = format!("weather/{}/property/location/setValue", self.client_id);
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties.location_version.load(Ordering::Relaxed),
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

    pub fn get_location_handle(&self) -> Arc<WriteRequestLockWatch<Option<LocationProperty>>> {
        self.properties.location.write_request().into()
    }

    /// Watch for changes to the `current_temperature` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_current_temperature(&self) -> watch::Receiver<Option<f32>> {
        self.properties.current_temperature.subscribe()
    }

    pub fn get_current_temperature_handle(&self) -> ReadOnlyLockWatch<Option<f32>> {
        self.properties.current_temperature.read_only()
    }

    /// Watch for changes to the `current_condition` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_current_condition(&self) -> watch::Receiver<Option<CurrentConditionProperty>> {
        self.properties.current_condition.subscribe()
    }

    pub fn get_current_condition_handle(&self) -> ReadOnlyLockWatch<CurrentConditionProperty> {
        self.properties.current_condition.read_only()
    }

    /// Watch for changes to the `daily_forecast` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_daily_forecast(&self) -> watch::Receiver<Option<DailyForecastProperty>> {
        self.properties.daily_forecast.subscribe()
    }

    pub fn get_daily_forecast_handle(&self) -> ReadOnlyLockWatch<DailyForecastProperty> {
        self.properties.daily_forecast.read_only()
    }

    /// Watch for changes to the `hourly_forecast` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_hourly_forecast(&self) -> watch::Receiver<Option<HourlyForecastProperty>> {
        self.properties.hourly_forecast.subscribe()
    }

    pub fn get_hourly_forecast_handle(&self) -> ReadOnlyLockWatch<HourlyForecastProperty> {
        self.properties.hourly_forecast.read_only()
    }

    /// Watch for changes to the `current_condition_refresh_interval` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_current_condition_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .current_condition_refresh_interval
            .subscribe()
    }

    /// Sets the `current_condition_refresh_interval` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_current_condition_refresh_interval(&mut self, value: i32) -> MethodReturnCode {
        let data = CurrentConditionRefreshIntervalProperty { seconds: value };
        let topic: String = format!(
            "weather/{}/property/currentConditionRefreshInterval/setValue",
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
                .current_condition_refresh_interval_version
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

    pub fn get_current_condition_refresh_interval_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<i32>>> {
        self.properties
            .current_condition_refresh_interval
            .write_request()
            .into()
    }

    /// Watch for changes to the `hourly_forecast_refresh_interval` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_hourly_forecast_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties.hourly_forecast_refresh_interval.subscribe()
    }

    /// Sets the `hourly_forecast_refresh_interval` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_hourly_forecast_refresh_interval(&mut self, value: i32) -> MethodReturnCode {
        let data = HourlyForecastRefreshIntervalProperty { seconds: value };
        let topic: String = format!(
            "weather/{}/property/hourlyForecastRefreshInterval/setValue",
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
                .hourly_forecast_refresh_interval_version
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

    pub fn get_hourly_forecast_refresh_interval_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<i32>>> {
        self.properties
            .hourly_forecast_refresh_interval
            .write_request()
            .into()
    }

    /// Watch for changes to the `daily_forecast_refresh_interval` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_daily_forecast_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties.daily_forecast_refresh_interval.subscribe()
    }

    /// Sets the `daily_forecast_refresh_interval` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_daily_forecast_refresh_interval(&mut self, value: i32) -> MethodReturnCode {
        let data = DailyForecastRefreshIntervalProperty { seconds: value };
        let topic: String = format!(
            "weather/{}/property/dailyForecastRefreshInterval/setValue",
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
                .daily_forecast_refresh_interval_version
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

    pub fn get_daily_forecast_refresh_interval_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<i32>>> {
        self.properties
            .daily_forecast_refresh_interval
            .write_request()
            .into()
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
            let client_id_for_location_prop = self.client_id.clone();
            let mut publisher_for_location_prop = self.mqtt_client.clone();
            let location_prop_version = props.location_version.clone();
            if let Some(mut rx_for_location_prop) = props.location.take_request_receiver() {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_location_prop.recv().await {
                        let topic: String = format!(
                            "weather/{}/property/location/setValue",
                            client_id_for_location_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            location_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_location_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_current_temperature_prop = self.client_id.clone();
            let mut publisher_for_current_temperature_prop = self.mqtt_client.clone();
            let current_temperature_prop_version = props.current_temperature_version.clone();
            if let Some(mut rx_for_current_temperature_prop) =
                props.current_temperature.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_current_temperature_prop.recv().await {
                        let topic: String = format!(
                            "weather/{}/property/currentTemperature/setValue",
                            client_id_for_current_temperature_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            current_temperature_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_current_temperature_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_current_condition_prop = self.client_id.clone();
            let mut publisher_for_current_condition_prop = self.mqtt_client.clone();
            let current_condition_prop_version = props.current_condition_version.clone();
            if let Some(mut rx_for_current_condition_prop) =
                props.current_condition.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_current_condition_prop.recv().await {
                        let topic: String = format!(
                            "weather/{}/property/currentCondition/setValue",
                            client_id_for_current_condition_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            current_condition_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_current_condition_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_daily_forecast_prop = self.client_id.clone();
            let mut publisher_for_daily_forecast_prop = self.mqtt_client.clone();
            let daily_forecast_prop_version = props.daily_forecast_version.clone();
            if let Some(mut rx_for_daily_forecast_prop) =
                props.daily_forecast.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_daily_forecast_prop.recv().await {
                        let topic: String = format!(
                            "weather/{}/property/dailyForecast/setValue",
                            client_id_for_daily_forecast_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            daily_forecast_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_daily_forecast_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_hourly_forecast_prop = self.client_id.clone();
            let mut publisher_for_hourly_forecast_prop = self.mqtt_client.clone();
            let hourly_forecast_prop_version = props.hourly_forecast_version.clone();
            if let Some(mut rx_for_hourly_forecast_prop) =
                props.hourly_forecast.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_hourly_forecast_prop.recv().await {
                        let topic: String = format!(
                            "weather/{}/property/hourlyForecast/setValue",
                            client_id_for_hourly_forecast_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            hourly_forecast_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_hourly_forecast_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_current_condition_refresh_interval_prop = self.client_id.clone();
            let mut publisher_for_current_condition_refresh_interval_prop =
                self.mqtt_client.clone();
            let current_condition_refresh_interval_prop_version =
                props.current_condition_refresh_interval_version.clone();
            if let Some(mut rx_for_current_condition_refresh_interval_prop) = props
                .current_condition_refresh_interval
                .take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) =
                        rx_for_current_condition_refresh_interval_prop.recv().await
                    {
                        let topic: String = format!(
                            "weather/{}/property/currentConditionRefreshInterval/setValue",
                            client_id_for_current_condition_refresh_interval_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            current_condition_refresh_interval_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_current_condition_refresh_interval_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_hourly_forecast_refresh_interval_prop = self.client_id.clone();
            let mut publisher_for_hourly_forecast_refresh_interval_prop = self.mqtt_client.clone();
            let hourly_forecast_refresh_interval_prop_version =
                props.hourly_forecast_refresh_interval_version.clone();
            if let Some(mut rx_for_hourly_forecast_refresh_interval_prop) = props
                .hourly_forecast_refresh_interval
                .take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) =
                        rx_for_hourly_forecast_refresh_interval_prop.recv().await
                    {
                        let topic: String = format!(
                            "weather/{}/property/hourlyForecastRefreshInterval/setValue",
                            client_id_for_hourly_forecast_refresh_interval_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            hourly_forecast_refresh_interval_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_hourly_forecast_refresh_interval_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_daily_forecast_refresh_interval_prop = self.client_id.clone();
            let mut publisher_for_daily_forecast_refresh_interval_prop = self.mqtt_client.clone();
            let daily_forecast_refresh_interval_prop_version =
                props.daily_forecast_refresh_interval_version.clone();
            if let Some(mut rx_for_daily_forecast_refresh_interval_prop) = props
                .daily_forecast_refresh_interval
                .take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) =
                        rx_for_daily_forecast_refresh_interval_prop.recv().await
                    {
                        let topic: String = format!(
                            "weather/{}/property/dailyForecastRefreshInterval/setValue",
                            client_id_for_daily_forecast_refresh_interval_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            daily_forecast_refresh_interval_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_daily_forecast_refresh_interval_prop
                            .publish(msg)
                            .await;
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
                    let return_code = WeatherClient::<C>::get_return_code_from_message(&msg);
                    if subscription_id == sub_ids.refresh_daily_forecast_method_resp {
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
                    // end refresh_daily_forecast method response handling
                    else if subscription_id == sub_ids.refresh_hourly_forecast_method_resp {
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
                    // end refresh_hourly_forecast method response handling
                    else if subscription_id == sub_ids.refresh_current_conditions_method_resp {
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
                    } // end refresh_current_conditions method response handling
                    if Some(subscription_id) == sub_ids.current_time_signal {
                        let chan = sig_chans.current_time_sender.clone();

                        match serde_json::from_slice::<CurrentTimeSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.current_time);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into CurrentTimeSignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    } // end current_time signal handling

                    if subscription_id == sub_ids.location_property_value {
                        match serde_json::from_slice::<LocationProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.location.write().await;

                                *guard = Some(pl.clone());

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.location_version.store(
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
                    // end location property value update
                    else if subscription_id == sub_ids.current_temperature_property_value {
                        match serde_json::from_slice::<CurrentTemperatureProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.current_temperature.write().await;

                                *guard = Some(pl.temperature_f.clone());

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.current_temperature_version.store(
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
                    // end current_temperature property value update
                    else if subscription_id == sub_ids.current_condition_property_value {
                        match serde_json::from_slice::<CurrentConditionProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.current_condition.write().await;

                                *guard = Some(pl.clone());

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.current_condition_version.store(
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
                    // end current_condition property value update
                    else if subscription_id == sub_ids.daily_forecast_property_value {
                        match serde_json::from_slice::<DailyForecastProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.daily_forecast.write().await;

                                *guard = Some(pl.clone());

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.daily_forecast_version.store(
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
                    // end daily_forecast property value update
                    else if subscription_id == sub_ids.hourly_forecast_property_value {
                        match serde_json::from_slice::<HourlyForecastProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.hourly_forecast.write().await;

                                *guard = Some(pl.clone());

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.hourly_forecast_version.store(
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
                    // end hourly_forecast property value update
                    else if subscription_id
                        == sub_ids.current_condition_refresh_interval_property_value
                    {
                        match serde_json::from_slice::<CurrentConditionRefreshIntervalProperty>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let mut guard =
                                    props.current_condition_refresh_interval.write().await;

                                *guard = Some(pl.seconds.clone());

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.current_condition_refresh_interval_version.store(
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
                    // end current_condition_refresh_interval property value update
                    else if subscription_id
                        == sub_ids.hourly_forecast_refresh_interval_property_value
                    {
                        match serde_json::from_slice::<HourlyForecastRefreshIntervalProperty>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let mut guard =
                                    props.hourly_forecast_refresh_interval.write().await;

                                *guard = Some(pl.seconds.clone());

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.hourly_forecast_refresh_interval_version.store(
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
                    // end hourly_forecast_refresh_interval property value update
                    else if subscription_id
                        == sub_ids.daily_forecast_refresh_interval_property_value
                    {
                        match serde_json::from_slice::<DailyForecastRefreshIntervalProperty>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let mut guard = props.daily_forecast_refresh_interval.write().await;

                                *guard = Some(pl.seconds.clone());

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.daily_forecast_refresh_interval_version.store(
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
                    } // end daily_forecast_refresh_interval property value update
                }
            }
        });

        Ok(())
    }
}
