use futures::executor::block_on;
use mqttier::MqttierClient;
use signal_only_client::SignalOnlyClient;
#[allow(unused_imports)]
use signal_only_types::{MethodReturnCode, *};
use tokio::join;
use tokio::time::{Duration, sleep};

#[tokio::main]
async fn main() {
    block_on(async {
        let mut mqttier_client =
            MqttierClient::new("localhost", 1883, Some("client_example".to_string())).unwrap();
        let api_client = SignalOnlyClient::new(&mut mqttier_client).await;

        let client_for_loop = api_client.clone();
        tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = client_for_loop.run_loop().await;
        });

        let mut sig_rx = api_client.get_another_signal_receiver();
        println!("Got signal receiver for anotherSignal");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task = tokio::spawn(async move {
            println!("Looping for signals");
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received anotherSignal signal with payload: {:?}", payload);
                    }
                    Err(e) => {
                        eprintln!("Error receiving anotherSignal signal: {:?}", e);
                        break;
                    }
                }
            }
        });

        let _ = join!(sig_rx_task);
    });
    // Ctrl-C to stop
}
