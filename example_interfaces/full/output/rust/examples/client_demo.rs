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
    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-client-demo".to_string())
        .build()
        .unwrap();
    let mut mqttier_client = MqttierClient::new(mqttier_options).unwrap();
    let _ = mqttier_client.start().await;

    let service_discovery = FullDiscovery::new(&mut mqttier_client).await.unwrap();
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
    let mut api_client = FullClient::new(mqttier_client.clone(), discovered_singleton).await;

    let mut client_for_loop = api_client.clone();
    tokio::spawn(async move {
        let _conn_loop = client_for_loop.run_loop().await;
    });

    let mut sig_rx = api_client.get_today_is_receiver();
    println!("Got signal receiver for todayIs");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task1 = tokio::spawn(async move {
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

    let client_for_prop_change = api_client.clone();
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

    println!("Calling echo with example values...");
    let result = api_client
        .echo("apples".to_string())
        .await
        .expect("Failed to call echo");
    println!("echo response: {:?}", result);

    println!("Calling what_time_is_it with example values...");
    let result = api_client
        .what_time_is_it(chrono::Utc::now())
        .await
        .expect("Failed to call what_time_is_it");
    println!("what_time_is_it response: {:?}", result);

    println!("Calling set_the_time with example values...");
    let result = api_client
        .set_the_time(chrono::Utc::now(), chrono::Utc::now())
        .await
        .expect("Failed to call set_the_time");
    println!("set_the_time response: {:?}", result);

    println!("Calling forward_time with example values...");
    let result = api_client
        .forward_time(chrono::Duration::seconds(3536))
        .await
        .expect("Failed to call forward_time");
    println!("forward_time response: {:?}", result);

    println!("Calling how_off_is_the_clock with example values...");
    let result = api_client
        .how_off_is_the_clock(chrono::Utc::now())
        .await
        .expect("Failed to call how_off_is_the_clock");
    println!("how_off_is_the_clock response: {:?}", result);

    let _ = api_client.set_favorite_number(42);

    let favorite_foods_new_value = FavoriteFoodsProperty {
        drink: "apples".to_string(),
        slices_of_pizza: 42,
        breakfast: Some("apples".to_string()),
    };
    let _ = api_client.set_favorite_foods(favorite_foods_new_value);

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
    let _ = api_client.set_lunch_menu(lunch_menu_new_value);

    let _ = api_client.set_family_name("apples".to_string());

    let _ = api_client.set_last_breakfast_time(chrono::Utc::now());

    let _ = api_client.set_breakfast_length(chrono::Duration::seconds(3536));

    let last_birthdays_new_value = LastBirthdaysProperty {
        mom: chrono::Utc::now(),
        dad: chrono::Utc::now(),
        sister: Some(chrono::Utc::now()),
        brothers_age: Some(42),
    };
    let _ = api_client.set_last_birthdays(last_birthdays_new_value);

    println!("Waiting for Ctrl-C to exit...");
    tokio::signal::ctrl_c()
        .await
        .expect("Failed to listen for Ctrl-C");
    println!("Ctrl-C received, shutting down...");

    sig_rx_task1.abort();

    // Join on all the signal emitting tasks.
    let _ = join!(sig_rx_task1);

    // Ctrl-C to stop
}
