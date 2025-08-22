/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the weather-forecast interface.
*/

extern crate paho_mqtt as mqtt;
use connection::{MessagePublisher, Connection, ReceivedMessage};

use json::{JsonValue};
use std::collections::HashMap;
use uuid::Uuid;
use serde_json;

#[allow(unused_imports)]
use connection::payloads::{*, MethodResultCode};

use std::sync::{Arc, Mutex};
use tokio::sync::{mpsc, broadcast, oneshot};
use tokio::join;
use tokio::task::JoinError;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct WeatherForecastSubscriptionIds {
    refresh_daily_forecast_method_resp: i32,refresh_hourly_forecast_method_resp: i32,refresh_current_conditions_method_resp: i32,
    current_time_signal: Option<i32>,
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When WeatherForecastClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct WeatherForecastSignalChannels {
    current_time_sender: broadcast::Sender<CurrentTimeSignalPayload>,
    
}

/// This is the struct for our API client.
pub struct WeatherForecastClient {
    /// Temporarily holds oneshot channels for responses to method calls.
    pending_responses: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>>,
    

    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Option<mpsc::Receiver<ReceivedMessage>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Through this MessagePublisher object, we can publish messages to MQTT.
    msg_publisher: MessagePublisher,
    
    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: WeatherForecastSubscriptionIds,

    /// Holds the channels used for sending signals to the application.
    signal_channels: WeatherForecastSignalChannels,
    
    /// Copy of MQTT Client ID
    client_id: String,
}

impl WeatherForecastClient {

    /// Creates a new WeatherForecastClient that uses elements from the provided Connection object.
    pub async fn new(connection: &mut Connection) -> Self {
        let _ = connection.connect().await.expect("Could not connect to MQTT broker");

        // Create a channel for messages to get from the Connection object to this WeatherForecastClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        // Create the publisher object.
        let publisher = connection.get_publisher();

        // Subscribe to all the topics needed for method responses.
        let topic_refresh_daily_forecast_method_resp = format!("client/{}/weather-forecast/method/refresh_daily_forecast/response", connection.client_id);
        let subscription_id_refresh_daily_forecast_method_resp = connection.subscribe(&topic_refresh_daily_forecast_method_resp, message_received_tx.clone()).await;
        let subscription_id_refresh_daily_forecast_method_resp = subscription_id_refresh_daily_forecast_method_resp.unwrap_or_else(|_| -1);
        let topic_refresh_hourly_forecast_method_resp = format!("client/{}/weather-forecast/method/refresh_hourly_forecast/response", connection.client_id);
        let subscription_id_refresh_hourly_forecast_method_resp = connection.subscribe(&topic_refresh_hourly_forecast_method_resp, message_received_tx.clone()).await;
        let subscription_id_refresh_hourly_forecast_method_resp = subscription_id_refresh_hourly_forecast_method_resp.unwrap_or_else(|_| -1);
        let topic_refresh_current_conditions_method_resp = format!("client/{}/weather-forecast/method/refresh_current_conditions/response", connection.client_id);
        let subscription_id_refresh_current_conditions_method_resp = connection.subscribe(&topic_refresh_current_conditions_method_resp, message_received_tx.clone()).await;
        let subscription_id_refresh_current_conditions_method_resp = subscription_id_refresh_current_conditions_method_resp.unwrap_or_else(|_| -1);
        

        // Subscribe to all the topics needed for signals.
        let topic_current_time_signal = "weather-forecast/signal/current_time";
        let subscription_id_current_time_signal = connection.subscribe(&topic_current_time_signal, message_received_tx.clone()).await;
        let subscription_id_current_time_signal = subscription_id_current_time_signal.unwrap_or_else(|_| -1);
        

        // Create structure for subscription ids.
        let sub_ids = WeatherForecastSubscriptionIds {
            refresh_daily_forecast_method_resp: subscription_id_refresh_daily_forecast_method_resp,
            refresh_hourly_forecast_method_resp: subscription_id_refresh_hourly_forecast_method_resp,
            refresh_current_conditions_method_resp: subscription_id_refresh_current_conditions_method_resp,
            current_time_signal: Some(subscription_id_current_time_signal),
            
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = WeatherForecastSignalChannels {
            current_time_sender: broadcast::channel(64).0,
            
        };

        // Create WeatherForecastClient structure.
        let inst = WeatherForecastClient {
            pending_responses: Arc::new(Mutex::new(HashMap::new())),
            msg_streamer_rx: Some(message_received_rx),
            msg_streamer_tx: message_received_tx,
            msg_publisher: publisher,
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
    /// and published to the `weather-forecast/method/refresh_daily_forecast` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn refresh_daily_forecast(&mut self, )->Result<(), MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let data = connection::payloads::RefreshDailyForecastRequestObject {
        };
        let response_topic = format!("client/{}/weather-forecast/method/refresh_daily_forecast/response", self.client_id);
        let _ = self.msg_publisher.publish_request_structure("weather-forecast/method/refresh_daily_forecast".to_string(), &data, response_topic.as_str(), correlation_id).await;
        let resp_obj = receiver.await.unwrap();
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
                        Err(_) => ()
                    }
                },
                None => ()
            }
        }
    }
    /// The `refresh_hourly_forecast` method.
    /// Method arguments are packed into a RefreshHourlyForecastRequestObject structure
    /// and published to the `weather-forecast/method/refresh_hourly_forecast` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn refresh_hourly_forecast(&mut self, )->Result<(), MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let data = connection::payloads::RefreshHourlyForecastRequestObject {
        };
        let response_topic = format!("client/{}/weather-forecast/method/refresh_hourly_forecast/response", self.client_id);
        let _ = self.msg_publisher.publish_request_structure("weather-forecast/method/refresh_hourly_forecast".to_string(), &data, response_topic.as_str(), correlation_id).await;
        let resp_obj = receiver.await.unwrap();
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
                        Err(_) => ()
                    }
                },
                None => ()
            }
        }
    }
    /// The `refresh_current_conditions` method.
    /// Method arguments are packed into a RefreshCurrentConditionsRequestObject structure
    /// and published to the `weather-forecast/method/refresh_current_conditions` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn refresh_current_conditions(&mut self, )->Result<(), MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let data = connection::payloads::RefreshCurrentConditionsRequestObject {
        };
        let response_topic = format!("client/{}/weather-forecast/method/refresh_current_conditions/response", self.client_id);
        let _ = self.msg_publisher.publish_request_structure("weather-forecast/method/refresh_current_conditions".to_string(), &data, response_topic.as_str(), correlation_id).await;
        let resp_obj = receiver.await.unwrap();
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
                        Err(_) => ()
                    }
                },
                None => ()
            }
        }
    }
    

    /// Starts the tasks that process messages received.
    pub async fn receive_loop(&mut self) -> Result<(), JoinError> {
        // Clone the Arc pointer to the map.  This will be moved into the loop_task.
        let resp_map: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>> = self.pending_responses.clone();
        
        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = self.msg_streamer_rx.take().expect("msg_streamer_rx should be Some");

        let sig_chans = self.signal_channels.clone();
        let sub_ids = self.subscription_ids.clone();

        let loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                let msg_props = msg.message.properties();
                let opt_corr_id_bin: Option<Vec<u8>> = msg_props.get_binary(mqtt::PropertyCode::CorrelationData);
                let corr_id: Option<Uuid> = opt_corr_id_bin.and_then(|b| Uuid::from_slice(&b).ok());
                if msg.subscription_id == sub_ids.refresh_daily_forecast_method_resp {
                    WeatherForecastClient::handle_refresh_daily_forecast_response(resp_map.clone(), msg.message.payload_str().to_string(), corr_id);
                }
                else if msg.subscription_id == sub_ids.refresh_hourly_forecast_method_resp {
                    WeatherForecastClient::handle_refresh_hourly_forecast_response(resp_map.clone(), msg.message.payload_str().to_string(), corr_id);
                }
                else if msg.subscription_id == sub_ids.refresh_current_conditions_method_resp {
                    WeatherForecastClient::handle_refresh_current_conditions_response(resp_map.clone(), msg.message.payload_str().to_string(), corr_id);
                }
                if msg.subscription_id == sub_ids.current_time_signal.unwrap_or_default() {
                    let chan = sig_chans.current_time_sender.clone();
                    let pl: connection::payloads::CurrentTimeSignalPayload =  serde_json::from_str(&msg.message.payload_str()).expect("Failed to deserialize");
                    let _send_result = chan.send(pl);
                }
                
            }   
        });

        println!("Started client receive task");
        Ok(())
    }
}