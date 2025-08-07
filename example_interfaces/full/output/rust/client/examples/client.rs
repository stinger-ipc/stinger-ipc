use futures::{executor::block_on};
use example_client::ExampleClient;
use connection::Connection;


fn print_today_is(day_of_month: i32, day_of_week: connection::payloads::DayOfTheWeek) {
    println!("Got a 'todayIs' signal:{} {} ", day_of_month, day_of_week);
}


#[tokio::main]
async fn main() {
    block_on(async {
        
        let connection = Connection::new_local_connection().await.expect("Failed to create connection");
        let mut client = ExampleClient::new(connection).await;
        
        client.set_signal_recv_callbacks_for_today_is(print_today_is);
        
        client.process_loop().await;
    });
    // Ctrl-C to stop
}