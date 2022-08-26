
use example_server::ExampleServer;
use connection::Connection;


fn main() {
    
    let connection = Connection::new(String::from("tcp://127.0.0.1:1883"));
    let mut server = ExampleServer::new(connection);
    
    server.emit_today_is(42, connection::enums::DayOfTheWeek::Monday);
    

}