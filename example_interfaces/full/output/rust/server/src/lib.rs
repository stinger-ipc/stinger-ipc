/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Example interface.
*/

use futures::StreamExt;
use connection::Connection;
use connection::return_structs::MethodResultCode;
use json::object;

use paho_mqtt::topic_matcher::TopicMatcher;

pub struct ExampleServer {
    connection: Connection,
    method_handler_for_add_numbers: Box<dyn FnMut(i32, i32)->Result<i32, MethodResultCode>>,
    method_handler_for_do_something: Box<dyn FnMut(String)->Result<connection::return_structs::DoSomethingReturnValue, MethodResultCode>>,
    
    topic_matcher: TopicMatcher::<u32>,
}

impl ExampleServer {
    pub async fn new(mut connection: Connection) -> ExampleServer {

        let interface_info = String::from(r#"{"name": "Example", "summary": "Example StingerAPI interface which demonstrates most features.", "title": "Fully Featured Example Interface", "version": "0.0.1"}"#);
        connection.publish("Example/interface".to_string(), interface_info, 1).await;

        let mut topic_matcher = TopicMatcher::<u32>::new();
        topic_matcher.insert("Example/method/addNumbers", 1);
        topic_matcher.insert("Example/method/doSomething", 2);
        

        ExampleServer {
            connection: connection,
            method_handler_for_add_numbers: Box::new( |_1, _2| { Err(MethodResultCode::ServerError) } ),
            method_handler_for_do_something: Box::new( |_1| { Err(MethodResultCode::ServerError) } ),
            
            topic_matcher: topic_matcher,
        }
    }

    pub async fn emit_today_is(&mut self, day_of_month: i32, day_of_week: connection::enums::DayOfTheWeek) {
        let data = object!{ 
            dayOfMonth: day_of_month,
            
            dayOfWeek: day_of_week as u32,
            
        };
        let data_str = json::stringify(data);
        self.connection.publish("Example/signal/todayIs".to_string(), data_str, 2).await;
    }
    

    pub fn set_method_handler_for_add_numbers(&mut self, cb: impl FnMut(i32, i32)->Result<i32, MethodResultCode> + 'static) {
        self.method_handler_for_add_numbers = Box::new(cb);
        self.connection.subscribe(String::from("Example/method/addNumbers"), 2);
    }
    pub fn set_method_handler_for_do_something(&mut self, cb: impl FnMut(String)->Result<connection::return_structs::DoSomethingReturnValue, MethodResultCode> + 'static) {
        self.method_handler_for_do_something = Box::new(cb);
        self.connection.subscribe(String::from("Example/method/doSomething"), 2);
    }
    

    async fn handle_add_numbers_request(&mut self, _topic: String, payload: String) {
        let payload_object = json::parse(&payload).unwrap();
        
        let temp_first = payload_object["first"].as_i32().unwrap();
        
        
        let temp_second = payload_object["second"].as_i32().unwrap();
        
        
        let rv = (self.method_handler_for_add_numbers)(temp_first, temp_second);
        if !payload_object["clientId"].is_null() {
            let mut response_json = json::JsonValue::new_object();
            if !payload_object["correlationId"].is_null() {
                response_json["correlationId"] = payload_object["correlationId"].as_str().unwrap().into();
            }
            match rv {
                Ok(return_value) => {
                    response_json["result"] = 0.into();
                    
                    response_json["sum"] = return_value.into();
                }
                Err(result_code) => {
                    response_json["result"] = (result_code as u32).into();
                }
            }
            let response_topic = format!("client/{}/Example/method/addNumbers/response", payload_object["clientId"].as_str().unwrap());
            self.connection.publish(response_topic, json::stringify(response_json), 2).await;
        }
    }
    async fn handle_do_something_request(&mut self, _topic: String, payload: String) {
        let payload_object = json::parse(&payload).unwrap();
        
        let temp_a_string = payload_object["aString"].as_str().unwrap().to_string();
        
        
        let rv = (self.method_handler_for_do_something)(temp_a_string);
        if !payload_object["clientId"].is_null() {
            let mut response_json = json::JsonValue::new_object();
            if !payload_object["correlationId"].is_null() {
                response_json["correlationId"] = payload_object["correlationId"].as_str().unwrap().into();
            }
            match rv {
                Ok(return_value) => {
                    response_json["result"] = 0.into();
                    
                    response_json["label"] = return_value.label.into();
                    response_json["identifier"] = return_value.identifier.into();
                    response_json["day"] = (return_value.day as u32).into();
                }
                Err(result_code) => {
                    response_json["result"] = (result_code as u32).into();
                }
            }
            let response_topic = format!("client/{}/Example/method/doSomething/response", payload_object["clientId"].as_str().unwrap());
            self.connection.publish(response_topic, json::stringify(response_json), 2).await;
        }
    }
    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(msg) = opt_msg {
                let topic = &msg.topic();
                let mut func_indexs: Vec<u32> = Vec::new();
                for item in self.topic_matcher.matches(topic) {
                    func_indexs.push(item.1);
                }
                for func_index in func_indexs.iter() {
                    match func_index {
                        1 => self.handle_add_numbers_request(topic.to_string(), msg.payload_str().to_string()).await,
                    
                        2 => self.handle_do_something_request(topic.to_string(), msg.payload_str().to_string()).await,
                    _ => ()
                    }
                }
            }
        }
    }
}