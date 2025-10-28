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
use stinger_mqtt_trait::MqttClient;
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
    pub location: Arc<Mutex<Option<LocationProperty>>>,
    location_tx_channel: watch::Sender<Option<LocationProperty>>,
    pub location_version: Arc<AtomicU32>,
    pub current_temperature: Arc<Mutex<Option<f32>>>,

    current_temperature_tx_channel: watch::Sender<Option<f32>>,
    pub current_temperature_version: Arc<AtomicU32>,
    pub current_condition: Arc<Mutex<Option<CurrentConditionProperty>>>,
    current_condition_tx_channel: watch::Sender<Option<CurrentConditionProperty>>,
    pub current_condition_version: Arc<AtomicU32>,
    pub daily_forecast: Arc<Mutex<Option<DailyForecastProperty>>>,
    daily_forecast_tx_channel: watch::Sender<Option<DailyForecastProperty>>,
    pub daily_forecast_version: Arc<AtomicU32>,
    pub hourly_forecast: Arc<Mutex<Option<HourlyForecastProperty>>>,
    hourly_forecast_tx_channel: watch::Sender<Option<HourlyForecastProperty>>,
    pub hourly_forecast_version: Arc<AtomicU32>,
    pub current_condition_refresh_interval: Arc<Mutex<Option<i32>>>,

    current_condition_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    pub current_condition_refresh_interval_version: Arc<AtomicU32>,
    pub hourly_forecast_refresh_interval: Arc<Mutex<Option<i32>>>,

    hourly_forecast_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    pub hourly_forecast_refresh_interval_version: Arc<AtomicU32>,
    pub daily_forecast_refresh_interval: Arc<Mutex<Option<i32>>>,

    daily_forecast_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    pub daily_forecast_refresh_interval_version: Arc<AtomicU32>,
}

/// This is the struct for our API client.
#[derive(Clone)]
pub struct WeatherClient<C: MqttClient> {
    mqtt_client: C,
    /// Temporarily holds oneshot channels for responses to method calls.
    pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<String>>>>,

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

impl<C: MqttClient + Clone> WeatherClient<C> {
    /// Creates a new WeatherClient that uses an MqttClient.
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
            location: Arc::new(Mutex::new(None)),
            location_tx_channel: watch::channel(None).0,
            location_version: Arc::new(AtomicU32::new(0)),

            current_temperature: Arc::new(Mutex::new(None)),
            current_temperature_tx_channel: watch::channel(None).0,
            current_temperature_version: Arc::new(AtomicU32::new(0)),
            current_condition: Arc::new(Mutex::new(None)),
            current_condition_tx_channel: watch::channel(None).0,
            current_condition_version: Arc::new(AtomicU32::new(0)),
            daily_forecast: Arc::new(Mutex::new(None)),
            daily_forecast_tx_channel: watch::channel(None).0,
            daily_forecast_version: Arc::new(AtomicU32::new(0)),
            hourly_forecast: Arc::new(Mutex::new(None)),
            hourly_forecast_tx_channel: watch::channel(None).0,
            hourly_forecast_version: Arc::new(AtomicU32::new(0)),

            current_condition_refresh_interval: Arc::new(Mutex::new(None)),
            current_condition_refresh_interval_tx_channel: watch::channel(None).0,
            current_condition_refresh_interval_version: Arc::new(AtomicU32::new(0)),

            hourly_forecast_refresh_interval: Arc::new(Mutex::new(None)),
            hourly_forecast_refresh_interval_tx_channel: watch::channel(None).0,
            hourly_forecast_refresh_interval_version: Arc::new(AtomicU32::new(0)),

            daily_forecast_refresh_interval: Arc::new(Mutex::new(None)),
            daily_forecast_refresh_interval_tx_channel: watch::channel(None).0,
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

    async fn start_refresh_daily_forecast(&mut self) -> oneshot::Receiver<String> {
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

        let _resp_str: String = receiver.await.unwrap();

        Ok(())
    }

    async fn start_refresh_hourly_forecast(&mut self) -> oneshot::Receiver<String> {
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

        let _resp_str: String = receiver.await.unwrap();

        Ok(())
    }

    async fn start_refresh_current_conditions(&mut self) -> oneshot::Receiver<String> {
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

        let _resp_str: String = receiver.await.unwrap();

        Ok(())
    }

    /// Watch for changes to the `location` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_location(&self) -> watch::Receiver<Option<LocationProperty>> {
        self.properties.location_tx_channel.subscribe()
    }

    pub fn set_location(&mut self, value: LocationProperty) -> Result<(), MethodReturnCode> {
        let data = value;
        let topic: String = format!("weather/{}/property/location/setValue", self.client_id);
        let msg = message::property_update_message(
            &topic,
            &data,
            self.properties.location_version.load(Ordering::Relaxed),
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);
        Ok(())
    }

