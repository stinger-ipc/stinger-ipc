/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/
use futures::executor::block_on;
use mqttier::{Connection, MqttierClient, MqttierOptions};
use signal_only_ipc::server::SignalOnlyServer;
use std::any::Any;
use tokio::time::{Duration, sleep};

#[allow(unused_imports)]
use signal_only_ipc::payloads::{MethodReturnCode, *};

#[tokio::main]
async fn main() {
    block_on(async {
        let mqttier_options = MqttierOptions::new()
            .connection(Connection::TcpLocalhost(1883))
            .client_id("rust-server-demo".to_string())
            .build();
        let mut connection = MqttierClient::new(mqttier_options).unwrap();

        let mut server =
            SignalOnlyServer::new(&mut connection, "rust-server-demo:1".to_string()).await;

        let mut looping_server = server.clone();
        tokio::spawn(async move {
            println!("Starting connection loop");
            let _conn_loop = looping_server.run_loop().await;
        });

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'anotherSignal'");
        let signal_result_future = server
            .emit_another_signal(3.14, true, "apples".to_string())
            .await;
        let signal_result = signal_result_future.await;
        println!("Signal 'anotherSignal' was sent: {:?}", signal_result);

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'bark'");
        let signal_result_future = server.emit_bark("apples".to_string()).await;
        let signal_result = signal_result_future.await;
        println!("Signal 'bark' was sent: {:?}", signal_result);

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'maybe_number'");
        let signal_result_future = server.emit_maybe_number(Some(42)).await;
        let signal_result = signal_result_future.await;
        println!("Signal 'maybe_number' was sent: {:?}", signal_result);

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'maybe_name'");
        let signal_result_future = server.emit_maybe_name(Some("apples".to_string())).await;
        let signal_result = signal_result_future.await;
        println!("Signal 'maybe_name' was sent: {:?}", signal_result);

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'now'");
        let signal_result_future = server.emit_now(chrono::Utc::now()).await;
        let signal_result = signal_result_future.await;
        println!("Signal 'now' was sent: {:?}", signal_result);
    });
    // Ctrl-C to stop
}
