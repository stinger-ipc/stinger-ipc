/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
*/

use futures::StreamExt;
use connection::Connection;

pub struct SignalOnlyClient {
    connection: Connection,
    signal_recv_callback_for_another_signal: Box<dyn FnMut(u32)->()>,
    
}

impl SignalOnlyClient {
    pub fn new(connection: Connection) -> SignalOnlyClient {

        SignalOnlyClient {
            connection: connection,
            signal_recv_callback_for_another_signal: Box::new( |_| {} ),
            
        }
    }

    pub fn set_signal_recv_callbacks_for_another_signal(&mut self, cb: impl FnMut(u32)->() + 'static) {
        self.signal_recv_callback_for_another_signal = Box::new(cb);
        self.connection.subscribe(String::from("SignalOnly/signal/anotherSignal"), 2);
    }
    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(msg) = opt_msg {
                if msg.topic() == "SignalOnly/signal/anotherSignal" {
                    (self.signal_recv_callback_for_another_signal)(1);
                }
                
            }
        }
    }
}