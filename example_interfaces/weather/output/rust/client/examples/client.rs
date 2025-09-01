use futures::{executor::block_on};
use mqttier::MqttierClient;
use weather_client::WeatherClient;
use tokio::time::{sleep, Duration};
use tokio::join;

#[tokio::main]
async fn main() {
    block_on(async {
        
        let mut mqttier_client = MqttierClient::new("localhost", 1883, Some("client_example".to_string())).unwrap();
        let mut api_client = WeatherClient::new(&mut mqttier_client).await;

        let client_for_loop = api_client.clone();
        tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = client_for_loop.run_loop().await;
        });

        
        let mut sig_rx = api_client.get_current_time_receiver();
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
        


        
        println!("Calling refresh_daily_forecast with example values...");
        let result = api_client.refresh_daily_forecast().await.expect("Failed to call refresh_daily_forecast");
        println!("refresh_daily_forecast response: {:?}", result);
        
        println!("Calling refresh_hourly_forecast with example values...");
        let result = api_client.refresh_hourly_forecast().await.expect("Failed to call refresh_hourly_forecast");
        println!("refresh_hourly_forecast response: {:?}", result);
        
        println!("Calling refresh_current_conditions with example values...");
        let result = api_client.refresh_current_conditions().await.expect("Failed to call refresh_current_conditions");
        println!("refresh_current_conditions response: {:?}", result);
        

        let _ = join!(sig_rx_task);
    });
    // Ctrl-C to stop
}