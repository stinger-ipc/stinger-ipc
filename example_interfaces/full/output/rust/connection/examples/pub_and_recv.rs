
use connection::Connection;
use tokio::time::{sleep, Duration};
use tokio::join;
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    
    let mut connection = Connection::new_local_connection().await.expect("Failed to create connection");
    let (recv_chan_tx, mut recv_chan_rx) = mpsc::channel(32);
    connection.connect().await.expect("Failed to connect to broker");
    connection.subscribe("example/recv_topic", recv_chan_tx.clone()).await.expect("Failed to subscribe to topic");
    let mut publisher = connection.get_publisher();
    let mut streamer = connection.get_streamer().await;

    let _stream_task = tokio::spawn(async move {
        let _ = streamer.receive_loop().await;
    });

    let loop_task = tokio::spawn(async move {
        connection.start_publish_loop().await;
    });

    let _pub_task = tokio::spawn(async move {
        let mut i = 0;
        loop {
            i = i + 1;
            sleep(Duration::from_secs(1)).await; // Simulate periodic publishing
            publisher.publish_simple("example/pub_topic".to_string(), format!("Periodic message {}",i).to_string()).await.expect("Failed to publish periodic message");
        }
    });

    let _receive_task = tokio::spawn(async move {
        loop {
            match recv_chan_rx.recv().await {
                Some(message) => {
                    println!("Received message: {:?}", message);
                },
                None => {
                    eprintln!("Receiver channel closed");
                    break;
                }
            }
        }
    });
    
    let _result = join!(loop_task);
}