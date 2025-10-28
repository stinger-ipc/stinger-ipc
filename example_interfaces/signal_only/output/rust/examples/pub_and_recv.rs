use mqttier::{Connection, MqttierClient, MqttierOptions};
use stinger_mqtt_trait::message::{MqttMessageBuilder, QoS};
use stinger_mqtt_trait::MqttClient;
use tokio::join;
use tokio::sync::broadcast;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    println!("Starting pub and recv example");

    let conn_opts = MqttierOptions::new()
        .connection(Connection::TcpLocalhost(1883))
        .build();
    let client = MqttierClient::new(conn_opts).unwrap();
    let (recv_chan_tx, mut recv_chan_rx) = broadcast::channel(22);
    let _subscription_id = client
        .subscribe("example/recv_topic".to_string(), 1, recv_chan_tx.clone())
        .await
        .expect("Failed to subscribe to topic");
    println!("Starting MQTT client loop");
    client.run_loop().await.unwrap();

    let mut client2 = client.clone();
    let _pub_task = tokio::spawn(async move {
        let mut i = 0;
        loop {
            i = i + 1;
            sleep(Duration::from_secs(1)).await; // Simulate periodic publishing
            let message_payload = format!("Periodic message {}", i);
            let msg = MqttMessageBuilder::default()
                .topic("example/pub_topic".to_string())
                .payload(message_payload)
                .qos(QoS::AtMostOnce)
                .content_type("text/plain".to_string())
                .retain(false)
                .build()
                .expect("Failed to build message");
            let pub_result = client2.publish(msg).await;
            match pub_result {
                Ok(_) => println!("Published message {}", i),
                Err(e) => eprintln!("Failed to publish message {}: {:?}", i, e),
            }
        }
    });

    let receive_task = tokio::spawn(async move {
        loop {
            match recv_chan_rx.recv().await {
                Ok(message) => {
                    println!("Received message: {:?}", message);
                }
                Err(_) => {
                    eprintln!("Receiver channel closed");
                    break;
                }
            }
        }
    });

    let _result = join!(receive_task);
}
