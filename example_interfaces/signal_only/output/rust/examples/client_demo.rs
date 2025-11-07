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
use signal_only_ipc::client::SignalOnlyClient;
use signal_only_ipc::discovery::SignalOnlyDiscovery;
#[allow(unused_imports)]
use signal_only_ipc::payloads::{MethodReturnCode, *};
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

    info!("Starting SignalOnly client demo...");
    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-client-demo".to_string())
        .build()
        .unwrap();
    let mut mqttier_client = MqttierClient::new(mqttier_options).unwrap();
    let _ = mqttier_client.start().await;

    let service_discovery = SignalOnlyDiscovery::new(&mut mqttier_client).await.unwrap();
    let discovered_singleton = service_discovery.get_singleton_service().await;

    #[cfg(feature = "metrics")]
    {
        let metrics = service_discovery
            .metrics
            .lock()
            .expect("Failed to lock metrics");
        println!("Discovery complete.  Metrics: {:?}", metrics);
        println!(
            "Time to first discovery (ms): {:?}",
            metrics.time_to_first_discovery_ms()
        );
    };
    drop(service_discovery);
    let signal_only_client =
        SignalOnlyClient::new(mqttier_client.clone(), discovered_singleton).await;

    let mut client_for_loop = signal_only_client.clone();
    tokio::spawn(async move {
        let _conn_loop = client_for_loop.run_loop().await;
    });

    let mut sig_rx = signal_only_client.get_another_signal_receiver();
    println!("Got signal receiver for anotherSignal");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task1 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received anotherSignal signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving anotherSignal signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = signal_only_client.get_bark_receiver();
    println!("Got signal receiver for bark");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task2 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("*** Received bark signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving bark signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = signal_only_client.get_maybe_number_receiver();
    println!("Got signal receiver for maybe_number");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task3 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received maybe_number signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving maybe_number signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = signal_only_client.get_maybe_name_receiver();
    println!("Got signal receiver for maybe_name");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task4 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("*** Received maybe_name signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving maybe_name signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = signal_only_client.get_now_receiver();
    println!("Got signal receiver for now");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task5 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("*** Received now signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving now signal: {:?}", e);
                    break;
                }
            }
        }
    });

    println!("Waiting for Ctrl-C to exit...");
    tokio::signal::ctrl_c()
        .await
        .expect("Failed to listen for Ctrl-C");
    println!("Ctrl-C received, shutting down...");

    sig_rx_task1.abort();

    sig_rx_task2.abort();

    sig_rx_task3.abort();

    sig_rx_task4.abort();

    sig_rx_task5.abort();

    // Join on all the signal emitting tasks.
    let _ = join!(
        sig_rx_task1,
        sig_rx_task2,
        sig_rx_task3,
        sig_rx_task4,
        sig_rx_task5
    );

    // Ctrl-C to stop
}
