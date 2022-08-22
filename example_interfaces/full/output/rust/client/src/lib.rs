/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Example interface.
*/

use futures::StreamExt;
use connection::Connection;

pub struct ExampleClient {
    connection: Connection,
    signal_recv_callback_for_today_is: Box<dyn FnMut(i32, connection::enums::DayOfTheWeek)->()>,
    
}

impl ExampleClient {
    pub fn new(connection: Connection) -> ExampleClient {

        ExampleClient {
            connection: connection,
            signal_recv_callback_for_today_is: Box::new( |_1, _2| {} ),
            
        }
    }

    pub fn set_signal_recv_callbacks_for_today_is(&mut self, cb: impl FnMut(i32, connection::enums::DayOfTheWeek)->() + 'static) {
        self.signal_recv_callback_for_today_is = Box::new(cb);
        self.connection.subscribe(String::from("Example/signal/todayIs"), 2);
    }
    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(msg) = opt_msg {
                let payload_object = json::parse(&msg.payload_str()).unwrap();
                if msg.topic() == "Example/signal/todayIs" {
                    
                    let temp_day_of_month = payload_object["dayOfMonth"].as_i32().unwrap();
                    
                    
                    let temp_day_of_week = connection::enums::DayOfTheWeek::from_u32(payload_object["dayOfWeek"].as_u32().unwrap());
                    
                    
                    (self.signal_recv_callback_for_today_is)(temp_day_of_month, temp_day_of_week);
                }
                
            }
        }
    }
}