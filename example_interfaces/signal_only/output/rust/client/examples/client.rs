use futures::{executor::block_on};
use signal_only_client::SignalOnlyClient;
use connection::Connection;


fn print_another_signal(one: f32, two: bool, three: String) {
    println!("Got a 'anotherSignal' signal:{} {} {} ", one, two, three);
}


fn main() {
    
    let connection = Connection::new_default_connection(String::from("localhost"), 1883);
    let mut client = SignalOnlyClient::new(connection);
    
    client.set_signal_recv_callbacks_for_another_signal(print_another_signal);
    
    block_on(async {
        client.process().await;
    });
    // Ctrl-C to stop
}