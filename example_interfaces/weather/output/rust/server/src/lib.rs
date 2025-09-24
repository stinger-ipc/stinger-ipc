/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the weather interface.
*/

use mqttier::{MqttierClient, PublishResult, ReceivedMessage};

use std::any::Any;
#[allow(unused_imports)]
use weather_types::MethodReturnCode;
use weather_types::payloads::*;

use async_trait::async_trait;
use std::sync::{Arc, Mutex};
use tokio::sync::Mutex as AsyncMutex;

use serde_json;
use tokio::sync::{mpsc, watch};

use tokio::task::JoinError;

use std::future::Future;
use std::pin::Pin;

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
    location: Arc<Mutex<Option<LocationProperty>>>,
    location_tx_channel: watch::Sender<Option<LocationProperty>>,
    current_temperature_topic: Arc<String>,
    current_temperature: Arc<Mutex<Option<f32>>>,
    current_temperature_tx_channel: watch::Sender<Option<f32>>,
    current_condition_topic: Arc<String>,
    current_condition: Arc<Mutex<Option<CurrentConditionProperty>>>,
    current_condition_tx_channel: watch::Sender<Option<CurrentConditionProperty>>,
    daily_forecast_topic: Arc<String>,
    daily_forecast: Arc<Mutex<Option<DailyForecastProperty>>>,
    daily_forecast_tx_channel: watch::Sender<Option<DailyForecastProperty>>,
    hourly_forecast_topic: Arc<String>,
    hourly_forecast: Arc<Mutex<Option<HourlyForecastProperty>>>,
    hourly_forecast_tx_channel: watch::Sender<Option<HourlyForecastProperty>>,
    current_condition_refresh_interval_topic: Arc<String>,
    current_condition_refresh_interval: Arc<Mutex<Option<i32>>>,
    current_condition_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    hourly_forecast_refresh_interval_topic: Arc<String>,
    hourly_forecast_refresh_interval: Arc<Mutex<Option<i32>>>,
    hourly_forecast_refresh_interval_tx_channel: watch::Sender<Option<i32>>,
    daily_forecast_refresh_interval_topic: Arc<String>,
    daily_forecast_refresh_interval: Arc<Mutex<Option<i32>>>,
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
}

