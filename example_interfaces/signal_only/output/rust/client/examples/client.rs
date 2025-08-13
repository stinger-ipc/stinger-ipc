use futures::{executor::block_on};
use signal_only_client::SignalOnlyClient;
use connection::Connection;
use tokio::time::{sleep, Duration};
use tokio::join;

#[tokio::main]
async fn main() {
    block_on(async {
        
        let mut connection = Connection::new_default_connection().await.expect("Failed to create connection");
        let mut client = SignalOnlyClient::new(&mut connection).await;

        tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = connection.start_loop().await;
        });

        
        let mut sig_rx = client.get_another_signal_receiver();
        println!("Got signal receiver for anotherSignal");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task = tokio::spawn(async move {
            println!("Looping for signals");
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received anotherSignal signal with payload: {:?}", payload);
                    },
                    Err(e) => {
                        eprintln!("Error receiving anotherSignal signal: {:?}", e);
                        break;
                    }
                }
            }
        });
        

        println!("Starting client receive loop");
        let _client_loop = client.receive_loop().await;

        

        join!(sig_rx_task);
    });
    // Ctrl-C to stop
}