/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Example interface.
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
struct ExampleServerSubscriptionIds {
    add_numbers_method_req: i32,
    do_something_method_req: i32,
    
    
    favorite_number_property_update: i32,
    
    favorite_foods_property_update: i32,
    
}

#[derive(Clone)]
struct ExampleServerMethodHandlers {
    /// Pointer to a function to handle the addNumbers method request.
    method_handler_for_add_numbers: Arc<Mutex<Box<dyn Fn(i32, i32, Option<i32>)->Result<i32, MethodResultCode> + Send>>>,
    /// Pointer to a function to handle the doSomething method request.
    method_handler_for_do_something: Arc<Mutex<Box<dyn Fn(String)->Result<connection::payloads::DoSomethingReturnValue, MethodResultCode> + Send>>>,
    
}

#[derive(Clone)]
struct ExampleProperties {
    favorite_number_topic: Arc<String>,
    favorite_number: Arc<Mutex<Option<i32>>>,
    favorite_foods_topic: Arc<String>,
    favorite_foods: Arc<Mutex<Option<connection::payloads::FavoriteFoodsProperty>>>,
}

pub struct ExampleServer {
    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Option<mpsc::Receiver<ReceivedMessage>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Through this MessagePublisher object, we can publish messages to MQTT.
    msg_publisher: MessagePublisher,

    /// Struct contains all the handlers for the various methods.
    method_handlers: ExampleServerMethodHandlers,
    
    /// Struct contains all the properties.
    properties: ExampleProperties,
    
    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: ExampleServerSubscriptionIds,

    /// Copy of MQTT Client ID
    client_id: String,
}

impl ExampleServer {
    pub async fn new(connection: &mut Connection) -> Self {
        let _ = connection.connect().await.expect("Could not connect to MQTT broker");

        //let interface_info = String::from(r#"{"name": "Example", "summary": "Example StingerAPI interface which demonstrates most features.", "title": "Fully Featured Example Interface", "version": "0.0.1"}"#);
        //connection.publish("Example/interface".to_string(), interface_info, 1).await;

        // Create a channel for messages to get from the Connection object to this ExampleClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        let publisher = connection.get_publisher();

        // Create method handler struct
        let subscription_id_add_numbers_method_req = connection.subscribe("Example/method/addNumbers", message_received_tx.clone()).await;
        let subscription_id_add_numbers_method_req = subscription_id_add_numbers_method_req.unwrap_or_else(|_| -1);
        let subscription_id_do_something_method_req = connection.subscribe("Example/method/doSomething", message_received_tx.clone()).await;
        let subscription_id_do_something_method_req = subscription_id_do_something_method_req.unwrap_or_else(|_| -1);
        

        
        let subscription_id_favorite_number_property_update = connection.subscribe("Example/property/favorite_number/set_value", message_received_tx.clone()).await;
        let subscription_id_favorite_number_property_update = subscription_id_favorite_number_property_update.unwrap_or_else(|_| -1);
        
        let subscription_id_favorite_foods_property_update = connection.subscribe("Example/property/favorite_foods/set_value", message_received_tx.clone()).await;
        let subscription_id_favorite_foods_property_update = subscription_id_favorite_foods_property_update.unwrap_or_else(|_| -1);
        

        // Create structure for method handlers.
        let method_handlers = ExampleServerMethodHandlers {method_handler_for_add_numbers: Arc::new(Mutex::new(Box::new( |_1, _2, _3| { Err(MethodResultCode::ServerError) } ))),
            method_handler_for_do_something: Arc::new(Mutex::new(Box::new( |_1| { Err(MethodResultCode::ServerError) } ))),
            
        };

        // Create structure for subscription ids.
        let sub_ids = ExampleServerSubscriptionIds {
            add_numbers_method_req: subscription_id_add_numbers_method_req,
            do_something_method_req: subscription_id_do_something_method_req,
            
            
            favorite_number_property_update: subscription_id_favorite_number_property_update,
            
            favorite_foods_property_update: subscription_id_favorite_foods_property_update,
            
        };

        
        let property_values = ExampleProperties {
            favorite_number_topic: Arc::new(String::from("Example/property/favorite_number")),
            
            favorite_number: Arc::new(Mutex::new(None)),
            favorite_foods_topic: Arc::new(String::from("Example/property/favorite_foods")),
            favorite_foods: Arc::new(Mutex::new(None)),
            
        };
        

        ExampleServer {

            msg_streamer_rx: Some(message_received_rx),
            msg_streamer_tx: message_received_tx,
            msg_publisher: publisher,
            method_handlers: method_handlers,
            properties: property_values,
            subscription_ids: sub_ids,
            client_id: connection.client_id.to_string(),
        }
    }

    pub async fn emit_today_is(&mut self, day_of_month: i32, day_of_week: Option<connection::payloads::DayOfTheWeek>) {
        let data = connection::payloads::TodayIsSignalPayload {
            
            dayOfMonth: day_of_month,
            
            dayOfWeek: day_of_week,
            
        };
        self.msg_publisher.publish_structure("Example/signal/todayIs".to_string(), &data).await;
    }
    

    pub fn set_method_handler_for_add_numbers(&mut self, cb: impl Fn(i32, i32, Option<i32>)->Result<i32, MethodResultCode> + 'static + Send) {
        self.method_handlers.method_handler_for_add_numbers = Arc::new(Mutex::new(Box::new(cb)));
    }
    pub fn set_method_handler_for_do_something(&mut self, cb: impl Fn(String)->Result<connection::payloads::DoSomethingReturnValue, MethodResultCode> + 'static + Send) {
        self.method_handlers.method_handler_for_do_something = Arc::new(Mutex::new(Box::new(cb)));
    }
    


