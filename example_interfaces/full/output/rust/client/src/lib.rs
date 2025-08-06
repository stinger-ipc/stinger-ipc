/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Example interface.
*/

extern crate paho_mqtt as mqtt;
use futures::{StreamExt};
use connection::{MessageStreamer, MessagePublisher, Connection, ReceivedMessage};

use json::{JsonValue, object};
use std::collections::HashMap;
use uuid::Uuid;
use connection::return_structs::MethodResultCode;

use std::io::Error;
use tokio::sync::mpsc::{self};
use tokio::time::{self, Duration};
use serde::Serialize;



pub struct ExampleClient {
    connection: Connection,
    signal_recv_callback_for_today_is: Box<dyn FnMut(i32, connection::enums::DayOfTheWeek)->()>,
    pending_responses: HashMap::<Uuid, oneshot::Sender::<JsonValue>>,
    msg_streamer_rx: Receiver<ReceivedMessage>,
    msg_streamer_tx: Sender<ReceivedMessage>,
    msg_publisher: MessagePublisher, 
}

impl ExampleClient {
    pub fn new(mut connection: Connection) -> ExampleClient {
        let (rcvr_tx: Sender<ReceivedMessage>, mut rcvr_rx: Receiver<ReceivedMessage>) = mpsc.channel(64);
        let publihser = connection.get_publisher()
        connection.subscribe(String::from(format!("client/{}/Example/method/addNumbers/response", connection.client_id)), rcvr_tx.clone());
        connection.subscribe(String::from(format!("client/{}/Example/method/doSomething/response", connection.client_id)), rcvr_tx.clone());
        
        
        let inst = ExampleClient {
            connection: connection,
            subsc_id_start: subsc_id_start,
            signal_recv_callback_for_today_is: Box::new( |_1, _2| {} ),
            
            pending_responses: HashMap::new(),
            msg_streamer_rx: rcvr_rx,
            msg_streamer_tx: rcvr_tx,
            msg_publisher: publisher,
        };
        inst
    }

    pub fn set_signal_recv_callbacks_for_today_is(&mut self, cb: impl FnMut(i32, connection::enums::DayOfTheWeek)->() + 'static) {
        self.signal_recv_callback_for_today_is = Box::new(cb);
        self.connection.subscribe(String::from("Example/signal/todayIs"), self.msg_streamer_tx.clone());
    }
    

    pub async fn add_numbers(&mut self, first: i32, second: i32)->Result<i32, MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        let correlation_id_str = format!("{}", correlation_id);
        self.pending_responses.insert(correlation_id, sender);
        let data = object!{
            correlationId: correlation_id_str,
            clientId: self.connection.client_id.clone(),
            first: first,
            
            second: second,
            
        };
        let data_str = json::stringify(data);
        let _ = self.connection.publish("Example/method/addNumbers".to_string(), data_str, 2, None).await;
        let resp_obj = receiver.recv().unwrap();
        Ok(resp_obj["sum"].as_i32().unwrap())
    }

    fn handle_add_numbers_response(&mut self, payload: String, opt_correlation_id: &Option<String>) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.as_ref()
                .and_then(|cid| Uuid::parse_str(cid.as_str()).ok())
                .and_then(|uuid| self.pending_responses.remove(&uuid));
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
    pub async fn do_something(&mut self, a_string: String)->Result<connection::return_structs::DoSomethingReturnValue, MethodResultCode> {
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        let correlation_id_str = format!("{}", correlation_id);
        self.pending_responses.insert(correlation_id, sender);
        let data = object!{
            correlationId: correlation_id_str,
            clientId: self.connection.client_id.clone(),
            aString: a_string,
            
        };
        let data_str = json::stringify(data);
        let _ = self.connection.publish("Example/method/doSomething".to_string(), data_str, 2, None).await;
        let resp_obj = receiver.recv().unwrap();
        Ok(connection::return_structs::DoSomethingReturnValue { 
            
            label: resp_obj["label"].as_str().unwrap().to_string(),
        
            
            identifier: resp_obj["identifier"].as_i32().unwrap(),
        
            day: connection::enums::DayOfTheWeek::from_u32(resp_obj["day"].as_u32().unwrap()).unwrap(),
            
        })
    }

    fn handle_do_something_response(&mut self, payload: String, opt_correlation_id: &Option<String>) {
        let payload_object = json::parse(&payload).unwrap();
        if opt_correlation_id.is_some() {
            let sender_opt = opt_correlation_id.as_ref()
                .and_then(|cid| Uuid::parse_str(cid.as_str()).ok())
                .and_then(|uuid| self.pending_responses.remove(&uuid));
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
    



}