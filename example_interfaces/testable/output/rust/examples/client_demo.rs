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
use test_able_ipc::client::TestAbleClient;
use test_able_ipc::discovery::TestAbleDiscovery;
#[allow(unused_imports)]
use test_able_ipc::payloads::{MethodReturnCode, *};
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

    info!("Starting Test Able client demo...");
    let mqttier_options = MqttierOptionsBuilder::default()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-client-demo".to_string())
        .build()
        .unwrap();
    let mut mqttier_client = MqttierClient::new(mqttier_options).unwrap();
    let _ = mqttier_client.start().await;

    let service_discovery = TestAbleDiscovery::new(&mut mqttier_client).await.unwrap();
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
    let mut test__able_client =
        TestAbleClient::new(mqttier_client.clone(), discovered_singleton).await;

    let mut client_for_loop = test__able_client.clone();
    tokio::spawn(async move {
        let _conn_loop = client_for_loop.run_loop().await;
    });

    let mut sig_rx = test__able_client.get_empty_receiver();
    println!("Got signal receiver for empty");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task1 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("*** Received empty signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving empty signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_int_receiver();
    println!("Got signal receiver for singleInt");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task2 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("*** Received singleInt signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving singleInt signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_optional_int_receiver();
    println!("Got signal receiver for singleOptionalInt");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task3 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleOptionalInt signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleOptionalInt signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_three_integers_receiver();
    println!("Got signal receiver for threeIntegers");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task4 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received threeIntegers signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving threeIntegers signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_string_receiver();
    println!("Got signal receiver for singleString");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task5 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleString signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleString signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_optional_string_receiver();
    println!("Got signal receiver for singleOptionalString");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task6 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleOptionalString signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleOptionalString signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_three_strings_receiver();
    println!("Got signal receiver for threeStrings");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task7 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received threeStrings signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving threeStrings signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_enum_receiver();
    println!("Got signal receiver for singleEnum");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task8 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("*** Received singleEnum signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving singleEnum signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_optional_enum_receiver();
    println!("Got signal receiver for singleOptionalEnum");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task9 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleOptionalEnum signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleOptionalEnum signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_three_enums_receiver();
    println!("Got signal receiver for threeEnums");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task10 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("*** Received threeEnums signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving threeEnums signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_struct_receiver();
    println!("Got signal receiver for singleStruct");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task11 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleStruct signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleStruct signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_optional_struct_receiver();
    println!("Got signal receiver for singleOptionalStruct");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task12 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleOptionalStruct signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleOptionalStruct signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_three_structs_receiver();
    println!("Got signal receiver for threeStructs");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task13 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received threeStructs signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving threeStructs signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_date_time_receiver();
    println!("Got signal receiver for singleDateTime");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task14 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleDateTime signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleDateTime signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_optional_datetime_receiver();
    println!("Got signal receiver for singleOptionalDatetime");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task15 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleOptionalDatetime signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleOptionalDatetime signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_three_date_times_receiver();
    println!("Got signal receiver for threeDateTimes");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task16 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received threeDateTimes signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving threeDateTimes signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_duration_receiver();
    println!("Got signal receiver for singleDuration");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task17 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleDuration signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleDuration signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_optional_duration_receiver();
    println!("Got signal receiver for singleOptionalDuration");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task18 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleOptionalDuration signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleOptionalDuration signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_three_durations_receiver();
    println!("Got signal receiver for threeDurations");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task19 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received threeDurations signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving threeDurations signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_binary_receiver();
    println!("Got signal receiver for singleBinary");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task20 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleBinary signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleBinary signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_optional_binary_receiver();
    println!("Got signal receiver for singleOptionalBinary");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task21 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleOptionalBinary signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleOptionalBinary signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_three_binaries_receiver();
    println!("Got signal receiver for threeBinaries");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task22 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received threeBinaries signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving threeBinaries signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_array_of_integers_receiver();
    println!("Got signal receiver for singleArrayOfIntegers");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task23 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleArrayOfIntegers signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving singleArrayOfIntegers signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_single_optional_array_of_strings_receiver();
    println!("Got signal receiver for singleOptionalArrayOfStrings");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task24 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received singleOptionalArrayOfStrings signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!(
                        "Error receiving singleOptionalArrayOfStrings signal: {:?}",
                        e
                    );
                    break;
                }
            }
        }
    });

    let mut sig_rx = test__able_client.get_array_of_every_type_receiver();
    println!("Got signal receiver for arrayOfEveryType");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task25 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "*** Received arrayOfEveryType signal with payload: {:?}",
                        payload
                    );
                }
                Err(e) => {
                    eprintln!("Error receiving arrayOfEveryType signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let client_for_prop_change = test__able_client.clone();
    let _prop_change_rx_task = tokio::spawn(async move {
        let mut read_write_integer_change_rx = client_for_prop_change.watch_read_write_integer();
        let mut read_only_integer_change_rx = client_for_prop_change.watch_read_only_integer();
        let mut read_write_optional_integer_change_rx =
            client_for_prop_change.watch_read_write_optional_integer();
        let mut read_write_two_integers_change_rx =
            client_for_prop_change.watch_read_write_two_integers();
        let mut read_only_string_change_rx = client_for_prop_change.watch_read_only_string();
        let mut read_write_string_change_rx = client_for_prop_change.watch_read_write_string();
        let mut read_write_optional_string_change_rx =
            client_for_prop_change.watch_read_write_optional_string();
        let mut read_write_two_strings_change_rx =
            client_for_prop_change.watch_read_write_two_strings();
        let mut read_write_struct_change_rx = client_for_prop_change.watch_read_write_struct();
        let mut read_write_optional_struct_change_rx =
            client_for_prop_change.watch_read_write_optional_struct();
        let mut read_write_two_structs_change_rx =
            client_for_prop_change.watch_read_write_two_structs();
        let mut read_only_enum_change_rx = client_for_prop_change.watch_read_only_enum();
        let mut read_write_enum_change_rx = client_for_prop_change.watch_read_write_enum();
        let mut read_write_optional_enum_change_rx =
            client_for_prop_change.watch_read_write_optional_enum();
        let mut read_write_two_enums_change_rx =
            client_for_prop_change.watch_read_write_two_enums();
        let mut read_write_datetime_change_rx = client_for_prop_change.watch_read_write_datetime();
        let mut read_write_optional_datetime_change_rx =
            client_for_prop_change.watch_read_write_optional_datetime();
        let mut read_write_two_datetimes_change_rx =
            client_for_prop_change.watch_read_write_two_datetimes();
        let mut read_write_duration_change_rx = client_for_prop_change.watch_read_write_duration();
        let mut read_write_optional_duration_change_rx =
            client_for_prop_change.watch_read_write_optional_duration();
        let mut read_write_two_durations_change_rx =
            client_for_prop_change.watch_read_write_two_durations();
        let mut read_write_binary_change_rx = client_for_prop_change.watch_read_write_binary();
        let mut read_write_optional_binary_change_rx =
            client_for_prop_change.watch_read_write_optional_binary();
        let mut read_write_two_binaries_change_rx =
            client_for_prop_change.watch_read_write_two_binaries();
        let mut read_write_list_of_strings_change_rx =
            client_for_prop_change.watch_read_write_list_of_strings();
        let mut read_write_lists_change_rx = client_for_prop_change.watch_read_write_lists();

        loop {
            tokio::select! {
                _ = read_write_integer_change_rx.changed() => {
                    println!("Property 'read_write_integer' changed to: {:?}", *read_write_integer_change_rx.borrow());
                }
                _ = read_only_integer_change_rx.changed() => {
                    println!("Property 'read_only_integer' changed to: {:?}", *read_only_integer_change_rx.borrow());
                }
                _ = read_write_optional_integer_change_rx.changed() => {
                    println!("Property 'read_write_optional_integer' changed to: {:?}", *read_write_optional_integer_change_rx.borrow());
                }
                _ = read_write_two_integers_change_rx.changed() => {
                    println!("Property 'read_write_two_integers' changed to: {:?}", *read_write_two_integers_change_rx.borrow());
                }
                _ = read_only_string_change_rx.changed() => {
                    println!("Property 'read_only_string' changed to: {:?}", *read_only_string_change_rx.borrow());
                }
                _ = read_write_string_change_rx.changed() => {
                    println!("Property 'read_write_string' changed to: {:?}", *read_write_string_change_rx.borrow());
                }
                _ = read_write_optional_string_change_rx.changed() => {
                    println!("Property 'read_write_optional_string' changed to: {:?}", *read_write_optional_string_change_rx.borrow());
                }
                _ = read_write_two_strings_change_rx.changed() => {
                    println!("Property 'read_write_two_strings' changed to: {:?}", *read_write_two_strings_change_rx.borrow());
                }
                _ = read_write_struct_change_rx.changed() => {
                    println!("Property 'read_write_struct' changed to: {:?}", *read_write_struct_change_rx.borrow());
                }
                _ = read_write_optional_struct_change_rx.changed() => {
                    println!("Property 'read_write_optional_struct' changed to: {:?}", *read_write_optional_struct_change_rx.borrow());
                }
                _ = read_write_two_structs_change_rx.changed() => {
                    println!("Property 'read_write_two_structs' changed to: {:?}", *read_write_two_structs_change_rx.borrow());
                }
                _ = read_only_enum_change_rx.changed() => {
                    println!("Property 'read_only_enum' changed to: {:?}", *read_only_enum_change_rx.borrow());
                }
                _ = read_write_enum_change_rx.changed() => {
                    println!("Property 'read_write_enum' changed to: {:?}", *read_write_enum_change_rx.borrow());
                }
                _ = read_write_optional_enum_change_rx.changed() => {
                    println!("Property 'read_write_optional_enum' changed to: {:?}", *read_write_optional_enum_change_rx.borrow());
                }
                _ = read_write_two_enums_change_rx.changed() => {
                    println!("Property 'read_write_two_enums' changed to: {:?}", *read_write_two_enums_change_rx.borrow());
                }
                _ = read_write_datetime_change_rx.changed() => {
                    println!("Property 'read_write_datetime' changed to: {:?}", *read_write_datetime_change_rx.borrow());
                }
                _ = read_write_optional_datetime_change_rx.changed() => {
                    println!("Property 'read_write_optional_datetime' changed to: {:?}", *read_write_optional_datetime_change_rx.borrow());
                }
                _ = read_write_two_datetimes_change_rx.changed() => {
                    println!("Property 'read_write_two_datetimes' changed to: {:?}", *read_write_two_datetimes_change_rx.borrow());
                }
                _ = read_write_duration_change_rx.changed() => {
                    println!("Property 'read_write_duration' changed to: {:?}", *read_write_duration_change_rx.borrow());
                }
                _ = read_write_optional_duration_change_rx.changed() => {
                    println!("Property 'read_write_optional_duration' changed to: {:?}", *read_write_optional_duration_change_rx.borrow());
                }
                _ = read_write_two_durations_change_rx.changed() => {
                    println!("Property 'read_write_two_durations' changed to: {:?}", *read_write_two_durations_change_rx.borrow());
                }
                _ = read_write_binary_change_rx.changed() => {
                    println!("Property 'read_write_binary' changed to: {:?}", *read_write_binary_change_rx.borrow());
                }
                _ = read_write_optional_binary_change_rx.changed() => {
                    println!("Property 'read_write_optional_binary' changed to: {:?}", *read_write_optional_binary_change_rx.borrow());
                }
                _ = read_write_two_binaries_change_rx.changed() => {
                    println!("Property 'read_write_two_binaries' changed to: {:?}", *read_write_two_binaries_change_rx.borrow());
                }
                _ = read_write_list_of_strings_change_rx.changed() => {
                    println!("Property 'read_write_list_of_strings' changed to: {:?}", *read_write_list_of_strings_change_rx.borrow());
                }
                _ = read_write_lists_change_rx.changed() => {
                    println!("Property 'read_write_lists' changed to: {:?}", *read_write_lists_change_rx.borrow());
                }
            }
        }
    });

    println!(">>> Calling callWithNothing with example values...");
    let result = test__able_client.call_with_nothing().await;
    println!("<<< callWithNothing response: {:?}", result);

    println!(">>> Calling callOneInteger with example values...");
    let result = test__able_client.call_one_integer(42).await;
    println!("<<< callOneInteger response: {:?}", result);

    println!(">>> Calling callOptionalInteger with example values...");
    let result = test__able_client.call_optional_integer(Some(42)).await;
    println!("<<< callOptionalInteger response: {:?}", result);

    println!(">>> Calling callThreeIntegers with example values...");
    let result = test__able_client
        .call_three_integers(42, 42, Some(42))
        .await;
    println!("<<< callThreeIntegers response: {:?}", result);

    println!(">>> Calling callOneString with example values...");
    let result = test__able_client
        .call_one_string("apples".to_string())
        .await;
    println!("<<< callOneString response: {:?}", result);

    println!(">>> Calling callOptionalString with example values...");
    let result = test__able_client
        .call_optional_string(Some("apples".to_string()))
        .await;
    println!("<<< callOptionalString response: {:?}", result);

    println!(">>> Calling callThreeStrings with example values...");
    let result = test__able_client
        .call_three_strings(
            "apples".to_string(),
            Some("apples".to_string()),
            "apples".to_string(),
        )
        .await;
    println!("<<< callThreeStrings response: {:?}", result);

    println!(">>> Calling callOneEnum with example values...");
    let result = test__able_client.call_one_enum(Numbers::One).await;
    println!("<<< callOneEnum response: {:?}", result);

    println!(">>> Calling callOptionalEnum with example values...");
    let result = test__able_client
        .call_optional_enum(Some(Numbers::One))
        .await;
    println!("<<< callOptionalEnum response: {:?}", result);

    println!(">>> Calling callThreeEnums with example values...");
    let result = test__able_client
        .call_three_enums(Numbers::One, Numbers::One, Some(Numbers::One))
        .await;
    println!("<<< callThreeEnums response: {:?}", result);

    println!(">>> Calling callOneStruct with example values...");
    let result = test__able_client
        .call_one_struct(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 2022],
            optional_array_of_integers: Some(vec![42, 2022, 2022]),
            array_of_strings: vec!["apples".to_string(), "foo".to_string()],
            optional_array_of_strings: Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: Some(vec![
                chrono::Utc::now(),
                chrono::Utc::now(),
                chrono::Utc::now(),
            ]),
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: Some(vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(967),
            ]),
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: Some(vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ]),
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: Some(vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ]),
        })
        .await;
    println!("<<< callOneStruct response: {:?}", result);

    println!(">>> Calling callOptionalStruct with example values...");
    let result = test__able_client
        .call_optional_struct(Some(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 2022],
            optional_array_of_integers: Some(vec![42, 2022, 2022]),
            array_of_strings: vec!["apples".to_string(), "foo".to_string()],
            optional_array_of_strings: Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: Some(vec![
                chrono::Utc::now(),
                chrono::Utc::now(),
                chrono::Utc::now(),
            ]),
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: Some(vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(967),
            ]),
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: Some(vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ]),
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: Some(vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ]),
        }))
        .await;
    println!("<<< callOptionalStruct response: {:?}", result);

    println!(">>> Calling callThreeStructs with example values...");
    let result = test__able_client
        .call_three_structs(
            Some(AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                an_entry_object: Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_entry_object: Some(Entry {
                    key: 42,
                    value: "apples".to_string(),
                }),
                optional_date_time: Some(chrono::Utc::now()),
                optional_duration: Some(chrono::Duration::seconds(3536)),
                optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                array_of_integers: vec![42, 2022],
                optional_array_of_integers: Some(vec![42, 2022, 2022]),
                array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                optional_array_of_strings: Some(vec![
                    "apples".to_string(),
                    "foo".to_string(),
                    "foo".to_string(),
                ]),
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: Some(vec![
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                ]),
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                ],
                optional_array_of_durations: Some(vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                    chrono::Duration::seconds(967),
                ]),
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: Some(vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ]),
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ],
                optional_array_of_entry_objects: Some(vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ]),
            }),
            AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                an_entry_object: Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_entry_object: Some(Entry {
                    key: 42,
                    value: "apples".to_string(),
                }),
                optional_date_time: Some(chrono::Utc::now()),
                optional_duration: Some(chrono::Duration::seconds(3536)),
                optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                array_of_integers: vec![42, 2022],
                optional_array_of_integers: Some(vec![42, 2022, 2022]),
                array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                optional_array_of_strings: Some(vec![
                    "apples".to_string(),
                    "foo".to_string(),
                    "foo".to_string(),
                ]),
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: Some(vec![
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                ]),
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                ],
                optional_array_of_durations: Some(vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                    chrono::Duration::seconds(967),
                ]),
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: Some(vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ]),
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ],
                optional_array_of_entry_objects: Some(vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ]),
            },
            AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                an_entry_object: Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_entry_object: Some(Entry {
                    key: 42,
                    value: "apples".to_string(),
                }),
                optional_date_time: Some(chrono::Utc::now()),
                optional_duration: Some(chrono::Duration::seconds(3536)),
                optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
                array_of_integers: vec![42, 2022],
                optional_array_of_integers: Some(vec![42, 2022, 2022]),
                array_of_strings: vec!["apples".to_string(), "foo".to_string()],
                optional_array_of_strings: Some(vec![
                    "apples".to_string(),
                    "foo".to_string(),
                    "foo".to_string(),
                ]),
                array_of_enums: vec![Numbers::One, Numbers::One],
                optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
                array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
                optional_array_of_datetimes: Some(vec![
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                    chrono::Utc::now(),
                ]),
                array_of_durations: vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                ],
                optional_array_of_durations: Some(vec![
                    chrono::Duration::seconds(3536),
                    chrono::Duration::seconds(975),
                    chrono::Duration::seconds(967),
                ]),
                array_of_binaries: vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ],
                optional_array_of_binaries: Some(vec![
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                    vec![101, 120, 97, 109, 112, 108, 101],
                ]),
                array_of_entry_objects: vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ],
                optional_array_of_entry_objects: Some(vec![
                    Entry {
                        key: 42,
                        value: "apples".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                    Entry {
                        key: 2022,
                        value: "foo".to_string(),
                    },
                ]),
            },
        )
        .await;
    println!("<<< callThreeStructs response: {:?}", result);

    println!(">>> Calling callOneDateTime with example values...");
    let result = test__able_client
        .call_one_date_time(chrono::Utc::now())
        .await;
    println!("<<< callOneDateTime response: {:?}", result);

    println!(">>> Calling callOptionalDateTime with example values...");
    let result = test__able_client
        .call_optional_date_time(Some(chrono::Utc::now()))
        .await;
    println!("<<< callOptionalDateTime response: {:?}", result);

    println!(">>> Calling callThreeDateTimes with example values...");
    let result = test__able_client
        .call_three_date_times(
            chrono::Utc::now(),
            chrono::Utc::now(),
            Some(chrono::Utc::now()),
        )
        .await;
    println!("<<< callThreeDateTimes response: {:?}", result);

    println!(">>> Calling callOneDuration with example values...");
    let result = test__able_client
        .call_one_duration(chrono::Duration::seconds(3536))
        .await;
    println!("<<< callOneDuration response: {:?}", result);

    println!(">>> Calling callOptionalDuration with example values...");
    let result = test__able_client
        .call_optional_duration(Some(chrono::Duration::seconds(3536)))
        .await;
    println!("<<< callOptionalDuration response: {:?}", result);

    println!(">>> Calling callThreeDurations with example values...");
    let result = test__able_client
        .call_three_durations(
            chrono::Duration::seconds(3536),
            chrono::Duration::seconds(3536),
            Some(chrono::Duration::seconds(3536)),
        )
        .await;
    println!("<<< callThreeDurations response: {:?}", result);

    println!(">>> Calling callOneBinary with example values...");
    let result = test__able_client
        .call_one_binary(vec![101, 120, 97, 109, 112, 108, 101])
        .await;
    println!("<<< callOneBinary response: {:?}", result);

    println!(">>> Calling callOptionalBinary with example values...");
    let result = test__able_client
        .call_optional_binary(Some(vec![101, 120, 97, 109, 112, 108, 101]))
        .await;
    println!("<<< callOptionalBinary response: {:?}", result);

    println!(">>> Calling callThreeBinaries with example values...");
    let result = test__able_client
        .call_three_binaries(
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
            Some(vec![101, 120, 97, 109, 112, 108, 101]),
        )
        .await;
    println!("<<< callThreeBinaries response: {:?}", result);

    println!(">>> Calling callOneListOfIntegers with example values...");
    let result = test__able_client
        .call_one_list_of_integers(vec![42, 2022])
        .await;
    println!("<<< callOneListOfIntegers response: {:?}", result);

    println!(">>> Calling callOptionalListOfFloats with example values...");
    let result = test__able_client
        .call_optional_list_of_floats(Some(vec![3.14, 1.0, 1.0]))
        .await;
    println!("<<< callOptionalListOfFloats response: {:?}", result);

    println!(">>> Calling callTwoLists with example values...");
    let result = test__able_client
        .call_two_lists(
            vec![Numbers::One, Numbers::One],
            Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
        )
        .await;
    println!("<<< callTwoLists response: {:?}", result);

    let _ = test__able_client.set_read_write_integer(42);

    let _ = test__able_client.set_read_write_optional_integer(Some(42));

    let read_write_two_integers_new_value = ReadWriteTwoIntegersProperty {
        first: 42,
        second: Some(42),
    };
    let _ = test__able_client.set_read_write_two_integers(read_write_two_integers_new_value);

    let _ = test__able_client.set_read_write_string("apples".to_string());

    let _ = test__able_client.set_read_write_optional_string(Some("apples".to_string()));

    let read_write_two_strings_new_value = ReadWriteTwoStringsProperty {
        first: "apples".to_string(),
        second: Some("apples".to_string()),
    };
    let _ = test__able_client.set_read_write_two_strings(read_write_two_strings_new_value);

    let _ = test__able_client.set_read_write_struct(AllTypes {
        the_bool: true,
        the_int: 42,
        the_number: 3.14,
        the_str: "apples".to_string(),
        the_enum: Numbers::One,
        an_entry_object: Entry {
            key: 42,
            value: "apples".to_string(),
        },
        date_and_time: chrono::Utc::now(),
        time_duration: chrono::Duration::seconds(3536),
        data: vec![101, 120, 97, 109, 112, 108, 101],
        optional_integer: Some(42),
        optional_string: Some("apples".to_string()),
        optional_enum: Some(Numbers::One),
        optional_entry_object: Some(Entry {
            key: 42,
            value: "apples".to_string(),
        }),
        optional_date_time: Some(chrono::Utc::now()),
        optional_duration: Some(chrono::Duration::seconds(3536)),
        optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
        array_of_integers: vec![42, 2022],
        optional_array_of_integers: Some(vec![42, 2022, 2022]),
        array_of_strings: vec!["apples".to_string(), "foo".to_string()],
        optional_array_of_strings: Some(vec![
            "apples".to_string(),
            "foo".to_string(),
            "foo".to_string(),
        ]),
        array_of_enums: vec![Numbers::One, Numbers::One],
        optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
        array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
        optional_array_of_datetimes: Some(vec![
            chrono::Utc::now(),
            chrono::Utc::now(),
            chrono::Utc::now(),
        ]),
        array_of_durations: vec![
            chrono::Duration::seconds(3536),
            chrono::Duration::seconds(975),
        ],
        optional_array_of_durations: Some(vec![
            chrono::Duration::seconds(3536),
            chrono::Duration::seconds(975),
            chrono::Duration::seconds(967),
        ]),
        array_of_binaries: vec![
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
        ],
        optional_array_of_binaries: Some(vec![
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
        ]),
        array_of_entry_objects: vec![
            Entry {
                key: 42,
                value: "apples".to_string(),
            },
            Entry {
                key: 2022,
                value: "foo".to_string(),
            },
        ],
        optional_array_of_entry_objects: Some(vec![
            Entry {
                key: 42,
                value: "apples".to_string(),
            },
            Entry {
                key: 2022,
                value: "foo".to_string(),
            },
            Entry {
                key: 2022,
                value: "foo".to_string(),
            },
        ]),
    });

    let _ = test__able_client.set_read_write_optional_struct(Some(AllTypes {
        the_bool: true,
        the_int: 42,
        the_number: 3.14,
        the_str: "apples".to_string(),
        the_enum: Numbers::One,
        an_entry_object: Entry {
            key: 42,
            value: "apples".to_string(),
        },
        date_and_time: chrono::Utc::now(),
        time_duration: chrono::Duration::seconds(3536),
        data: vec![101, 120, 97, 109, 112, 108, 101],
        optional_integer: Some(42),
        optional_string: Some("apples".to_string()),
        optional_enum: Some(Numbers::One),
        optional_entry_object: Some(Entry {
            key: 42,
            value: "apples".to_string(),
        }),
        optional_date_time: Some(chrono::Utc::now()),
        optional_duration: Some(chrono::Duration::seconds(3536)),
        optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
        array_of_integers: vec![42, 2022],
        optional_array_of_integers: Some(vec![42, 2022, 2022]),
        array_of_strings: vec!["apples".to_string(), "foo".to_string()],
        optional_array_of_strings: Some(vec![
            "apples".to_string(),
            "foo".to_string(),
            "foo".to_string(),
        ]),
        array_of_enums: vec![Numbers::One, Numbers::One],
        optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
        array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
        optional_array_of_datetimes: Some(vec![
            chrono::Utc::now(),
            chrono::Utc::now(),
            chrono::Utc::now(),
        ]),
        array_of_durations: vec![
            chrono::Duration::seconds(3536),
            chrono::Duration::seconds(975),
        ],
        optional_array_of_durations: Some(vec![
            chrono::Duration::seconds(3536),
            chrono::Duration::seconds(975),
            chrono::Duration::seconds(967),
        ]),
        array_of_binaries: vec![
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
        ],
        optional_array_of_binaries: Some(vec![
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
        ]),
        array_of_entry_objects: vec![
            Entry {
                key: 42,
                value: "apples".to_string(),
            },
            Entry {
                key: 2022,
                value: "foo".to_string(),
            },
        ],
        optional_array_of_entry_objects: Some(vec![
            Entry {
                key: 42,
                value: "apples".to_string(),
            },
            Entry {
                key: 2022,
                value: "foo".to_string(),
            },
            Entry {
                key: 2022,
                value: "foo".to_string(),
            },
        ]),
    }));

    let read_write_two_structs_new_value = ReadWriteTwoStructsProperty {
        first: AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 2022],
            optional_array_of_integers: Some(vec![42, 2022, 2022]),
            array_of_strings: vec!["apples".to_string(), "foo".to_string()],
            optional_array_of_strings: Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: Some(vec![
                chrono::Utc::now(),
                chrono::Utc::now(),
                chrono::Utc::now(),
            ]),
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: Some(vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(967),
            ]),
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: Some(vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ]),
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: Some(vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ]),
        },
        second: Some(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            an_entry_object: Entry {
                key: 42,
                value: "apples".to_string(),
            },
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_entry_object: Some(Entry {
                key: 42,
                value: "apples".to_string(),
            }),
            optional_date_time: Some(chrono::Utc::now()),
            optional_duration: Some(chrono::Duration::seconds(3536)),
            optional_binary: Some(vec![101, 120, 97, 109, 112, 108, 101]),
            array_of_integers: vec![42, 2022],
            optional_array_of_integers: Some(vec![42, 2022, 2022]),
            array_of_strings: vec!["apples".to_string(), "foo".to_string()],
            optional_array_of_strings: Some(vec![
                "apples".to_string(),
                "foo".to_string(),
                "foo".to_string(),
            ]),
            array_of_enums: vec![Numbers::One, Numbers::One],
            optional_array_of_enums: Some(vec![Numbers::One, Numbers::One, Numbers::One]),
            array_of_datetimes: vec![chrono::Utc::now(), chrono::Utc::now()],
            optional_array_of_datetimes: Some(vec![
                chrono::Utc::now(),
                chrono::Utc::now(),
                chrono::Utc::now(),
            ]),
            array_of_durations: vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
            ],
            optional_array_of_durations: Some(vec![
                chrono::Duration::seconds(3536),
                chrono::Duration::seconds(975),
                chrono::Duration::seconds(967),
            ]),
            array_of_binaries: vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ],
            optional_array_of_binaries: Some(vec![
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
                vec![101, 120, 97, 109, 112, 108, 101],
            ]),
            array_of_entry_objects: vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ],
            optional_array_of_entry_objects: Some(vec![
                Entry {
                    key: 42,
                    value: "apples".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
                Entry {
                    key: 2022,
                    value: "foo".to_string(),
                },
            ]),
        }),
    };
    let _ = test__able_client.set_read_write_two_structs(read_write_two_structs_new_value);

    let _ = test__able_client.set_read_write_enum(Numbers::One);

    let _ = test__able_client.set_read_write_optional_enum(Some(Numbers::One));

    let read_write_two_enums_new_value = ReadWriteTwoEnumsProperty {
        first: Numbers::One,
        second: Some(Numbers::One),
    };
    let _ = test__able_client.set_read_write_two_enums(read_write_two_enums_new_value);

    let _ = test__able_client.set_read_write_datetime(chrono::Utc::now());

    let _ = test__able_client.set_read_write_optional_datetime(Some(chrono::Utc::now()));

    let read_write_two_datetimes_new_value = ReadWriteTwoDatetimesProperty {
        first: chrono::Utc::now(),
        second: Some(chrono::Utc::now()),
    };
    let _ = test__able_client.set_read_write_two_datetimes(read_write_two_datetimes_new_value);

    let _ = test__able_client.set_read_write_duration(chrono::Duration::seconds(3536));

    let _ =
        test__able_client.set_read_write_optional_duration(Some(chrono::Duration::seconds(3536)));

    let read_write_two_durations_new_value = ReadWriteTwoDurationsProperty {
        first: chrono::Duration::seconds(3536),
        second: Some(chrono::Duration::seconds(3536)),
    };
    let _ = test__able_client.set_read_write_two_durations(read_write_two_durations_new_value);

    let _ = test__able_client.set_read_write_binary(vec![101, 120, 97, 109, 112, 108, 101]);

    let _ = test__able_client
        .set_read_write_optional_binary(Some(vec![101, 120, 97, 109, 112, 108, 101]));

    let read_write_two_binaries_new_value = ReadWriteTwoBinariesProperty {
        first: vec![101, 120, 97, 109, 112, 108, 101],
        second: Some(vec![101, 120, 97, 109, 112, 108, 101]),
    };
    let _ = test__able_client.set_read_write_two_binaries(read_write_two_binaries_new_value);

    let _ = test__able_client
        .set_read_write_list_of_strings(vec!["apples".to_string(), "foo".to_string()]);

    let read_write_lists_new_value = ReadWriteListsProperty {
        the_list: vec![Numbers::One, Numbers::One],
        optional_list: Some(vec![
            chrono::Utc::now(),
            chrono::Utc::now(),
            chrono::Utc::now(),
        ]),
    };
    let _ = test__able_client.set_read_write_lists(read_write_lists_new_value);

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

    sig_rx_task6.abort();

    sig_rx_task7.abort();

    sig_rx_task8.abort();

    sig_rx_task9.abort();

    sig_rx_task10.abort();

    sig_rx_task11.abort();

    sig_rx_task12.abort();

    sig_rx_task13.abort();

    sig_rx_task14.abort();

    sig_rx_task15.abort();

    sig_rx_task16.abort();

    sig_rx_task17.abort();

    sig_rx_task18.abort();

    sig_rx_task19.abort();

    sig_rx_task20.abort();

    sig_rx_task21.abort();

    sig_rx_task22.abort();

    sig_rx_task23.abort();

    sig_rx_task24.abort();

    sig_rx_task25.abort();

    // Join on all the signal emitting tasks.
    let _ = join!(
        sig_rx_task1,
        sig_rx_task2,
        sig_rx_task3,
        sig_rx_task4,
        sig_rx_task5,
        sig_rx_task6,
        sig_rx_task7,
        sig_rx_task8,
        sig_rx_task9,
        sig_rx_task10,
        sig_rx_task11,
        sig_rx_task12,
        sig_rx_task13,
        sig_rx_task14,
        sig_rx_task15,
        sig_rx_task16,
        sig_rx_task17,
        sig_rx_task18,
        sig_rx_task19,
        sig_rx_task20,
        sig_rx_task21,
        sig_rx_task22,
        sig_rx_task23,
        sig_rx_task24,
        sig_rx_task25
    );

    // Ctrl-C to stop
}
