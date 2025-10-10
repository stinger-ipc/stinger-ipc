/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/
use full_ipc::server::{FullMethodHandlers, FullServer};
use futures::executor::block_on;
use mqttier::{Connection, MqttierClient, MqttierOptions};
use std::any::Any;
use tokio::time::{Duration, sleep};

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;

#[allow(unused_imports)]
use full_ipc::payloads::{MethodReturnCode, *};

struct FullMethodImpl {
    server: Option<FullServer>,
}

impl FullMethodImpl {
    fn new() -> Self {
        Self { server: None }
    }
}

#[async_trait]
impl FullMethodHandlers for FullMethodImpl {
    async fn initialize(&mut self, server: FullServer) -> Result<(), MethodReturnCode> {
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
        _a_string: String,
    ) -> Result<DoSomethingReturnValues, MethodReturnCode> {
        println!("Handling doSomething");
        let rv = DoSomethingReturnValues {
            label: "apples".to_string(),
            identifier: 42,
            day: DayOfTheWeek::Saturday,
        };
        Ok(rv)
    }

    async fn handle_echo(&self, _message: String) -> Result<String, MethodReturnCode> {
        println!("Handling echo");
        Ok("apples".to_string())
    }

    async fn handle_what_time_is_it(
        &self,
        _the_first_time: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> {
        println!("Handling what_time_is_it");
        Ok(chrono::Utc::now())
    }

    async fn handle_set_the_time(
        &self,
        _the_first_time: chrono::DateTime<chrono::Utc>,
        _the_second_time: chrono::DateTime<chrono::Utc>,
    ) -> Result<SetTheTimeReturnValues, MethodReturnCode> {
        println!("Handling set_the_time");
        let rv = SetTheTimeReturnValues {
            timestamp: chrono::Utc::now(),
            confirmation_message: "apples".to_string(),
        };
        Ok(rv)
    }

    async fn handle_forward_time(
        &self,
        _adjustment: chrono::Duration,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> {
        println!("Handling forward_time");
        Ok(chrono::Utc::now())
    }

    async fn handle_how_off_is_the_clock(
        &self,
        _actual_time: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::Duration, MethodReturnCode> {
        println!("Handling how_off_is_the_clock");
        Ok(chrono::Duration::seconds(3536))
    }

    fn as_any(&self) -> &dyn Any {
        self
    }
}

#[tokio::main]
async fn main() {
    block_on(async {
        let mqttier_options = MqttierOptions::new()
            .connection(Connection::TcpLocalhost(1883))
            .client_id("rust-server-demo".to_string())
            .build();
        let mut connection = MqttierClient::new(mqttier_options).unwrap();

        let handlers: Arc<Mutex<Box<dyn FullMethodHandlers>>> =
            Arc::new(Mutex::new(Box::new(FullMethodImpl::new())));

        let mut server = FullServer::new(
            &mut connection,
            handlers.clone(),
            "rust-server-demo:1".to_string(),
        )
        .await;

        let mut looping_server = server.clone();
        tokio::spawn(async move {
            println!("Starting connection loop");
            let _conn_loop = looping_server.run_loop().await;
        });

        println!("Setting initial value for property 'favorite_number'");
        let prop_init_future = server.set_favorite_number(42).await;
        if let Err(e) = prop_init_future.await {
            eprintln!("Error initializing property 'favorite_number': {:?}", e);
        }

        println!("Setting initial value for property 'favorite_foods'");
        let new_value = FavoriteFoodsProperty {
            drink: "apples".to_string(),
            slices_of_pizza: 42,
            breakfast: Some("apples".to_string()),
        };
        let prop_init_future = server.set_favorite_foods(new_value).await;

        if let Err(e) = prop_init_future.await {
            eprintln!("Error initializing property 'favorite_foods': {:?}", e);
        }

        println!("Setting initial value for property 'lunch_menu'");
        let new_value = LunchMenuProperty {
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
        let prop_init_future = server.set_lunch_menu(new_value).await;

        if let Err(e) = prop_init_future.await {
            eprintln!("Error initializing property 'lunch_menu': {:?}", e);
        }

        println!("Setting initial value for property 'family_name'");
        let prop_init_future = server.set_family_name("apples".to_string()).await;
        if let Err(e) = prop_init_future.await {
            eprintln!("Error initializing property 'family_name': {:?}", e);
        }

        println!("Setting initial value for property 'last_breakfast_time'");
        let prop_init_future = server.set_last_breakfast_time(chrono::Utc::now()).await;
        if let Err(e) = prop_init_future.await {
            eprintln!("Error initializing property 'last_breakfast_time': {:?}", e);
        }

        println!("Setting initial value for property 'breakfast_length'");
        let prop_init_future = server
            .set_breakfast_length(chrono::Duration::seconds(3536))
            .await;
        if let Err(e) = prop_init_future.await {
            eprintln!("Error initializing property 'breakfast_length': {:?}", e);
        }

        println!("Setting initial value for property 'last_birthdays'");
        let new_value = LastBirthdaysProperty {
            mom: chrono::Utc::now(),
            dad: chrono::Utc::now(),
            sister: chrono::Utc::now(),
            brothers_age: Some(42),
        };
        let prop_init_future = server.set_last_birthdays(new_value).await;

        if let Err(e) = prop_init_future.await {
            eprintln!("Error initializing property 'last_birthdays': {:?}", e);
        }

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'todayIs'");
        let signal_result_future = server
            .emit_today_is(
                42,
                Some(DayOfTheWeek::Saturday),
                chrono::Utc::now(),
                chrono::Duration::seconds(3536),
                vec![101, 120, 97, 109, 112, 108, 101],
            )
            .await;
        let signal_result = signal_result_future.await;
        println!("Signal 'todayIs' was sent: {:?}", signal_result);

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'favorite_number'");
        let prop_change_future = server.set_favorite_number(2022).await;
        if let Err(e) = prop_change_future.await {
            eprintln!("Error changing property 'favorite_number': {:?}", e);
        }

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'favorite_foods'");
        let new_value = FavoriteFoodsProperty {
            drink: "foo".to_string(),
            slices_of_pizza: 2022,
            breakfast: Some("foo".to_string()),
        };
        let _ = server.set_favorite_foods(new_value).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'lunch_menu'");
        let new_value = LunchMenuProperty {
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
        let _ = server.set_lunch_menu(new_value).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'family_name'");
        let prop_change_future = server.set_family_name("foo".to_string()).await;
        if let Err(e) = prop_change_future.await {
            eprintln!("Error changing property 'family_name': {:?}", e);
        }

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'last_breakfast_time'");
        let prop_change_future = server.set_last_breakfast_time(chrono::Utc::now()).await;
        if let Err(e) = prop_change_future.await {
            eprintln!("Error changing property 'last_breakfast_time': {:?}", e);
        }

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'breakfast_length'");
        let prop_change_future = server
            .set_breakfast_length(chrono::Duration::seconds(975))
            .await;
        if let Err(e) = prop_change_future.await {
            eprintln!("Error changing property 'breakfast_length': {:?}", e);
        }

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'last_birthdays'");
        let new_value = LastBirthdaysProperty {
            mom: chrono::Utc::now(),
            dad: chrono::Utc::now(),
            sister: chrono::Utc::now(),
            brothers_age: Some(2022),
        };
        let _ = server.set_last_birthdays(new_value).await;
    });
    // Ctrl-C to stop
}
