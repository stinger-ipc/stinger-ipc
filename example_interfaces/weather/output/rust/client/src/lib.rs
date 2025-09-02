/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the weather interface.
*/

use mqttier::{MqttierClient, ReceivedMessage};
use std::collections::HashMap;
use json::JsonValue;
use uuid::Uuid;
use serde_json;


#[allow(unused_imports)]
use weather_types::{MethodResultCode, *};

use std::sync::{Arc, Mutex};
use tokio::sync::{broadcast, mpsc, oneshot};
use tokio::task::JoinError;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct WeatherSubscriptionIds {
    refresh_daily_forecast_method_resp: usize,
    refresh_hourly_forecast_method_resp: usize,
    refresh_current_conditions_method_resp: usize,
    
    current_time_signal: Option<usize>,
    location_property_value: usize,
    current_temperature_property_value: usize,
    current_condition_property_value: usize,
    daily_forecast_property_value: usize,
    hourly_forecast_property_value: usize,
    current_condition_refresh_interval_property_value: usize,
    hourly_forecast_refresh_interval_property_value: usize,
    daily_forecast_refresh_interval_property_value: usize,
    
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When WeatherClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct WeatherSignalChannels {
    current_time_sender: broadcast::Sender<CurrentTimeSignalPayload>,
    
}


#[derive(Clone)]
pub struct WeatherProperties {
    
    pub location: Arc<Mutex<Option<LocationProperty>>>,
    pub current_temperature: Arc<Mutex<Option<f32>>>,
    
    pub current_condition: Arc<Mutex<Option<CurrentConditionProperty>>>,
    pub daily_forecast: Arc<Mutex<Option<DailyForecastProperty>>>,
    pub hourly_forecast: Arc<Mutex<Option<HourlyForecastProperty>>>,
    pub current_condition_refresh_interval: Arc<Mutex<Option<i32>>>,
    
    pub hourly_forecast_refresh_interval: Arc<Mutex<Option<i32>>>,
    
    pub daily_forecast_refresh_interval: Arc<Mutex<Option<i32>>>,
    
}


/// This is the struct for our API client.
#[derive(Clone)]
pub struct WeatherClient {
    mqttier_client: MqttierClient,
    /// Temporarily holds oneshot channels for responses to method calls.
    pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<JsonValue>>>>,
    

    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<mpsc::Receiver<ReceivedMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,
    
    /// Struct contains all the properties.
    pub properties: WeatherProperties,
    
    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: WeatherSubscriptionIds,
    /// Holds the channels used for sending signals to the application.
    signal_channels: WeatherSignalChannels,
    
    /// Copy of MQTT Client ID
    pub client_id: String,
}

impl WeatherClient {

    /// Creates a new WeatherClient that uses an MqttierClient.
    pub async fn new(connection: &mut MqttierClient) -> Self {

        // Create a channel for messages to get from the Connection object to this WeatherClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        let topic_refresh_daily_forecast_method_resp = format!("client/{}/weather/method/refreshDailyForecast/response", connection.client_id);
        let subscription_id_refresh_daily_forecast_method_resp = connection.subscribe(topic_refresh_daily_forecast_method_resp, 2, message_received_tx.clone()).await;
        let subscription_id_refresh_daily_forecast_method_resp = subscription_id_refresh_daily_forecast_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_refresh_hourly_forecast_method_resp = format!("client/{}/weather/method/refreshHourlyForecast/response", connection.client_id);
        let subscription_id_refresh_hourly_forecast_method_resp = connection.subscribe(topic_refresh_hourly_forecast_method_resp, 2, message_received_tx.clone()).await;
        let subscription_id_refresh_hourly_forecast_method_resp = subscription_id_refresh_hourly_forecast_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_refresh_current_conditions_method_resp = format!("client/{}/weather/method/refreshCurrentConditions/response", connection.client_id);
        let subscription_id_refresh_current_conditions_method_resp = connection.subscribe(topic_refresh_current_conditions_method_resp, 2, message_received_tx.clone()).await;
        let subscription_id_refresh_current_conditions_method_resp = subscription_id_refresh_current_conditions_method_resp.unwrap_or_else(|_| usize::MAX);
        

        // Subscribe to all the topics needed for signals.
        let topic_current_time_signal = "weather/signal/currentTime".to_string();
        let subscription_id_current_time_signal = connection.subscribe(topic_current_time_signal, 2, message_received_tx.clone()).await;
        let subscription_id_current_time_signal = subscription_id_current_time_signal.unwrap_or_else(|_| usize::MAX);
        

        // Subscribe to all the topics needed for properties.
        
        let topic_location_property_value = "weather/property/location/value".to_string();
        let subscription_id_location_property_value = connection.subscribe(topic_location_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_location_property_value = subscription_id_location_property_value.unwrap_or_else(|_| usize::MAX);
        
        let topic_current_temperature_property_value = "weather/property/currentTemperature/value".to_string();
        let subscription_id_current_temperature_property_value = connection.subscribe(topic_current_temperature_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_current_temperature_property_value = subscription_id_current_temperature_property_value.unwrap_or_else(|_| usize::MAX);
        
        let topic_current_condition_property_value = "weather/property/currentCondition/value".to_string();
        let subscription_id_current_condition_property_value = connection.subscribe(topic_current_condition_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_current_condition_property_value = subscription_id_current_condition_property_value.unwrap_or_else(|_| usize::MAX);
        
        let topic_daily_forecast_property_value = "weather/property/dailyForecast/value".to_string();
        let subscription_id_daily_forecast_property_value = connection.subscribe(topic_daily_forecast_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_daily_forecast_property_value = subscription_id_daily_forecast_property_value.unwrap_or_else(|_| usize::MAX);
        
        let topic_hourly_forecast_property_value = "weather/property/hourlyForecast/value".to_string();
        let subscription_id_hourly_forecast_property_value = connection.subscribe(topic_hourly_forecast_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_hourly_forecast_property_value = subscription_id_hourly_forecast_property_value.unwrap_or_else(|_| usize::MAX);
        
        let topic_current_condition_refresh_interval_property_value = "weather/property/currentConditionRefreshInterval/value".to_string();
        let subscription_id_current_condition_refresh_interval_property_value = connection.subscribe(topic_current_condition_refresh_interval_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_current_condition_refresh_interval_property_value = subscription_id_current_condition_refresh_interval_property_value.unwrap_or_else(|_| usize::MAX);
        
        let topic_hourly_forecast_refresh_interval_property_value = "weather/property/hourlyForecastRefreshInterval/value".to_string();
        let subscription_id_hourly_forecast_refresh_interval_property_value = connection.subscribe(topic_hourly_forecast_refresh_interval_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_hourly_forecast_refresh_interval_property_value = subscription_id_hourly_forecast_refresh_interval_property_value.unwrap_or_else(|_| usize::MAX);
        
        let topic_daily_forecast_refresh_interval_property_value = "weather/property/dailyForecastRefreshInterval/value".to_string();
        let subscription_id_daily_forecast_refresh_interval_property_value = connection.subscribe(topic_daily_forecast_refresh_interval_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_daily_forecast_refresh_interval_property_value = subscription_id_daily_forecast_refresh_interval_property_value.unwrap_or_else(|_| usize::MAX);
        

        
        let property_values = WeatherProperties {
            location: Arc::new(Mutex::new(None)),
            
            
            current_temperature: Arc::new(Mutex::new(None)),
            current_condition: Arc::new(Mutex::new(None)),
            
            daily_forecast: Arc::new(Mutex::new(None)),
            
            hourly_forecast: Arc::new(Mutex::new(None)),
            
            
            current_condition_refresh_interval: Arc::new(Mutex::new(None)),
            
            hourly_forecast_refresh_interval: Arc::new(Mutex::new(None)),
            
            daily_forecast_refresh_interval: Arc::new(Mutex::new(None)),
        };
        
        // Create structure for subscription ids.
        let sub_ids = WeatherSubscriptionIds {
            refresh_daily_forecast_method_resp: subscription_id_refresh_daily_forecast_method_resp,
            refresh_hourly_forecast_method_resp: subscription_id_refresh_hourly_forecast_method_resp,
            refresh_current_conditions_method_resp: subscription_id_refresh_current_conditions_method_resp,
            current_time_signal: Some(subscription_id_current_time_signal),
            location_property_value: subscription_id_location_property_value,
            current_temperature_property_value: subscription_id_current_temperature_property_value,
            current_condition_property_value: subscription_id_current_condition_property_value,
            daily_forecast_property_value: subscription_id_daily_forecast_property_value,
            hourly_forecast_property_value: subscription_id_hourly_forecast_property_value,
            current_condition_refresh_interval_property_value: subscription_id_current_condition_refresh_interval_property_value,
            hourly_forecast_refresh_interval_property_value: subscription_id_hourly_forecast_refresh_interval_property_value,
            daily_forecast_refresh_interval_property_value: subscription_id_daily_forecast_refresh_interval_property_value,
            
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = WeatherSignalChannels {
            current_time_sender: broadcast::channel(64).0,
            
        };

        // Create WeatherClient structure.
        let inst = WeatherClient {
            mqttier_client: connection.clone(),
            pending_responses: Arc::new(Mutex::new(HashMap::new())),
            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,
            
            properties: property_values,
            
            subscription_ids: sub_ids,
            signal_channels: signal_channels,
            client_id: connection.client_id.to_string(),
        };
        inst
    }

    /// Get the RX receiver side of the broadcast channel for the current_time signal.
    /// The signal payload, `CurrentTimeSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_current_time_receiver(&self) -> broadcast::Receiver<CurrentTimeSignalPayload> {
        self.signal_channels.current_time_sender.subscribe()
    }
    

    /// The `refresh_daily_forecast` method.
    /// Method arguments are packed into a RefreshDailyForecastRequestObject structure
    /// and published to the `weather/method/refreshDailyForecast` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn refresh_daily_forecast(&mut self)->Result<(), MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = RefreshDailyForecastRequestObject {
        };

        let response_topic: String = format!("client/{}/weather/method/refreshDailyForecast/response", self.client_id);
        let _ = self.mqttier_client.publish_request("weather/method/refreshDailyForecast".to_string(), &data, response_topic, correlation_data).await;
        let _resp_obj = receiver.await.unwrap();
        Ok(())
        
    }

    /// Handler for responses to `refresh_daily_forecast` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_refresh_daily_forecast_response(pending_responses: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>>, payload: String, opt_correlation_id: Option<Uuid>) {
        
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id
                .and_then(|uuid| {
                    let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                    hashmap.remove(&uuid)
                });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
    }
    /// The `refresh_hourly_forecast` method.
    /// Method arguments are packed into a RefreshHourlyForecastRequestObject structure
    /// and published to the `weather/method/refreshHourlyForecast` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn refresh_hourly_forecast(&mut self)->Result<(), MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = RefreshHourlyForecastRequestObject {
        };

        let response_topic: String = format!("client/{}/weather/method/refreshHourlyForecast/response", self.client_id);
        let _ = self.mqttier_client.publish_request("weather/method/refreshHourlyForecast".to_string(), &data, response_topic, correlation_data).await;
        let _resp_obj = receiver.await.unwrap();
        Ok(())
        
    }

    /// Handler for responses to `refresh_hourly_forecast` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_refresh_hourly_forecast_response(pending_responses: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>>, payload: String, opt_correlation_id: Option<Uuid>) {
        
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id
                .and_then(|uuid| {
                    let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                    hashmap.remove(&uuid)
                });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
    }
    /// The `refresh_current_conditions` method.
    /// Method arguments are packed into a RefreshCurrentConditionsRequestObject structure
    /// and published to the `weather/method/refreshCurrentConditions` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn refresh_current_conditions(&mut self)->Result<(), MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = RefreshCurrentConditionsRequestObject {
        };

        let response_topic: String = format!("client/{}/weather/method/refreshCurrentConditions/response", self.client_id);
        let _ = self.mqttier_client.publish_request("weather/method/refreshCurrentConditions".to_string(), &data, response_topic, correlation_data).await;
        let _resp_obj = receiver.await.unwrap();
        Ok(())
        
    }

    /// Handler for responses to `refresh_current_conditions` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_refresh_current_conditions_response(pending_responses: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>>, payload: String, opt_correlation_id: Option<Uuid>) {
        
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id
                .and_then(|uuid| {
                    let mut hashmap = pending_responses.lock().expect("Mutex was poisoned");
                    hashmap.remove(&uuid)
                });
            match sender_opt {
                Some(sender) => {
                    let oss: oneshot::Sender<JsonValue> = sender;
                    match oss.send(payload_object) {
                        Ok(_) => (),
                        Err(_) => (),
                    }
                }
                None => (),
            }
        }
    }
    

    /// Starts the tasks that process messages received.
    pub async fn run_loop(&self) -> Result<(), JoinError> {
        // Make sure the MqttierClient is connected and running.
        let _ = self.mqttier_client.run_loop().await;

        // Clone the Arc pointer to the map.  This will be moved into the loop_task.
        let resp_map: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>> = self.pending_responses.clone();
        
        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = {
            let mut guard = self.msg_streamer_rx.lock().expect("Mutex was poisoned");
            guard.take().expect("msg_streamer_rx should be Some")
        };

        let sig_chans = self.signal_channels.clone();
        let sub_ids = self.subscription_ids.clone();
        let props = self.properties.clone();
        
        let _loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                
                let opt_corr_data: Option<Vec<u8>> = msg.correlation_data.clone();
                let opt_corr_id: Option<Uuid> = opt_corr_data.and_then(|b| Uuid::from_slice(b.as_slice()).ok());

                let payload = String::from_utf8_lossy(&msg.payload).to_string();
                if msg.subscription_id == sub_ids.refresh_daily_forecast_method_resp {
                    WeatherClient::handle_refresh_daily_forecast_response(resp_map.clone(), payload, opt_corr_id);
                }
                else if msg.subscription_id == sub_ids.refresh_hourly_forecast_method_resp {
                    WeatherClient::handle_refresh_hourly_forecast_response(resp_map.clone(), payload, opt_corr_id);
                }
                else if msg.subscription_id == sub_ids.refresh_current_conditions_method_resp {
                    WeatherClient::handle_refresh_current_conditions_response(resp_map.clone(), payload, opt_corr_id);
                }
                
                if msg.subscription_id == sub_ids.current_time_signal.unwrap_or_default() {
                    let chan = sig_chans.current_time_sender.clone();
                    let pl: CurrentTimeSignalPayload =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let _send_result = chan.send(pl);
                }
                
                if msg.subscription_id == sub_ids.location_property_value {
                    let pl: LocationProperty =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.location.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
                else if msg.subscription_id == sub_ids.current_temperature_property_value {
                    let pl: f32 =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.current_temperature.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
                else if msg.subscription_id == sub_ids.current_condition_property_value {
                    let pl: CurrentConditionProperty =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.current_condition.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
                else if msg.subscription_id == sub_ids.daily_forecast_property_value {
                    let pl: DailyForecastProperty =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.daily_forecast.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
                else if msg.subscription_id == sub_ids.hourly_forecast_property_value {
                    let pl: HourlyForecastProperty =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.hourly_forecast.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
                else if msg.subscription_id == sub_ids.current_condition_refresh_interval_property_value {
                    let pl: i32 =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.current_condition_refresh_interval.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
                else if msg.subscription_id == sub_ids.hourly_forecast_refresh_interval_property_value {
                    let pl: i32 =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.hourly_forecast_refresh_interval.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
                else if msg.subscription_id == sub_ids.daily_forecast_refresh_interval_property_value {
                    let pl: i32 =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.daily_forecast_refresh_interval.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
            }   
        });

        println!("Started client receive task");
        Ok(())
    }
}