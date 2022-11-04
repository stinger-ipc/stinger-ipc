/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/
use futures::{executor::block_on};
use signal_only_server::SignalOnlyServer;
use connection::Connection;




fn main() {
    block_on(async {
        
        let connection = Connection::new_default_connection(String::from("localhost"), 1883).await;
        let mut server = SignalOnlyServer::new(connection).await;
        
        
        server.emit_another_signal(3.14, true, "apples".to_string()).await;
        

    
        server.process().await;
    });
    // Ctrl-C to stop
}