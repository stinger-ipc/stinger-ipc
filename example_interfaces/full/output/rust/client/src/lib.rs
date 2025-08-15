/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Example interface.
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
struct ExampleSubscriptionIds {
    add_numbers_method_resp: i32,do_something_method_resp: i32,
    today_is_signal: Option<i32>,
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When ExampleClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct ExampleSignalChannels {
    today_is_sender: broadcast::Sender<TodayIsSignalPayload>,
    
}

/// This is the struct for our API client.
pub struct ExampleClient {
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
    subscription_ids: ExampleSubscriptionIds,

    /// Holds the channels used for sending signals to the application.
    signal_channels: ExampleSignalChannels,
    
    /// Copy of MQTT Client ID
    client_id: String,
}

impl ExampleClient {

    /// Creates a new ExampleClient that uses elements from the provided Connection object.
    pub async fn new(connection: &mut Connection) -> Self {
        let _ = connection.connect().await.expect("Could not connect to MQTT broker");

        // Create a channel for messages to get from the Connection object to this ExampleClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        // Create the publisher object.
        let publisher = connection.get_publisher();

        // Subscribe to all the topics needed for method responses.
        let topic_add_numbers_method_resp = format!("client/{}/Example/method/addNumbers/response", connection.client_id);
        let subscription_id_add_numbers_method_resp = connection.subscribe(&topic_add_numbers_method_resp, message_received_tx.clone()).await;
        let subscription_id_add_numbers_method_resp = subscription_id_add_numbers_method_resp.unwrap_or_else(|_| -1);
        let topic_do_something_method_resp = format!("client/{}/Example/method/doSomething/response", connection.client_id);
        let subscription_id_do_something_method_resp = connection.subscribe(&topic_do_something_method_resp, message_received_tx.clone()).await;
        let subscription_id_do_something_method_resp = subscription_id_do_something_method_resp.unwrap_or_else(|_| -1);
        

        // Subscribe to all the topics needed for signals.
        let topic_today_is_signal = "Example/signal/todayIs";
        let subscription_id_today_is_signal = connection.subscribe(&topic_today_is_signal, message_received_tx.clone()).await;
        let subscription_id_today_is_signal = subscription_id_today_is_signal.unwrap_or_else(|_| -1);
        

        // Create structure for subscription ids.
        let sub_ids = ExampleSubscriptionIds {
            add_numbers_method_resp: subscription_id_add_numbers_method_resp,
            do_something_method_resp: subscription_id_do_something_method_resp,
            today_is_signal: Some(subscription_id_today_is_signal),
            
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = ExampleSignalChannels {
            today_is_sender: broadcast::channel(64).0,
            
        };

        // Create ExampleClient structure.
        let inst = ExampleClient {
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

    /// Get the RX receiver side of the broadcast channel for the todayIs signal.
    /// The signal payload, `TodayIsSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_today_is_receiver(&self) -> broadcast::Receiver<TodayIsSignalPayload> {
        self.signal_channels.today_is_sender.subscribe()
    }
    

    /// The `addNumbers` method.
    /// Method arguments are packed into a AddNumbersRequestObject structure
    /// and published to the `Example/method/addNumbers` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn add_numbers(&mut self, first: i32, second: i32)->Result<i32, MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let data = connection::payloads::AddNumbersRequestObject {
            first: first,
            second: second,
        };
        let response_topic = format!("client/{}/Example/method/addNumbers/response", self.client_id);
        let _ = self.msg_publisher.publish_request_structure("Example/method/addNumbers".to_string(), &data, response_topic.as_str(), correlation_id).await;
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
                        Err(_) => ()
                    }
                },
                None => ()
            }
        }
    }
    /// The `doSomething` method.
    /// Method arguments are packed into a DoSomethingRequestObject structure
    /// and published to the `Example/method/doSomething` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn do_something(&mut self, a_string: String)->Result<connection::payloads::DoSomethingReturnValue, MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let data = connection::payloads::DoSomethingRequestObject {
            aString: a_string,
        };
        let response_topic = format!("client/{}/Example/method/doSomething/response", self.client_id);
        let _ = self.msg_publisher.publish_request_structure("Example/method/doSomething".to_string(), &data, response_topic.as_str(), correlation_id).await;
        let resp_obj = receiver.await.unwrap();
        Ok(connection::payloads::DoSomethingReturnValue { 
            
            label: resp_obj["label"].as_str().unwrap().to_string(),
        
            
            identifier: resp_obj["identifier"].as_i32().unwrap(),
        
            day: connection::payloads::DayOfTheWeek::from_u32(resp_obj["day"].as_u32().unwrap()).unwrap(),
            
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
                if msg.subscription_id == sub_ids.add_numbers_method_resp {
                    ExampleClient::handle_add_numbers_response(resp_map.clone(), msg.message.payload_str().to_string(), corr_id);
                }
                else if msg.subscription_id == sub_ids.do_something_method_resp {
                    ExampleClient::handle_do_something_response(resp_map.clone(), msg.message.payload_str().to_string(), corr_id);
                }
                if msg.subscription_id == sub_ids.today_is_signal.unwrap_or_default() {
                    let chan = sig_chans.today_is_sender.clone();
                    let pl: connection::payloads::TodayIsSignalPayload =  serde_json::from_str(&msg.message.payload_str()).expect("Failed to deserialize");
                    let _send_result = chan.send(pl);
                }
                
            }   
        });

        println!("Started client receive task");
        Ok(())
    }
}