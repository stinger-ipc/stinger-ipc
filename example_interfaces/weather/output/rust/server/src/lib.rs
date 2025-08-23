/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the weather-forecast interface.
*/

extern crate paho_mqtt as mqtt;
use connection::{MessagePublisher, Connection, ReceivedMessage};

#[allow(unused_imports)]
use connection::payloads::{*, MethodResultCode};

use std::sync::{Arc, Mutex};
use tokio::sync::{mpsc};
use tokio::join;
use tokio::task::JoinError;
use serde::{Serialize, Deserialize};
use serde_json;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct WeatherForecastServerSubscriptionIds {
    refresh_daily_forecast_method_req: i32,
    refresh_hourly_forecast_method_req: i32,
    refresh_current_conditions_method_req: i32,
    
    
    location_property_update: i32,
    
    current_condition_refresh_interval_property_update: i32,
    
    hourly_forecast_refresh_interval_property_update: i32,
    
    daily_forecast_refresh_interval_property_update: i32,
    
}

#[derive(Clone)]
struct WeatherForecastServerMethodHandlers {
    /// Pointer to a function to handle the refresh_daily_forecast method request.
    method_handler_for_refresh_daily_forecast: Arc<Mutex<Box<dyn Fn()->Result<(), MethodResultCode> + Send>>>,
    /// Pointer to a function to handle the refresh_hourly_forecast method request.
    method_handler_for_refresh_hourly_forecast: Arc<Mutex<Box<dyn Fn()->Result<(), MethodResultCode> + Send>>>,
    /// Pointer to a function to handle the refresh_current_conditions method request.
    method_handler_for_refresh_current_conditions: Arc<Mutex<Box<dyn Fn()->Result<(), MethodResultCode> + Send>>>,
    
}

#[derive(Clone)]
struct WeatherForecastProperties {
    location_topic: Arc<String>,
    location: Arc<Mutex<Option<connection::payloads::LocationProperty>>>,current_temperature_topic: Arc<String>,
    current_temperature: Arc<Mutex<Option<f32>>>,
    current_condition_topic: Arc<String>,
    current_condition: Arc<Mutex<Option<connection::payloads::CurrentConditionProperty>>>,daily_forecast_topic: Arc<String>,
    daily_forecast: Arc<Mutex<Option<connection::payloads::DailyForecastProperty>>>,hourly_forecast_topic: Arc<String>,
    hourly_forecast: Arc<Mutex<Option<connection::payloads::HourlyForecastProperty>>>,current_condition_refresh_interval_topic: Arc<String>,
    current_condition_refresh_interval: Arc<Mutex<Option<i32>>>,
    hourly_forecast_refresh_interval_topic: Arc<String>,
    hourly_forecast_refresh_interval: Arc<Mutex<Option<i32>>>,
    daily_forecast_refresh_interval_topic: Arc<String>,
    daily_forecast_refresh_interval: Arc<Mutex<Option<i32>>>,
    
}

pub struct WeatherForecastServer {
    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Option<mpsc::Receiver<ReceivedMessage>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Through this MessagePublisher object, we can publish messages to MQTT.
    msg_publisher: MessagePublisher,

    /// Struct contains all the handlers for the various methods.
    method_handlers: WeatherForecastServerMethodHandlers,
    
    /// Struct contains all the properties.
    properties: WeatherForecastProperties,
    
    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: WeatherForecastServerSubscriptionIds,

    /// Copy of MQTT Client ID
    client_id: String,
}

