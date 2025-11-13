//! Client module for Full IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

use mqttier::{Connection, MqttierClient, MqttierOptionsBuilder};
use tokio::join;
use tokio::time::{sleep, Duration};
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};
use weather_ipc::client::WeatherClient;
use weather_ipc::discovery::WeatherDiscovery;
#[allow(unused_imports)]
use weather_ipc::payloads::{MethodReturnCode, *};
#[tokio::main]
async fn main() {
    // Initialize tracing subscriber to see log output
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    info!("Starting weather client demo...");

    // Create an MQTT client that implements the MqttPubSub trait.
    // Application code is responsible for managing the client object.
    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-client-demo".to_string())
        .build()
        .unwrap();
    let mut mqttier_client = MqttierClient::new(mqttier_options).unwrap();
    let _ = mqttier_client.start().await;

    // We need to discover a service instance before we can create the client.
    // For this demo, we assume a singleton server.
    let service_discovery = WeatherDiscovery::new(&mut mqttier_client).await.unwrap();
    // The `discovered_singleton` struct contains the service_id and initial property values.
    let discovered_singleton = service_discovery.get_singleton_service().await;

    #[cfg(feature = "metrics")]
    {
        let metrics = service_discovery
            .metrics
            .lock()
            .expect("Failed to lock metrics");
        println!("Discovery complete.  Metrics: {:?}", metrics);
        println!(
            "Time to first discovery (ms): {:?}",
            metrics.time_to_first_discovery_ms()
        );
    };
    drop(service_discovery);
    let mut weather_client = WeatherClient::new(mqttier_client.clone(), discovered_singleton).await;

    let mut client_for_loop = weather_client.clone();
    tokio::spawn(async move {
        let _conn_loop = client_for_loop.run_loop().await;
    });

    let mut sig_rx = weather_client.get_current_time_receiver();
    println!("Got signal receiver for current_time");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task1 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received current_time signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving current_time signal: {:?}", e);
                    break;
                }
            }
        }
    });

    // This task subscribes to a watch chanel for each property to get notified of changes.
    let client_for_prop_change = weather_client.clone();
    let _prop_change_rx_task = tokio::spawn(async move {
        let mut location_change_rx = client_for_prop_change.watch_location();
        let mut current_temperature_change_rx = client_for_prop_change.watch_current_temperature();
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

    println!(">>> Calling refresh_daily_forecast with example values...");
    let result = weather_client.refresh_daily_forecast().await;
    println!("<<< refresh_daily_forecast response: {:?}", result);

    println!(">>> Calling refresh_hourly_forecast with example values...");
    let result = weather_client.refresh_hourly_forecast().await;
    println!("<<< refresh_hourly_forecast response: {:?}", result);

    println!(">>> Calling refresh_current_conditions with example values...");
    let result = weather_client.refresh_current_conditions().await;
    println!("<<< refresh_current_conditions response: {:?}", result);

    // Property handles are Send so we can move them into tasks.

    let location_handle = weather_client.get_location_handle();

    let current_temperature_handle = weather_client.get_current_temperature_handle();

    let current_condition_handle = weather_client.get_current_condition_handle();

    let daily_forecast_handle = weather_client.get_daily_forecast_handle();

    let hourly_forecast_handle = weather_client.get_hourly_forecast_handle();

    let current_condition_refresh_interval_handle =
        weather_client.get_current_condition_refresh_interval_handle();

    let hourly_forecast_refresh_interval_handle =
        weather_client.get_hourly_forecast_refresh_interval_handle();

    let daily_forecast_refresh_interval_handle =
        weather_client.get_daily_forecast_refresh_interval_handle();

    let property_update_task = tokio::spawn(async move {
        let mut i = 0;
        loop {
            sleep(Duration::from_secs(20)).await;

            {
                // Scoping for 'location' property.  Demonstrates reading the value.
                let current_value_ref = location_handle.read().await;
                println!(
                    "Current value of property 'location': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'location' property.  Demonstrates creating a request to set the value.
                let location_new_value = LocationProperty {
                    latitude: 3.14,
                    longitude: 3.14,
                };
                let mut write_lock = location_handle.write().await;
                *write_lock = location_new_value;
                println!(
                    "Sending request to update property 'location' to new value: {:?}",
                    *write_lock
                );
            }
            sleep(Duration::from_secs(10)).await;

            {
                // Scoping for 'current_temperature' property.  Demonstrates reading the value.
                let current_value_ref = current_temperature_handle.read().await;
                println!(
                    "Current value of property 'current_temperature': {:?}",
                    *current_value_ref
                );
            }

            // We can't do `current_temperature_handle.write()` here because it is a read-only lock.

            {
                // Scoping for 'current_condition' property.  Demonstrates reading the value.
                let current_value_ref = current_condition_handle.read().await;
                println!(
                    "Current value of property 'current_condition': {:?}",
                    *current_value_ref
                );
            }

            // We can't do `current_condition_handle.write()` here because it is a read-only lock.

            {
                // Scoping for 'daily_forecast' property.  Demonstrates reading the value.
                let current_value_ref = daily_forecast_handle.read().await;
                println!(
                    "Current value of property 'daily_forecast': {:?}",
                    *current_value_ref
                );
            }

            // We can't do `daily_forecast_handle.write()` here because it is a read-only lock.

            {
                // Scoping for 'hourly_forecast' property.  Demonstrates reading the value.
                let current_value_ref = hourly_forecast_handle.read().await;
                println!(
                    "Current value of property 'hourly_forecast': {:?}",
                    *current_value_ref
                );
            }

            // We can't do `hourly_forecast_handle.write()` here because it is a read-only lock.

            {
                // Scoping for 'current_condition_refresh_interval' property.  Demonstrates reading the value.
                let current_value_ref = current_condition_refresh_interval_handle.read().await;
                println!(
                    "Current value of property 'current_condition_refresh_interval': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'current_condition_refresh_interval' property.  Demonstrates creating a request to set the value.
                let current_condition_refresh_interval_new_value = 42;
                let mut write_lock = current_condition_refresh_interval_handle.write().await;
                *write_lock = current_condition_refresh_interval_new_value;
                println!("Sending request to update property 'current_condition_refresh_interval' to new value: {:?}", *write_lock);
            }
            sleep(Duration::from_secs(10)).await;

            {
                // Scoping for 'hourly_forecast_refresh_interval' property.  Demonstrates reading the value.
                let current_value_ref = hourly_forecast_refresh_interval_handle.read().await;
                println!(
                    "Current value of property 'hourly_forecast_refresh_interval': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'hourly_forecast_refresh_interval' property.  Demonstrates creating a request to set the value.
                let hourly_forecast_refresh_interval_new_value = 42;
                let mut write_lock = hourly_forecast_refresh_interval_handle.write().await;
                *write_lock = hourly_forecast_refresh_interval_new_value;
                println!("Sending request to update property 'hourly_forecast_refresh_interval' to new value: {:?}", *write_lock);
            }
            sleep(Duration::from_secs(10)).await;

            {
                // Scoping for 'daily_forecast_refresh_interval' property.  Demonstrates reading the value.
                let current_value_ref = daily_forecast_refresh_interval_handle.read().await;
                println!(
                    "Current value of property 'daily_forecast_refresh_interval': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'daily_forecast_refresh_interval' property.  Demonstrates creating a request to set the value.
                let daily_forecast_refresh_interval_new_value = 42;
                let mut write_lock = daily_forecast_refresh_interval_handle.write().await;
                *write_lock = daily_forecast_refresh_interval_new_value;
                println!("Sending request to update property 'daily_forecast_refresh_interval' to new value: {:?}", *write_lock);
            }
            sleep(Duration::from_secs(10)).await;

            i += 1;
        }
    });

    println!("Setting 'location' property to new value using blocking method...");

    // Set 'location' property values using the blocking setter.
    let location_new_value = LocationProperty {
        latitude: 3.14,
        longitude: 3.14,
    };
    let _ = weather_client.set_location(location_new_value).await;

    println!("Setting 'current_condition_refresh_interval' property to new value using blocking method...");

    // Set 'current_condition_refresh_interval' property using the blocking setter.
    let _ = weather_client
        .set_current_condition_refresh_interval(42)
        .await;

    println!(
        "Setting 'hourly_forecast_refresh_interval' property to new value using blocking method..."
    );

    // Set 'hourly_forecast_refresh_interval' property using the blocking setter.
    let _ = weather_client
        .set_hourly_forecast_refresh_interval(42)
        .await;

    println!(
        "Setting 'daily_forecast_refresh_interval' property to new value using blocking method..."
    );

    // Set 'daily_forecast_refresh_interval' property using the blocking setter.
    let _ = weather_client.set_daily_forecast_refresh_interval(42).await;

    println!("Waiting for Ctrl-C to exit...");
    tokio::signal::ctrl_c()
        .await
        .expect("Failed to listen for Ctrl-C");
    println!("Ctrl-C received, shutting down...");

    sig_rx_task1.abort();

    property_update_task.abort();

    // Join on all the signal emitting tasks.
    let _ = join!(property_update_task, sig_rx_task1);

    // Ctrl-C to stop
}
