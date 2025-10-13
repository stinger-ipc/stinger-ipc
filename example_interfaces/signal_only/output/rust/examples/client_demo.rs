//! Client module for Full IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.
*/

use futures::executor::block_on;
use mqttier::{Connection, MqttierClient, MqttierOptions};
use signal_only_ipc::client::SignalOnlyClient;
use signal_only_ipc::discovery::SignalOnlyDiscovery;
#[allow(unused_imports)]
use signal_only_ipc::payloads::{MethodReturnCode, *};
use tokio::join;
use tokio::time::{Duration, sleep};

#[tokio::main]
async fn main() {
    block_on(async {
        let mqttier_options = MqttierOptions::new()
            .connection(Connection::TcpLocalhost(1883))
            .client_id("rust-client-demo".to_string())
            .build();
        let mut mqttier_client = MqttierClient::new(mqttier_options).unwrap();

        let discovery = SignalOnlyDiscovery::new(&mut mqttier_client).await.unwrap();
        let singleton_info = discovery.get_singleton_service().await;

        let api_client = SignalOnlyClient::new(&mut mqttier_client, singleton_info.instance).await;

        let client_for_loop = api_client.clone();
        tokio::spawn(async move {
            println!("Making call to start connection loop");
            let _conn_loop = client_for_loop.run_loop().await;
        });

        let mut sig_rx = api_client.get_another_signal_receiver();
        println!("Got signal receiver for anotherSignal");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task1 = tokio::spawn(async move {
            println!("Looping for signals");
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received anotherSignal signal with payload: {:?}", payload);
                    }
                    Err(e) => {
                        eprintln!("Error receiving anotherSignal signal: {:?}", e);
                        break;
                    }
                }
            }
        });

        let mut sig_rx = api_client.get_bark_receiver();
        println!("Got signal receiver for bark");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task2 = tokio::spawn(async move {
            println!("Looping for signals");
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received bark signal with payload: {:?}", payload);
                    }
                    Err(e) => {
                        eprintln!("Error receiving bark signal: {:?}", e);
                        break;
                    }
                }
            }
        });

        let mut sig_rx = api_client.get_maybe_number_receiver();
        println!("Got signal receiver for maybe_number");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task3 = tokio::spawn(async move {
            println!("Looping for signals");
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received maybe_number signal with payload: {:?}", payload);
                    }
                    Err(e) => {
                        eprintln!("Error receiving maybe_number signal: {:?}", e);
                        break;
                    }
                }
            }
        });

        let mut sig_rx = api_client.get_maybe_name_receiver();
        println!("Got signal receiver for maybe_name");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task4 = tokio::spawn(async move {
            println!("Looping for signals");
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received maybe_name signal with payload: {:?}", payload);
                    }
                    Err(e) => {
                        eprintln!("Error receiving maybe_name signal: {:?}", e);
                        break;
                    }
                }
            }
        });

        let mut sig_rx = api_client.get_now_receiver();
        println!("Got signal receiver for now");

        sleep(Duration::from_secs(5)).await;

        let sig_rx_task5 = tokio::spawn(async move {
            println!("Looping for signals");
            loop {
                match sig_rx.recv().await {
                    Ok(payload) => {
                        println!("Received now signal with payload: {:?}", payload);
                    }
                    Err(e) => {
                        eprintln!("Error receiving now signal: {:?}", e);
                        break;
                    }
                }
            }
        });

        // Join on all the signal emitting tasks.
        let _ = join!(
            sig_rx_task1,
            sig_rx_task2,
            sig_rx_task3,
            sig_rx_task4,
            sig_rx_task5
        );
    });
    // Ctrl-C to stop
}
