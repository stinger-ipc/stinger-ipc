/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/
use futures::executor::block_on;
use mqttier::MqttierClient;
use signal_only_server::SignalOnlyServer;
use tokio::time::{Duration, sleep};

#[allow(unused_imports)]
use signal_only_types::payloads::{MethodResultCode, *};

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
        server
            .emit_another_signal(3.14, true, "apples".to_string())
            .await;

        let _server_loop_task = server.receive_loop().await;
    });
    // Ctrl-C to stop
}
