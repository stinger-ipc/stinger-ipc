/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/
use futures::{executor::block_on};
use mqttier::MqttierClient;
use signal_only_server::SignalOnlyServer;
use tokio::time::{sleep, Duration};
use tokio::join;

#[allow(unused_imports)]
use signal_only_types::payloads::{MethodResultCode, *};




#[tokio::main]
async fn main() {
    block_on(async {
        
        let mut connection = MqttierClient::new("localhost", 1883, None).unwrap();
        let mut server = SignalOnlyServer::new(&mut connection).await;
        
        let loop_task = tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = connection.run_loop().await;
        });
        
        
        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'anotherSignal'");
        server.emit_another_signal(3.14, true, "apples".to_string()).await;
        
        let _ = server.receive_loop().await;
        let _ = join!(loop_task);
    });
    // Ctrl-C to stop
}