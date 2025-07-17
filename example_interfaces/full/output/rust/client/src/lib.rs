/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Example interface.
*/

extern crate paho_mqtt as mqtt;
use futures::{StreamExt};
use connection::Connection;

use json::{JsonValue, object};
use std::collections::HashMap;
use uuid::Uuid;
use connection::return_structs::MethodResultCode;




pub struct ExampleClient {
    connection: Connection,
    subsc_id_start: u32,
    signal_recv_callback_for_today_is: Box<dyn FnMut(i32, connection::enums::DayOfTheWeek)->()>,
    pending_responses: HashMap::<Uuid, oneshot::Sender::<JsonValue>>,
}

impl ExampleClient {
    pub fn new(connection: Connection) -> ExampleClient {
        let subsc_id_start = connection.get_subcr_id_range_start();
        connection.subscribe(String::from(format!("client/{}/Example/method/addNumbers/response", connection.client_id)), 2, Some(subsc_id_start+101));
        connection.subscribe(String::from(format!("client/{}/Example/method/doSomething/response", connection.client_id)), 2, Some(subsc_id_start+102));
        
        ExampleClient {
            connection: connection,
            subsc_id_start: subsc_id_start,
            signal_recv_callback_for_today_is: Box::new( |_1, _2| {} ),
            
            pending_responses: HashMap::new(),
        }
    }

    pub fn set_signal_recv_callbacks_for_today_is(&mut self, cb: impl FnMut(i32, connection::enums::DayOfTheWeek)->() + 'static) {
        self.signal_recv_callback_for_today_is = Box::new(cb);
        self.connection.subscribe(String::from("Example/signal/todayIs"), 2, Some(201));
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
        self.connection.publish("Example/method/addNumbers".to_string(), data_str, 2, None).await;
        let resp_obj = receiver.recv().unwrap();
        Ok(resp_obj["sum"].as_i32().unwrap())
    }

    fn handle_add_numbers_response(&mut self, payload: String, correlation_id_str: Option<String>) {
        let payload_object = json::parse(&payload).unwrap();
        if Some(correlation_id_str) {
            let corr_id = Uuid::parse_str(correlation_id_str).unwrap();
            let sender_opt = self.pending_responses.remove(&corr_id);
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
        self.connection.publish("Example/method/doSomething".to_string(), data_str, 2, None).await;
        let resp_obj = receiver.recv().unwrap();
        Ok(connection::return_structs::DoSomethingReturnValue { 
            
            label: resp_obj["label"].as_str().unwrap().to_string(),
        
            
            identifier: resp_obj["identifier"].as_i32().unwrap(),
        
            day: connection::enums::DayOfTheWeek::from_u32(resp_obj["day"].as_u32().unwrap()).unwrap(),
            
        })
    }

    fn handle_do_something_response(&mut self, payload: String, correlation_id_str: Option<String>) {
        let payload_object = json::parse(&payload).unwrap();
        if Some(correlation_id_str) {
            let corr_id = Uuid::parse_str(correlation_id_str).unwrap();
            let sender_opt = self.pending_responses.remove(&corr_id);
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
    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(msg) = opt_msg {
                let payload_str = msg.payload_str().to_string();
                let payload_object = json::parse(&payload_str).unwrap();
                let correlation_id = msg.properties().iter(mqtt::PropertyCode::CorrelationData).next().map(|p| p.get_string().unwrap().to_string());
                let prop_itr = msg.properties().iter(mqtt::PropertyCode::SubscriptionIdentifier);

                for subscription_identifier in prop_itr {
                    let subsc_id = subscription_identifier.get_u32().unwrap() - self.subsc_id_start;
                    match subsc_id {
                        101 => {
                            self.handle_add_numbers_response(msg.payload_str().to_string(), correlation_id);
                        }
                        
                        102 => {
                            self.handle_do_something_response(msg.payload_str().to_string(), correlation_id);
                        }
                        201 => {
                            
                            let temp_day_of_month = payload_object["dayOfMonth"].as_i32().unwrap();
                            
                            
                            let temp_day_of_week = connection::enums::DayOfTheWeek::from_u32(payload_object["dayOfWeek"].as_u32().unwrap()).unwrap();
                            
                            
                            (self.signal_recv_callback_for_today_is)(temp_day_of_month, temp_day_of_week);
                        }
                        _ => ()
                    }
                }
            
            }
        }
    }
}