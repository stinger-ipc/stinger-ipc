use mqttier::MqttierClient;
use tokio::join;
use tokio::sync::mpsc;
use tokio::time::{Duration, sleep};

#[tokio::main]
async fn main() {
    println!("Starting pub and recv example");
    let client = MqttierClient::new("localhost", 1883, None).unwrap();
    let (recv_chan_tx, mut recv_chan_rx) = mpsc::channel(32);
    client
        .subscribe("example/recv_topic".to_string(), 1, recv_chan_tx.clone())
        .await
        .expect("Failed to subscribe to topic");

    println!("Starting MQTT client loop");
    client.run_loop().await.unwrap();

    let client2 = client.clone();
    let _pub_task = tokio::spawn(async move {
        let mut i = 0;
        loop {
            i = i + 1;
            sleep(Duration::from_secs(1)).await; // Simulate periodic publishing
            let message = format!("Periodic message {}", i);
            let pub_result_rx = client2
                .publish_string("example/pub_topic".to_string(), message, 1, false, None)
                .await;
            let pub_result = pub_result_rx.await;
        }
    });

    let receive_task = tokio::spawn(async move {
        loop {
            match recv_chan_rx.recv().await {
                Some(message) => {
                    println!("Received message: {:?}", message);
                }
                None => {
                    eprintln!("Receiver channel closed");
                    break;
                }
            }
        }
    });

    let _result = join!(receive_task);
}