impl WeatherServer {
    pub async fn new(
        connection: &mut MqttierClient,
        method_handlers: Arc<AsyncMutex<Box<dyn WeatherMethodHandlers>>>,
    ) -> Self {
        // Create a channel for messages to get from the MqttierClient object to this WeatherServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel::<ReceivedMessage>(64);

        // Create method handler struct
        let subscription_id_refresh_daily_forecast_method_req = connection
            .subscribe(
                "weather/method/refreshDailyForecast".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_daily_forecast_method_req =
            subscription_id_refresh_daily_forecast_method_req.unwrap_or_else(|_| usize::MAX);
        let subscription_id_refresh_hourly_forecast_method_req = connection
            .subscribe(
                "weather/method/refreshHourlyForecast".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_hourly_forecast_method_req =
            subscription_id_refresh_hourly_forecast_method_req.unwrap_or_else(|_| usize::MAX);
        let subscription_id_refresh_current_conditions_method_req = connection
            .subscribe(
                "weather/method/refreshCurrentConditions".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_refresh_current_conditions_method_req =
            subscription_id_refresh_current_conditions_method_req.unwrap_or_else(|_| usize::MAX);

        let subscription_id_location_property_update = connection
            .subscribe(
                "weather/property/location/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_location_property_update =
            subscription_id_location_property_update.unwrap_or_else(|_| usize::MAX);

        let subscription_id_current_condition_refresh_interval_property_update = connection
            .subscribe(
                "weather/property/currentConditionRefreshInterval/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_current_condition_refresh_interval_property_update =
            subscription_id_current_condition_refresh_interval_property_update
                .unwrap_or_else(|_| usize::MAX);

        let subscription_id_hourly_forecast_refresh_interval_property_update = connection
            .subscribe(
                "weather/property/hourlyForecastRefreshInterval/setValue".to_string(),
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_hourly_forecast_refresh_interval_property_update =
            subscription_id_hourly_forecast_refresh_interval_property_update
                .unwrap_or_else(|_| usize::MAX);

        let subscription_id_daily_forecast_refresh_interval_property_update = connection
            .subscribe(
                "weather/property/dailyForecastRefreshInterval/setValue".to_string(),
                2,
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
            location_topic: Arc::new(String::from("weather/property/location/value")),

            location: Arc::new(Mutex::new(None)),
            location_tx_channel: watch::channel(None).0,
            current_temperature_topic: Arc::new(String::from(
                "weather/property/currentTemperature/value",
            )),

            current_temperature: Arc::new(Mutex::new(None)),
            current_temperature_tx_channel: watch::channel(None).0,
            current_condition_topic: Arc::new(String::from(
                "weather/property/currentCondition/value",
            )),

            current_condition: Arc::new(Mutex::new(None)),
            current_condition_tx_channel: watch::channel(None).0,
            daily_forecast_topic: Arc::new(String::from("weather/property/dailyForecast/value")),

            daily_forecast: Arc::new(Mutex::new(None)),
            daily_forecast_tx_channel: watch::channel(None).0,
            hourly_forecast_topic: Arc::new(String::from("weather/property/hourlyForecast/value")),

            hourly_forecast: Arc::new(Mutex::new(None)),
            hourly_forecast_tx_channel: watch::channel(None).0,
            current_condition_refresh_interval_topic: Arc::new(String::from(
                "weather/property/currentConditionRefreshInterval/value",
            )),

            current_condition_refresh_interval: Arc::new(Mutex::new(None)),
            current_condition_refresh_interval_tx_channel: watch::channel(None).0,
            hourly_forecast_refresh_interval_topic: Arc::new(String::from(
                "weather/property/hourlyForecastRefreshInterval/value",
            )),

            hourly_forecast_refresh_interval: Arc::new(Mutex::new(None)),
            hourly_forecast_refresh_interval_tx_channel: watch::channel(None).0,
            daily_forecast_refresh_interval_topic: Arc::new(String::from(
                "weather/property/dailyForecastRefreshInterval/value",
            )),

            daily_forecast_refresh_interval: Arc::new(Mutex::new(None)),
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
        }
    }

    /// Emits the current_time signal with the given arguments.
    pub async fn emit_current_time(
        &mut self,
        current_time: String,
    ) -> Pin<Box<dyn Future<Output = Result<(), MethodReturnCode>>>> {
        let data = CurrentTimeSignalPayload {
            current_time: current_time,
        };
        let publish_oneshot = self
            .mqttier_client
            .publish_structure("weather/signal/currentTime".to_string(), &data)
            .await;
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
                Ok(_) => {
                    let retval = RefreshDailyForecastReturnValue {};

                    let _publish_result = publisher
                        .publish_response(resp_topic, &retval, corr_data)
                        .await;
                }
                Err(err) => {
                    eprintln!(
                        "Error occurred while handling {}: {:?}",
                        stringify!(refresh_daily_forecast),
                        err
                    );
                }
            }
        } else {
            eprintln!("No response topic found in message properties.");
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
                Ok(_) => {
                    let retval = RefreshHourlyForecastReturnValue {};

                    let _publish_result = publisher
                        .publish_response(resp_topic, &retval, corr_data)
                        .await;
                }
                Err(err) => {
                    eprintln!(
                        "Error occurred while handling {}: {:?}",
                        stringify!(refresh_hourly_forecast),
                        err
                    );
                }
            }
        } else {
            eprintln!("No response topic found in message properties.");
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
                Ok(_) => {
                    let retval = RefreshCurrentConditionsReturnValue {};

                    let _publish_result = publisher
                        .publish_response(resp_topic, &retval, corr_data)
                        .await;
                }
                Err(err) => {
                    eprintln!(
                        "Error occurred while handling {}: {:?}",
                        stringify!(refresh_current_conditions),
                        err
                    );
                }
            }
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }

    async fn publish_location_value(
        publisher: MqttierClient,
        topic: String,
        data: LocationProperty,
    ) {
        let _pub_result = publisher.publish_state(topic, &data, 1).await;
    }

    async fn update_location_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        data: Arc<Mutex<Option<LocationProperty>>>,
        watch_sender: watch::Sender<Option<LocationProperty>>,
        msg: ReceivedMessage,
    ) {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_data: LocationProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.clone());

        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data;

        let data_to_send_to_watchers = data2.clone();
        let _ = watch_sender.send(Some(data_to_send_to_watchers));
        let _ = tokio::spawn(async move {
            WeatherServer::publish_location_value(publisher2, topic2, data2).await;
        });
    }

    pub async fn watch_location(&self) -> watch::Receiver<Option<LocationProperty>> {
        self.properties.location_tx_channel.subscribe()
    }

    pub async fn set_location(&mut self, data: LocationProperty) {
        println!("Setting location of type LocationProperty");
        let prop = self.properties.location.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let data_to_send_to_watchers = data.clone();
        let _ = self
            .properties
            .location_tx_channel
            .send(Some(data_to_send_to_watchers));

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.location_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property location of type LocationProperty to {}",
                topic2
            );
            WeatherServer::publish_location_value(publisher2, topic2, data).await;
        });
    }

    async fn publish_current_temperature_value(publisher: MqttierClient, topic: String, data: f32) {
        let new_data = CurrentTemperatureProperty {
            temperature_f: data,
        };
        println!("Publishing to topic {}", topic);
        let _pub_result = publisher.publish_state(topic, &new_data, 1).await;
    }

    pub async fn set_current_temperature(&mut self, data: f32) {
        println!("Setting current_temperature of type f32");
        let prop = self.properties.current_temperature.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let data_to_send_to_watchers = data.clone();
        let _ = self
            .properties
            .current_temperature_tx_channel
            .send(Some(data_to_send_to_watchers));

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.current_temperature_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property current_temperature of type f32 to {}",
                topic2
            );
            WeatherServer::publish_current_temperature_value(publisher2, topic2, data).await;
        });
    }

    async fn publish_current_condition_value(
        publisher: MqttierClient,
        topic: String,
        data: CurrentConditionProperty,
    ) {
        let _pub_result = publisher.publish_state(topic, &data, 1).await;
    }

    pub async fn set_current_condition(&mut self, data: CurrentConditionProperty) {
        println!("Setting current_condition of type CurrentConditionProperty");
        let prop = self.properties.current_condition.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let data_to_send_to_watchers = data.clone();
        let _ = self
            .properties
            .current_condition_tx_channel
            .send(Some(data_to_send_to_watchers));

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.current_condition_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property current_condition of type CurrentConditionProperty to {}",
                topic2
            );
            WeatherServer::publish_current_condition_value(publisher2, topic2, data).await;
        });
    }

    async fn publish_daily_forecast_value(
        publisher: MqttierClient,
        topic: String,
        data: DailyForecastProperty,
    ) {
        let _pub_result = publisher.publish_state(topic, &data, 1).await;
    }

    pub async fn set_daily_forecast(&mut self, data: DailyForecastProperty) {
        println!("Setting daily_forecast of type DailyForecastProperty");
        let prop = self.properties.daily_forecast.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let data_to_send_to_watchers = data.clone();
        let _ = self
            .properties
            .daily_forecast_tx_channel
            .send(Some(data_to_send_to_watchers));

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.daily_forecast_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property daily_forecast of type DailyForecastProperty to {}",
                topic2
            );
            WeatherServer::publish_daily_forecast_value(publisher2, topic2, data).await;
        });
    }

    async fn publish_hourly_forecast_value(
        publisher: MqttierClient,
        topic: String,
        data: HourlyForecastProperty,
    ) {
        let _pub_result = publisher.publish_state(topic, &data, 1).await;
    }

    pub async fn set_hourly_forecast(&mut self, data: HourlyForecastProperty) {
        println!("Setting hourly_forecast of type HourlyForecastProperty");
        let prop = self.properties.hourly_forecast.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let data_to_send_to_watchers = data.clone();
        let _ = self
            .properties
            .hourly_forecast_tx_channel
            .send(Some(data_to_send_to_watchers));

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self.properties.hourly_forecast_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property hourly_forecast of type HourlyForecastProperty to {}",
                topic2
            );
            WeatherServer::publish_hourly_forecast_value(publisher2, topic2, data).await;
        });
    }

    async fn publish_current_condition_refresh_interval_value(
        publisher: MqttierClient,
        topic: String,
        data: i32,
    ) {
        let new_data = CurrentConditionRefreshIntervalProperty { seconds: data };
        println!("Publishing to topic {}", topic);
        let _pub_result = publisher.publish_state(topic, &new_data, 1).await;
    }

    async fn update_current_condition_refresh_interval_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        data: Arc<Mutex<Option<i32>>>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: ReceivedMessage,
    ) {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_data: CurrentConditionRefreshIntervalProperty =
            serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.seconds);
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.seconds;
        let data_to_send_to_watchers = data2.clone();
        let _ = watch_sender.send(Some(data_to_send_to_watchers));
        let _ = tokio::spawn(async move {
            WeatherServer::publish_current_condition_refresh_interval_value(
                publisher2, topic2, data2,
            )
            .await;
        });
    }

    pub async fn watch_current_condition_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .current_condition_refresh_interval_tx_channel
            .subscribe()
    }

    pub async fn set_current_condition_refresh_interval(&mut self, data: i32) {
        println!("Setting current_condition_refresh_interval of type i32");
        let prop = self.properties.current_condition_refresh_interval.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let data_to_send_to_watchers = data.clone();
        let _ = self
            .properties
            .current_condition_refresh_interval_tx_channel
            .send(Some(data_to_send_to_watchers));

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self
            .properties
            .current_condition_refresh_interval_topic
            .as_ref()
            .clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property current_condition_refresh_interval of type i32 to {}",
                topic2
            );
            WeatherServer::publish_current_condition_refresh_interval_value(
                publisher2, topic2, data,
            )
            .await;
        });
    }

    async fn publish_hourly_forecast_refresh_interval_value(
        publisher: MqttierClient,
        topic: String,
        data: i32,
    ) {
        let new_data = HourlyForecastRefreshIntervalProperty { seconds: data };
        println!("Publishing to topic {}", topic);
        let _pub_result = publisher.publish_state(topic, &new_data, 1).await;
    }

    async fn update_hourly_forecast_refresh_interval_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        data: Arc<Mutex<Option<i32>>>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: ReceivedMessage,
    ) {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_data: HourlyForecastRefreshIntervalProperty =
            serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.seconds);
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.seconds;
        let data_to_send_to_watchers = data2.clone();
        let _ = watch_sender.send(Some(data_to_send_to_watchers));
        let _ = tokio::spawn(async move {
            WeatherServer::publish_hourly_forecast_refresh_interval_value(
                publisher2, topic2, data2,
            )
            .await;
        });
    }

    pub async fn watch_hourly_forecast_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .hourly_forecast_refresh_interval_tx_channel
            .subscribe()
    }

    pub async fn set_hourly_forecast_refresh_interval(&mut self, data: i32) {
        println!("Setting hourly_forecast_refresh_interval of type i32");
        let prop = self.properties.hourly_forecast_refresh_interval.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let data_to_send_to_watchers = data.clone();
        let _ = self
            .properties
            .hourly_forecast_refresh_interval_tx_channel
            .send(Some(data_to_send_to_watchers));

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self
            .properties
            .hourly_forecast_refresh_interval_topic
            .as_ref()
            .clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property hourly_forecast_refresh_interval of type i32 to {}",
                topic2
            );
            WeatherServer::publish_hourly_forecast_refresh_interval_value(publisher2, topic2, data)
                .await;
        });
    }

    async fn publish_daily_forecast_refresh_interval_value(
        publisher: MqttierClient,
        topic: String,
        data: i32,
    ) {
        let new_data = DailyForecastRefreshIntervalProperty { seconds: data };
        println!("Publishing to topic {}", topic);
        let _pub_result = publisher.publish_state(topic, &new_data, 1).await;
    }

    async fn update_daily_forecast_refresh_interval_value(
        publisher: MqttierClient,
        topic: Arc<String>,
        data: Arc<Mutex<Option<i32>>>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: ReceivedMessage,
    ) {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_data: DailyForecastRefreshIntervalProperty =
            serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.seconds);
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.seconds;
        let data_to_send_to_watchers = data2.clone();
        let _ = watch_sender.send(Some(data_to_send_to_watchers));
        let _ = tokio::spawn(async move {
            WeatherServer::publish_daily_forecast_refresh_interval_value(publisher2, topic2, data2)
                .await;
        });
    }

    pub async fn watch_daily_forecast_refresh_interval(&self) -> watch::Receiver<Option<i32>> {
        self.properties
            .daily_forecast_refresh_interval_tx_channel
            .subscribe()
    }

    pub async fn set_daily_forecast_refresh_interval(&mut self, data: i32) {
        println!("Setting daily_forecast_refresh_interval of type i32");
        let prop = self.properties.daily_forecast_refresh_interval.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let data_to_send_to_watchers = data.clone();
        let _ = self
            .properties
            .daily_forecast_refresh_interval_tx_channel
            .send(Some(data_to_send_to_watchers));

        let publisher2 = self.mqttier_client.clone();
        let topic2 = self
            .properties
            .daily_forecast_refresh_interval_topic
            .as_ref()
            .clone();
        let _ = tokio::spawn(async move {
            println!(
                "Will publish property daily_forecast_refresh_interval of type i32 to {}",
                topic2
            );
            WeatherServer::publish_daily_forecast_refresh_interval_value(publisher2, topic2, data)
                .await;
        });
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
                } else if msg.subscription_id == sub_ids.location_property_update {
                    WeatherServer::update_location_value(
                        publisher.clone(),
                        properties.location_topic.clone(),
                        properties.location.clone(),
                        properties.location_tx_channel.clone(),
                        msg,
                    )
                    .await;
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
                    .await;
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
                    .await;
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
                    .await;
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
