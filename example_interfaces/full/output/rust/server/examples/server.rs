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

//use full_server::handler::FullMethodHandlers;
//use full_server::init::Initializable;
#[allow(unused_imports)]
use full_types::payloads::{MethodResultCode, *};
use std::sync::{Arc, Mutex};

struct FullMethodImpl {
    server: Option<FullServer>,
}

impl FullMethodImpl {
    fn new() -> Self {
        Self { server: None }
    }
}

impl FullMethodHandlers for FullMethodImpl {
    fn initialize(&mut self, server: FullServer) -> Result<(), MethodResultCode> {
        self.server = Some(server.clone());
        Ok(())
    }

    fn handle_add_numbers(
        &self,
        _first: i32,
        _second: i32,
        _third: Option<i32>,
    ) -> Result<i32, MethodResultCode> {
        println!("Handling addNumbers");
        Ok(42)
    }

    fn handle_do_something(
        &self,
        _a_string: String,
    ) -> Result<DoSomethingReturnValue, MethodResultCode> {
        println!("Handling doSomething");
        let rv = DoSomethingReturnValue {
            label: "apples".to_string(),
            identifier: 42,
            day: DayOfTheWeek::Monday,
        };
        Ok(rv)
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

        sleep(Duration::from_secs(1)).await;
        println!("Emitting signal 'todayIs'");
        server.emit_today_is(42, Some(DayOfTheWeek::Monday)).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'favorite_number'");
        server.set_favorite_number(2022).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'favorite_foods'");
        let new_value = FavoriteFoodsProperty {
            drink: "Joe".to_string(),
            slices_of_pizza: 2022,
            breakfast: Some("Joe".to_string()),
        };
        server.set_favorite_foods(new_value).await;

        sleep(Duration::from_secs(1)).await;
        println!("Changing property 'lunch_menu'");
        let new_value = LunchMenuProperty {
            monday: Lunch {
                drink: true,
                sandwich: "Joe".to_string(),
                crackers: 1.0,
                day: DayOfTheWeek::Monday,
                order_number: Some(2022),
            },
            tuesday: Lunch {
                drink: true,
                sandwich: "Joe".to_string(),
                crackers: 1.0,
                day: DayOfTheWeek::Monday,
                order_number: Some(2022),
            },
        };
        server.set_lunch_menu(new_value).await;

        let _server_loop_task = server.run_loop().await;
    });
    // Ctrl-C to stop
}
