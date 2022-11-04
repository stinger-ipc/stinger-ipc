/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Example interface.
*/
use futures::{executor::block_on};
use example_server::ExampleServer;
use connection::Connection;
use connection::return_structs::MethodResultCode;


fn add_numbers_handler(_first: i32, _second: i32) -> Result<i32, MethodResultCode> {
    println!("Handling addNumbers");
    Ok(42)
    
}

fn do_something_handler(_a_string: String) -> Result<connection::return_structs::DoSomethingReturnValue, MethodResultCode> {
    println!("Handling doSomething");
    let rv = connection::return_structs::DoSomethingReturnValue {
        
        label: "apples".to_string(),
        
        identifier: 42,
        
        day: connection::enums::DayOfTheWeek::Monday,
        
    };
    Ok(rv)
    
}


fn main() {
    block_on(async {
        
        let connection = Connection::new_local_connection().await;
        let mut server = ExampleServer::new(connection).await;
        
        server.set_method_handler_for_add_numbers(add_numbers_handler);
        
        server.set_method_handler_for_do_something(do_something_handler);
        
        
        server.emit_today_is(42, connection::enums::DayOfTheWeek::Monday).await;
        

    
        server.process().await;
    });
    // Ctrl-C to stop
}