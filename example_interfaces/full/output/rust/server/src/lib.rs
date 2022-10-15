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
    topic_matcher: TopicMatcher::<Box<dyn Fn(std::string::String, std::string::String)>>,
}

impl ExampleServer {
    pub fn new(mut connection: Connection) -> ExampleServer {

        let interface_info = String::from(r#"{"name": "Example", "summary": "Example StingerAPI interface which demonstrates most features.", "title": "Fully Featured Example Interface", "version": "0.0.1"}"#);
        connection.publish("Example/interface".to_string(), interface_info, 1);

        let mut topic_matcher = TopicMatcher::<Box<dyn Fn(String, String)>>::new();
        topic_matcher.insert("Example/signal/todayIs", Box::new(Self::handle_today_is_request));
        

        ExampleServer{
            connection: connection,
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
    

    fn handle_today_is_request(_topic: String, payload: String) {
        let _payload_object = json::parse(&payload).unwrap();
    }
    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(msg) = opt_msg {
                //
                let topic = &msg.topic();
                for item in self.topic_matcher.matches(topic) {
                    (&item.1)(topic.to_string(),msg.payload_str().to_string());
                }
            }
        }
    }
}