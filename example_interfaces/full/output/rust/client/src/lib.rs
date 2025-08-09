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

#[derive(Clone, Debug)]
struct ExampleSubscriptionIds {
    add_numbers_method: i32,do_something_method: i32,
    today_is_signal: Option<i32>,
}

#[derive(Clone)]
struct ExampleSignalChannels {
    today_is_sender: broadcast::Sender<TodayIsSignalPayload>,
    
}

pub struct ExampleClient {
    connection: Connection,pending_responses: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>>,
    msg_streamer_rx: Option<mpsc::Receiver<ReceivedMessage>>,
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,
    msg_publisher: MessagePublisher,
    subscription_ids: ExampleSubscriptionIds,
    signal_channels: ExampleSignalChannels,
}

impl ExampleClient {
    pub async fn new(mut connection: Connection) -> ExampleClient {
        let _ = connection.connect().await;
        let (rcvr_tx, rcvr_rx) = mpsc::channel(64);
        let publisher = connection.get_publisher();
        let topic_add_numbers_method = format!("client/{}/Example/method/addNumbers/response", connection.client_id);
        let subscription_id_add_numbers_method = connection.subscribe(&topic_add_numbers_method, rcvr_tx.clone()).await;
        let subscription_id_add_numbers_method = subscription_id_add_numbers_method.unwrap_or_else(|_| -1);
        let topic_do_something_method = format!("client/{}/Example/method/doSomething/response", connection.client_id);
        let subscription_id_do_something_method = connection.subscribe(&topic_do_something_method, rcvr_tx.clone()).await;
        let subscription_id_do_something_method = subscription_id_do_something_method.unwrap_or_else(|_| -1);
        
        // Signal subscriptions here are temporary.  Eventually, we'll subscribe when registering the callback.
        let topic_today_is_signal = "Example/signal/todayIs";
        let subscription_id_today_is_signal = connection.subscribe(&topic_today_is_signal, rcvr_tx.clone()).await;
        let subscription_id_today_is_signal = subscription_id_today_is_signal.unwrap_or_else(|_| -1);
        
        let sub_ids = ExampleSubscriptionIds {
            add_numbers_method: subscription_id_add_numbers_method,
            do_something_method: subscription_id_do_something_method,
            
            today_is_signal: Some(subscription_id_today_is_signal),
            
        };
        let signal_channels = ExampleSignalChannels {
            today_is_sender: broadcast::channel(64).0,
            
        };
        let inst = ExampleClient {
            connection: connection,
            pending_responses: Arc::new(Mutex::new(HashMap::new())),
            msg_streamer_rx: Some(rcvr_rx),
            msg_streamer_tx: rcvr_tx,
            msg_publisher: publisher,
            subscription_ids: sub_ids,
            signal_channels: signal_channels,
        };
        inst
    }

    pub fn get_today_is_receiver(&self) -> broadcast::Receiver<TodayIsSignalPayload> {
        self.signal_channels.today_is_sender.subscribe()
    }
    

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
        let _ = self.msg_publisher.publish_request_structure("Example/method/addNumbers".to_string(), &data, "", correlation_id).await;
        let resp_obj = receiver.await.unwrap();
        Ok(resp_obj["sum"].as_i32().unwrap())
    }

    fn handle_add_numbers_response(pending_responses: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>>, payload: String, opt_correlation_id: Option<String>) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.as_ref()
                .and_then(|cid| Uuid::parse_str(cid.as_str()).ok())
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
        let _ = self.msg_publisher.publish_request_structure("Example/method/doSomething".to_string(), &data, "", correlation_id).await;
        let resp_obj = receiver.await.unwrap();
        Ok(connection::payloads::DoSomethingReturnValue { 
            
            label: resp_obj["label"].as_str().unwrap().to_string(),
        
            
            identifier: resp_obj["identifier"].as_i32().unwrap(),
        
            day: connection::payloads::DayOfTheWeek::from_u32(resp_obj["day"].as_u32().unwrap()).unwrap(),
            
        })
    }

    fn handle_do_something_response(pending_responses: Arc<Mutex<HashMap::<Uuid, oneshot::Sender::<JsonValue>>>>, payload: String, opt_correlation_id: Option<String>) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.as_ref()
                .and_then(|cid| Uuid::parse_str(cid.as_str()).ok())
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
    

    pub async fn process_loop(&mut self) {
        let resp_map = self.pending_responses.clone();
        let mut receiver = self.msg_streamer_rx.take().expect("msg_streamer_rx should be Some");
        let mut streamer = self.connection.get_streamer().await;
        let sig_chans = self.signal_channels.clone();
        let task1 = tokio::spawn(async move {
            streamer.receive_loop().await;
        });

        let sub_ids = self.subscription_ids.clone();
        let task2 = tokio::spawn(async move {
            while let Some(msg) = receiver.recv().await {
                println!("Received mqtt message: {:?} against subscription id {}", msg.message.payload_str(), msg.subscription_id);
                println!("Our subscriptions are: {:?}", sub_ids);
                if msg.subscription_id == sub_ids.add_numbers_method {
                    println!("Found subscription match for {}({:?}) as a response to addNumbers", msg.message.topic(), sub_ids.add_numbers_method);
                    ExampleClient::handle_add_numbers_response(resp_map.clone(), msg.message.payload_str().to_string(), None);
                }
                else if msg.subscription_id == sub_ids.do_something_method {
                    println!("Found subscription match for {}({:?}) as a response to doSomething", msg.message.topic(), sub_ids.do_something_method);
                    ExampleClient::handle_do_something_response(resp_map.clone(), msg.message.payload_str().to_string(), None);
                }
                if msg.subscription_id == sub_ids.today_is_signal.unwrap_or_default() {
                    println!("Found subscription match for {}({:?}) as a todayIs signal", msg.message.topic(), sub_ids.today_is_signal);
                    let chan = sig_chans.today_is_sender.clone();
                    let pl: connection::payloads::TodayIsSignalPayload =  serde_json::from_str(&msg.message.payload_str()).expect("Failed to deserialize");
                    let send_result = chan.send(pl);
                    println!("Sent todayIs signal with payload: {:?}", msg.message.payload_str());
                }
                
            }   
        });

        task1.await;
        task2.await;
    }
}