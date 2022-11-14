
extern crate uuid;
extern crate paho_mqtt as mqtt;

use std::process;
use std::time::Duration;
use std::thread;
use uuid::Uuid;

pub mod enums;
pub mod return_structs;

pub struct Connection {
    cli: mqtt::AsyncClient,
    pub rx: mqtt::AsyncReceiver<Option<mqtt::Message>>,
    pub client_id: String,
}

impl Connection {

    pub async fn new_with_client_id(uri: String, client_id: String) -> Connection {
        let create_opts = mqtt::CreateOptionsBuilder::new()
            .server_uri(uri)
            .client_id(client_id.clone())
            .finalize();

        let mut cli = mqtt::AsyncClient::new(create_opts).unwrap_or_else(|err| {
            println!("Error creating the client: {:?}", err);
            process::exit(1);
        });

        let rx = cli.get_stream(1024);

        let conn_opts = mqtt::ConnectOptionsBuilder::new()
            .keep_alive_interval(Duration::from_secs(20))
            .clean_session(true)
            .finalize();

        // Connect and wait for it to complete or fail
        if let Err(e) = cli.connect(conn_opts).await {
            println!("Unable to connect:\n\t{:?}", e);
            process::exit(1);
        }

        // Set a closure to be called whenever the client loses the connection.
        // It will attempt to reconnect, and set up function callbacks to keep
        // retrying until the connection is re-established.
        cli.set_connection_lost_callback(|cli: &mqtt::AsyncClient| {
            println!("Connection lost. Attempting reconnect.");
            thread::sleep(Duration::from_millis(2500));
            cli.reconnect();
        });

       
        Connection { 
            cli: cli, 
            rx: rx,
            client_id: client_id
        }
    }

    pub async fn new(uri: String) -> Connection {
        let client_id = format!("{}", Uuid::new_v4());
        let conn: Connection = Self::new_with_client_id(uri, client_id).await;
        conn
    }

    
    pub async fn new_default_connection (hostname: String, port: u32) -> Connection {
        let uri = format!("tcp://{}:{}", hostname, port);
        Connection::new(uri).await
    }
    

    pub async fn publish(&mut self, topic: String, message: String, qos: u8) {
        // Create a message and publish it
        let msg = mqtt::Message::new(topic, message, qos.into());
        let tok = self.cli.publish(msg);
    
        if let Err(e) = tok.await {
            println!("Error sending message: {:?}", e);
        }
    }

    pub fn subscribe(&mut self, topic: String, qos: i32) {
        self.cli.subscribe(topic, qos);
    }
}

impl Drop for Connection {
    fn drop(&mut self) {
        // Disconnect from the broker
        let tok = self.cli.disconnect(None);
        tok.wait().unwrap();
    }
}