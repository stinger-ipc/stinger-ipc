//! Client module for Full IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

use mqttier::{Connection, MqttierClient, MqttierOptionsBuilder};
use simple_ipc::client::SimpleClient;
use simple_ipc::discovery::SimpleDiscovery;
#[allow(unused_imports)]
use simple_ipc::payloads::{MethodReturnCode, *};
use tokio::join;
use tokio::time::{sleep, Duration};
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};
#[tokio::main]
async fn main() {
    // Initialize tracing subscriber to see log output
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info")),
        )
        .init();

    info!("Starting Simple client demo...");
    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-client-demo".to_string())
        .build()
        .unwrap();
    let mut mqttier_client = MqttierClient::new(mqttier_options).unwrap();
    let _ = mqttier_client.start().await.unwrap();

    let discovery = SimpleDiscovery::new(&mut mqttier_client).await.unwrap();
    let singleton_info = discovery.get_singleton_service().await;

    let mut api_client = SimpleClient::new(mqttier_client.clone(), singleton_info.instance).await;

    let mut client_for_loop = api_client.clone();
    tokio::spawn(async move {
        let _conn_loop = client_for_loop.run_loop().await;
    });

    let mut sig_rx = api_client.get_person_entered_receiver();
    println!("Got signal receiver for person_entered");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task1 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received person_entered signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving person_entered signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let client_for_prop_change = api_client.clone();
    let _prop_change_rx_task = tokio::spawn(async move {
        let mut school_change_rx = client_for_prop_change.watch_school();

        loop {
            tokio::select! {
                _ = school_change_rx.changed() => {
                    println!("Property 'school' changed to: {:?}", *school_change_rx.borrow());
                }
            }
        }
    });

    println!("Calling trade_numbers with example values...");
    let result = api_client
        .trade_numbers(42)
        .await
        .expect("Failed to call trade_numbers");
    println!("trade_numbers response: {:?}", result);

    let _ = api_client.set_school("apples".to_string());

    // Join on all the signal emitting tasks.
    let _ = join!(sig_rx_task1);

    // Ctrl-C to stop
}