impl WeatherForecastServer {
    pub async fn new(connection: &mut Connection) -> Self {
        let _ = connection.connect().await.expect("Could not connect to MQTT broker");

        //let interface_info = String::from(r#"{"name": "weather-forecast", "summary": "Current conditions, daily and hourly forecasts from the NWS API", "title": "NWS weather forecast", "version": "0.0.1"}"#);
        //connection.publish("weather-forecast/interface".to_string(), interface_info, 1).await;

        // Create a channel for messages to get from the Connection object to this WeatherForecastClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        let publisher = connection.get_publisher();

        // Create method handler struct
        let subscription_id_refresh_daily_forecast_method_req = connection.subscribe("weather-forecast/method/refresh_daily_forecast", message_received_tx.clone()).await;
        let subscription_id_refresh_daily_forecast_method_req = subscription_id_refresh_daily_forecast_method_req.unwrap_or_else(|_| -1);
        let subscription_id_refresh_hourly_forecast_method_req = connection.subscribe("weather-forecast/method/refresh_hourly_forecast", message_received_tx.clone()).await;
        let subscription_id_refresh_hourly_forecast_method_req = subscription_id_refresh_hourly_forecast_method_req.unwrap_or_else(|_| -1);
        let subscription_id_refresh_current_conditions_method_req = connection.subscribe("weather-forecast/method/refresh_current_conditions", message_received_tx.clone()).await;
        let subscription_id_refresh_current_conditions_method_req = subscription_id_refresh_current_conditions_method_req.unwrap_or_else(|_| -1);
        

        
        let subscription_id_location_property_update = connection.subscribe("weather-forecast/property/location/set_value", message_received_tx.clone()).await;
        let subscription_id_location_property_update = subscription_id_location_property_update.unwrap_or_else(|_| -1);
        
        let subscription_id_current_condition_refresh_interval_property_update = connection.subscribe("weather-forecast/property/current_condition_refresh_interval/set_value", message_received_tx.clone()).await;
        let subscription_id_current_condition_refresh_interval_property_update = subscription_id_current_condition_refresh_interval_property_update.unwrap_or_else(|_| -1);
        
        let subscription_id_hourly_forecast_refresh_interval_property_update = connection.subscribe("weather-forecast/property/hourly_forecast_refresh_interval/set_value", message_received_tx.clone()).await;
        let subscription_id_hourly_forecast_refresh_interval_property_update = subscription_id_hourly_forecast_refresh_interval_property_update.unwrap_or_else(|_| -1);
        
        let subscription_id_daily_forecast_refresh_interval_property_update = connection.subscribe("weather-forecast/property/daily_forecast_refresh_interval/set_value", message_received_tx.clone()).await;
        let subscription_id_daily_forecast_refresh_interval_property_update = subscription_id_daily_forecast_refresh_interval_property_update.unwrap_or_else(|_| -1);
        

        // Create structure for method handlers.
        let method_handlers = WeatherForecastServerMethodHandlers {method_handler_for_refresh_daily_forecast: Arc::new(Mutex::new(Box::new( || { Err(MethodResultCode::ServerError) } ))),
            method_handler_for_refresh_hourly_forecast: Arc::new(Mutex::new(Box::new( || { Err(MethodResultCode::ServerError) } ))),
            method_handler_for_refresh_current_conditions: Arc::new(Mutex::new(Box::new( || { Err(MethodResultCode::ServerError) } ))),
            
        };

        // Create structure for subscription ids.
        let sub_ids = WeatherForecastServerSubscriptionIds {
            refresh_daily_forecast_method_req: subscription_id_refresh_daily_forecast_method_req,
            refresh_hourly_forecast_method_req: subscription_id_refresh_hourly_forecast_method_req,
            refresh_current_conditions_method_req: subscription_id_refresh_current_conditions_method_req,
            
            
            location_property_update: subscription_id_location_property_update,
            
            current_condition_refresh_interval_property_update: subscription_id_current_condition_refresh_interval_property_update,
            
            hourly_forecast_refresh_interval_property_update: subscription_id_hourly_forecast_refresh_interval_property_update,
            
            daily_forecast_refresh_interval_property_update: subscription_id_daily_forecast_refresh_interval_property_update,
            
        };

        
        let property_values = WeatherForecastProperties {
            location_topic: Arc::new(String::from("weather-forecast/property/location")),
            location: Arc::new(Mutex::new(None)),
            
            current_temperature_topic: Arc::new(String::from("weather-forecast/property/current_temperature")),
            
            current_temperature: Arc::new(Mutex::new(None)),
            current_condition_topic: Arc::new(String::from("weather-forecast/property/current_condition")),
            current_condition: Arc::new(Mutex::new(None)),
            
            daily_forecast_topic: Arc::new(String::from("weather-forecast/property/daily_forecast")),
            daily_forecast: Arc::new(Mutex::new(None)),
            
            hourly_forecast_topic: Arc::new(String::from("weather-forecast/property/hourly_forecast")),
            hourly_forecast: Arc::new(Mutex::new(None)),
            
            current_condition_refresh_interval_topic: Arc::new(String::from("weather-forecast/property/current_condition_refresh_interval")),
            
            current_condition_refresh_interval: Arc::new(Mutex::new(None)),
            hourly_forecast_refresh_interval_topic: Arc::new(String::from("weather-forecast/property/hourly_forecast_refresh_interval")),
            
            hourly_forecast_refresh_interval: Arc::new(Mutex::new(None)),
            daily_forecast_refresh_interval_topic: Arc::new(String::from("weather-forecast/property/daily_forecast_refresh_interval")),
            
            daily_forecast_refresh_interval: Arc::new(Mutex::new(None)),
        };
        

        WeatherForecastServer {

            msg_streamer_rx: Some(message_received_rx),
            msg_streamer_tx: message_received_tx,
            msg_publisher: publisher,
            method_handlers: method_handlers,
            properties: property_values,
            subscription_ids: sub_ids,
            client_id: connection.client_id.to_string(),
        }
    }

