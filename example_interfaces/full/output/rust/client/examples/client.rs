use futures::{executor::block_on};

use connection::Connection;


fn print_today_is(i: u32) {
    println!("Got a 'todayIs' signal: {}", i);
}


fn main() {
    
    let mut connection = Connection::new(String::from("tcp://127.0.0.1:1883"));
    let mut client = lib::ExampleClient::new(connection);
    
    client.set_signal_recv_callbacks_for_today_is(print_today_is);
    
    block_on(async {
        client.process().await;
    });
    // Ctrl-C to stop
}