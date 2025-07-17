/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
*/

extern crate paho_mqtt as mqtt;
use futures::{StreamExt};
use connection::Connection;


pub struct SignalOnlyClient {
    connection: Connection,
    subsc_id_start: u32,
    signal_recv_callback_for_another_signal: Box<dyn FnMut(f32, bool, String)->()>,
    
}

impl SignalOnlyClient {
    pub fn new(mut connection: Connection) -> SignalOnlyClient {
        let subsc_id_start = connection.get_subcr_id_range_start();
        
        SignalOnlyClient {
            connection: connection,
            subsc_id_start: subsc_id_start,
            signal_recv_callback_for_another_signal: Box::new( |_1, _2, _3| {} ),
            
            
        }
    }

    pub fn set_signal_recv_callbacks_for_another_signal(&mut self, cb: impl FnMut(f32, bool, String)->() + 'static) {
        self.signal_recv_callback_for_another_signal = Box::new(cb);
        self.connection.subscribe(String::from("SignalOnly/signal/anotherSignal"), 2, Some(201));
    }
    

    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(msg) = opt_msg {
                let payload_str = msg.payload_str().to_string();
                let payload_object = json::parse(&payload_str).unwrap();
                
                let prop_itr = msg.properties().iter(mqtt::PropertyCode::SubscriptionIdentifier);

                for subscription_identifier in prop_itr {
                    let subsc_id = subscription_identifier.get_u32().unwrap() - self.subsc_id_start;
                    match subsc_id {201 => {
                            
                            let temp_one = payload_object["one"].as_f32().unwrap();
                            
                            
                            let temp_two = payload_object["two"].as_bool().unwrap();
                            
                            
                            let temp_three = payload_object["three"].as_str().unwrap().to_string();
                            
                            
                            (self.signal_recv_callback_for_another_signal)(temp_one, temp_two, temp_three);
                        }
                        _ => ()
                    }
                }
            
            }
        }
    }
}