    pub async fn emit_current_time(&mut self, current_time: String) {
        let data = connection::payloads::CurrentTimeSignalPayload {
            
            current_time: current_time,
            
        };
        self.msg_publisher.publish_structure("weather-forecast/signal/current_time".to_string(), &data).await;
    }
    

    pub fn set_method_handler_for_refresh_daily_forecast(&mut self, cb: impl Fn()->Result<(), MethodResultCode> + 'static + Send) {
        self.method_handlers.method_handler_for_refresh_daily_forecast = Arc::new(Mutex::new(Box::new(cb)));
    }
    pub fn set_method_handler_for_refresh_hourly_forecast(&mut self, cb: impl Fn()->Result<(), MethodResultCode> + 'static + Send) {
        self.method_handlers.method_handler_for_refresh_hourly_forecast = Arc::new(Mutex::new(Box::new(cb)));
    }
    pub fn set_method_handler_for_refresh_current_conditions(&mut self, cb: impl Fn()->Result<(), MethodResultCode> + 'static + Send) {
        self.method_handlers.method_handler_for_refresh_current_conditions = Arc::new(Mutex::new(Box::new(cb)));
    }
    


    async fn handle_refresh_daily_forecast_request(publisher: &mut MessagePublisher, handlers: &mut WeatherForecastServerMethodHandlers, msg: mqtt::Message) {
        let props = msg.properties();
        let opt_corr_id_bin: Option<Vec<u8>> = props.get_binary(mqtt::PropertyCode::CorrelationData);
        let opt_resp_topic = props.get_string(mqtt::PropertyCode::ResponseTopic);
        let payload_str = msg.payload_str();
        let payload = serde_json::from_str::<RefreshDailyForecastRequestObject>(&payload_str).unwrap();

        // call the method handler
        let rv: () = {
            let func_guard = handlers.method_handler_for_refresh_daily_forecast.lock().unwrap();
            (*func_guard)().unwrap()
        };
        if let Some(resp_topic) = opt_resp_topic {
            publisher.publish_response_structure(resp_topic, &rv, opt_corr_id_bin).await.expect("Failed to publish response structure");
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }
    async fn handle_refresh_hourly_forecast_request(publisher: &mut MessagePublisher, handlers: &mut WeatherForecastServerMethodHandlers, msg: mqtt::Message) {
        let props = msg.properties();
        let opt_corr_id_bin: Option<Vec<u8>> = props.get_binary(mqtt::PropertyCode::CorrelationData);
        let opt_resp_topic = props.get_string(mqtt::PropertyCode::ResponseTopic);
        let payload_str = msg.payload_str();
        let payload = serde_json::from_str::<RefreshHourlyForecastRequestObject>(&payload_str).unwrap();

        // call the method handler
        let rv: () = {
            let func_guard = handlers.method_handler_for_refresh_hourly_forecast.lock().unwrap();
            (*func_guard)().unwrap()
        };
        if let Some(resp_topic) = opt_resp_topic {
            publisher.publish_response_structure(resp_topic, &rv, opt_corr_id_bin).await.expect("Failed to publish response structure");
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }
    async fn handle_refresh_current_conditions_request(publisher: &mut MessagePublisher, handlers: &mut WeatherForecastServerMethodHandlers, msg: mqtt::Message) {
        let props = msg.properties();
        let opt_corr_id_bin: Option<Vec<u8>> = props.get_binary(mqtt::PropertyCode::CorrelationData);
        let opt_resp_topic = props.get_string(mqtt::PropertyCode::ResponseTopic);
        let payload_str = msg.payload_str();
        let payload = serde_json::from_str::<RefreshCurrentConditionsRequestObject>(&payload_str).unwrap();

        // call the method handler
        let rv: () = {
            let func_guard = handlers.method_handler_for_refresh_current_conditions.lock().unwrap();
            (*func_guard)().unwrap()
        };
        if let Some(resp_topic) = opt_resp_topic {
            publisher.publish_response_structure(resp_topic, &rv, opt_corr_id_bin).await.expect("Failed to publish response structure");
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }
    
    async fn publish_location_value(mut publisher: MessagePublisher, topic: String, data: connection::payloads::LocationProperty)
    {
        let _pub_result = publisher.publish_structure(topic, &data).await;
        
    }
    
    async fn update_location_value(publisher: &mut MessagePublisher, topic: Arc<String>, data: Arc<Mutex<Option<connection::payloads::LocationProperty>>>, msg: mqtt::Message)
    {
        let payload_str = msg.payload_str();
        let new_data: LocationProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.clone());
        
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data;
        
        let _ = tokio::spawn(async move {
            WeatherForecastServer::publish_location_value(publisher2, topic2, data2).await;
        });
    }
    
    pub async fn set_location(&mut self, data: connection::payloads::LocationProperty) {
        println!("Setting location of type connection::payloads::LocationProperty");
        let prop = self.properties.location.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.location_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!("Will publish property location of type connection::payloads::LocationProperty to {}", topic2);
            WeatherForecastServer::publish_location_value(publisher2, topic2, data).await;
        });
    }
    