    /// Watch for changes to the `current_temperature` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_current_temperature(&self) -> watch::Receiver<Option<f32>> {
        self.properties.current_temperature_tx_channel.subscribe()
    }

    /// Watch for changes to the `current_condition` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_current_condition(&self) -> watch::Receiver<Option<CurrentConditionProperty>> {
        self.properties.current_condition_tx_channel.subscribe()
    }

    /// Watch for changes to the `daily_forecast` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_daily_forecast(&self) -> watch::Receiver<Option<DailyForecastProperty>> {
        self.properties.daily_forecast_tx_channel.subscribe()
    }

    /// Watch for changes to the `hourly_forecast` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_hourly_forecast(&self) -> watch::Receiver<Option<HourlyForecastProperty>> {
        self.properties.hourly_forecast_tx_channel.subscribe()
    }

    /// Watch for changes to the `current_condition_refresh_interval` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_current_condition_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .current_condition_refresh_interval_tx_channel
            .subscribe()
    }

    pub fn set_current_condition_refresh_interval(
        &mut self,
        value: i32,
    ) -> Result<(), MethodReturnCode> {
        let data = CurrentConditionRefreshIntervalProperty { seconds: value };
        let topic: String = format!(
            "weather/{}/property/currentConditionRefreshInterval/setValue",
            self.client_id
        );
        let msg = message::property_update_message(
            &topic,
            &data,
            self.properties
                .current_condition_refresh_interval_version
                .load(Ordering::Relaxed),
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);
        Ok(())
    }

    /// Watch for changes to the `hourly_forecast_refresh_interval` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_hourly_forecast_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .hourly_forecast_refresh_interval_tx_channel
            .subscribe()
    }

    pub fn set_hourly_forecast_refresh_interval(
        &mut self,
        value: i32,
    ) -> Result<(), MethodReturnCode> {
        let data = HourlyForecastRefreshIntervalProperty { seconds: value };
        let topic: String = format!(
            "weather/{}/property/hourlyForecastRefreshInterval/setValue",
            self.client_id
        );
        let msg = message::property_update_message(
            &topic,
            &data,
            self.properties
                .hourly_forecast_refresh_interval_version
                .load(Ordering::Relaxed),
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);
        Ok(())
    }

    /// Watch for changes to the `daily_forecast_refresh_interval` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_daily_forecast_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .daily_forecast_refresh_interval_tx_channel
            .subscribe()
    }

    pub fn set_daily_forecast_refresh_interval(
        &mut self,
        value: i32,
    ) -> Result<(), MethodReturnCode> {
        let data = DailyForecastRefreshIntervalProperty { seconds: value };
        let topic: String = format!(
            "weather/{}/property/dailyForecastRefreshInterval/setValue",
            self.client_id
        );
        let msg = message::property_update_message(
            &topic,
            &data,
            self.properties
                .daily_forecast_refresh_interval_version
                .load(Ordering::Relaxed),
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);
        Ok(())
    }

    /// Starts the tasks that process messages received.
    pub async fn run_loop(&mut self) -> Result<(), JoinError> {
        // Make sure the MqttClient is connected and running.
        let _ = self.mqtt_client.start().await;

        // Clone the Arc pointer to the map.  This will be moved into the loop_task.
        let resp_map: Arc<Mutex<HashMap<Uuid, oneshot::Sender<String>>>> =
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
            while let Ok(msg) = message_receiver.recv().await {
                let opt_corr_data: Option<Vec<u8>> =
                    msg.correlation_data.clone().map(|b| b.to_vec());
                let opt_corr_id: Option<Uuid> =
                    opt_corr_data.and_then(|b| Uuid::from_slice(b.as_slice()).ok());

                if let Some(subscription_id) = msg.subscription_id {
                    let payload = String::from_utf8_lossy(&msg.payload).to_string();
                    if subscription_id == sub_ids.refresh_daily_forecast_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<String> = sender;
                                match oss.send(payload) {
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
                                let oss: oneshot::Sender<String> = sender;
                                match oss.send(payload) {
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
                                let oss: oneshot::Sender<String> = sender;
                                match oss.send(payload) {
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
                                let mut guard = props.location.lock().expect("Mutex was poisoned");

                                *guard = Some(pl.clone());
                                let _ = props.location_tx_channel.send(Some(pl));
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
                                let mut guard = props
                                    .current_temperature
                                    .lock()
                                    .expect("Mutex was poisoned");

                                *guard = Some(pl.temperature_f.clone());
                                let _ = props
                                    .current_temperature_tx_channel
                                    .send(Some(pl.temperature_f));
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
                                let mut guard =
                                    props.current_condition.lock().expect("Mutex was poisoned");

                                *guard = Some(pl.clone());
                                let _ = props.current_condition_tx_channel.send(Some(pl));
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
                                let mut guard =
                                    props.daily_forecast.lock().expect("Mutex was poisoned");

                                *guard = Some(pl.clone());
                                let _ = props.daily_forecast_tx_channel.send(Some(pl));
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
                                let mut guard =
                                    props.hourly_forecast.lock().expect("Mutex was poisoned");

                                *guard = Some(pl.clone());
                                let _ = props.hourly_forecast_tx_channel.send(Some(pl));
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
                                let mut guard = props
                                    .current_condition_refresh_interval
                                    .lock()
                                    .expect("Mutex was poisoned");

                                *guard = Some(pl.seconds.clone());
                                let _ = props
                                    .current_condition_refresh_interval_tx_channel
                                    .send(Some(pl.seconds));
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
                                let mut guard = props
                                    .hourly_forecast_refresh_interval
                                    .lock()
                                    .expect("Mutex was poisoned");

                                *guard = Some(pl.seconds.clone());
                                let _ = props
                                    .hourly_forecast_refresh_interval_tx_channel
                                    .send(Some(pl.seconds));
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
                                let mut guard = props
                                    .daily_forecast_refresh_interval
                                    .lock()
                                    .expect("Mutex was poisoned");

                                *guard = Some(pl.seconds.clone());
                                let _ = props
                                    .daily_forecast_refresh_interval_tx_channel
                                    .send(Some(pl.seconds));
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
