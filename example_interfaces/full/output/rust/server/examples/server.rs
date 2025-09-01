/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/
use futures::{executor::block_on};
use mqttier::MqttierClient;
use full_server::FullServer;
use tokio::time::{sleep, Duration};
use tokio::join;

#[allow(unused_imports)]
use full_types::payloads::{MethodResultCode, *};


fn add_numbers_handler(_first: i32, _second: i32, _third: Option<i32>) -> Result<i32, MethodResultCode> {
    println!("Handling addNumbers");
    Ok(42)
    
}

fn do_something_handler(_a_string: String) -> Result<DoSomethingReturnValue, MethodResultCode> {
    println!("Handling doSomething");
    let rv = DoSomethingReturnValue {
        label: "apples".to_string(),
        identifier: 42,
        day: DayOfTheWeek::Monday,
        
    };
    Ok(rv)
    
}



#[tokio::main]
async fn main() {
    block_on(async {
        
        let mut connection = MqttierClient::new("localhost", 1883, None).unwrap();
        let mut server = FullServer::new(&mut connection).await;
        
        let loop_task = tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = connection.run_loop().await;
        });
        
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
                monday: Lunch {drink: true, sandwich: "apples".to_string(), crackers: 3.14, day: DayOfTheWeek::Monday, order_number: Some(42)},
                tuesday: Lunch {drink: true, sandwich: "apples".to_string(), crackers: 3.14, day: DayOfTheWeek::Monday, order_number: Some(42)},
        };
        server.set_lunch_menu(new_value).await;
        
        
        server.set_method_handler_for_add_numbers(add_numbers_handler);
        
        server.set_method_handler_for_do_something(do_something_handler);
        
        
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
                monday: Lunch {drink: true, sandwich: "Joe".to_string(), crackers: 1.0, day: DayOfTheWeek::Monday, order_number: Some(2022)},
                tuesday: Lunch {drink: true, sandwich: "Joe".to_string(), crackers: 1.0, day: DayOfTheWeek::Monday, order_number: Some(2022)},
        };
        server.set_lunch_menu(new_value).await;
        
        let _ = server.receive_loop().await;
        let _ = join!(loop_task);
    });
    // Ctrl-C to stop
}