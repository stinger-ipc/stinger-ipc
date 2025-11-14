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

use full_ipc::client::FullClient;
use full_ipc::discovery::FullDiscovery;
#[allow(unused_imports)]
use full_ipc::payloads::{MethodReturnCode, *};
use mqttier::{Connection, MqttierClient, MqttierOptionsBuilder};
use tokio::join;
use tokio::time::{sleep, Duration};
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};
#[tokio::main]
async fn main() {
    // Initialize tracing subscriber to see log output
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    info!("Starting Full client demo...");

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
    let service_discovery = FullDiscovery::new(&mut mqttier_client).await.unwrap();
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
    let mut full_client = FullClient::new(mqttier_client.clone(), discovered_singleton).await;

    let mut client_for_loop = full_client.clone();
    tokio::spawn(async move {
        let _conn_loop = client_for_loop.run_loop().await;
    });

    let mut sig_rx = full_client.get_today_is_receiver();
    println!("Got signal receiver for todayIs");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task1 = tokio::spawn(async move {
        println!("Looping for signal reception...");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("*** Received todayIs signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving todayIs signal: {:?}", e);
                    break;
                }
            }
        }
    });

    // This task subscribes to a watch chanel for each property to get notified of changes.
    let client_for_prop_change = full_client.clone();
    let _prop_change_rx_task = tokio::spawn(async move {
        let mut favorite_number_change_rx = client_for_prop_change.watch_favorite_number();
        let mut favorite_foods_change_rx = client_for_prop_change.watch_favorite_foods();
        let mut lunch_menu_change_rx = client_for_prop_change.watch_lunch_menu();
        let mut family_name_change_rx = client_for_prop_change.watch_family_name();
        let mut last_breakfast_time_change_rx = client_for_prop_change.watch_last_breakfast_time();
        let mut breakfast_length_change_rx = client_for_prop_change.watch_breakfast_length();
        let mut last_birthdays_change_rx = client_for_prop_change.watch_last_birthdays();

        loop {
            tokio::select! {
                _ = favorite_number_change_rx.changed() => {
                    println!("Property 'favorite_number' changed to: {:?}", *favorite_number_change_rx.borrow());
                }
                _ = favorite_foods_change_rx.changed() => {
                    println!("Property 'favorite_foods' changed to: {:?}", *favorite_foods_change_rx.borrow());
                }
                _ = lunch_menu_change_rx.changed() => {
                    println!("Property 'lunch_menu' changed to: {:?}", *lunch_menu_change_rx.borrow());
                }
                _ = family_name_change_rx.changed() => {
                    println!("Property 'family_name' changed to: {:?}", *family_name_change_rx.borrow());
                }
                _ = last_breakfast_time_change_rx.changed() => {
                    println!("Property 'last_breakfast_time' changed to: {:?}", *last_breakfast_time_change_rx.borrow());
                }
                _ = breakfast_length_change_rx.changed() => {
                    println!("Property 'breakfast_length' changed to: {:?}", *breakfast_length_change_rx.borrow());
                }
                _ = last_birthdays_change_rx.changed() => {
                    println!("Property 'last_birthdays' changed to: {:?}", *last_birthdays_change_rx.borrow());
                }
            }
        }
    });

    let mut client_for_method_calling = full_client.clone();
    let method_calling_task = tokio::spawn(async move {
        sleep(Duration::from_secs(19)).await;
        loop {
            println!(">>> Calling addNumbers with example values...");
            let result = client_for_method_calling
                .add_numbers(42, 42, Some(42))
                .await;
            println!("<<< addNumbers response: {:?}", result);
            sleep(Duration::from_secs(19)).await;

            println!(">>> Calling doSomething with example values...");
            let result = client_for_method_calling
                .do_something("apples".to_string())
                .await;
            println!("<<< doSomething response: {:?}", result);
            sleep(Duration::from_secs(19)).await;

            println!(">>> Calling echo with example values...");
            let result = client_for_method_calling.echo("apples".to_string()).await;
            println!("<<< echo response: {:?}", result);
            sleep(Duration::from_secs(19)).await;

            println!(">>> Calling what_time_is_it with example values...");
            let result = client_for_method_calling
                .what_time_is_it(chrono::Utc::now())
                .await;
            println!("<<< what_time_is_it response: {:?}", result);
            sleep(Duration::from_secs(19)).await;

            println!(">>> Calling set_the_time with example values...");
            let result = client_for_method_calling
                .set_the_time(chrono::Utc::now(), chrono::Utc::now())
                .await;
            println!("<<< set_the_time response: {:?}", result);
            sleep(Duration::from_secs(19)).await;

            println!(">>> Calling forward_time with example values...");
            let result = client_for_method_calling
                .forward_time(chrono::Duration::seconds(3536))
                .await;
            println!("<<< forward_time response: {:?}", result);
            sleep(Duration::from_secs(19)).await;

            println!(">>> Calling how_off_is_the_clock with example values...");
            let result = client_for_method_calling
                .how_off_is_the_clock(chrono::Utc::now())
                .await;
            println!("<<< how_off_is_the_clock response: {:?}", result);
            sleep(Duration::from_secs(19)).await;

            sleep(Duration::from_secs(29)).await;
        }
    });

    // Property handles are Send so we can move them into tasks.

    let favorite_number_handle = full_client.get_favorite_number_handle();

    let favorite_foods_handle = full_client.get_favorite_foods_handle();

    let lunch_menu_handle = full_client.get_lunch_menu_handle();

    let family_name_handle = full_client.get_family_name_handle();

    let last_breakfast_time_handle = full_client.get_last_breakfast_time_handle();

    let breakfast_length_handle = full_client.get_breakfast_length_handle();

    let last_birthdays_handle = full_client.get_last_birthdays_handle();

    let property_update_task = tokio::spawn(async move {
        let mut i = 0;
        loop {
            sleep(Duration::from_secs(20)).await;

            {
                // Scoping for 'favorite_number' property.  Demonstrates reading the value.
                let current_value_ref = favorite_number_handle.read().await;
                println!(
                    "=== Current value of property 'favorite_number': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'favorite_number' property.  Demonstrates creating a request to set the value.
                let favorite_number_new_value = 42;
                let mut write_lock = favorite_number_handle.write().await;
                *write_lock = favorite_number_new_value;
                println!(
                    "<~~ Sending request to update property 'favorite_number' to new value: {:?}",
                    *write_lock
                );
            }
            sleep(Duration::from_secs(10)).await;

            {
                // Scoping for 'favorite_foods' property.  Demonstrates reading the value.
                let current_value_ref = favorite_foods_handle.read().await;
                println!(
                    "=== Current value of property 'favorite_foods': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'favorite_foods' property.  Demonstrates creating a request to set the value.
                let favorite_foods_new_value = FavoriteFoodsProperty {
                    drink: format!("new-value-{}", i).into(),
                    slices_of_pizza: 42,
                    breakfast: format!("new-value-{}", i).into(),
                };
                let mut write_lock = favorite_foods_handle.write().await;
                *write_lock = favorite_foods_new_value;
                println!(
                    "<~~ Sending request to update property 'favorite_foods' to new value: {:?}",
                    *write_lock
                );
            }
            sleep(Duration::from_secs(10)).await;

            {
                // Scoping for 'lunch_menu' property.  Demonstrates reading the value.
                let current_value_ref = lunch_menu_handle.read().await;
                println!(
                    "=== Current value of property 'lunch_menu': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'lunch_menu' property.  Demonstrates creating a request to set the value.
                let lunch_menu_new_value = LunchMenuProperty {
                    monday: Lunch {
                        drink: true,
                        sandwich: "apples".to_string(),
                        crackers: 3.14,
                        day: DayOfTheWeek::Saturday,
                        order_number: Some(42),
                        time_of_lunch: chrono::Utc::now(),
                        duration_of_lunch: chrono::Duration::seconds(3536),
                    },
                    tuesday: Lunch {
                        drink: true,
                        sandwich: "apples".to_string(),
                        crackers: 3.14,
                        day: DayOfTheWeek::Saturday,
                        order_number: Some(42),
                        time_of_lunch: chrono::Utc::now(),
                        duration_of_lunch: chrono::Duration::seconds(3536),
                    },
                };
                let mut write_lock = lunch_menu_handle.write().await;
                *write_lock = lunch_menu_new_value;
                println!(
                    "<~~ Sending request to update property 'lunch_menu' to new value: {:?}",
                    *write_lock
                );
            }
            sleep(Duration::from_secs(10)).await;

            {
                // Scoping for 'family_name' property.  Demonstrates reading the value.
                let current_value_ref = family_name_handle.read().await;
                println!(
                    "=== Current value of property 'family_name': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'family_name' property.  Demonstrates creating a request to set the value.
                let family_name_new_value = format!("new-value-{}", i).into();
                let mut write_lock = family_name_handle.write().await;
                *write_lock = family_name_new_value;
                println!(
                    "<~~ Sending request to update property 'family_name' to new value: {:?}",
                    *write_lock
                );
            }
            sleep(Duration::from_secs(10)).await;

            {
                // Scoping for 'last_breakfast_time' property.  Demonstrates reading the value.
                let current_value_ref = last_breakfast_time_handle.read().await;
                println!(
                    "=== Current value of property 'last_breakfast_time': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'last_breakfast_time' property.  Demonstrates creating a request to set the value.
                let last_breakfast_time_new_value = chrono::Utc::now();
                let mut write_lock = last_breakfast_time_handle.write().await;
                *write_lock = last_breakfast_time_new_value;
                println!("<~~ Sending request to update property 'last_breakfast_time' to new value: {:?}", *write_lock);
            }
            sleep(Duration::from_secs(10)).await;

            {
                // Scoping for 'breakfast_length' property.  Demonstrates reading the value.
                let current_value_ref = breakfast_length_handle.read().await;
                println!(
                    "=== Current value of property 'breakfast_length': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'breakfast_length' property.  Demonstrates creating a request to set the value.
                let breakfast_length_new_value = chrono::Duration::seconds(3536);
                let mut write_lock = breakfast_length_handle.write().await;
                *write_lock = breakfast_length_new_value;
                println!(
                    "<~~ Sending request to update property 'breakfast_length' to new value: {:?}",
                    *write_lock
                );
            }
            sleep(Duration::from_secs(10)).await;

            {
                // Scoping for 'last_birthdays' property.  Demonstrates reading the value.
                let current_value_ref = last_birthdays_handle.read().await;
                println!(
                    "=== Current value of property 'last_birthdays': {:?}",
                    *current_value_ref
                );
            }

            sleep(Duration::from_secs(2)).await;
            {
                // Scoping for 'last_birthdays' property.  Demonstrates creating a request to set the value.
                let last_birthdays_new_value = LastBirthdaysProperty {
                    mom: chrono::Utc::now(),
                    dad: chrono::Utc::now(),
                    sister: Some(chrono::Utc::now()),
                    brothers_age: Some(42),
                };
                let mut write_lock = last_birthdays_handle.write().await;
                *write_lock = last_birthdays_new_value;
                println!(
                    "<~~ Sending request to update property 'last_birthdays' to new value: {:?}",
                    *write_lock
                );
            }
            sleep(Duration::from_secs(10)).await;

            i += 1;
        }
    });

    println!("Waiting for Ctrl-C to exit...");
    tokio::signal::ctrl_c()
        .await
        .expect("Failed to listen for Ctrl-C");
    println!("Ctrl-C received, shutting down...");

    sig_rx_task1.abort();

    property_update_task.abort();

    method_calling_task.abort();

    // Join on all the signal emitting tasks.
    let _ = join!(property_update_task, sig_rx_task1, method_calling_task,);

    // Ctrl-C to stop
}
