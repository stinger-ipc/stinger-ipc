//! Client module for Full IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.
*/

use mqttier::{Connection, MqttierClient, MqttierOptions};
use test_able_ipc::client::TestAbleClient;
use test_able_ipc::discovery::TestAbleDiscovery;
#[allow(unused_imports)]
use test_able_ipc::payloads::{MethodReturnCode, *};
use tokio::join;
use tokio::time::{Duration, sleep};
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
    let mqttier_options = MqttierOptions::new()
        .connection(Connection::TcpLocalhost(1883))
        .client_id("rust-client-demo".to_string())
        .build();
    let mut mqttier_client = MqttierClient::new(mqttier_options).unwrap();
    let discovery = TestAbleDiscovery::new(&mut mqttier_client).await.unwrap();
    let singleton_info = discovery.get_singleton_service().await;

    let mut api_client = TestAbleClient::new(&mut mqttier_client, singleton_info.instance).await;

    let client_for_loop = api_client.clone();
    tokio::spawn(async move {
        let _conn_loop = client_for_loop.run_loop().await;
    });

    let mut sig_rx = api_client.get_empty_receiver();
    println!("Got signal receiver for empty");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task1 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received empty signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving empty signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_int_receiver();
    println!("Got signal receiver for singleInt");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task2 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received singleInt signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving singleInt signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_optional_int_receiver();
    println!("Got signal receiver for singleOptionalInt");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task3 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "Received singleOptionalInt signal with payload: {:?}",
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

    let mut sig_rx = api_client.get_three_integers_receiver();
    println!("Got signal receiver for threeIntegers");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task4 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received threeIntegers signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving threeIntegers signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_string_receiver();
    println!("Got signal receiver for singleString");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task5 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received singleString signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving singleString signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_optional_string_receiver();
    println!("Got signal receiver for singleOptionalString");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task6 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "Received singleOptionalString signal with payload: {:?}",
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

    let mut sig_rx = api_client.get_three_strings_receiver();
    println!("Got signal receiver for threeStrings");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task7 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received threeStrings signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving threeStrings signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_enum_receiver();
    println!("Got signal receiver for singleEnum");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task8 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received singleEnum signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving singleEnum signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_optional_enum_receiver();
    println!("Got signal receiver for singleOptionalEnum");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task9 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "Received singleOptionalEnum signal with payload: {:?}",
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

    let mut sig_rx = api_client.get_three_enums_receiver();
    println!("Got signal receiver for threeEnums");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task10 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received threeEnums signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving threeEnums signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_struct_receiver();
    println!("Got signal receiver for singleStruct");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task11 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received singleStruct signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving singleStruct signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_optional_struct_receiver();
    println!("Got signal receiver for singleOptionalStruct");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task12 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "Received singleOptionalStruct signal with payload: {:?}",
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

    let mut sig_rx = api_client.get_three_structs_receiver();
    println!("Got signal receiver for threeStructs");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task13 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received threeStructs signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving threeStructs signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_date_time_receiver();
    println!("Got signal receiver for singleDateTime");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task14 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received singleDateTime signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving singleDateTime signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_optional_datetime_receiver();
    println!("Got signal receiver for singleOptionalDatetime");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task15 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "Received singleOptionalDatetime signal with payload: {:?}",
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

    let mut sig_rx = api_client.get_three_date_times_receiver();
    println!("Got signal receiver for threeDateTimes");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task16 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received threeDateTimes signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving threeDateTimes signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_duration_receiver();
    println!("Got signal receiver for singleDuration");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task17 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received singleDuration signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving singleDuration signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_optional_duration_receiver();
    println!("Got signal receiver for singleOptionalDuration");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task18 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "Received singleOptionalDuration signal with payload: {:?}",
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

    let mut sig_rx = api_client.get_three_durations_receiver();
    println!("Got signal receiver for threeDurations");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task19 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received threeDurations signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving threeDurations signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_binary_receiver();
    println!("Got signal receiver for singleBinary");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task20 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received singleBinary signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving singleBinary signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let mut sig_rx = api_client.get_single_optional_binary_receiver();
    println!("Got signal receiver for singleOptionalBinary");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task21 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!(
                        "Received singleOptionalBinary signal with payload: {:?}",
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

    let mut sig_rx = api_client.get_three_binaries_receiver();
    println!("Got signal receiver for threeBinaries");

    sleep(Duration::from_secs(5)).await;

    let sig_rx_task22 = tokio::spawn(async move {
        println!("Looping for signals");
        loop {
            match sig_rx.recv().await {
                Ok(payload) => {
                    println!("Received threeBinaries signal with payload: {:?}", payload);
                }
                Err(e) => {
                    eprintln!("Error receiving threeBinaries signal: {:?}", e);
                    break;
                }
            }
        }
    });

    let client_for_prop_change = api_client.clone();
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
            }
        }
    });

    println!("Calling callWithNothing with example values...");
    let result = api_client
        .call_with_nothing()
        .await
        .expect("Failed to call callWithNothing");
    println!("callWithNothing response: {:?}", result);

    println!("Calling callOneInteger with example values...");
    let result = api_client
        .call_one_integer(42)
        .await
        .expect("Failed to call callOneInteger");
    println!("callOneInteger response: {:?}", result);

    println!("Calling callOptionalInteger with example values...");
    let result = api_client
        .call_optional_integer(Some(42))
        .await
        .expect("Failed to call callOptionalInteger");
    println!("callOptionalInteger response: {:?}", result);

    println!("Calling callThreeIntegers with example values...");
    let result = api_client
        .call_three_integers(42, 42, Some(42))
        .await
        .expect("Failed to call callThreeIntegers");
    println!("callThreeIntegers response: {:?}", result);

    println!("Calling callOneString with example values...");
    let result = api_client
        .call_one_string("apples".to_string())
        .await
        .expect("Failed to call callOneString");
    println!("callOneString response: {:?}", result);

    println!("Calling callOptionalString with example values...");
    let result = api_client
        .call_optional_string(Some("apples".to_string()))
        .await
        .expect("Failed to call callOptionalString");
    println!("callOptionalString response: {:?}", result);

    println!("Calling callThreeStrings with example values...");
    let result = api_client
        .call_three_strings(
            "apples".to_string(),
            Some("apples".to_string()),
            "apples".to_string(),
        )
        .await
        .expect("Failed to call callThreeStrings");
    println!("callThreeStrings response: {:?}", result);

    println!("Calling callOneEnum with example values...");
    let result = api_client
        .call_one_enum(Numbers::One)
        .await
        .expect("Failed to call callOneEnum");
    println!("callOneEnum response: {:?}", result);

    println!("Calling callOptionalEnum with example values...");
    let result = api_client
        .call_optional_enum(Some(Numbers::One))
        .await
        .expect("Failed to call callOptionalEnum");
    println!("callOptionalEnum response: {:?}", result);

    println!("Calling callThreeEnums with example values...");
    let result = api_client
        .call_three_enums(Numbers::One, Numbers::One, Some(Numbers::One))
        .await
        .expect("Failed to call callThreeEnums");
    println!("callThreeEnums response: {:?}", result);

    println!("Calling callOneStruct with example values...");
    let result = api_client
        .call_one_struct(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_date_time: chrono::Utc::now(),
            optional_duration: chrono::Duration::seconds(3536),
            optional_binary: vec![101, 120, 97, 109, 112, 108, 101],
        })
        .await
        .expect("Failed to call callOneStruct");
    println!("callOneStruct response: {:?}", result);

    println!("Calling callOptionalStruct with example values...");
    let result = api_client
        .call_optional_struct(AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_date_time: chrono::Utc::now(),
            optional_duration: chrono::Duration::seconds(3536),
            optional_binary: vec![101, 120, 97, 109, 112, 108, 101],
        })
        .await
        .expect("Failed to call callOptionalStruct");
    println!("callOptionalStruct response: {:?}", result);

    println!("Calling callThreeStructs with example values...");
    let result = api_client
        .call_three_structs(
            AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_date_time: chrono::Utc::now(),
                optional_duration: chrono::Duration::seconds(3536),
                optional_binary: vec![101, 120, 97, 109, 112, 108, 101],
            },
            AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_date_time: chrono::Utc::now(),
                optional_duration: chrono::Duration::seconds(3536),
                optional_binary: vec![101, 120, 97, 109, 112, 108, 101],
            },
            AllTypes {
                the_bool: true,
                the_int: 42,
                the_number: 3.14,
                the_str: "apples".to_string(),
                the_enum: Numbers::One,
                date_and_time: chrono::Utc::now(),
                time_duration: chrono::Duration::seconds(3536),
                data: vec![101, 120, 97, 109, 112, 108, 101],
                optional_integer: Some(42),
                optional_string: Some("apples".to_string()),
                optional_enum: Some(Numbers::One),
                optional_date_time: chrono::Utc::now(),
                optional_duration: chrono::Duration::seconds(3536),
                optional_binary: vec![101, 120, 97, 109, 112, 108, 101],
            },
        )
        .await
        .expect("Failed to call callThreeStructs");
    println!("callThreeStructs response: {:?}", result);

    println!("Calling callOneDateTime with example values...");
    let result = api_client
        .call_one_date_time(chrono::Utc::now())
        .await
        .expect("Failed to call callOneDateTime");
    println!("callOneDateTime response: {:?}", result);

    println!("Calling callOptionalDateTime with example values...");
    let result = api_client
        .call_optional_date_time(chrono::Utc::now())
        .await
        .expect("Failed to call callOptionalDateTime");
    println!("callOptionalDateTime response: {:?}", result);

    println!("Calling callThreeDateTimes with example values...");
    let result = api_client
        .call_three_date_times(chrono::Utc::now(), chrono::Utc::now(), chrono::Utc::now())
        .await
        .expect("Failed to call callThreeDateTimes");
    println!("callThreeDateTimes response: {:?}", result);

    println!("Calling callOneDuration with example values...");
    let result = api_client
        .call_one_duration(chrono::Duration::seconds(3536))
        .await
        .expect("Failed to call callOneDuration");
    println!("callOneDuration response: {:?}", result);

    println!("Calling callOptionalDuration with example values...");
    let result = api_client
        .call_optional_duration(chrono::Duration::seconds(3536))
        .await
        .expect("Failed to call callOptionalDuration");
    println!("callOptionalDuration response: {:?}", result);

    println!("Calling callThreeDurations with example values...");
    let result = api_client
        .call_three_durations(
            chrono::Duration::seconds(3536),
            chrono::Duration::seconds(3536),
            chrono::Duration::seconds(3536),
        )
        .await
        .expect("Failed to call callThreeDurations");
    println!("callThreeDurations response: {:?}", result);

    println!("Calling callOneBinary with example values...");
    let result = api_client
        .call_one_binary(vec![101, 120, 97, 109, 112, 108, 101])
        .await
        .expect("Failed to call callOneBinary");
    println!("callOneBinary response: {:?}", result);

    println!("Calling callOptionalBinary with example values...");
    let result = api_client
        .call_optional_binary(vec![101, 120, 97, 109, 112, 108, 101])
        .await
        .expect("Failed to call callOptionalBinary");
    println!("callOptionalBinary response: {:?}", result);

    println!("Calling callThreeBinaries with example values...");
    let result = api_client
        .call_three_binaries(
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
            vec![101, 120, 97, 109, 112, 108, 101],
        )
        .await
        .expect("Failed to call callThreeBinaries");
    println!("callThreeBinaries response: {:?}", result);

    let _ = api_client.set_read_write_integer(42);

    let _ = api_client.set_read_write_optional_integer(Some(42));

    let read_write_two_integers_new_value = ReadWriteTwoIntegersProperty {
        first: 42,
        second: Some(42),
    };
    let _ = api_client.set_read_write_two_integers(read_write_two_integers_new_value);

    let _ = api_client.set_read_write_string("apples".to_string());

    let _ = api_client.set_read_write_optional_string(Some("apples".to_string()));

    let read_write_two_strings_new_value = ReadWriteTwoStringsProperty {
        first: "apples".to_string(),
        second: Some("apples".to_string()),
    };
    let _ = api_client.set_read_write_two_strings(read_write_two_strings_new_value);

    let _ = api_client.set_read_write_struct(AllTypes {
        the_bool: true,
        the_int: 42,
        the_number: 3.14,
        the_str: "apples".to_string(),
        the_enum: Numbers::One,
        date_and_time: chrono::Utc::now(),
        time_duration: chrono::Duration::seconds(3536),
        data: vec![101, 120, 97, 109, 112, 108, 101],
        optional_integer: Some(42),
        optional_string: Some("apples".to_string()),
        optional_enum: Some(Numbers::One),
        optional_date_time: chrono::Utc::now(),
        optional_duration: chrono::Duration::seconds(3536),
        optional_binary: vec![101, 120, 97, 109, 112, 108, 101],
    });

    let _ = api_client.set_read_write_optional_struct(AllTypes {
        the_bool: true,
        the_int: 42,
        the_number: 3.14,
        the_str: "apples".to_string(),
        the_enum: Numbers::One,
        date_and_time: chrono::Utc::now(),
        time_duration: chrono::Duration::seconds(3536),
        data: vec![101, 120, 97, 109, 112, 108, 101],
        optional_integer: Some(42),
        optional_string: Some("apples".to_string()),
        optional_enum: Some(Numbers::One),
        optional_date_time: chrono::Utc::now(),
        optional_duration: chrono::Duration::seconds(3536),
        optional_binary: vec![101, 120, 97, 109, 112, 108, 101],
    });

    let read_write_two_structs_new_value = ReadWriteTwoStructsProperty {
        first: AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_date_time: chrono::Utc::now(),
            optional_duration: chrono::Duration::seconds(3536),
            optional_binary: vec![101, 120, 97, 109, 112, 108, 101],
        },
        second: AllTypes {
            the_bool: true,
            the_int: 42,
            the_number: 3.14,
            the_str: "apples".to_string(),
            the_enum: Numbers::One,
            date_and_time: chrono::Utc::now(),
            time_duration: chrono::Duration::seconds(3536),
            data: vec![101, 120, 97, 109, 112, 108, 101],
            optional_integer: Some(42),
            optional_string: Some("apples".to_string()),
            optional_enum: Some(Numbers::One),
            optional_date_time: chrono::Utc::now(),
            optional_duration: chrono::Duration::seconds(3536),
            optional_binary: vec![101, 120, 97, 109, 112, 108, 101],
        },
    };
    let _ = api_client.set_read_write_two_structs(read_write_two_structs_new_value);

    let _ = api_client.set_read_write_enum(Numbers::One);

    let _ = api_client.set_read_write_optional_enum(Some(Numbers::One));

    let read_write_two_enums_new_value = ReadWriteTwoEnumsProperty {
        first: Numbers::One,
        second: Some(Numbers::One),
    };
    let _ = api_client.set_read_write_two_enums(read_write_two_enums_new_value);

    let _ = api_client.set_read_write_datetime(chrono::Utc::now());

    let _ = api_client.set_read_write_optional_datetime(chrono::Utc::now());

    let read_write_two_datetimes_new_value = ReadWriteTwoDatetimesProperty {
        first: chrono::Utc::now(),
        second: chrono::Utc::now(),
    };
    let _ = api_client.set_read_write_two_datetimes(read_write_two_datetimes_new_value);

    let _ = api_client.set_read_write_duration(chrono::Duration::seconds(3536));

    let _ = api_client.set_read_write_optional_duration(chrono::Duration::seconds(3536));

    let read_write_two_durations_new_value = ReadWriteTwoDurationsProperty {
        first: chrono::Duration::seconds(3536),
        second: chrono::Duration::seconds(3536),
    };
    let _ = api_client.set_read_write_two_durations(read_write_two_durations_new_value);

    let _ = api_client.set_read_write_binary(vec![101, 120, 97, 109, 112, 108, 101]);

    let _ = api_client.set_read_write_optional_binary(vec![101, 120, 97, 109, 112, 108, 101]);

    let read_write_two_binaries_new_value = ReadWriteTwoBinariesProperty {
        first: vec![101, 120, 97, 109, 112, 108, 101],
        second: vec![101, 120, 97, 109, 112, 108, 101],
    };
    let _ = api_client.set_read_write_two_binaries(read_write_two_binaries_new_value);

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
        sig_rx_task22
    );

    // Ctrl-C to stop
}
