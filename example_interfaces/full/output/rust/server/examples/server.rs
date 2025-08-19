/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Example interface.
*/
use futures::{executor::block_on};
use example_server::ExampleServer;
use connection::Connection;
use tokio::time::{sleep, Duration};
use tokio::join;
use connection::payloads::MethodResultCode;


fn add_numbers_handler(_first: i32, _second: i32, _third: Option<i32>) -> Result<i32, MethodResultCode> {
    println!("Handling addNumbers");
    Ok(42)
    
}

fn do_something_handler(_a_string: String) -> Result<connection::payloads::DoSomethingReturnValue, MethodResultCode> {
    println!("Handling doSomething");
    let rv = connection::payloads::DoSomethingReturnValue {
        
        label: "apples".to_string(),
        
        identifier: 42,
        
        day: connection::payloads::DayOfTheWeek::Monday,
        
    };
    Ok(rv)
    
}



#[tokio::main]
async fn main() {
    block_on(async {
        
        let mut connection = Connection::new_local_connection().await.unwrap();
        let mut server = ExampleServer::new(&mut connection).await;

        let loop_task = tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = connection.start_loop().await;
        });

        
        server.set_method_handler_for_add_numbers(add_numbers_handler);
        
        server.set_method_handler_for_do_something(do_something_handler);
        

        
        server.emit_today_is(42, Some(connection::payloads::DayOfTheWeek::Monday)).await;
        

        server.receive_loop().await;
        join!(loop_task);
    });
    // Ctrl-C to stop
}