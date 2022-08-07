use futures::{executor::block_on};

use connection::Connection;


fn print_another_signal(i: u32) {
    println!("Got a 'anotherSignal' signal: {}", i);
}


fn main() {
    
    let mut connection = Connection::new(String::from("tcp://localhost:1883"));
    let mut client = lib::SignalOnlyClient::new(connection);
    
    client.set_signal_recv_callbacks_for_another_signal(print_another_signal);
    
    block_on(async {
        client.process().await;
    });
    // Ctrl-C to stop
}