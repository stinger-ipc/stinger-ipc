use full_client::FullClient;
use futures::executor::block_on;
use mqttier::MqttierClient;
use tokio::join;
use tokio::time::{Duration, sleep};

#[tokio::main]
async fn main() {
    block_on(async {
        let mut mqttier_client =
            MqttierClient::new("localhost", 1883, Some("client_example".to_string())).unwrap();
        let mut api_client = FullClient::new(&mut mqttier_client).await;

        let client_for_loop = api_client.clone();
        tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = client_for_loop.run_loop().await;
        });

        let mut sig_rx = api_client.get_today_is_receiver();
        println!("Got signal receiver for todayIs");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task = tokio::spawn(async move {
            println!("Looping for signals");
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received todayIs signal with payload: {:?}", payload);
                    }
                    Err(e) => {
                        eprintln!("Error receiving todayIs signal: {:?}", e);
                        break;
                    }
                }
            }
        });

        println!("Calling addNumbers with example values...");
        let result = api_client
            .add_numbers(42, 42, Some(42))
            .await
            .expect("Failed to call addNumbers");
        println!("addNumbers response: {:?}", result);

        println!("Calling doSomething with example values...");
        let result = api_client
            .do_something("apples".to_string())
            .await
            .expect("Failed to call doSomething");
        println!("doSomething response: {:?}", result);

        let _ = join!(sig_rx_task);
    });
    // Ctrl-C to stop
}
