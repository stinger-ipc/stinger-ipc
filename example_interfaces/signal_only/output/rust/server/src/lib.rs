/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.
*/

use futures::StreamExt;
use connection::Connection;
use json::object;

use paho_mqtt::topic_matcher::TopicMatcher;

pub struct SignalOnlyServer {
    connection: Connection,
    topic_matcher: TopicMatcher::<Box<dyn FnMut(std::string::String, std::string::String)>>,
}

impl SignalOnlyServer {
    pub fn new(mut connection: Connection) -> SignalOnlyServer {

        let interface_info = String::from(r#"{"name": "SignalOnly", "summary": "", "title": "SignalOnly", "version": "0.0.1"}"#);
        connection.publish("SignalOnly/interface".to_string(), interface_info, 1);

        let mut topic_matcher = TopicMatcher::<Box<dyn FnMut(String, String)>>::new();
        topic_matcher.insert("SignalOnly/signal/anotherSignal", Box::new(Self::handle_another_signal_request));
        

        SignalOnlyServer{
            connection: connection,
            topic_matcher: topic_matcher,
        }
    }

    pub fn emit_another_signal(&mut self, one: f32, two: bool, three: String) {
        let data = object!{ 
            one: one,
            
            two: two,
            
            three: three,
            
        };
        let data_str = json::stringify(data);
        self.connection.publish("SignalOnly/signal/anotherSignal".to_string(), data_str, 2);
    }
    

    fn handle_another_signal_request(_topic: String, _payload: String) {

    }
    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(msg) = opt_msg {
                //let payload_object = json::parse(&msg.payload_str()).unwrap();
                let topic = &msg.topic();
                if let Some(_box_fn) = self.topic_matcher.get(topic) {
                    println!("Matches");
                }
            }
        }
    }
}