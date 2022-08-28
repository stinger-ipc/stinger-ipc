
use signal_only_server::SignalOnlyServer;
use connection::Connection;


fn main() {
    
    let connection = Connection::new_default_connection(String::from("localhost"), 1883);
    let mut server = SignalOnlyServer::new(connection);
    
    server.emit_another_signal(3.14, true, "apples".to_string());
    

}