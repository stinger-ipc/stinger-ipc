use futures::{executor::block_on};
use example_client::ExampleClient;
use connection::Connection;


#[tokio::main]
async fn main() {
    block_on(async {
        
        let connection = Connection::new_local_connection().await.expect("Failed to create connection");
        let mut client = ExampleClient::new(connection).await;
        
        let mut sig_rx = client.get_today_is_receiver();
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
        
        client.process_loop().await;
    });
    // Ctrl-C to stop
}