    async fn publish_current_temperature_value(mut publisher: MessagePublisher, topic: String, data: f32)
    {
        let new_data = CurrentTemperatureProperty {
            temperature_f: data,
        };
        let _pub_result = publisher.publish_structure(topic, &new_data).await;
        
    }
    
    pub async fn set_current_temperature(&mut self, data: f32) {
        println!("Setting current_temperature of type f32");
        let prop = self.properties.current_temperature.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.current_temperature_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!("Will publish property current_temperature of type f32 to {}", topic2);
            WeatherForecastServer::publish_current_temperature_value(publisher2, topic2, data).await;
        });
    }
    
    async fn publish_current_condition_value(mut publisher: MessagePublisher, topic: String, data: connection::payloads::CurrentConditionProperty)
    {
        let _pub_result = publisher.publish_structure(topic, &data).await;
        
    }
    
    pub async fn set_current_condition(&mut self, data: connection::payloads::CurrentConditionProperty) {
        println!("Setting current_condition of type connection::payloads::CurrentConditionProperty");
        let prop = self.properties.current_condition.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.current_condition_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!("Will publish property current_condition of type connection::payloads::CurrentConditionProperty to {}", topic2);
            WeatherForecastServer::publish_current_condition_value(publisher2, topic2, data).await;
        });
    }
    
    async fn publish_daily_forecast_value(mut publisher: MessagePublisher, topic: String, data: connection::payloads::DailyForecastProperty)
    {
        let _pub_result = publisher.publish_structure(topic, &data).await;
        
    }
    
    pub async fn set_daily_forecast(&mut self, data: connection::payloads::DailyForecastProperty) {
        println!("Setting daily_forecast of type connection::payloads::DailyForecastProperty");
        let prop = self.properties.daily_forecast.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.daily_forecast_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!("Will publish property daily_forecast of type connection::payloads::DailyForecastProperty to {}", topic2);
            WeatherForecastServer::publish_daily_forecast_value(publisher2, topic2, data).await;
        });
    }
    
    async fn publish_hourly_forecast_value(mut publisher: MessagePublisher, topic: String, data: connection::payloads::HourlyForecastProperty)
    {
        let _pub_result = publisher.publish_structure(topic, &data).await;
        
    }
    
    pub async fn set_hourly_forecast(&mut self, data: connection::payloads::HourlyForecastProperty) {
        println!("Setting hourly_forecast of type connection::payloads::HourlyForecastProperty");
        let prop = self.properties.hourly_forecast.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.hourly_forecast_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!("Will publish property hourly_forecast of type connection::payloads::HourlyForecastProperty to {}", topic2);
            WeatherForecastServer::publish_hourly_forecast_value(publisher2, topic2, data).await;
        });
    }
    
    async fn publish_current_condition_refresh_interval_value(mut publisher: MessagePublisher, topic: String, data: i32)
    {
        let new_data = CurrentConditionRefreshIntervalProperty {
            seconds: data,
        };
        let _pub_result = publisher.publish_structure(topic, &new_data).await;
        
    }
    
    async fn update_current_condition_refresh_interval_value(publisher: &mut MessagePublisher, topic: Arc<String>, data: Arc<Mutex<Option<i32>>>, msg: mqtt::Message)
    {
        let payload_str = msg.payload_str();
        let new_data: CurrentConditionRefreshIntervalProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.seconds);
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.seconds;
        let _ = tokio::spawn(async move {
            WeatherForecastServer::publish_current_condition_refresh_interval_value(publisher2, topic2, data2).await;
        });
    }
    
    pub async fn set_current_condition_refresh_interval(&mut self, data: i32) {
        println!("Setting current_condition_refresh_interval of type i32");
        let prop = self.properties.current_condition_refresh_interval.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.current_condition_refresh_interval_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!("Will publish property current_condition_refresh_interval of type i32 to {}", topic2);
            WeatherForecastServer::publish_current_condition_refresh_interval_value(publisher2, topic2, data).await;
        });
    }
    
    async fn publish_hourly_forecast_refresh_interval_value(mut publisher: MessagePublisher, topic: String, data: i32)
    {
        let new_data = HourlyForecastRefreshIntervalProperty {
            seconds: data,
        };
        let _pub_result = publisher.publish_structure(topic, &new_data).await;
        
    }
    
    async fn update_hourly_forecast_refresh_interval_value(publisher: &mut MessagePublisher, topic: Arc<String>, data: Arc<Mutex<Option<i32>>>, msg: mqtt::Message)
    {
        let payload_str = msg.payload_str();
        let new_data: HourlyForecastRefreshIntervalProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.seconds);
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.seconds;
        let _ = tokio::spawn(async move {
            WeatherForecastServer::publish_hourly_forecast_refresh_interval_value(publisher2, topic2, data2).await;
        });
    }
    
    pub async fn set_hourly_forecast_refresh_interval(&mut self, data: i32) {
        println!("Setting hourly_forecast_refresh_interval of type i32");
        let prop = self.properties.hourly_forecast_refresh_interval.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.hourly_forecast_refresh_interval_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!("Will publish property hourly_forecast_refresh_interval of type i32 to {}", topic2);
            WeatherForecastServer::publish_hourly_forecast_refresh_interval_value(publisher2, topic2, data).await;
        });
    }
    
    async fn publish_daily_forecast_refresh_interval_value(mut publisher: MessagePublisher, topic: String, data: i32)
    {
        let new_data = DailyForecastRefreshIntervalProperty {
            seconds: data,
        };
        let _pub_result = publisher.publish_structure(topic, &new_data).await;
        
    }
    
    async fn update_daily_forecast_refresh_interval_value(publisher: &mut MessagePublisher, topic: Arc<String>, data: Arc<Mutex<Option<i32>>>, msg: mqtt::Message)
    {
        let payload_str = msg.payload_str();
        let new_data: DailyForecastRefreshIntervalProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.seconds);
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.seconds;
        let _ = tokio::spawn(async move {
            WeatherForecastServer::publish_daily_forecast_refresh_interval_value(publisher2, topic2, data2).await;
        });
    }
    
    pub async fn set_daily_forecast_refresh_interval(&mut self, data: i32) {
        println!("Setting daily_forecast_refresh_interval of type i32");
        let prop = self.properties.daily_forecast_refresh_interval.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.daily_forecast_refresh_interval_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            println!("Will publish property daily_forecast_refresh_interval of type i32 to {}", topic2);
            WeatherForecastServer::publish_daily_forecast_refresh_interval_value(publisher2, topic2, data).await;
        });
    }
    

    /// Starts the tasks that process messages received.
    /// In the task, it loops over messages received from the rx side of the message_receiver channel.
    /// Based on the subscription id of the received message, it will call a function to handle the
    /// received message.
    pub async fn receive_loop(&mut self) -> Result<(), JoinError> {

        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = self.msg_streamer_rx.take().expect("msg_streamer_rx should be Some");
        let mut method_handlers = self.method_handlers.clone();
        let sub_ids = self.subscription_ids.clone();
        let mut publisher = self.msg_publisher.clone();
        let properties = self.properties.clone();
        
        let _loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                if msg.subscription_id == sub_ids.refresh_daily_forecast_method_req {
                    WeatherForecastServer::handle_refresh_daily_forecast_request(&mut publisher, &mut method_handlers, msg.message).await;
                }
                else if msg.subscription_id == sub_ids.refresh_hourly_forecast_method_req {
                    WeatherForecastServer::handle_refresh_hourly_forecast_request(&mut publisher, &mut method_handlers, msg.message).await;
                }
                else if msg.subscription_id == sub_ids.refresh_current_conditions_method_req {
                    WeatherForecastServer::handle_refresh_current_conditions_request(&mut publisher, &mut method_handlers, msg.message).await;
                }
                else if msg.subscription_id == sub_ids.location_property_update {
                    WeatherForecastServer::update_location_value(&mut publisher, properties.location_topic.clone(), properties.location.clone(), msg.message).await;
                }
                else if msg.subscription_id == sub_ids.current_condition_refresh_interval_property_update {
                    WeatherForecastServer::update_current_condition_refresh_interval_value(&mut publisher, properties.current_condition_refresh_interval_topic.clone(), properties.current_condition_refresh_interval.clone(), msg.message).await;
                }
                else if msg.subscription_id == sub_ids.hourly_forecast_refresh_interval_property_update {
                    WeatherForecastServer::update_hourly_forecast_refresh_interval_value(&mut publisher, properties.hourly_forecast_refresh_interval_topic.clone(), properties.hourly_forecast_refresh_interval.clone(), msg.message).await;
                }
                else if msg.subscription_id == sub_ids.daily_forecast_refresh_interval_property_update {
                    WeatherForecastServer::update_daily_forecast_refresh_interval_value(&mut publisher, properties.daily_forecast_refresh_interval_topic.clone(), properties.daily_forecast_refresh_interval.clone(), msg.message).await;
                }
            }   
        });

        println!("Started client receive task");
        Ok(())
    }
}