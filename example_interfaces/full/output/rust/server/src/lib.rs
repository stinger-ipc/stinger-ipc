/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Example interface.
*/

use futures::StreamExt;
use connection::Connection;
use json::object;

use paho_mqtt::topic_matcher::TopicMatcher;

pub struct ExampleServer {
    connection: Connection,
    method_handler_for_add_numbers: Box<dyn FnMut(i32, i32)->()>,
    method_handler_for_do_something: Box<dyn FnMut(String)->()>,
    
    topic_matcher: TopicMatcher::<u32>,
}

impl ExampleServer {
    pub fn new(mut connection: Connection) -> ExampleServer {

        let interface_info = String::from(r#"{"name": "Example", "summary": "Example StingerAPI interface which demonstrates most features.", "title": "Fully Featured Example Interface", "version": "0.0.1"}"#);
        connection.publish("Example/interface".to_string(), interface_info, 1);

        let mut topic_matcher = TopicMatcher::<u32>::new();
        topic_matcher.insert("Example/method/addNumbers", 1);
        topic_matcher.insert("Example/method/doSomething", 2);
        

        ExampleServer {
            connection: connection,
            method_handler_for_add_numbers: Box::new( |_1, _2| {} ),
            method_handler_for_do_something: Box::new( |_1| {} ),
            
            topic_matcher: topic_matcher,
        }
    }

    pub fn emit_today_is(&mut self, day_of_month: i32, day_of_week: connection::enums::DayOfTheWeek) {
        let data = object!{ 
            dayOfMonth: day_of_month,
            
            dayOfWeek: day_of_week as u32,
            
        };
        let data_str = json::stringify(data);
        self.connection.publish("Example/signal/todayIs".to_string(), data_str, 2);
    }
    

    pub fn set_method_handler_for_add_numbers(&mut self, cb: impl FnMut(i32, i32)->() + 'static) {
        self.method_handler_for_add_numbers = Box::new(cb);
        self.connection.subscribe(String::from("Example/method/addNumbers"), 2);
    }
    pub fn set_method_handler_for_do_something(&mut self, cb: impl FnMut(String)->() + 'static) {
        self.method_handler_for_do_something = Box::new(cb);
        self.connection.subscribe(String::from("Example/method/doSomething"), 2);
    }
    

    fn handle_add_numbers_request(&mut self, _topic: String, payload: String) {
        let payload_object = json::parse(&payload).unwrap();
        
        let temp_first = payload_object["first"].as_i32().unwrap();
        
        
        let temp_second = payload_object["second"].as_i32().unwrap();
        
        
        (self.method_handler_for_add_numbers)(temp_first, temp_second);
    }
    fn handle_do_something_request(&mut self, _topic: String, payload: String) {
        let payload_object = json::parse(&payload).unwrap();
        
        let temp_a_string = payload_object["aString"].as_str().unwrap().to_string();
        
        
        (self.method_handler_for_do_something)(temp_a_string);
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
                        1 => self.handle_add_numbers_request(topic.to_string(), msg.payload_str().to_string()),
                    
                        2 => self.handle_do_something_request(topic.to_string(), msg.payload_str().to_string()),
                    _ => ()
                    }
                }
            }
        }
    }
}