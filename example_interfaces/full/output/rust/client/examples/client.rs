use futures::{executor::block_on};
use example_client::ExampleClient;
use connection::Connection;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    block_on(async {
        
        let connection = Connection::new_local_connection().await.expect("Failed to create connection");
        let mut client = ExampleClient::new(connection).await;
        
        let mut sig_rx = client.get_today_is_receiver();

        client.process_loop().await;
        sleep(Duration::from_secs(5)).await;

        tokio::spawn(async move {
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received todayIs signal with payload: {:?}", payload);
                    },
                    Err(e) => {
                        eprintln!("Error receiving todayIs signal: {:?}", e);
                        break;
                    }
                }
            }
        });
        

        
        println!("Calling addNumbers with example values...");
        let _ = client.add_numbers(42, 42).await.expect("Failed to call addNumbers");
        
        println!("Calling doSomething with example values...");
        let _ = client.do_something("apples".to_string()).await.expect("Failed to call doSomething");
        
    });
    // Ctrl-C to stop
}