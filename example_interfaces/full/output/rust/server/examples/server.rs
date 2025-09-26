/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/
use full_server::{FullMethodHandlers, FullServer};
use futures::executor::block_on;
use mqttier::MqttierClient;
use std::any::Any;
use tokio::time::{Duration, sleep};

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;

use full_types::MethodReturnCode;
#[allow(unused_imports)]
use full_types::payloads::*;

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
    ) -> Result<DoSomethingReturnValue, MethodReturnCode> {
        println!("Handling doSomething");
        let rv = DoSomethingReturnValue {
            label: "apples".to_string(),
            identifier: 42,
            day: DayOfTheWeek::Monday,
        };
        Ok(rv)
    }

    async fn handle_echo(&self, _message: String) -> Result<String, MethodReturnCode> {
        println!("Handling echo");
        Ok("apples".to_string())
    }

    fn as_any(&self) -> &dyn Any {
        self
    }
}

#[tokio::main]
async fn main() {
    env_logger::Builder::from_default_env()
        .target(env_logger::Target::Stdout)
        .init();

    block_on(async {
        let mut connection = MqttierClient::new("localhost", 1883, None).unwrap();

        let handlers: Arc<Mutex<Box<dyn FullMethodHandlers>>> =
            Arc::new(Mutex::new(Box::new(FullMethodImpl::new())));
        let mut server = FullServer::new(&mut connection, handlers.clone()).await;

        println!("Setting initial value for property 'favorite_number'");
        server.set_favorite_number(42).await;

        println!("Setting initial value for property 'favorite_foods'");
        let new_value = FavoriteFoodsProperty {
            drink: "apples".to_string(),
            slices_of_pizza: 42,
            breakfast: Some("apples".to_string()),
        };
        server.set_favorite_foods(new_value).await;

        println!("Setting initial value for property 'lunch_menu'");
        let new_value = LunchMenuProperty {
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
        server.set_lunch_menu(new_value).await;

        println!("Setting initial value for property 'family_name'");
        server.set_family_name("apples".to_string()).await;

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'todayIs'");
        let signal_result_future = server.emit_today_is(42, Some(DayOfTheWeek::Monday)).await;
        let signal_result = signal_result_future.await;
        println!("Signal 'todayIs' was sent: {:?}", signal_result);

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'favorite_number'");
        server.set_favorite_number(2022).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'favorite_foods'");
        let new_value = FavoriteFoodsProperty {
            drink: "foo".to_string(),
            slices_of_pizza: 2022,
            breakfast: Some("foo".to_string()),
        };
        server.set_favorite_foods(new_value).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'lunch_menu'");
        let new_value = LunchMenuProperty {
            monday: Lunch {
                drink: true,
                sandwich: "foo".to_string(),
                crackers: 1.0,
                day: DayOfTheWeek::Monday,
                order_number: Some(2022),
            },
            tuesday: Lunch {
                drink: true,
                sandwich: "foo".to_string(),
                crackers: 1.0,
                day: DayOfTheWeek::Monday,
                order_number: Some(2022),
            },
        };
        server.set_lunch_menu(new_value).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'family_name'");
        server.set_family_name("foo".to_string()).await;
        let _server_loop_task = server.run_loop().await;
    });
    // Ctrl-C to stop
}
