use futures::{executor::block_on};
use example_client::ExampleClient;
use connection::Connection;


fn print_today_is(day_of_month: i32, day_of_week: connection::enums::DayOfTheWeek) {
    println!("Got a 'todayIs' signal:{} {} ", day_of_month, day_of_week);
}


fn main() {
    
    let connection = Connection::new(String::from("tcp://127.0.0.1:1883"));
    let mut client = ExampleClient::new(connection);
    
    client.set_signal_recv_callbacks_for_today_is(print_today_is);
    
    block_on(async {
        client.process().await;
    });
    // Ctrl-C to stop
}