/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/
use std::any::Any;

use full_ipc::property::FullInitialPropertyValues;
use full_ipc::server::{FullMethodHandlers, FullServer};
use mqttier::{Connection, MqttierClient, MqttierOptionsBuilder};
use tokio::time::{sleep, Duration};

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;
use tracing_subscriber;

#[allow(unused_imports)]
use full_ipc::payloads::{MethodReturnCode, *};
use tokio::join;

struct FullMethodImpl {
    server: Option<FullServer<MqttierClient>>,
}

impl FullMethodImpl {
    fn new() -> Self {
        Self { server: None }
    }
}

#[async_trait]
impl FullMethodHandlers<MqttierClient> for FullMethodImpl {
    async fn initialize(
        &mut self,
        server: FullServer<MqttierClient>,
    ) -> Result<(), MethodReturnCode> {
        self.server = Some(server.clone());
        Ok(())
    }

    async fn handle_add_numbers(
        &self,
        _first: i32,
        _second: i32,
        _third: Option<i32>,
    ) -> Result<i32, MethodReturnCode> {
        println!("Handling addNumbers");
        Ok(42)
    }

    async fn handle_do_something(
        &self,
        _task_to_do: String,
    ) -> Result<DoSomethingReturnValues, MethodReturnCode> {
        println!("Handling doSomething");
        let rv = DoSomethingReturnValues {
            label: "apples".to_string(),
            identifier: 42,
        };
        Ok(rv)
    }

    async fn handle_what_time_is_it(
        &self,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> {
        println!("Handling what_time_is_it");
        Ok(chrono::Utc::now())
    }

    async fn handle_hold_temperature(
        &self,
        _temperature_celsius: f32,
    ) -> Result<bool, MethodReturnCode> {
        println!("Handling hold_temperature");
        Ok(true)
    }

    fn as_any(&self) -> &dyn Any {
        self
    }
}

#[tokio::main]
async fn main() {
    // Initialize tracing subscriber to see log output
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    // Set up an MQTT client connection.
    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-server-demo".to_string())
        .build()
        .unwrap();
    let mut connection = MqttierClient::new(mqttier_options).unwrap();
    let _ = connection.start().await.unwrap();

    let initial_property_values = FullInitialPropertyValues {
        favorite_number: 42,
        favorite_number_version: 1,

        favorite_foods: FavoriteFoodsProperty {
            drink: "apples".to_string(),
            slices_of_pizza: 42,
            breakfast: Some("apples".to_string()),
        },
        favorite_foods_version: 1,

        lunch_menu: LunchMenuProperty {
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
        },
        lunch_menu_version: 1,

        family_name: "apples".to_string(),
        family_name_version: 1,

        last_breakfast_time: chrono::Utc::now(),
        last_breakfast_time_version: 1,

        last_birthdays: LastBirthdaysProperty {
            mom: chrono::Utc::now(),
            dad: chrono::Utc::now(),
            sister: Some(chrono::Utc::now()),
            brothers_age: Some(42),
        },
        last_birthdays_version: 1,
    };

    // Create an object that implements the method handlers.
    let handlers: Arc<Mutex<Box<dyn FullMethodHandlers<MqttierClient>>>> =
        Arc::new(Mutex::new(Box::new(FullMethodImpl::new())));

    // Create the server object.
    let mut server = FullServer::new(
        connection,
        handlers.clone(),
        "rust-server-demo:1".to_string(),
        initial_property_values,
    )
    .await;

    // Start the server connection loop in a separate task.
    let mut looping_server = server.clone();
    let _loop_join_handle = tokio::spawn(async move {
        println!("Starting connection loop");
        let _conn_loop = looping_server.run_loop().await;
    });

    let mut server_clone1 = server.clone();
    let signal_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'todayIs'");
            let signal_result_future = server_clone1
                .emit_today_is(42, DayOfTheWeek::Saturday)
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'todayIs' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'randomWord'");
            let signal_result_future = server_clone1
                .emit_random_word("apples".to_string(), chrono::Utc::now())
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'randomWord' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(67)).await;
        }
    });

    // Provide property handles to the property_publish_task which will use them to continuously update property values.

    let favorite_number_property = server.get_favorite_number_handle();

    let favorite_foods_property = server.get_favorite_foods_handle();

    let lunch_menu_property = server.get_lunch_menu_handle();

    let family_name_property = server.get_family_name_handle();

    let last_breakfast_time_property = server.get_last_breakfast_time_handle();

    let last_birthdays_property = server.get_last_birthdays_handle();
    let property_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(51)).await;

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'favorite_number'");
                let mut favorite_number_guard = favorite_number_property.write().await;
                *favorite_number_guard = 2022;
                // Value is changed and published when favorite_number_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'favorite_foods'");
                let mut favorite_foods_guard = favorite_foods_property.write().await;
                let new_favorite_foods_value = FavoriteFoodsProperty {
                    drink: "foo".to_string(),
                    slices_of_pizza: 2022,
                    breakfast: Some("foo".to_string()),
                };
                *favorite_foods_guard = new_favorite_foods_value;
                // Value is changed and published when favorite_foods_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'lunch_menu'");
                let mut lunch_menu_guard = lunch_menu_property.write().await;
                let new_lunch_menu_value = LunchMenuProperty {
                    monday: Lunch {
                        drink: true,
                        sandwich: "foo".to_string(),
                        crackers: 1.0,
                        day: DayOfTheWeek::Monday,
                        order_number: Some(2022),
                        time_of_lunch: chrono::Utc::now(),
                        duration_of_lunch: chrono::Duration::seconds(967),
                    },
                    tuesday: Lunch {
                        drink: true,
                        sandwich: "foo".to_string(),
                        crackers: 1.0,
                        day: DayOfTheWeek::Monday,
                        order_number: Some(2022),
                        time_of_lunch: chrono::Utc::now(),
                        duration_of_lunch: chrono::Duration::seconds(967),
                    },
                };
                *lunch_menu_guard = new_lunch_menu_value;
                // Value is changed and published when lunch_menu_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'family_name'");
                let mut family_name_guard = family_name_property.write().await;
                *family_name_guard = "foo".to_string();
                // Value is changed and published when family_name_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'last_breakfast_time'");
                let mut last_breakfast_time_guard = last_breakfast_time_property.write().await;
                *last_breakfast_time_guard = chrono::Utc::now();
                // Value is changed and published when last_breakfast_time_guard goes out of scope and is dropped.
            }

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'last_birthdays'");
                let mut last_birthdays_guard = last_birthdays_property.write().await;
                let new_last_birthdays_value = LastBirthdaysProperty {
                    mom: chrono::Utc::now(),
                    dad: chrono::Utc::now(),
                    sister: Some(chrono::Utc::now()),
                    brothers_age: Some(2022),
                };
                *last_birthdays_guard = new_last_birthdays_value;
                // Value is changed and published when last_birthdays_guard goes out of scope and is dropped.
            }
        }
    });

    let _ = join!(signal_publish_task, property_publish_task);

    // Ctrl-C to stop
}
