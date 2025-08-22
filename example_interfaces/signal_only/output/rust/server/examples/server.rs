/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/
use futures::{executor::block_on};
use signal_only_server::SignalOnlyServer;
use connection::Connection;
use tokio::time::{sleep, Duration};
use tokio::join;
use connection::payloads::{MethodResultCode, *};




#[tokio::main]
async fn main() {
    block_on(async {
        
        let mut connection = Connection::new_default_connection().await.unwrap();
        let mut server = SignalOnlyServer::new(&mut connection).await;

        let loop_task = tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = connection.start_loop().await;
        });
        
        
        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'anotherSignal'");
        server.emit_another_signal(3.14, true, "apples".to_string()).await;
        
        server.receive_loop().await;
        join!(loop_task);
    });
    // Ctrl-C to stop
}