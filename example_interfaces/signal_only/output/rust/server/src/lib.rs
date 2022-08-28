/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.
*/

use futures::StreamExt;
use connection::Connection;
use json::object;


pub struct SignalOnlyServer {
    connection: Connection,
}

impl SignalOnlyServer {
    pub fn new(mut connection: Connection) -> SignalOnlyServer {

        let interface_info = String::from(r#"{"name": "SignalOnly", "summary": "", "title": "SignalOnly", "version": "0.0.1"}"#);
        connection.publish("SignalOnly/interface".to_string(), interface_info, 1);

        SignalOnlyServer{
            connection: connection,
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
    

    pub async fn process(&mut self) {
        while let Some(opt_msg) = self.connection.rx.next().await {
            if let Some(_msg) = opt_msg {

            }
        }
    }
}