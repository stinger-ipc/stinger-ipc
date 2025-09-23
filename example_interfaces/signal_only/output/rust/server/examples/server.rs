/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/
use futures::executor::block_on;
use mqttier::MqttierClient;
use signal_only_server::SignalOnlyServer;
use std::any::Any;
use tokio::time::{Duration, sleep};

use signal_only_types::MethodReturnCode;
#[allow(unused_imports)]
use signal_only_types::payloads::*;

#[tokio::main]
async fn main() {
    env_logger::Builder::from_default_env()
        .target(env_logger::Target::Stdout)
        .init();

    block_on(async {
        let mut connection = MqttierClient::new("localhost", 1883, None).unwrap();

        let mut server = SignalOnlyServer::new(&mut connection).await;

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'anotherSignal'");
        let signal_result_future = server
            .emit_another_signal(3.14, true, "apples".to_string())
            .await;
        let signal_result = signal_result_future.await;
        println!("Signal 'anotherSignal' was sent: {:?}", signal_result);

        let _server_loop_task = server.run_loop().await;
    });
    // Ctrl-C to stop
}
