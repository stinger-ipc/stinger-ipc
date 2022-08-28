
use example_server::ExampleServer;
use connection::Connection;


fn main() {
    
    let connection = Connection::new_local_connection();
    let mut server = ExampleServer::new(connection);
    
    server.emit_today_is(42, connection::enums::DayOfTheWeek::Monday);
    

}