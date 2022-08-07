/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Example interface.
*/

use futures::StreamExt;
use connection::Connection;

pub struct ExampleClient {
    connection: Connection,
    signal_recv_callback_for_today_is: Box<dyn FnMut(u32)->()>,
    
}

impl ExampleClient {
    pub fn new(connection: Connection) -> ExampleClient {

        ExampleClient {
            connection: connection,
            signal_recv_callback_for_today_is: Box::new( |_| {} ),
            
        }
    }

    pub fn set_signal_recv_callbacks_for_today_is(&mut self, cb: impl FnMut(u32)->() + 'static) {
        self.signal_recv_callback_for_today_is = Box::new(cb);
        self.connection.subscribe(String::from("Example/signal/todayIs"), 2);
    }
    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(msg) = opt_msg {
                if msg.topic() == "Example/signal/todayIs" {
                    (self.signal_recv_callback_for_today_is)(1);
                }
                
            }
        }
    }
}