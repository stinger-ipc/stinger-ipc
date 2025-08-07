use futures::{executor::block_on};
use signal_only_client::SignalOnlyClient;
use connection::Connection;


fn print_another_signal(one: f32, two: bool, three: String) {
    println!("Got a 'anotherSignal' signal:{} {} {} ", one, two, three);
}


#[tokio::main]
async fn main() {
    block_on(async {
        
        let connection = Connection::new_default_connection().await.expect("Failed to create connection");
        let mut client = SignalOnlyClient::new(connection).await;
        
        client.set_signal_recv_callbacks_for_another_signal(print_another_signal).await;
        
        client.process_loop().await;
    });
    // Ctrl-C to stop
}