    async fn handle_add_numbers_request(publisher: &mut MessagePublisher, handlers: &mut ExampleServerMethodHandlers, msg: mqtt::Message) {
        let props = msg.properties();
        let opt_corr_id_bin: Option<Vec<u8>> = props.get_binary(mqtt::PropertyCode::CorrelationData);
        let opt_resp_topic = props.get_string(mqtt::PropertyCode::ResponseTopic);
        let payload_str = msg.payload_str();
        let payload = serde_json::from_str::<AddNumbersRequestObject>(&payload_str).unwrap();

        // call the method handler
        let rv: i32 = {
            let func_guard = handlers.method_handler_for_add_numbers.lock().unwrap();
            (*func_guard)(payload.first, payload.second, payload.third).unwrap()
        };let rv = AddNumbersReturnValue {
            sum: rv,
        };
        
        if let Some(resp_topic) = opt_resp_topic {
            publisher.publish_response_structure(resp_topic, &rv, opt_corr_id_bin).await.expect("Failed to publish response structure");
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }
    async fn handle_do_something_request(publisher: &mut MessagePublisher, handlers: &mut ExampleServerMethodHandlers, msg: mqtt::Message) {
        let props = msg.properties();
        let opt_corr_id_bin: Option<Vec<u8>> = props.get_binary(mqtt::PropertyCode::CorrelationData);
        let opt_resp_topic = props.get_string(mqtt::PropertyCode::ResponseTopic);
        let payload_str = msg.payload_str();
        let payload = serde_json::from_str::<DoSomethingRequestObject>(&payload_str).unwrap();

        // call the method handler
        let rv: connection::payloads::DoSomethingReturnValue = {
            let func_guard = handlers.method_handler_for_do_something.lock().unwrap();
            (*func_guard)(payload.aString).unwrap()
        };
        if let Some(resp_topic) = opt_resp_topic {
            publisher.publish_response_structure(resp_topic, &rv, opt_corr_id_bin).await.expect("Failed to publish response structure");
        } else {
            eprintln!("No response topic found in message properties.");
        }
    }
    
    async fn publish_favorite_number_value(mut publisher: MessagePublisher, topic: String, data: i32)
    {
        let new_data = FavoriteNumberProperty {
            number: data,
        };
        let _pub_result = publisher.publish_structure(topic, &new_data);
        
    }
    
    async fn update_favorite_number_value(publisher: &mut MessagePublisher, topic: Arc<String>, data: Arc<Mutex<Option<i32>>>, msg: mqtt::Message)
    {
        let payload_str = msg.payload_str();
        let new_data: FavoriteNumberProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.number);
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data.number;
        let _ = tokio::spawn(async move {
            ExampleServer::publish_favorite_number_value(publisher2, topic2, data2).await;
        });
    }
    
    pub async fn set_favorite_number(&mut self, data: i32) {
        let prop = self.properties.favorite_number.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.favorite_number_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            ExampleServer::publish_favorite_number_value(publisher2, topic2, data).await;
        });
    }
    
    async fn publish_favorite_foods_value(mut publisher: MessagePublisher, topic: String, data: connection::payloads::FavoriteFoodsProperty)
    {
        let _pub_result = publisher.publish_structure(topic, &data);
        
    }
    
    async fn update_favorite_foods_value(publisher: &mut MessagePublisher, topic: Arc<String>, data: Arc<Mutex<Option<connection::payloads::FavoriteFoodsProperty>>>, msg: mqtt::Message)
    {
        let payload_str = msg.payload_str();
        let new_data: FavoriteFoodsProperty = serde_json::from_str(&payload_str).unwrap();
        let mut locked_data = data.lock().unwrap();
        *locked_data = Some(new_data.clone());
        
        let publisher2 = publisher.clone();
        let topic2: String = topic.as_ref().clone();
        let data2 = new_data;
        
        let _ = tokio::spawn(async move {
            ExampleServer::publish_favorite_foods_value(publisher2, topic2, data2).await;
        });
    }
    
    pub async fn set_favorite_foods(&mut self, data: connection::payloads::FavoriteFoodsProperty) {
        let prop = self.properties.favorite_foods.clone();
        {
            let mut locked_data = prop.lock().unwrap();
            *locked_data = Some(data.clone());
        }

        let publisher2 = self.msg_publisher.clone();
        let topic2 = self.properties.favorite_foods_topic.as_ref().clone();
        let _ = tokio::spawn(async move {
            ExampleServer::publish_favorite_foods_value(publisher2, topic2, data).await;
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
                if msg.subscription_id == sub_ids.add_numbers_method_req {
                    ExampleServer::handle_add_numbers_request(&mut publisher, &mut method_handlers, msg.message).await;
                }
                else if msg.subscription_id == sub_ids.do_something_method_req {
                    ExampleServer::handle_do_something_request(&mut publisher, &mut method_handlers, msg.message).await;
                }
                else if msg.subscription_id == sub_ids.favorite_number_property_update {
                    ExampleServer::update_favorite_number_value(&mut publisher, properties.favorite_number_topic.clone(), properties.favorite_number.clone(), msg.message).await;
                }
                else if msg.subscription_id == sub_ids.favorite_foods_property_update {
                    ExampleServer::update_favorite_foods_value(&mut publisher, properties.favorite_foods_topic.clone(), properties.favorite_foods.clone(), msg.message).await;
                }
            }   
        });

        println!("Started client receive task");
        Ok(())
    }
}