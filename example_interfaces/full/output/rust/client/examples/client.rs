use futures::{executor::block_on};
use example_client::ExampleClient;
use connection::Connection;
use tokio::time::{sleep, Duration};
use tokio::join;

#[tokio::main]
async fn main() {
    block_on(async {
        
        let mut connection = Connection::new_local_connection().await.expect("Failed to create connection");
        let mut client = ExampleClient::new(&mut connection).await;

        tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = connection.start_loop().await;
        });

        
        let mut sig_rx = client.get_today_is_receiver();
        println!("Got signal receiver for todayIs");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task = tokio::spawn(async move {
            println!("Looping for signals");
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
        

        println!("Starting client receive loop");
        let _client_loop = client.receive_loop().await;

        
        println!("Calling addNumbers with example values...");
        let result = client.add_numbers(42, 42, Some(42)).await.expect("Failed to call addNumbers");
        println!("addNumbers response: {:?}", result);
        
        println!("Calling doSomething with example values...");
        let result = client.do_something("apples".to_string()).await.expect("Failed to call doSomething");
        println!("doSomething response: {:?}", result);
        

        join!(sig_rx_task);
    });
    // Ctrl-C to stop
}