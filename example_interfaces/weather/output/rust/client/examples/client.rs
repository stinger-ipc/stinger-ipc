use futures::{executor::block_on};
use weather_client::WeatherClient;
use connection::Connection;
use tokio::time::{sleep, Duration};
use tokio::join;

#[tokio::main]
async fn main() {
    block_on(async {
        
        let mut connection = Connection::new_default_connection().await.expect("Failed to create connection");
        let mut client = WeatherClient::new(&mut connection).await;

        tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = connection.start_loop().await;
        });

        
        let mut sig_rx = client.get_current_time_receiver();
        println!("Got signal receiver for current_time");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task = tokio::spawn(async move {
            println!("Looping for signals");
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received current_time signal with payload: {:?}", payload);
                    },
                    Err(e) => {
                        eprintln!("Error receiving current_time signal: {:?}", e);
                        break;
                    }
                }
            }
        });
        

        println!("Starting client receive loop");
        let _client_loop = client.receive_loop().await;

        
        println!("Calling refresh_daily_forecast with example values...");
        let result = client.refresh_daily_forecast().await.expect("Failed to call refresh_daily_forecast");
        println!("refresh_daily_forecast response: {:?}", result);
        
        println!("Calling refresh_hourly_forecast with example values...");
        let result = client.refresh_hourly_forecast().await.expect("Failed to call refresh_hourly_forecast");
        println!("refresh_hourly_forecast response: {:?}", result);
        
        println!("Calling refresh_current_conditions with example values...");
        let result = client.refresh_current_conditions().await.expect("Failed to call refresh_current_conditions");
        println!("refresh_current_conditions response: {:?}", result);
        

        join!(sig_rx_task);
    });
    // Ctrl-C to stop
}