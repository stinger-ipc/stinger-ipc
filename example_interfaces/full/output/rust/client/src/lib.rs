/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.
*/

use mqttier::{MqttierClient, ReceivedMessage};
use std::collections::HashMap;
use json::JsonValue;
use uuid::Uuid;
use serde_json;


#[allow(unused_imports)]
use full_types::{MethodResultCode, *};

use std::sync::{Arc, Mutex};
use tokio::sync::{broadcast, mpsc, oneshot};
use tokio::task::JoinError;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct FullSubscriptionIds {
    add_numbers_method_resp: usize,
    do_something_method_resp: usize,
    
    today_is_signal: Option<usize>,
    favorite_number_property_value: usize,
    favorite_foods_property_value: usize,
    lunch_menu_property_value: usize,
    
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When FullClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct FullSignalChannels {
    today_is_sender: broadcast::Sender<TodayIsSignalPayload>,
    
}


#[derive(Clone)]
pub struct FullProperties {
    
    pub favorite_number: Arc<Mutex<Option<i32>>>,
    
    pub favorite_foods: Arc<Mutex<Option<FavoriteFoodsProperty>>>,
    pub lunch_menu: Arc<Mutex<Option<LunchMenuProperty>>>,
}


/// This is the struct for our API client.
#[derive(Clone)]
pub struct FullClient {
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
    pub properties: FullProperties,
    
    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: FullSubscriptionIds,
    /// Holds the channels used for sending signals to the application.
    signal_channels: FullSignalChannels,
    
    /// Copy of MQTT Client ID
    pub client_id: String,
}

impl FullClient {

    /// Creates a new FullClient that uses an MqttierClient.
    pub async fn new(connection: &mut MqttierClient) -> Self {

        // Create a channel for messages to get from the Connection object to this FullClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        let topic_add_numbers_method_resp = format!("client/{}/full/method/addNumbers/response", connection.client_id);
        let subscription_id_add_numbers_method_resp = connection.subscribe(topic_add_numbers_method_resp, 2, message_received_tx.clone()).await;
        let subscription_id_add_numbers_method_resp = subscription_id_add_numbers_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_do_something_method_resp = format!("client/{}/full/method/doSomething/response", connection.client_id);
        let subscription_id_do_something_method_resp = connection.subscribe(topic_do_something_method_resp, 2, message_received_tx.clone()).await;
        let subscription_id_do_something_method_resp = subscription_id_do_something_method_resp.unwrap_or_else(|_| usize::MAX);
        

        // Subscribe to all the topics needed for signals.
        let topic_today_is_signal = "full/signal/todayIs".to_string();
        let subscription_id_today_is_signal = connection.subscribe(topic_today_is_signal, 2, message_received_tx.clone()).await;
        let subscription_id_today_is_signal = subscription_id_today_is_signal.unwrap_or_else(|_| usize::MAX);
        

        // Subscribe to all the topics needed for properties.
        
        let topic_favorite_number_property_value = "full/property/favoriteNumber/value".to_string();
        let subscription_id_favorite_number_property_value = connection.subscribe(topic_favorite_number_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_favorite_number_property_value = subscription_id_favorite_number_property_value.unwrap_or_else(|_| usize::MAX);
        
        let topic_favorite_foods_property_value = "full/property/favoriteFoods/value".to_string();
        let subscription_id_favorite_foods_property_value = connection.subscribe(topic_favorite_foods_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_favorite_foods_property_value = subscription_id_favorite_foods_property_value.unwrap_or_else(|_| usize::MAX);
        
        let topic_lunch_menu_property_value = "full/property/lunchMenu/value".to_string();
        let subscription_id_lunch_menu_property_value = connection.subscribe(topic_lunch_menu_property_value, 1, message_received_tx.clone()).await;
        let subscription_id_lunch_menu_property_value = subscription_id_lunch_menu_property_value.unwrap_or_else(|_| usize::MAX);
        

        
        let property_values = FullProperties {
            
            favorite_number: Arc::new(Mutex::new(None)),
            favorite_foods: Arc::new(Mutex::new(None)),
            
            lunch_menu: Arc::new(Mutex::new(None)),
            
        };
        
        // Create structure for subscription ids.
        let sub_ids = FullSubscriptionIds {
            add_numbers_method_resp: subscription_id_add_numbers_method_resp,
            do_something_method_resp: subscription_id_do_something_method_resp,
            today_is_signal: Some(subscription_id_today_is_signal),
            favorite_number_property_value: subscription_id_favorite_number_property_value,
            favorite_foods_property_value: subscription_id_favorite_foods_property_value,
            lunch_menu_property_value: subscription_id_lunch_menu_property_value,
            
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = FullSignalChannels {
            today_is_sender: broadcast::channel(64).0,
            
        };

        // Create FullClient structure.
        let inst = FullClient {
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

    /// Get the RX receiver side of the broadcast channel for the todayIs signal.
    /// The signal payload, `TodayIsSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_today_is_receiver(&self) -> broadcast::Receiver<TodayIsSignalPayload> {
        self.signal_channels.today_is_sender.subscribe()
    }
    

    /// The `addNumbers` method.
    /// Method arguments are packed into a AddNumbersRequestObject structure
    /// and published to the `full/method/addNumbers` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn add_numbers(&mut self, first: i32, second: i32, third: Option<i32>)->Result<i32, MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = AddNumbersRequestObject {
            first: first,
            second: second,
            third: third,
        };

        let response_topic: String = format!("client/{}/full/method/addNumbers/response", self.client_id);
        let _ = self.mqttier_client.publish_request("full/method/addNumbers".to_string(), &data, response_topic, correlation_data).await;
        let resp_obj = receiver.await.unwrap();
        Ok(resp_obj["sum"].as_i32().unwrap())
    }

    /// Handler for responses to `addNumbers` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_add_numbers_response(pending_responses: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>>, payload: String, opt_correlation_id: Option<Uuid>) {
        
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
    /// The `doSomething` method.
    /// Method arguments are packed into a DoSomethingRequestObject structure
    /// and published to the `full/method/doSomething` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn do_something(&mut self, a_string: String)->Result<DoSomethingReturnValue, MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = DoSomethingRequestObject {
            aString: a_string,
        };

        let response_topic: String = format!("client/{}/full/method/doSomething/response", self.client_id);
        let _ = self.mqttier_client.publish_request("full/method/doSomething".to_string(), &data, response_topic, correlation_data).await;
        let resp_obj = receiver.await.unwrap();
        Ok(DoSomethingReturnValue {
            
            label: resp_obj["label"].as_str().unwrap().to_string(),
        
            
            identifier: resp_obj["identifier"].as_i32().unwrap(),
        
            day: DayOfTheWeek::from_u32(resp_obj["day"].as_u32().unwrap()).unwrap(),
            
        })
        
    }

    /// Handler for responses to `doSomething` method calls.
    /// It finds oneshot channel created for the method call, and sends the response to that channel.
    fn handle_do_something_response(pending_responses: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>>, payload: String, opt_correlation_id: Option<Uuid>) {
        
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
                if msg.subscription_id == sub_ids.add_numbers_method_resp {
                    FullClient::handle_add_numbers_response(resp_map.clone(), payload, opt_corr_id);
                }
                else if msg.subscription_id == sub_ids.do_something_method_resp {
                    FullClient::handle_do_something_response(resp_map.clone(), payload, opt_corr_id);
                }
                
                if msg.subscription_id == sub_ids.today_is_signal.unwrap_or_default() {
                    let chan = sig_chans.today_is_sender.clone();
                    let pl: TodayIsSignalPayload =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let _send_result = chan.send(pl);
                }
                
                if msg.subscription_id == sub_ids.favorite_number_property_value {
                    let pl: i32 =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.favorite_number.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
                else if msg.subscription_id == sub_ids.favorite_foods_property_value {
                    let pl: FavoriteFoodsProperty =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.favorite_foods.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
                else if msg.subscription_id == sub_ids.lunch_menu_property_value {
                    let pl: LunchMenuProperty =  serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let mut guard = props.lunch_menu.lock().expect("Mutex was poisoned");
                    *guard = Some(pl);
                }
                
            }   
        });

        println!("Started client receive task");
        Ok(())
    }
}