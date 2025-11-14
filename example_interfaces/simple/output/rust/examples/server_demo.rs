/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/
use std::any::Any;

use mqttier::{Connection, MqttierClient, MqttierOptionsBuilder};
use simple_ipc::property::SimpleInitialPropertyValues;
use simple_ipc::server::{SimpleMethodHandlers, SimpleServer};
use tokio::time::{sleep, Duration};

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::Mutex;
use tracing_subscriber;

#[allow(unused_imports)]
use simple_ipc::payloads::{MethodReturnCode, *};
use tokio::join;

struct SimpleMethodImpl {
    server: Option<SimpleServer<MqttierClient>>,
}

impl SimpleMethodImpl {
    fn new() -> Self {
        Self { server: None }
    }
}

#[async_trait]
impl SimpleMethodHandlers<MqttierClient> for SimpleMethodImpl {
    async fn initialize(
        &mut self,
        server: SimpleServer<MqttierClient>,
    ) -> Result<(), MethodReturnCode> {
        self.server = Some(server.clone());
        Ok(())
    }

    async fn handle_trade_numbers(&self, _your_number: i32) -> Result<i32, MethodReturnCode> {
        println!("Handling trade_numbers");
        Ok(42)
    }

    fn as_any(&self) -> &dyn Any {
        self
    }
}

#[tokio::main]
async fn main() {
    // Initialize tracing subscriber to see log output
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    // Set up an MQTT client connection.
    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-server-demo".to_string())
        .build()
        .unwrap();
    let mut connection = MqttierClient::new(mqttier_options).unwrap();
    let _ = connection.start().await.unwrap();

    let initial_property_values = SimpleInitialPropertyValues {
        school: "apples".to_string(),
        school_version: 1,
    };

    // Create an object that implements the method handlers.
    let handlers: Arc<Mutex<Box<dyn SimpleMethodHandlers<MqttierClient>>>> =
        Arc::new(Mutex::new(Box::new(SimpleMethodImpl::new())));

    // Create the server object.
    let mut server = SimpleServer::new(
        connection,
        handlers.clone(),
        "rust-server-demo:1".to_string(),
        initial_property_values,
    )
    .await;

    // Start the server connection loop in a separate task.
    let mut looping_server = server.clone();
    let _loop_join_handle = tokio::spawn(async move {
        println!("Starting connection loop");
        let _conn_loop = looping_server.run_loop().await;
    });

    let mut server_clone1 = server.clone();
    let signal_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(1)).await;
            println!("Emitting signal 'person_entered'");
            let signal_result_future = server_clone1
                .emit_person_entered(Person {
                    name: "apples".to_string(),
                    gender: Gender::Male,
                })
                .await;
            let signal_result = signal_result_future.await;
            println!("Signal 'person_entered' was sent: {:?}", signal_result);

            sleep(Duration::from_secs(67)).await;
        }
    });

    // Provide property handles to the property_publish_task which will use them to continuously update property values.

    let school_property = server.get_school_handle();
    let property_publish_task = tokio::spawn(async move {
        loop {
            sleep(Duration::from_secs(51)).await;

            sleep(Duration::from_secs(1)).await;
            {
                println!("Changing property 'school'");
                let mut school_guard = school_property.write().await;
                *school_guard = "foo".to_string();
                // Value is changed and published when school_guard goes out of scope and is dropped.
            }
        }
    });

    let _ = join!(signal_publish_task, property_publish_task);

    // Ctrl-C to stop
}
