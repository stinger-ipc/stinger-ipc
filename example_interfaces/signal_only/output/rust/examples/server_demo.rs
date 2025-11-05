/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/
use std::any::Any;

use mqttier::{Connection, MqttierClient, MqttierOptionsBuilder};
use signal_only_ipc::server::SignalOnlyServer;
use tokio::time::{sleep, Duration};

#[allow(unused_imports)]
use signal_only_ipc::payloads::{MethodReturnCode, *};
use tokio::join;

#[tokio::main]
async fn main() {
    // Initialize tracing subscriber to see log output
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-server-demo".to_string())
        .build()
        .unwrap();
    let mut connection = MqttierClient::new(mqttier_options).unwrap();
    let _ = connection.start().await.unwrap();

    let mut server = SignalOnlyServer::new(connection, "rust-server-demo:1".to_string()).await;

    let mut looping_server = server.clone();
    let _loop_join_handle = tokio::spawn(async move {
        println!("Starting connection loop");
        let _conn_loop = looping_server.run_loop().await;
    });

    let mut server_clone1 = server.clone();
    let signal_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'anotherSignal'");
            let signal_result_future = server_clone1
                .emit_another_signal(3.14, true, "apples".to_string())
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'anotherSignal' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'bark'");
            let signal_result_future = server_clone1.emit_bark("apples".to_string()).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'bark' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'maybe_number'");
            let signal_result_future = server_clone1.emit_maybe_number(Some(42)).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'maybe_number' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'maybe_name'");
            let signal_result_future = server_clone1
                .emit_maybe_name(Some("apples".to_string()))
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'maybe_name' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'now'");
            let signal_result_future = server_clone1.emit_now(chrono::Utc::now()).await;
            let signal_result = signal_result_future.await;
            println!("Signal 'now' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(67)).await;
        }
    });

    let property_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(51)).await;
        }
    });

    let _ = join!(signal_publish_task, property_publish_task);

    // Ctrl-C to stop
}
