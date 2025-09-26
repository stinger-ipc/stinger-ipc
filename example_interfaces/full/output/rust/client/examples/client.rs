use full_client::FullClient;
#[allow(unused_imports)]
use full_types::{MethodReturnCode, *};
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

        let client_for_prop_change = api_client.clone();
        let _prop_change_rx_task = tokio::spawn(async move {
            let mut favorite_number_change_rx = client_for_prop_change.watch_favorite_number();
            let mut favorite_foods_change_rx = client_for_prop_change.watch_favorite_foods();
            let mut lunch_menu_change_rx = client_for_prop_change.watch_lunch_menu();
            let mut family_name_change_rx = client_for_prop_change.watch_family_name();

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

        let _ = join!(sig_rx_task);
    });
    // Ctrl-C to stop
}
