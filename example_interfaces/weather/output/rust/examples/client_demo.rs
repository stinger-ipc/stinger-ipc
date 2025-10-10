//! Client module for Full IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.
*/

use futures::executor::block_on;
use mqttier::{Connection, MqttierClient, MqttierOptions};
use tokio::join;
use tokio::time::{Duration, sleep};
use weather_ipc::client::WeatherClient;
use weather_ipc::discovery::WeatherDiscovery;
#[allow(unused_imports)]
use weather_ipc::payloads::{MethodReturnCode, *};

#[tokio::main]
async fn main() {
    block_on(async {
        let mqttier_options = MqttierOptions::new()
            .connection(Connection::TcpLocalhost(1883))
            .client_id("rust-client-demo".to_string())
            .build();
        let mut mqttier_client = MqttierClient::new(mqttier_options).unwrap();

        let discovery = WeatherDiscovery::new(&mut mqttier_client).await.unwrap();
        let singleton_info = discovery.get_singleton_service().await;

        let mut api_client = WeatherClient::new(&mut mqttier_client, singleton_info.instance).await;

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
                    }
                    Err(e) => {
                        eprintln!("Error receiving current_time signal: {:?}", e);
                        break;
                    }
                }
            }
        });

        let client_for_prop_change = api_client.clone();
        let _prop_change_rx_task = tokio::spawn(async move {
            let mut location_change_rx = client_for_prop_change.watch_location();
            let mut current_temperature_change_rx =
                client_for_prop_change.watch_current_temperature();
            let mut current_condition_change_rx = client_for_prop_change.watch_current_condition();
            let mut daily_forecast_change_rx = client_for_prop_change.watch_daily_forecast();
            let mut hourly_forecast_change_rx = client_for_prop_change.watch_hourly_forecast();
            let mut current_condition_refresh_interval_change_rx =
                client_for_prop_change.watch_current_condition_refresh_interval();
            let mut hourly_forecast_refresh_interval_change_rx =
                client_for_prop_change.watch_hourly_forecast_refresh_interval();
            let mut daily_forecast_refresh_interval_change_rx =
                client_for_prop_change.watch_daily_forecast_refresh_interval();

            loop {
                tokio::select! {
                    _ = location_change_rx.changed() => {
                        println!("Property 'location' changed to: {:?}", *location_change_rx.borrow());
                    }
                    _ = current_temperature_change_rx.changed() => {
                        println!("Property 'current_temperature' changed to: {:?}", *current_temperature_change_rx.borrow());
                    }
                    _ = current_condition_change_rx.changed() => {
                        println!("Property 'current_condition' changed to: {:?}", *current_condition_change_rx.borrow());
                    }
                    _ = daily_forecast_change_rx.changed() => {
                        println!("Property 'daily_forecast' changed to: {:?}", *daily_forecast_change_rx.borrow());
                    }
                    _ = hourly_forecast_change_rx.changed() => {
                        println!("Property 'hourly_forecast' changed to: {:?}", *hourly_forecast_change_rx.borrow());
                    }
                    _ = current_condition_refresh_interval_change_rx.changed() => {
                        println!("Property 'current_condition_refresh_interval' changed to: {:?}", *current_condition_refresh_interval_change_rx.borrow());
                    }
                    _ = hourly_forecast_refresh_interval_change_rx.changed() => {
                        println!("Property 'hourly_forecast_refresh_interval' changed to: {:?}", *hourly_forecast_refresh_interval_change_rx.borrow());
                    }
                    _ = daily_forecast_refresh_interval_change_rx.changed() => {
                        println!("Property 'daily_forecast_refresh_interval' changed to: {:?}", *daily_forecast_refresh_interval_change_rx.borrow());
                    }
                }
            }
        });

        println!("Calling refresh_daily_forecast with example values...");
        let result = api_client
            .refresh_daily_forecast()
            .await
            .expect("Failed to call refresh_daily_forecast");
        println!("refresh_daily_forecast response: {:?}", result);

        println!("Calling refresh_hourly_forecast with example values...");
        let result = api_client
            .refresh_hourly_forecast()
            .await
            .expect("Failed to call refresh_hourly_forecast");
        println!("refresh_hourly_forecast response: {:?}", result);

        println!("Calling refresh_current_conditions with example values...");
        let result = api_client
            .refresh_current_conditions()
            .await
            .expect("Failed to call refresh_current_conditions");
        println!("refresh_current_conditions response: {:?}", result);

        let location_new_value = LocationProperty {
            latitude: 3.14,
            longitude: 3.14,
        };
        let _ = api_client.set_location(location_new_value);

        let _ = api_client.set_current_condition_refresh_interval(42);

        let _ = api_client.set_hourly_forecast_refresh_interval(42);

        let _ = api_client.set_daily_forecast_refresh_interval(42);

        let _ = join!(sig_rx_task);
    });
    // Ctrl-C to stop
}
