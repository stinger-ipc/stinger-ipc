
extern crate uuid;
extern crate paho_mqtt as mqtt;

use std::process;
use std::time::Duration;
use std::thread;
use uuid::Uuid;

pub mod enums;
pub mod return_structs;

pub struct Connection {
    pub cli: mqtt::AsyncClient,
    pub client_id: String,
    next_subsc_id_range: u32,
}

impl Connection {

    pub async fn new_with_client_id(uri: String, client_id: String) -> Connection {
        let create_opts = mqtt::CreateOptionsBuilder::new()
            .server_uri(uri)
            .client_id(client_id.clone())
            .mqtt_version(mqtt::MQTT_VERSION_5)
            .allow_disconnected_send_at_anytime(true)
            .finalize();

        let mut cli = mqtt::AsyncClient::new(create_opts).unwrap_or_else(|err| {
            println!("Error creating the client: {:?}", err);
            process::exit(1);
        });

        let conn_opts = mqtt::ConnectOptionsBuilder::new_v5()
            .keep_alive_interval(Duration::from_secs(20))
            .clean_start(true)
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
            client_id: client_id,
            next_subsc_id_range: 1000,
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
    

    pub async fn publish(&mut self, topic: String, message: String, qos: u8, correlation_data: Option<Vec<u8>>) -> Result<u32, mqtt::Error> {

        // Create PUBLISH properties
        let mut properties = mqtt::Properties::new();

        if let Some(cd) = correlation_data {
            let prop = mqtt::Property::new(mqtt::PropertyCode::CorrelationData, cd)?;
            properties.push(prop)?;
        }

        // Create a message and publish it
        let msg = mqtt::MessageBuilder::new()
            .topic(topic)
            .payload(message)
            .qos(qos as u32)
            .finalize();
        let tok = self.cli.publish(msg);
    
        if let Err(e) = tok.await {
            println!("Error sending message: {:?}", e);
        }

        Ok(1)
    }

    pub fn subscribe(&mut self, topic: String, qos: i32, subscription_identifier: Option<u32>) {
        let subscribe_options = mqtt::SubscribeOptions::new(true, false, mqtt::RetainHandling::SendRetainedOnSubscribe);
        let mut subscribe_properties = mqtt::Properties::new();
        if let Some(si) = subscription_identifier {
            let prop = mqtt::Property::new(mqtt::PropertyCode::SubscriptionIdentifier, si as i32);
            match prop {
                Ok(prop) => {
                    let prop_add_result = subscribe_properties.push(prop);
                    if let Err(e) = prop_add_result {
                        println!("Error adding subscription identifier property: {:?}", e);
                    }
                    ()
                },
                Err(prop) => println!("Error with creating Subscription Identifier property: {}", prop),
            }
            
        }
        self.cli.subscribe_with_options(topic, qos, subscribe_options, subscribe_properties);
    }

    pub fn get_subcr_id_range_start(&mut self) -> u32 {
        let subsc_id = self.next_subsc_id_range;
        self.next_subsc_id_range += 1000;
        subsc_id
    }
}

impl Drop for Connection {
    fn drop(&mut self) {
        // Disconnect from the broker
        let tok = self.cli.disconnect(None);
        tok.wait().unwrap();
    }
}