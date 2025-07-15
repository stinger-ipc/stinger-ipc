/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Example interface.
*/


use futures::{StreamExt};
use connection::Connection;

use json::{JsonValue, object};
use std::collections::HashMap;
use uuid::Uuid;
use connection::return_structs::MethodResultCode;


pub struct ExampleClient {
    connection: Connection,
    signal_recv_callback_for_today_is: Box<dyn FnMut(i32, connection::enums::DayOfTheWeek)->()>,
    
    pending_responses: HashMap::<Uuid, oneshot::Sender::<JsonValue>>,
}

impl ExampleClient {
    pub fn new(connection: Connection) -> ExampleClient {
        ExampleClient {
            connection: connection,
            signal_recv_callback_for_today_is: Box::new( |_1, _2| {} ),
            
            pending_responses: HashMap::new(),
        }
    }

    pub fn set_signal_recv_callbacks_for_today_is(&mut self, cb: impl FnMut(i32, connection::enums::DayOfTheWeek)->() + 'static) {
        self.signal_recv_callback_for_today_is = Box::new(cb);
        self.connection.subscribe(String::from("Example/signal/todayIs"), 2, Some(101));
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

    fn handle_add_numbers_response(&mut self, payload: String) {
        let payload_object = json::parse(&payload).unwrap();
        if !payload_object["correlationId"].is_null() {
            let correlation_id_str = payload_object["correlationId"].as_str().unwrap().into();
            let correlation_id = Uuid::parse_str(correlation_id_str).unwrap();
            let sender_opt = self.pending_responses.remove(&correlation_id);
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

    fn handle_do_something_response(&mut self, payload: String) {
        let payload_object = json::parse(&payload).unwrap();
        if !payload_object["correlationId"].is_null() {
            let correlation_id_str = payload_object["correlationId"].as_str().unwrap().into();
            let correlation_id = Uuid::parse_str(correlation_id_str).unwrap();
            let sender_opt = self.pending_responses.remove(&correlation_id);
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
                let topic = &msg.topic();
                let mut func_indexs: Vec<u32> = Vec::new();

                //for item in self.topic_matcher.matches(topic) {
                //    func_indexs.push(*item.1);
                //}
                for func_index in func_indexs.iter() {
                    if func_index >= &1234 {
                        let payload_object = json::parse(&msg.payload_str()).unwrap();
                        match func_index {
                            1235 => {
                                
                                let temp_day_of_month = payload_object["dayOfMonth"].as_i32().unwrap();
                                
                                
                                let temp_day_of_week = connection::enums::DayOfTheWeek::from_u32(payload_object["dayOfWeek"].as_u32().unwrap()).unwrap();
                                
                                
                                (self.signal_recv_callback_for_today_is)(temp_day_of_month, temp_day_of_week);
                            }
                            _ => ()
                        }
                    
                    } else {
                        match func_index {
                            1 => self.handle_add_numbers_response(msg.payload_str().to_string()),
                        
                            2 => self.handle_do_something_response(msg.payload_str().to_string()),
                        _ => ()
                        }
                    }
                }
            }
        }
    }
}