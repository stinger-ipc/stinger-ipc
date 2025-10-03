//! Client module for Full IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.
*/

use full_ipc::client::FullClient;
#[allow(unused_imports)]
use full_ipc::payloads::{MethodReturnCode, *};
use futures::executor::block_on;
use mqttier::{Connection, MqttierClient, MqttierOptions};
use tokio::join;
use tokio::time::{Duration, sleep};

#[tokio::main]
async fn main() {
    block_on(async {
        let mqttier_options = MqttierOptions::new()
            .connection(Connection::TcpLocalhost(1883))
            .build();
        let mut mqttier_client = MqttierClient::new(mqttier_options).unwrap();
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

        let client_for_prop_change = api_client.clone();
        let _prop_change_rx_task = tokio::spawn(async move {
            let mut favorite_number_change_rx = client_for_prop_change.watch_favorite_number();
            let mut favorite_foods_change_rx = client_for_prop_change.watch_favorite_foods();
            let mut lunch_menu_change_rx = client_for_prop_change.watch_lunch_menu();
            let mut family_name_change_rx = client_for_prop_change.watch_family_name();
            let mut last_breakfast_time_change_rx =
                client_for_prop_change.watch_last_breakfast_time();
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
                day: DayOfTheWeek::Monday,
                order_number: Some(42),
            },
            tuesday: Lunch {
                drink: true,
                sandwich: "apples".to_string(),
                crackers: 3.14,
                day: DayOfTheWeek::Monday,
                order_number: Some(42),
            },
        };
        let _ = api_client.set_lunch_menu(lunch_menu_new_value);

        let _ = api_client.set_family_name("apples".to_string());

        let _ = api_client.set_last_breakfast_time(chrono::Utc::now());

        let last_birthdays_new_value = LastBirthdaysProperty {
            mom: chrono::Utc::now(),
            dad: chrono::Utc::now(),
            sister: chrono::Utc::now(),
        };
        let _ = api_client.set_last_birthdays(last_birthdays_new_value);

        let _ = join!(sig_rx_task);
    });
    // Ctrl-C to stop
}
