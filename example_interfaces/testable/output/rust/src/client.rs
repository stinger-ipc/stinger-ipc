//! Client module for Test Able IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Test Able interface.
*/
#[cfg(feature = "client")]
use mqttier::{MqttierClient, ReceivedMessage};
use serde_json;
use std::collections::HashMap;
use uuid::Uuid;

#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
#[allow(unused_imports)]
use iso8601_duration::Duration as IsoDuration;
use std::sync::{Arc, Mutex};
use tokio::sync::{broadcast, mpsc, oneshot, watch};
use tokio::task::JoinError;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct TestAbleSubscriptionIds {
    call_with_nothing_method_resp: usize,
    call_one_integer_method_resp: usize,
    call_optional_integer_method_resp: usize,
    call_three_integers_method_resp: usize,
    call_one_string_method_resp: usize,
    call_optional_string_method_resp: usize,
    call_three_strings_method_resp: usize,
    call_one_enum_method_resp: usize,
    call_optional_enum_method_resp: usize,
    call_three_enums_method_resp: usize,
    call_one_struct_method_resp: usize,
    call_optional_struct_method_resp: usize,
    call_three_structs_method_resp: usize,
    call_one_date_time_method_resp: usize,
    call_optional_date_time_method_resp: usize,
    call_three_date_times_method_resp: usize,
    call_one_duration_method_resp: usize,
    call_optional_duration_method_resp: usize,
    call_three_durations_method_resp: usize,
    call_one_binary_method_resp: usize,
    call_optional_binary_method_resp: usize,
    call_three_binaries_method_resp: usize,

    empty_signal: Option<usize>,
    single_int_signal: Option<usize>,
    single_optional_int_signal: Option<usize>,
    three_integers_signal: Option<usize>,
    single_string_signal: Option<usize>,
    single_optional_string_signal: Option<usize>,
    three_strings_signal: Option<usize>,
    single_enum_signal: Option<usize>,
    single_optional_enum_signal: Option<usize>,
    three_enums_signal: Option<usize>,
    single_struct_signal: Option<usize>,
    single_optional_struct_signal: Option<usize>,
    three_structs_signal: Option<usize>,
    single_date_time_signal: Option<usize>,
    single_optional_datetime_signal: Option<usize>,
    three_date_times_signal: Option<usize>,
    single_duration_signal: Option<usize>,
    single_optional_duration_signal: Option<usize>,
    three_durations_signal: Option<usize>,
    single_binary_signal: Option<usize>,
    single_optional_binary_signal: Option<usize>,
    three_binaries_signal: Option<usize>,
    read_write_integer_property_value: usize,
    read_only_integer_property_value: usize,
    read_write_optional_integer_property_value: usize,
    read_write_two_integers_property_value: usize,
    read_only_string_property_value: usize,
    read_write_string_property_value: usize,
    read_write_optional_string_property_value: usize,
    read_write_two_strings_property_value: usize,
    read_write_struct_property_value: usize,
    read_write_optional_struct_property_value: usize,
    read_write_two_structs_property_value: usize,
    read_only_enum_property_value: usize,
    read_write_enum_property_value: usize,
    read_write_optional_enum_property_value: usize,
    read_write_two_enums_property_value: usize,
    read_write_datetime_property_value: usize,
    read_write_optional_datetime_property_value: usize,
    read_write_two_datetimes_property_value: usize,
    read_write_duration_property_value: usize,
    read_write_optional_duration_property_value: usize,
    read_write_two_durations_property_value: usize,
    read_write_binary_property_value: usize,
    read_write_optional_binary_property_value: usize,
    read_write_two_binaries_property_value: usize,
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When TestAbleClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct TestAbleSignalChannels {
    empty_sender: broadcast::Sender<()>,
    single_int_sender: broadcast::Sender<i32>,
    single_optional_int_sender: broadcast::Sender<Option<i32>>,
    three_integers_sender: broadcast::Sender<ThreeIntegersSignalPayload>,
    single_string_sender: broadcast::Sender<String>,
    single_optional_string_sender: broadcast::Sender<Option<String>>,
    three_strings_sender: broadcast::Sender<ThreeStringsSignalPayload>,
    single_enum_sender: broadcast::Sender<Numbers>,
    single_optional_enum_sender: broadcast::Sender<Option<Numbers>>,
    three_enums_sender: broadcast::Sender<ThreeEnumsSignalPayload>,
    single_struct_sender: broadcast::Sender<AllTypes>,
    single_optional_struct_sender: broadcast::Sender<AllTypes>,
    three_structs_sender: broadcast::Sender<ThreeStructsSignalPayload>,
    single_date_time_sender: broadcast::Sender<chrono::DateTime<chrono::Utc>>,
    single_optional_datetime_sender: broadcast::Sender<chrono::DateTime<chrono::Utc>>,
    three_date_times_sender: broadcast::Sender<ThreeDateTimesSignalPayload>,
    single_duration_sender: broadcast::Sender<chrono::Duration>,
    single_optional_duration_sender: broadcast::Sender<chrono::Duration>,
    three_durations_sender: broadcast::Sender<ThreeDurationsSignalPayload>,
    single_binary_sender: broadcast::Sender<Vec<u8>>,
    single_optional_binary_sender: broadcast::Sender<Vec<u8>>,
    three_binaries_sender: broadcast::Sender<ThreeBinariesSignalPayload>,
}

#[derive(Clone)]
pub struct TestAbleProperties {
    pub read_write_integer: Arc<Mutex<Option<i32>>>,

    read_write_integer_tx_channel: watch::Sender<Option<i32>>,
    pub read_only_integer: Arc<Mutex<Option<i32>>>,

    read_only_integer_tx_channel: watch::Sender<Option<i32>>,
    pub read_write_optional_integer: Arc<Mutex<Option<Option<i32>>>>,

    read_write_optional_integer_tx_channel: watch::Sender<Option<Option<i32>>>,
    pub read_write_two_integers: Arc<Mutex<Option<ReadWriteTwoIntegersProperty>>>,
    read_write_two_integers_tx_channel: watch::Sender<Option<ReadWriteTwoIntegersProperty>>,
    pub read_only_string: Arc<Mutex<Option<String>>>,

    read_only_string_tx_channel: watch::Sender<Option<String>>,
    pub read_write_string: Arc<Mutex<Option<String>>>,

    read_write_string_tx_channel: watch::Sender<Option<String>>,
    pub read_write_optional_string: Arc<Mutex<Option<Option<String>>>>,

    read_write_optional_string_tx_channel: watch::Sender<Option<Option<String>>>,
    pub read_write_two_strings: Arc<Mutex<Option<ReadWriteTwoStringsProperty>>>,
    read_write_two_strings_tx_channel: watch::Sender<Option<ReadWriteTwoStringsProperty>>,
    pub read_write_struct: Arc<Mutex<Option<AllTypes>>>,

    read_write_struct_tx_channel: watch::Sender<Option<AllTypes>>,
    pub read_write_optional_struct: Arc<Mutex<Option<AllTypes>>>,

    read_write_optional_struct_tx_channel: watch::Sender<Option<AllTypes>>,
    pub read_write_two_structs: Arc<Mutex<Option<ReadWriteTwoStructsProperty>>>,
    read_write_two_structs_tx_channel: watch::Sender<Option<ReadWriteTwoStructsProperty>>,
    pub read_only_enum: Arc<Mutex<Option<Numbers>>>,

    read_only_enum_tx_channel: watch::Sender<Option<Numbers>>,
    pub read_write_enum: Arc<Mutex<Option<Numbers>>>,

    read_write_enum_tx_channel: watch::Sender<Option<Numbers>>,
    pub read_write_optional_enum: Arc<Mutex<Option<Option<Numbers>>>>,

    read_write_optional_enum_tx_channel: watch::Sender<Option<Option<Numbers>>>,
    pub read_write_two_enums: Arc<Mutex<Option<ReadWriteTwoEnumsProperty>>>,
    read_write_two_enums_tx_channel: watch::Sender<Option<ReadWriteTwoEnumsProperty>>,
    pub read_write_datetime: Arc<Mutex<Option<chrono::DateTime<chrono::Utc>>>>,

    read_write_datetime_tx_channel: watch::Sender<Option<chrono::DateTime<chrono::Utc>>>,
    pub read_write_optional_datetime: Arc<Mutex<Option<chrono::DateTime<chrono::Utc>>>>,

    read_write_optional_datetime_tx_channel: watch::Sender<Option<chrono::DateTime<chrono::Utc>>>,
    pub read_write_two_datetimes: Arc<Mutex<Option<ReadWriteTwoDatetimesProperty>>>,
    read_write_two_datetimes_tx_channel: watch::Sender<Option<ReadWriteTwoDatetimesProperty>>,
    pub read_write_duration: Arc<Mutex<Option<chrono::Duration>>>,

    read_write_duration_tx_channel: watch::Sender<Option<chrono::Duration>>,
    pub read_write_optional_duration: Arc<Mutex<Option<chrono::Duration>>>,

    read_write_optional_duration_tx_channel: watch::Sender<Option<chrono::Duration>>,
    pub read_write_two_durations: Arc<Mutex<Option<ReadWriteTwoDurationsProperty>>>,
    read_write_two_durations_tx_channel: watch::Sender<Option<ReadWriteTwoDurationsProperty>>,
    pub read_write_binary: Arc<Mutex<Option<Vec<u8>>>>,

    read_write_binary_tx_channel: watch::Sender<Option<Vec<u8>>>,
    pub read_write_optional_binary: Arc<Mutex<Option<Vec<u8>>>>,

    read_write_optional_binary_tx_channel: watch::Sender<Option<Vec<u8>>>,
    pub read_write_two_binaries: Arc<Mutex<Option<ReadWriteTwoBinariesProperty>>>,
    read_write_two_binaries_tx_channel: watch::Sender<Option<ReadWriteTwoBinariesProperty>>,
}

/// This is the struct for our API client.
#[derive(Clone)]
pub struct TestAbleClient {
    mqttier_client: MqttierClient,
    /// Temporarily holds oneshot channels for responses to method calls.
    pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<String>>>>,

    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<mpsc::Receiver<ReceivedMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Struct contains all the properties.
    pub properties: TestAbleProperties,

    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: TestAbleSubscriptionIds,
    /// Holds the channels used for sending signals to the application.
    signal_channels: TestAbleSignalChannels,

    /// Copy of MQTT Client ID
    pub client_id: String,

    /// Instance ID of the server
    service_instance_id: String,
}

impl TestAbleClient {
    /// Creates a new TestAbleClient that uses an MqttierClient.
    pub async fn new(connection: &mut MqttierClient, service_id: String) -> Self {
        // Create a channel for messages to get from the Connection object to this TestAbleClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        let topic_call_with_nothing_method_resp =
            format!("client/{}/callWithNothing/response", connection.client_id);
        let subscription_id_call_with_nothing_method_resp = connection
            .subscribe(
                topic_call_with_nothing_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_with_nothing_method_resp =
            subscription_id_call_with_nothing_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_one_integer_method_resp =
            format!("client/{}/callOneInteger/response", connection.client_id);
        let subscription_id_call_one_integer_method_resp = connection
            .subscribe(
                topic_call_one_integer_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_integer_method_resp =
            subscription_id_call_one_integer_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_optional_integer_method_resp = format!(
            "client/{}/callOptionalInteger/response",
            connection.client_id
        );
        let subscription_id_call_optional_integer_method_resp = connection
            .subscribe(
                topic_call_optional_integer_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_integer_method_resp =
            subscription_id_call_optional_integer_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_three_integers_method_resp =
            format!("client/{}/callThreeIntegers/response", connection.client_id);
        let subscription_id_call_three_integers_method_resp = connection
            .subscribe(
                topic_call_three_integers_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_integers_method_resp =
            subscription_id_call_three_integers_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_one_string_method_resp =
            format!("client/{}/callOneString/response", connection.client_id);
        let subscription_id_call_one_string_method_resp = connection
            .subscribe(
                topic_call_one_string_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_string_method_resp =
            subscription_id_call_one_string_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_optional_string_method_resp = format!(
            "client/{}/callOptionalString/response",
            connection.client_id
        );
        let subscription_id_call_optional_string_method_resp = connection
            .subscribe(
                topic_call_optional_string_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_string_method_resp =
            subscription_id_call_optional_string_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_three_strings_method_resp =
            format!("client/{}/callThreeStrings/response", connection.client_id);
        let subscription_id_call_three_strings_method_resp = connection
            .subscribe(
                topic_call_three_strings_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_strings_method_resp =
            subscription_id_call_three_strings_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_one_enum_method_resp =
            format!("client/{}/callOneEnum/response", connection.client_id);
        let subscription_id_call_one_enum_method_resp = connection
            .subscribe(
                topic_call_one_enum_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_enum_method_resp =
            subscription_id_call_one_enum_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_optional_enum_method_resp =
            format!("client/{}/callOptionalEnum/response", connection.client_id);
        let subscription_id_call_optional_enum_method_resp = connection
            .subscribe(
                topic_call_optional_enum_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_enum_method_resp =
            subscription_id_call_optional_enum_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_three_enums_method_resp =
            format!("client/{}/callThreeEnums/response", connection.client_id);
        let subscription_id_call_three_enums_method_resp = connection
            .subscribe(
                topic_call_three_enums_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_enums_method_resp =
            subscription_id_call_three_enums_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_one_struct_method_resp =
            format!("client/{}/callOneStruct/response", connection.client_id);
        let subscription_id_call_one_struct_method_resp = connection
            .subscribe(
                topic_call_one_struct_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_struct_method_resp =
            subscription_id_call_one_struct_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_optional_struct_method_resp = format!(
            "client/{}/callOptionalStruct/response",
            connection.client_id
        );
        let subscription_id_call_optional_struct_method_resp = connection
            .subscribe(
                topic_call_optional_struct_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_struct_method_resp =
            subscription_id_call_optional_struct_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_three_structs_method_resp =
            format!("client/{}/callThreeStructs/response", connection.client_id);
        let subscription_id_call_three_structs_method_resp = connection
            .subscribe(
                topic_call_three_structs_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_structs_method_resp =
            subscription_id_call_three_structs_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_one_date_time_method_resp =
            format!("client/{}/callOneDateTime/response", connection.client_id);
        let subscription_id_call_one_date_time_method_resp = connection
            .subscribe(
                topic_call_one_date_time_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_date_time_method_resp =
            subscription_id_call_one_date_time_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_optional_date_time_method_resp = format!(
            "client/{}/callOptionalDateTime/response",
            connection.client_id
        );
        let subscription_id_call_optional_date_time_method_resp = connection
            .subscribe(
                topic_call_optional_date_time_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_date_time_method_resp =
            subscription_id_call_optional_date_time_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_three_date_times_method_resp = format!(
            "client/{}/callThreeDateTimes/response",
            connection.client_id
        );
        let subscription_id_call_three_date_times_method_resp = connection
            .subscribe(
                topic_call_three_date_times_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_date_times_method_resp =
            subscription_id_call_three_date_times_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_one_duration_method_resp =
            format!("client/{}/callOneDuration/response", connection.client_id);
        let subscription_id_call_one_duration_method_resp = connection
            .subscribe(
                topic_call_one_duration_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_duration_method_resp =
            subscription_id_call_one_duration_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_optional_duration_method_resp = format!(
            "client/{}/callOptionalDuration/response",
            connection.client_id
        );
        let subscription_id_call_optional_duration_method_resp = connection
            .subscribe(
                topic_call_optional_duration_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_duration_method_resp =
            subscription_id_call_optional_duration_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_three_durations_method_resp = format!(
            "client/{}/callThreeDurations/response",
            connection.client_id
        );
        let subscription_id_call_three_durations_method_resp = connection
            .subscribe(
                topic_call_three_durations_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_durations_method_resp =
            subscription_id_call_three_durations_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_one_binary_method_resp =
            format!("client/{}/callOneBinary/response", connection.client_id);
        let subscription_id_call_one_binary_method_resp = connection
            .subscribe(
                topic_call_one_binary_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_binary_method_resp =
            subscription_id_call_one_binary_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_optional_binary_method_resp = format!(
            "client/{}/callOptionalBinary/response",
            connection.client_id
        );
        let subscription_id_call_optional_binary_method_resp = connection
            .subscribe(
                topic_call_optional_binary_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_binary_method_resp =
            subscription_id_call_optional_binary_method_resp.unwrap_or_else(|_| usize::MAX);
        let topic_call_three_binaries_method_resp =
            format!("client/{}/callThreeBinaries/response", connection.client_id);
        let subscription_id_call_three_binaries_method_resp = connection
            .subscribe(
                topic_call_three_binaries_method_resp,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_binaries_method_resp =
            subscription_id_call_three_binaries_method_resp.unwrap_or_else(|_| usize::MAX);

        // Subscribe to all the topics needed for signals.
        let topic_empty_signal = format!("testAble/{}/signal/empty", service_id);
        let subscription_id_empty_signal = connection
            .subscribe(topic_empty_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_empty_signal =
            subscription_id_empty_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_int_signal = format!("testAble/{}/signal/singleInt", service_id);
        let subscription_id_single_int_signal = connection
            .subscribe(topic_single_int_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_single_int_signal =
            subscription_id_single_int_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_optional_int_signal =
            format!("testAble/{}/signal/singleOptionalInt", service_id);
        let subscription_id_single_optional_int_signal = connection
            .subscribe(
                topic_single_optional_int_signal,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_int_signal =
            subscription_id_single_optional_int_signal.unwrap_or_else(|_| usize::MAX);
        let topic_three_integers_signal = format!("testAble/{}/signal/threeIntegers", service_id);
        let subscription_id_three_integers_signal = connection
            .subscribe(topic_three_integers_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_three_integers_signal =
            subscription_id_three_integers_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_string_signal = format!("testAble/{}/signal/singleString", service_id);
        let subscription_id_single_string_signal = connection
            .subscribe(topic_single_string_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_single_string_signal =
            subscription_id_single_string_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_optional_string_signal =
            format!("testAble/{}/signal/singleOptionalString", service_id);
        let subscription_id_single_optional_string_signal = connection
            .subscribe(
                topic_single_optional_string_signal,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_string_signal =
            subscription_id_single_optional_string_signal.unwrap_or_else(|_| usize::MAX);
        let topic_three_strings_signal = format!("testAble/{}/signal/threeStrings", service_id);
        let subscription_id_three_strings_signal = connection
            .subscribe(topic_three_strings_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_three_strings_signal =
            subscription_id_three_strings_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_enum_signal = format!("testAble/{}/signal/singleEnum", service_id);
        let subscription_id_single_enum_signal = connection
            .subscribe(topic_single_enum_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_single_enum_signal =
            subscription_id_single_enum_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_optional_enum_signal =
            format!("testAble/{}/signal/singleOptionalEnum", service_id);
        let subscription_id_single_optional_enum_signal = connection
            .subscribe(
                topic_single_optional_enum_signal,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_enum_signal =
            subscription_id_single_optional_enum_signal.unwrap_or_else(|_| usize::MAX);
        let topic_three_enums_signal = format!("testAble/{}/signal/threeEnums", service_id);
        let subscription_id_three_enums_signal = connection
            .subscribe(topic_three_enums_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_three_enums_signal =
            subscription_id_three_enums_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_struct_signal = format!("testAble/{}/signal/singleStruct", service_id);
        let subscription_id_single_struct_signal = connection
            .subscribe(topic_single_struct_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_single_struct_signal =
            subscription_id_single_struct_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_optional_struct_signal =
            format!("testAble/{}/signal/singleOptionalStruct", service_id);
        let subscription_id_single_optional_struct_signal = connection
            .subscribe(
                topic_single_optional_struct_signal,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_struct_signal =
            subscription_id_single_optional_struct_signal.unwrap_or_else(|_| usize::MAX);
        let topic_three_structs_signal = format!("testAble/{}/signal/threeStructs", service_id);
        let subscription_id_three_structs_signal = connection
            .subscribe(topic_three_structs_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_three_structs_signal =
            subscription_id_three_structs_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_date_time_signal =
            format!("testAble/{}/signal/singleDateTime", service_id);
        let subscription_id_single_date_time_signal = connection
            .subscribe(
                topic_single_date_time_signal,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_date_time_signal =
            subscription_id_single_date_time_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_optional_datetime_signal =
            format!("testAble/{}/signal/singleOptionalDatetime", service_id);
        let subscription_id_single_optional_datetime_signal = connection
            .subscribe(
                topic_single_optional_datetime_signal,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_datetime_signal =
            subscription_id_single_optional_datetime_signal.unwrap_or_else(|_| usize::MAX);
        let topic_three_date_times_signal =
            format!("testAble/{}/signal/threeDateTimes", service_id);
        let subscription_id_three_date_times_signal = connection
            .subscribe(
                topic_three_date_times_signal,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_three_date_times_signal =
            subscription_id_three_date_times_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_duration_signal = format!("testAble/{}/signal/singleDuration", service_id);
        let subscription_id_single_duration_signal = connection
            .subscribe(topic_single_duration_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_single_duration_signal =
            subscription_id_single_duration_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_optional_duration_signal =
            format!("testAble/{}/signal/singleOptionalDuration", service_id);
        let subscription_id_single_optional_duration_signal = connection
            .subscribe(
                topic_single_optional_duration_signal,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_duration_signal =
            subscription_id_single_optional_duration_signal.unwrap_or_else(|_| usize::MAX);
        let topic_three_durations_signal = format!("testAble/{}/signal/threeDurations", service_id);
        let subscription_id_three_durations_signal = connection
            .subscribe(topic_three_durations_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_three_durations_signal =
            subscription_id_three_durations_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_binary_signal = format!("testAble/{}/signal/singleBinary", service_id);
        let subscription_id_single_binary_signal = connection
            .subscribe(topic_single_binary_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_single_binary_signal =
            subscription_id_single_binary_signal.unwrap_or_else(|_| usize::MAX);
        let topic_single_optional_binary_signal =
            format!("testAble/{}/signal/singleOptionalBinary", service_id);
        let subscription_id_single_optional_binary_signal = connection
            .subscribe(
                topic_single_optional_binary_signal,
                2,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_binary_signal =
            subscription_id_single_optional_binary_signal.unwrap_or_else(|_| usize::MAX);
        let topic_three_binaries_signal = format!("testAble/{}/signal/threeBinaries", service_id);
        let subscription_id_three_binaries_signal = connection
            .subscribe(topic_three_binaries_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_three_binaries_signal =
            subscription_id_three_binaries_signal.unwrap_or_else(|_| usize::MAX);

        // Subscribe to all the topics needed for properties.

        let topic_read_write_integer_property_value =
            format!("testAble/{}/property/readWriteInteger/value", service_id);
        let subscription_id_read_write_integer_property_value = connection
            .subscribe(
                topic_read_write_integer_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_integer_property_value =
            subscription_id_read_write_integer_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_only_integer_property_value =
            format!("testAble/{}/property/readOnlyInteger/value", service_id);
        let subscription_id_read_only_integer_property_value = connection
            .subscribe(
                topic_read_only_integer_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_only_integer_property_value =
            subscription_id_read_only_integer_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_optional_integer_property_value = format!(
            "testAble/{}/property/readWriteOptionalInteger/value",
            service_id
        );
        let subscription_id_read_write_optional_integer_property_value = connection
            .subscribe(
                topic_read_write_optional_integer_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_integer_property_value =
            subscription_id_read_write_optional_integer_property_value
                .unwrap_or_else(|_| usize::MAX);

        let topic_read_write_two_integers_property_value = format!(
            "testAble/{}/property/readWriteTwoIntegers/value",
            service_id
        );
        let subscription_id_read_write_two_integers_property_value = connection
            .subscribe(
                topic_read_write_two_integers_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_integers_property_value =
            subscription_id_read_write_two_integers_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_only_string_property_value =
            format!("testAble/{}/property/readOnlyString/value", service_id);
        let subscription_id_read_only_string_property_value = connection
            .subscribe(
                topic_read_only_string_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_only_string_property_value =
            subscription_id_read_only_string_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_string_property_value =
            format!("testAble/{}/property/readWriteString/value", service_id);
        let subscription_id_read_write_string_property_value = connection
            .subscribe(
                topic_read_write_string_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_string_property_value =
            subscription_id_read_write_string_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_optional_string_property_value = format!(
            "testAble/{}/property/readWriteOptionalString/value",
            service_id
        );
        let subscription_id_read_write_optional_string_property_value = connection
            .subscribe(
                topic_read_write_optional_string_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_string_property_value =
            subscription_id_read_write_optional_string_property_value
                .unwrap_or_else(|_| usize::MAX);

        let topic_read_write_two_strings_property_value =
            format!("testAble/{}/property/readWriteTwoStrings/value", service_id);
        let subscription_id_read_write_two_strings_property_value = connection
            .subscribe(
                topic_read_write_two_strings_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_strings_property_value =
            subscription_id_read_write_two_strings_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_struct_property_value =
            format!("testAble/{}/property/readWriteStruct/value", service_id);
        let subscription_id_read_write_struct_property_value = connection
            .subscribe(
                topic_read_write_struct_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_struct_property_value =
            subscription_id_read_write_struct_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_optional_struct_property_value = format!(
            "testAble/{}/property/readWriteOptionalStruct/value",
            service_id
        );
        let subscription_id_read_write_optional_struct_property_value = connection
            .subscribe(
                topic_read_write_optional_struct_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_struct_property_value =
            subscription_id_read_write_optional_struct_property_value
                .unwrap_or_else(|_| usize::MAX);

        let topic_read_write_two_structs_property_value =
            format!("testAble/{}/property/readWriteTwoStructs/value", service_id);
        let subscription_id_read_write_two_structs_property_value = connection
            .subscribe(
                topic_read_write_two_structs_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_structs_property_value =
            subscription_id_read_write_two_structs_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_only_enum_property_value =
            format!("testAble/{}/property/readOnlyEnum/value", service_id);
        let subscription_id_read_only_enum_property_value = connection
            .subscribe(
                topic_read_only_enum_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_only_enum_property_value =
            subscription_id_read_only_enum_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_enum_property_value =
            format!("testAble/{}/property/readWriteEnum/value", service_id);
        let subscription_id_read_write_enum_property_value = connection
            .subscribe(
                topic_read_write_enum_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_enum_property_value =
            subscription_id_read_write_enum_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_optional_enum_property_value = format!(
            "testAble/{}/property/readWriteOptionalEnum/value",
            service_id
        );
        let subscription_id_read_write_optional_enum_property_value = connection
            .subscribe(
                topic_read_write_optional_enum_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_enum_property_value =
            subscription_id_read_write_optional_enum_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_two_enums_property_value =
            format!("testAble/{}/property/readWriteTwoEnums/value", service_id);
        let subscription_id_read_write_two_enums_property_value = connection
            .subscribe(
                topic_read_write_two_enums_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_enums_property_value =
            subscription_id_read_write_two_enums_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_datetime_property_value =
            format!("testAble/{}/property/readWriteDatetime/value", service_id);
        let subscription_id_read_write_datetime_property_value = connection
            .subscribe(
                topic_read_write_datetime_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_datetime_property_value =
            subscription_id_read_write_datetime_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_optional_datetime_property_value = format!(
            "testAble/{}/property/readWriteOptionalDatetime/value",
            service_id
        );
        let subscription_id_read_write_optional_datetime_property_value = connection
            .subscribe(
                topic_read_write_optional_datetime_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_datetime_property_value =
            subscription_id_read_write_optional_datetime_property_value
                .unwrap_or_else(|_| usize::MAX);

        let topic_read_write_two_datetimes_property_value = format!(
            "testAble/{}/property/readWriteTwoDatetimes/value",
            service_id
        );
        let subscription_id_read_write_two_datetimes_property_value = connection
            .subscribe(
                topic_read_write_two_datetimes_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_datetimes_property_value =
            subscription_id_read_write_two_datetimes_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_duration_property_value =
            format!("testAble/{}/property/readWriteDuration/value", service_id);
        let subscription_id_read_write_duration_property_value = connection
            .subscribe(
                topic_read_write_duration_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_duration_property_value =
            subscription_id_read_write_duration_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_optional_duration_property_value = format!(
            "testAble/{}/property/readWriteOptionalDuration/value",
            service_id
        );
        let subscription_id_read_write_optional_duration_property_value = connection
            .subscribe(
                topic_read_write_optional_duration_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_duration_property_value =
            subscription_id_read_write_optional_duration_property_value
                .unwrap_or_else(|_| usize::MAX);

        let topic_read_write_two_durations_property_value = format!(
            "testAble/{}/property/readWriteTwoDurations/value",
            service_id
        );
        let subscription_id_read_write_two_durations_property_value = connection
            .subscribe(
                topic_read_write_two_durations_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_durations_property_value =
            subscription_id_read_write_two_durations_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_binary_property_value =
            format!("testAble/{}/property/readWriteBinary/value", service_id);
        let subscription_id_read_write_binary_property_value = connection
            .subscribe(
                topic_read_write_binary_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_binary_property_value =
            subscription_id_read_write_binary_property_value.unwrap_or_else(|_| usize::MAX);

        let topic_read_write_optional_binary_property_value = format!(
            "testAble/{}/property/readWriteOptionalBinary/value",
            service_id
        );
        let subscription_id_read_write_optional_binary_property_value = connection
            .subscribe(
                topic_read_write_optional_binary_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_binary_property_value =
            subscription_id_read_write_optional_binary_property_value
                .unwrap_or_else(|_| usize::MAX);

        let topic_read_write_two_binaries_property_value = format!(
            "testAble/{}/property/readWriteTwoBinaries/value",
            service_id
        );
        let subscription_id_read_write_two_binaries_property_value = connection
            .subscribe(
                topic_read_write_two_binaries_property_value,
                1,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_binaries_property_value =
            subscription_id_read_write_two_binaries_property_value.unwrap_or_else(|_| usize::MAX);

        let property_values = TestAbleProperties {
            read_write_integer: Arc::new(Mutex::new(None)),
            read_write_integer_tx_channel: watch::channel(None).0,

            read_only_integer: Arc::new(Mutex::new(None)),
            read_only_integer_tx_channel: watch::channel(None).0,

            read_write_optional_integer: Arc::new(Mutex::new(None)),
            read_write_optional_integer_tx_channel: watch::channel(None).0,
            read_write_two_integers: Arc::new(Mutex::new(None)),
            read_write_two_integers_tx_channel: watch::channel(None).0,

            read_only_string: Arc::new(Mutex::new(None)),
            read_only_string_tx_channel: watch::channel(None).0,

            read_write_string: Arc::new(Mutex::new(None)),
            read_write_string_tx_channel: watch::channel(None).0,

            read_write_optional_string: Arc::new(Mutex::new(None)),
            read_write_optional_string_tx_channel: watch::channel(None).0,
            read_write_two_strings: Arc::new(Mutex::new(None)),
            read_write_two_strings_tx_channel: watch::channel(None).0,

            read_write_struct: Arc::new(Mutex::new(None)),
            read_write_struct_tx_channel: watch::channel(None).0,

            read_write_optional_struct: Arc::new(Mutex::new(None)),
            read_write_optional_struct_tx_channel: watch::channel(None).0,
            read_write_two_structs: Arc::new(Mutex::new(None)),
            read_write_two_structs_tx_channel: watch::channel(None).0,

            read_only_enum: Arc::new(Mutex::new(None)),
            read_only_enum_tx_channel: watch::channel(None).0,

            read_write_enum: Arc::new(Mutex::new(None)),
            read_write_enum_tx_channel: watch::channel(None).0,

            read_write_optional_enum: Arc::new(Mutex::new(None)),
            read_write_optional_enum_tx_channel: watch::channel(None).0,
            read_write_two_enums: Arc::new(Mutex::new(None)),
            read_write_two_enums_tx_channel: watch::channel(None).0,

            read_write_datetime: Arc::new(Mutex::new(None)),
            read_write_datetime_tx_channel: watch::channel(None).0,

            read_write_optional_datetime: Arc::new(Mutex::new(None)),
            read_write_optional_datetime_tx_channel: watch::channel(None).0,
            read_write_two_datetimes: Arc::new(Mutex::new(None)),
            read_write_two_datetimes_tx_channel: watch::channel(None).0,

            read_write_duration: Arc::new(Mutex::new(None)),
            read_write_duration_tx_channel: watch::channel(None).0,

            read_write_optional_duration: Arc::new(Mutex::new(None)),
            read_write_optional_duration_tx_channel: watch::channel(None).0,
            read_write_two_durations: Arc::new(Mutex::new(None)),
            read_write_two_durations_tx_channel: watch::channel(None).0,

            read_write_binary: Arc::new(Mutex::new(None)),
            read_write_binary_tx_channel: watch::channel(None).0,

            read_write_optional_binary: Arc::new(Mutex::new(None)),
            read_write_optional_binary_tx_channel: watch::channel(None).0,
            read_write_two_binaries: Arc::new(Mutex::new(None)),
            read_write_two_binaries_tx_channel: watch::channel(None).0,
        };

        // Create structure for subscription ids.
        let sub_ids = TestAbleSubscriptionIds {
            call_with_nothing_method_resp: subscription_id_call_with_nothing_method_resp,
            call_one_integer_method_resp: subscription_id_call_one_integer_method_resp,
            call_optional_integer_method_resp: subscription_id_call_optional_integer_method_resp,
            call_three_integers_method_resp: subscription_id_call_three_integers_method_resp,
            call_one_string_method_resp: subscription_id_call_one_string_method_resp,
            call_optional_string_method_resp: subscription_id_call_optional_string_method_resp,
            call_three_strings_method_resp: subscription_id_call_three_strings_method_resp,
            call_one_enum_method_resp: subscription_id_call_one_enum_method_resp,
            call_optional_enum_method_resp: subscription_id_call_optional_enum_method_resp,
            call_three_enums_method_resp: subscription_id_call_three_enums_method_resp,
            call_one_struct_method_resp: subscription_id_call_one_struct_method_resp,
            call_optional_struct_method_resp: subscription_id_call_optional_struct_method_resp,
            call_three_structs_method_resp: subscription_id_call_three_structs_method_resp,
            call_one_date_time_method_resp: subscription_id_call_one_date_time_method_resp,
            call_optional_date_time_method_resp:
                subscription_id_call_optional_date_time_method_resp,
            call_three_date_times_method_resp: subscription_id_call_three_date_times_method_resp,
            call_one_duration_method_resp: subscription_id_call_one_duration_method_resp,
            call_optional_duration_method_resp: subscription_id_call_optional_duration_method_resp,
            call_three_durations_method_resp: subscription_id_call_three_durations_method_resp,
            call_one_binary_method_resp: subscription_id_call_one_binary_method_resp,
            call_optional_binary_method_resp: subscription_id_call_optional_binary_method_resp,
            call_three_binaries_method_resp: subscription_id_call_three_binaries_method_resp,
            empty_signal: Some(subscription_id_empty_signal),
            single_int_signal: Some(subscription_id_single_int_signal),
            single_optional_int_signal: Some(subscription_id_single_optional_int_signal),
            three_integers_signal: Some(subscription_id_three_integers_signal),
            single_string_signal: Some(subscription_id_single_string_signal),
            single_optional_string_signal: Some(subscription_id_single_optional_string_signal),
            three_strings_signal: Some(subscription_id_three_strings_signal),
            single_enum_signal: Some(subscription_id_single_enum_signal),
            single_optional_enum_signal: Some(subscription_id_single_optional_enum_signal),
            three_enums_signal: Some(subscription_id_three_enums_signal),
            single_struct_signal: Some(subscription_id_single_struct_signal),
            single_optional_struct_signal: Some(subscription_id_single_optional_struct_signal),
            three_structs_signal: Some(subscription_id_three_structs_signal),
            single_date_time_signal: Some(subscription_id_single_date_time_signal),
            single_optional_datetime_signal: Some(subscription_id_single_optional_datetime_signal),
            three_date_times_signal: Some(subscription_id_three_date_times_signal),
            single_duration_signal: Some(subscription_id_single_duration_signal),
            single_optional_duration_signal: Some(subscription_id_single_optional_duration_signal),
            three_durations_signal: Some(subscription_id_three_durations_signal),
            single_binary_signal: Some(subscription_id_single_binary_signal),
            single_optional_binary_signal: Some(subscription_id_single_optional_binary_signal),
            three_binaries_signal: Some(subscription_id_three_binaries_signal),
            read_write_integer_property_value: subscription_id_read_write_integer_property_value,
            read_only_integer_property_value: subscription_id_read_only_integer_property_value,
            read_write_optional_integer_property_value:
                subscription_id_read_write_optional_integer_property_value,
            read_write_two_integers_property_value:
                subscription_id_read_write_two_integers_property_value,
            read_only_string_property_value: subscription_id_read_only_string_property_value,
            read_write_string_property_value: subscription_id_read_write_string_property_value,
            read_write_optional_string_property_value:
                subscription_id_read_write_optional_string_property_value,
            read_write_two_strings_property_value:
                subscription_id_read_write_two_strings_property_value,
            read_write_struct_property_value: subscription_id_read_write_struct_property_value,
            read_write_optional_struct_property_value:
                subscription_id_read_write_optional_struct_property_value,
            read_write_two_structs_property_value:
                subscription_id_read_write_two_structs_property_value,
            read_only_enum_property_value: subscription_id_read_only_enum_property_value,
            read_write_enum_property_value: subscription_id_read_write_enum_property_value,
            read_write_optional_enum_property_value:
                subscription_id_read_write_optional_enum_property_value,
            read_write_two_enums_property_value:
                subscription_id_read_write_two_enums_property_value,
            read_write_datetime_property_value: subscription_id_read_write_datetime_property_value,
            read_write_optional_datetime_property_value:
                subscription_id_read_write_optional_datetime_property_value,
            read_write_two_datetimes_property_value:
                subscription_id_read_write_two_datetimes_property_value,
            read_write_duration_property_value: subscription_id_read_write_duration_property_value,
            read_write_optional_duration_property_value:
                subscription_id_read_write_optional_duration_property_value,
            read_write_two_durations_property_value:
                subscription_id_read_write_two_durations_property_value,
            read_write_binary_property_value: subscription_id_read_write_binary_property_value,
            read_write_optional_binary_property_value:
                subscription_id_read_write_optional_binary_property_value,
            read_write_two_binaries_property_value:
                subscription_id_read_write_two_binaries_property_value,
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = TestAbleSignalChannels {
            empty_sender: broadcast::channel(64).0,
            single_int_sender: broadcast::channel(64).0,
            single_optional_int_sender: broadcast::channel(64).0,
            three_integers_sender: broadcast::channel(64).0,
            single_string_sender: broadcast::channel(64).0,
            single_optional_string_sender: broadcast::channel(64).0,
            three_strings_sender: broadcast::channel(64).0,
            single_enum_sender: broadcast::channel(64).0,
            single_optional_enum_sender: broadcast::channel(64).0,
            three_enums_sender: broadcast::channel(64).0,
            single_struct_sender: broadcast::channel(64).0,
            single_optional_struct_sender: broadcast::channel(64).0,
            three_structs_sender: broadcast::channel(64).0,
            single_date_time_sender: broadcast::channel(64).0,
            single_optional_datetime_sender: broadcast::channel(64).0,
            three_date_times_sender: broadcast::channel(64).0,
            single_duration_sender: broadcast::channel(64).0,
            single_optional_duration_sender: broadcast::channel(64).0,
            three_durations_sender: broadcast::channel(64).0,
            single_binary_sender: broadcast::channel(64).0,
            single_optional_binary_sender: broadcast::channel(64).0,
            three_binaries_sender: broadcast::channel(64).0,
        };

        // Create TestAbleClient structure.
        let inst = TestAbleClient {
            mqttier_client: connection.clone(),
            pending_responses: Arc::new(Mutex::new(HashMap::new())),
            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,

            properties: property_values,

            subscription_ids: sub_ids,
            signal_channels: signal_channels,
            client_id: connection.client_id.to_string(),

            service_instance_id: service_id,
        };
        inst
    }

    /// Get the RX receiver side of the broadcast channel for the empty signal.
    /// The signal payload, `EmptySignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_empty_receiver(&self) -> broadcast::Receiver<()> {
        self.signal_channels.empty_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleInt signal.
    /// The signal payload, `SingleIntSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_int_receiver(&self) -> broadcast::Receiver<i32> {
        self.signal_channels.single_int_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleOptionalInt signal.
    /// The signal payload, `SingleOptionalIntSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_optional_int_receiver(&self) -> broadcast::Receiver<Option<i32>> {
        self.signal_channels.single_optional_int_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the threeIntegers signal.
    /// The signal payload, `ThreeIntegersSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_three_integers_receiver(&self) -> broadcast::Receiver<ThreeIntegersSignalPayload> {
        self.signal_channels.three_integers_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleString signal.
    /// The signal payload, `SingleStringSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_string_receiver(&self) -> broadcast::Receiver<String> {
        self.signal_channels.single_string_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleOptionalString signal.
    /// The signal payload, `SingleOptionalStringSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_optional_string_receiver(&self) -> broadcast::Receiver<Option<String>> {
        self.signal_channels
            .single_optional_string_sender
            .subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the threeStrings signal.
    /// The signal payload, `ThreeStringsSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_three_strings_receiver(&self) -> broadcast::Receiver<ThreeStringsSignalPayload> {
        self.signal_channels.three_strings_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleEnum signal.
    /// The signal payload, `SingleEnumSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_enum_receiver(&self) -> broadcast::Receiver<Numbers> {
        self.signal_channels.single_enum_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleOptionalEnum signal.
    /// The signal payload, `SingleOptionalEnumSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_optional_enum_receiver(&self) -> broadcast::Receiver<Option<Numbers>> {
        self.signal_channels.single_optional_enum_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the threeEnums signal.
    /// The signal payload, `ThreeEnumsSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_three_enums_receiver(&self) -> broadcast::Receiver<ThreeEnumsSignalPayload> {
        self.signal_channels.three_enums_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleStruct signal.
    /// The signal payload, `SingleStructSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_struct_receiver(&self) -> broadcast::Receiver<AllTypes> {
        self.signal_channels.single_struct_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleOptionalStruct signal.
    /// The signal payload, `SingleOptionalStructSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_optional_struct_receiver(&self) -> broadcast::Receiver<AllTypes> {
        self.signal_channels
            .single_optional_struct_sender
            .subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the threeStructs signal.
    /// The signal payload, `ThreeStructsSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_three_structs_receiver(&self) -> broadcast::Receiver<ThreeStructsSignalPayload> {
        self.signal_channels.three_structs_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleDateTime signal.
    /// The signal payload, `SingleDateTimeSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_date_time_receiver(
        &self,
    ) -> broadcast::Receiver<chrono::DateTime<chrono::Utc>> {
        self.signal_channels.single_date_time_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleOptionalDatetime signal.
    /// The signal payload, `SingleOptionalDatetimeSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_optional_datetime_receiver(
        &self,
    ) -> broadcast::Receiver<chrono::DateTime<chrono::Utc>> {
        self.signal_channels
            .single_optional_datetime_sender
            .subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the threeDateTimes signal.
    /// The signal payload, `ThreeDateTimesSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_three_date_times_receiver(
        &self,
    ) -> broadcast::Receiver<ThreeDateTimesSignalPayload> {
        self.signal_channels.three_date_times_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleDuration signal.
    /// The signal payload, `SingleDurationSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_duration_receiver(&self) -> broadcast::Receiver<chrono::Duration> {
        self.signal_channels.single_duration_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleOptionalDuration signal.
    /// The signal payload, `SingleOptionalDurationSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_optional_duration_receiver(&self) -> broadcast::Receiver<chrono::Duration> {
        self.signal_channels
            .single_optional_duration_sender
            .subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the threeDurations signal.
    /// The signal payload, `ThreeDurationsSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_three_durations_receiver(&self) -> broadcast::Receiver<ThreeDurationsSignalPayload> {
        self.signal_channels.three_durations_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleBinary signal.
    /// The signal payload, `SingleBinarySignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_binary_receiver(&self) -> broadcast::Receiver<Vec<u8>> {
        self.signal_channels.single_binary_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleOptionalBinary signal.
    /// The signal payload, `SingleOptionalBinarySignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_optional_binary_receiver(&self) -> broadcast::Receiver<Vec<u8>> {
        self.signal_channels
            .single_optional_binary_sender
            .subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the threeBinaries signal.
    /// The signal payload, `ThreeBinariesSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_three_binaries_receiver(&self) -> broadcast::Receiver<ThreeBinariesSignalPayload> {
        self.signal_channels.three_binaries_sender.subscribe()
    }

    async fn start_call_with_nothing(&mut self) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallWithNothingRequestObject {};

        let response_topic: String = format!("client/{}/callWithNothing/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callWithNothing",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callWithNothing` method.
    /// Method arguments are packed into a CallWithNothingRequestObject structure
    /// and published to the `testAble/{}/method/callWithNothing` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_with_nothing(&mut self) -> Result<(), MethodReturnCode> {
        let receiver = self.start_call_with_nothing().await;

        let _resp_str: String = receiver.await.unwrap();

        Ok(())
    }

    async fn start_call_one_integer(&mut self, input1: i32) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneIntegerRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneInteger/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOneInteger",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOneInteger` method.
    /// Method arguments are packed into a CallOneIntegerRequestObject structure
    /// and published to the `testAble/{}/method/callOneInteger` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_integer(&mut self, input1: i32) -> Result<i32, MethodReturnCode> {
        let receiver = self.start_call_one_integer(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOneIntegerReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_optional_integer(
        &mut self,
        input1: Option<i32>,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalIntegerRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalInteger/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOptionalInteger",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOptionalInteger` method.
    /// Method arguments are packed into a CallOptionalIntegerRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalInteger` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_integer(
        &mut self,
        input1: Option<i32>,
    ) -> Result<Option<i32>, MethodReturnCode> {
        let receiver = self.start_call_optional_integer(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOptionalIntegerReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_three_integers(
        &mut self,
        input1: i32,
        input2: i32,
        input3: Option<i32>,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallThreeIntegersRequestObject {
            input1: input1,
            input2: input2,
            input3: input3,
        };

        let response_topic: String =
            format!("client/{}/callThreeIntegers/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callThreeIntegers",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callThreeIntegers` method.
    /// Method arguments are packed into a CallThreeIntegersRequestObject structure
    /// and published to the `testAble/{}/method/callThreeIntegers` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_three_integers(
        &mut self,
        input1: i32,
        input2: i32,
        input3: Option<i32>,
    ) -> Result<CallThreeIntegersReturnValues, MethodReturnCode> {
        let receiver = self.start_call_three_integers(input1, input2, input3).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallThreeIntegersReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values)
    }

    async fn start_call_one_string(&mut self, input1: String) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneStringRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneString/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!("testAble/{}/method/callOneString", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOneString` method.
    /// Method arguments are packed into a CallOneStringRequestObject structure
    /// and published to the `testAble/{}/method/callOneString` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_string(&mut self, input1: String) -> Result<String, MethodReturnCode> {
        let receiver = self.start_call_one_string(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOneStringReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_optional_string(
        &mut self,
        input1: Option<String>,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalStringRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalString/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOptionalString",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOptionalString` method.
    /// Method arguments are packed into a CallOptionalStringRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalString` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_string(
        &mut self,
        input1: Option<String>,
    ) -> Result<Option<String>, MethodReturnCode> {
        let receiver = self.start_call_optional_string(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOptionalStringReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_three_strings(
        &mut self,
        input1: String,
        input2: Option<String>,
        input3: String,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallThreeStringsRequestObject {
            input1: input1,
            input2: input2,
            input3: input3,
        };

        let response_topic: String = format!("client/{}/callThreeStrings/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callThreeStrings",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callThreeStrings` method.
    /// Method arguments are packed into a CallThreeStringsRequestObject structure
    /// and published to the `testAble/{}/method/callThreeStrings` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_three_strings(
        &mut self,
        input1: String,
        input2: Option<String>,
        input3: String,
    ) -> Result<CallThreeStringsReturnValues, MethodReturnCode> {
        let receiver = self.start_call_three_strings(input1, input2, input3).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallThreeStringsReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values)
    }

    async fn start_call_one_enum(&mut self, input1: Numbers) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneEnumRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneEnum/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!("testAble/{}/method/callOneEnum", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOneEnum` method.
    /// Method arguments are packed into a CallOneEnumRequestObject structure
    /// and published to the `testAble/{}/method/callOneEnum` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_enum(&mut self, input1: Numbers) -> Result<Numbers, MethodReturnCode> {
        let receiver = self.start_call_one_enum(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOneEnumReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_optional_enum(
        &mut self,
        input1: Option<Numbers>,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalEnumRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOptionalEnum/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOptionalEnum",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOptionalEnum` method.
    /// Method arguments are packed into a CallOptionalEnumRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalEnum` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_enum(
        &mut self,
        input1: Option<Numbers>,
    ) -> Result<Option<Numbers>, MethodReturnCode> {
        let receiver = self.start_call_optional_enum(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOptionalEnumReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_three_enums(
        &mut self,
        input1: Numbers,
        input2: Numbers,
        input3: Option<Numbers>,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallThreeEnumsRequestObject {
            input1: input1,
            input2: input2,
            input3: input3,
        };

        let response_topic: String = format!("client/{}/callThreeEnums/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callThreeEnums",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callThreeEnums` method.
    /// Method arguments are packed into a CallThreeEnumsRequestObject structure
    /// and published to the `testAble/{}/method/callThreeEnums` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_three_enums(
        &mut self,
        input1: Numbers,
        input2: Numbers,
        input3: Option<Numbers>,
    ) -> Result<CallThreeEnumsReturnValues, MethodReturnCode> {
        let receiver = self.start_call_three_enums(input1, input2, input3).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallThreeEnumsReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values)
    }

    async fn start_call_one_struct(&mut self, input1: AllTypes) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneStructRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneStruct/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!("testAble/{}/method/callOneStruct", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOneStruct` method.
    /// Method arguments are packed into a CallOneStructRequestObject structure
    /// and published to the `testAble/{}/method/callOneStruct` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_struct(
        &mut self,
        input1: AllTypes,
    ) -> Result<AllTypes, MethodReturnCode> {
        let receiver = self.start_call_one_struct(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOneStructReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_optional_struct(&mut self, input1: AllTypes) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalStructRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalStruct/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOptionalStruct",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOptionalStruct` method.
    /// Method arguments are packed into a CallOptionalStructRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalStruct` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_struct(
        &mut self,
        input1: AllTypes,
    ) -> Result<AllTypes, MethodReturnCode> {
        let receiver = self.start_call_optional_struct(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOptionalStructReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_three_structs(
        &mut self,
        input1: AllTypes,
        input2: AllTypes,
        input3: AllTypes,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallThreeStructsRequestObject {
            input1: input1,
            input2: input2,
            input3: input3,
        };

        let response_topic: String = format!("client/{}/callThreeStructs/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callThreeStructs",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callThreeStructs` method.
    /// Method arguments are packed into a CallThreeStructsRequestObject structure
    /// and published to the `testAble/{}/method/callThreeStructs` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_three_structs(
        &mut self,
        input1: AllTypes,
        input2: AllTypes,
        input3: AllTypes,
    ) -> Result<CallThreeStructsReturnValues, MethodReturnCode> {
        let receiver = self.start_call_three_structs(input1, input2, input3).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallThreeStructsReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values)
    }

    async fn start_call_one_date_time(
        &mut self,
        input1: chrono::DateTime<chrono::Utc>,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneDateTimeRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneDateTime/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOneDateTime",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOneDateTime` method.
    /// Method arguments are packed into a CallOneDateTimeRequestObject structure
    /// and published to the `testAble/{}/method/callOneDateTime` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_date_time(
        &mut self,
        input1: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> {
        let receiver = self.start_call_one_date_time(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOneDateTimeReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_optional_date_time(
        &mut self,
        input1: chrono::DateTime<chrono::Utc>,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalDateTimeRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalDateTime/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOptionalDateTime",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOptionalDateTime` method.
    /// Method arguments are packed into a CallOptionalDateTimeRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalDateTime` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_date_time(
        &mut self,
        input1: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> {
        let receiver = self.start_call_optional_date_time(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOptionalDateTimeReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_three_date_times(
        &mut self,
        input1: chrono::DateTime<chrono::Utc>,
        input2: chrono::DateTime<chrono::Utc>,
        input3: chrono::DateTime<chrono::Utc>,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallThreeDateTimesRequestObject {
            input1: input1,
            input2: input2,
            input3: input3,
        };

        let response_topic: String =
            format!("client/{}/callThreeDateTimes/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callThreeDateTimes",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callThreeDateTimes` method.
    /// Method arguments are packed into a CallThreeDateTimesRequestObject structure
    /// and published to the `testAble/{}/method/callThreeDateTimes` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_three_date_times(
        &mut self,
        input1: chrono::DateTime<chrono::Utc>,
        input2: chrono::DateTime<chrono::Utc>,
        input3: chrono::DateTime<chrono::Utc>,
    ) -> Result<CallThreeDateTimesReturnValues, MethodReturnCode> {
        let receiver = self
            .start_call_three_date_times(input1, input2, input3)
            .await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallThreeDateTimesReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values)
    }

    async fn start_call_one_duration(
        &mut self,
        input1: chrono::Duration,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneDurationRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneDuration/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOneDuration",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOneDuration` method.
    /// Method arguments are packed into a CallOneDurationRequestObject structure
    /// and published to the `testAble/{}/method/callOneDuration` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_duration(
        &mut self,
        input1: chrono::Duration,
    ) -> Result<chrono::Duration, MethodReturnCode> {
        let receiver = self.start_call_one_duration(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOneDurationReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_optional_duration(
        &mut self,
        input1: chrono::Duration,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalDurationRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalDuration/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOptionalDuration",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOptionalDuration` method.
    /// Method arguments are packed into a CallOptionalDurationRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalDuration` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_duration(
        &mut self,
        input1: chrono::Duration,
    ) -> Result<chrono::Duration, MethodReturnCode> {
        let receiver = self.start_call_optional_duration(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOptionalDurationReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_three_durations(
        &mut self,
        input1: chrono::Duration,
        input2: chrono::Duration,
        input3: chrono::Duration,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallThreeDurationsRequestObject {
            input1: input1,
            input2: input2,
            input3: input3,
        };

        let response_topic: String =
            format!("client/{}/callThreeDurations/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callThreeDurations",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callThreeDurations` method.
    /// Method arguments are packed into a CallThreeDurationsRequestObject structure
    /// and published to the `testAble/{}/method/callThreeDurations` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_three_durations(
        &mut self,
        input1: chrono::Duration,
        input2: chrono::Duration,
        input3: chrono::Duration,
    ) -> Result<CallThreeDurationsReturnValues, MethodReturnCode> {
        let receiver = self
            .start_call_three_durations(input1, input2, input3)
            .await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallThreeDurationsReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values)
    }

    async fn start_call_one_binary(&mut self, input1: Vec<u8>) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneBinaryRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneBinary/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!("testAble/{}/method/callOneBinary", self.service_instance_id),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOneBinary` method.
    /// Method arguments are packed into a CallOneBinaryRequestObject structure
    /// and published to the `testAble/{}/method/callOneBinary` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_binary(&mut self, input1: Vec<u8>) -> Result<Vec<u8>, MethodReturnCode> {
        let receiver = self.start_call_one_binary(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOneBinaryReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_optional_binary(&mut self, input1: Vec<u8>) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalBinaryRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalBinary/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callOptionalBinary",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callOptionalBinary` method.
    /// Method arguments are packed into a CallOptionalBinaryRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalBinary` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_binary(
        &mut self,
        input1: Vec<u8>,
    ) -> Result<Vec<u8>, MethodReturnCode> {
        let receiver = self.start_call_optional_binary(input1).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallOptionalBinaryReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values.output1)
    }

    async fn start_call_three_binaries(
        &mut self,
        input1: Vec<u8>,
        input2: Vec<u8>,
        input3: Vec<u8>,
    ) -> oneshot::Receiver<String> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let correlation_data = correlation_id.as_bytes().to_vec();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallThreeBinariesRequestObject {
            input1: input1,
            input2: input2,
            input3: input3,
        };

        let response_topic: String =
            format!("client/{}/callThreeBinaries/response", self.client_id);
        let _ = self
            .mqttier_client
            .publish_request(
                format!(
                    "testAble/{}/method/callThreeBinaries",
                    self.service_instance_id
                ),
                &data,
                response_topic,
                correlation_data,
            )
            .await;
        receiver
    }

    /// The `callThreeBinaries` method.
    /// Method arguments are packed into a CallThreeBinariesRequestObject structure
    /// and published to the `testAble/{}/method/callThreeBinaries` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_three_binaries(
        &mut self,
        input1: Vec<u8>,
        input2: Vec<u8>,
        input3: Vec<u8>,
    ) -> Result<CallThreeBinariesReturnValues, MethodReturnCode> {
        let receiver = self.start_call_three_binaries(input1, input2, input3).await;

        let resp_str: String = receiver.await.unwrap();

        let return_values: CallThreeBinariesReturnValues = serde_json::from_str(&resp_str)
            .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

        Ok(return_values)
    }

    /// Watch for changes to the `read_write_integer` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_integer(&self) -> watch::Receiver<Option<i32>> {
        self.properties.read_write_integer_tx_channel.subscribe()
    }

    pub fn set_read_write_integer(&mut self, value: i32) -> Result<(), MethodReturnCode> {
        let data = ReadWriteIntegerProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteInteger/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_only_integer` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_only_integer(&self) -> watch::Receiver<Option<i32>> {
        self.properties.read_only_integer_tx_channel.subscribe()
    }

    /// Watch for changes to the `read_write_optional_integer` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_integer(&self) -> watch::Receiver<Option<Option<i32>>> {
        self.properties
            .read_write_optional_integer_tx_channel
            .subscribe()
    }

    pub fn set_read_write_optional_integer(
        &mut self,
        value: Option<i32>,
    ) -> Result<(), MethodReturnCode> {
        let data = ReadWriteOptionalIntegerProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteOptionalInteger/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_two_integers` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_integers(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoIntegersProperty>> {
        self.properties
            .read_write_two_integers_tx_channel
            .subscribe()
    }

    pub fn set_read_write_two_integers(
        &mut self,
        value: ReadWriteTwoIntegersProperty,
    ) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteTwoIntegers/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_only_string` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_only_string(&self) -> watch::Receiver<Option<String>> {
        self.properties.read_only_string_tx_channel.subscribe()
    }

    /// Watch for changes to the `read_write_string` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_string(&self) -> watch::Receiver<Option<String>> {
        self.properties.read_write_string_tx_channel.subscribe()
    }

    pub fn set_read_write_string(&mut self, value: String) -> Result<(), MethodReturnCode> {
        let data = ReadWriteStringProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteString/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_optional_string` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_string(&self) -> watch::Receiver<Option<Option<String>>> {
        self.properties
            .read_write_optional_string_tx_channel
            .subscribe()
    }

    pub fn set_read_write_optional_string(
        &mut self,
        value: Option<String>,
    ) -> Result<(), MethodReturnCode> {
        let data = ReadWriteOptionalStringProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteOptionalString/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_two_strings` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_strings(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoStringsProperty>> {
        self.properties
            .read_write_two_strings_tx_channel
            .subscribe()
    }

    pub fn set_read_write_two_strings(
        &mut self,
        value: ReadWriteTwoStringsProperty,
    ) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteTwoStrings/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_struct` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_struct(&self) -> watch::Receiver<Option<AllTypes>> {
        self.properties.read_write_struct_tx_channel.subscribe()
    }

    pub fn set_read_write_struct(&mut self, value: AllTypes) -> Result<(), MethodReturnCode> {
        let data = ReadWriteStructProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteStruct/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_optional_struct` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_struct(&self) -> watch::Receiver<Option<AllTypes>> {
        self.properties
            .read_write_optional_struct_tx_channel
            .subscribe()
    }

    pub fn set_read_write_optional_struct(
        &mut self,
        value: AllTypes,
    ) -> Result<(), MethodReturnCode> {
        let data = ReadWriteOptionalStructProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteOptionalStruct/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_two_structs` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_structs(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoStructsProperty>> {
        self.properties
            .read_write_two_structs_tx_channel
            .subscribe()
    }

    pub fn set_read_write_two_structs(
        &mut self,
        value: ReadWriteTwoStructsProperty,
    ) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteTwoStructs/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_only_enum` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_only_enum(&self) -> watch::Receiver<Option<Numbers>> {
        self.properties.read_only_enum_tx_channel.subscribe()
    }

    /// Watch for changes to the `read_write_enum` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_enum(&self) -> watch::Receiver<Option<Numbers>> {
        self.properties.read_write_enum_tx_channel.subscribe()
    }

    pub fn set_read_write_enum(&mut self, value: Numbers) -> Result<(), MethodReturnCode> {
        let data = ReadWriteEnumProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteEnum/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_optional_enum` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_enum(&self) -> watch::Receiver<Option<Option<Numbers>>> {
        self.properties
            .read_write_optional_enum_tx_channel
            .subscribe()
    }

    pub fn set_read_write_optional_enum(
        &mut self,
        value: Option<Numbers>,
    ) -> Result<(), MethodReturnCode> {
        let data = ReadWriteOptionalEnumProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteOptionalEnum/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_two_enums` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_enums(&self) -> watch::Receiver<Option<ReadWriteTwoEnumsProperty>> {
        self.properties.read_write_two_enums_tx_channel.subscribe()
    }

    pub fn set_read_write_two_enums(
        &mut self,
        value: ReadWriteTwoEnumsProperty,
    ) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteTwoEnums/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_datetime` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_datetime(
        &self,
    ) -> watch::Receiver<Option<chrono::DateTime<chrono::Utc>>> {
        self.properties.read_write_datetime_tx_channel.subscribe()
    }

    pub fn set_read_write_datetime(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> Result<(), MethodReturnCode> {
        let data = ReadWriteDatetimeProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteDatetime/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_optional_datetime` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_datetime(
        &self,
    ) -> watch::Receiver<Option<chrono::DateTime<chrono::Utc>>> {
        self.properties
            .read_write_optional_datetime_tx_channel
            .subscribe()
    }

    pub fn set_read_write_optional_datetime(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> Result<(), MethodReturnCode> {
        let data = ReadWriteOptionalDatetimeProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteOptionalDatetime/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_two_datetimes` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_datetimes(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoDatetimesProperty>> {
        self.properties
            .read_write_two_datetimes_tx_channel
            .subscribe()
    }

    pub fn set_read_write_two_datetimes(
        &mut self,
        value: ReadWriteTwoDatetimesProperty,
    ) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteTwoDatetimes/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_duration` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_duration(&self) -> watch::Receiver<Option<chrono::Duration>> {
        self.properties.read_write_duration_tx_channel.subscribe()
    }

    pub fn set_read_write_duration(
        &mut self,
        value: chrono::Duration,
    ) -> Result<(), MethodReturnCode> {
        let data = ReadWriteDurationProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteDuration/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_optional_duration` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_duration(&self) -> watch::Receiver<Option<chrono::Duration>> {
        self.properties
            .read_write_optional_duration_tx_channel
            .subscribe()
    }

    pub fn set_read_write_optional_duration(
        &mut self,
        value: chrono::Duration,
    ) -> Result<(), MethodReturnCode> {
        let data = ReadWriteOptionalDurationProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteOptionalDuration/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_two_durations` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_durations(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoDurationsProperty>> {
        self.properties
            .read_write_two_durations_tx_channel
            .subscribe()
    }

    pub fn set_read_write_two_durations(
        &mut self,
        value: ReadWriteTwoDurationsProperty,
    ) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteTwoDurations/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_binary` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_binary(&self) -> watch::Receiver<Option<Vec<u8>>> {
        self.properties.read_write_binary_tx_channel.subscribe()
    }

    pub fn set_read_write_binary(&mut self, value: Vec<u8>) -> Result<(), MethodReturnCode> {
        let data = ReadWriteBinaryProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteBinary/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_optional_binary` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_binary(&self) -> watch::Receiver<Option<Vec<u8>>> {
        self.properties
            .read_write_optional_binary_tx_channel
            .subscribe()
    }

    pub fn set_read_write_optional_binary(
        &mut self,
        value: Vec<u8>,
    ) -> Result<(), MethodReturnCode> {
        let data = ReadWriteOptionalBinaryProperty { value: value };
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteOptionalBinary/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Watch for changes to the `read_write_two_binaries` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_binaries(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoBinariesProperty>> {
        self.properties
            .read_write_two_binaries_tx_channel
            .subscribe()
    }

    pub fn set_read_write_two_binaries(
        &mut self,
        value: ReadWriteTwoBinariesProperty,
    ) -> Result<(), MethodReturnCode> {
        let data = value;
        let _publish_result = self.mqttier_client.publish_structure(
            "testAble/{}/property/readWriteTwoBinaries/setValue".to_string(),
            &data,
        );
        Ok(())
    }

    /// Starts the tasks that process messages received.
    pub async fn run_loop(&self) -> Result<(), JoinError> {
        // Make sure the MqttierClient is connected and running.
        let _ = self.mqttier_client.run_loop().await;

        // Clone the Arc pointer to the map.  This will be moved into the loop_task.
        let resp_map: Arc<Mutex<HashMap<Uuid, oneshot::Sender<String>>>> =
            self.pending_responses.clone();

        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = {
            let mut guard = self.msg_streamer_rx.lock().expect("Mutex was poisoned");
            guard.take().expect("msg_streamer_rx should be Some")
        };

        let sig_chans = self.signal_channels.clone();

        let sub_ids = self.subscription_ids.clone();
        let props = self.properties.clone();

        let _loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                let opt_corr_data: Option<Vec<u8>> = msg.correlation_data.clone();
                let opt_corr_id: Option<Uuid> =
                    opt_corr_data.and_then(|b| Uuid::from_slice(b.as_slice()).ok());

                let payload = String::from_utf8_lossy(&msg.payload).to_string();
                if msg.subscription_id == sub_ids.call_with_nothing_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_one_integer_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_optional_integer_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_three_integers_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_one_string_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_optional_string_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_three_strings_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_one_enum_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_optional_enum_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_three_enums_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_one_struct_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_optional_struct_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_three_structs_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_one_date_time_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_optional_date_time_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_three_date_times_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_one_duration_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_optional_duration_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_three_durations_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_one_binary_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_optional_binary_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                } else if msg.subscription_id == sub_ids.call_three_binaries_method_resp {
                    // TODO: Simplify subscription because we'll always look up by correlation id.
                    if opt_corr_id.is_some() {
                        let opt_sender = opt_corr_id.and_then(|uuid| {
                            let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                            hashmap.remove(&uuid)
                        });
                        if let Some(sender) = opt_sender {
                            let oss: oneshot::Sender<String> = sender;
                            match oss.send(payload) {
                                Ok(_) => (),
                                Err(_) => (),
                            }
                        }
                    }
                }

                if msg.subscription_id == sub_ids.empty_signal.unwrap_or_default() {
                    let chan = sig_chans.empty_sender.clone();

                    let _send_result = chan.send(());
                } else if msg.subscription_id == sub_ids.single_int_signal.unwrap_or_default() {
                    let chan = sig_chans.single_int_sender.clone();

                    match serde_json::from_slice::<SingleIntSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SingleIntSignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id
                    == sub_ids.single_optional_int_signal.unwrap_or_default()
                {
                    let chan = sig_chans.single_optional_int_sender.clone();

                    match serde_json::from_slice::<SingleOptionalIntSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleOptionalIntSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.three_integers_signal.unwrap_or_default() {
                    let chan = sig_chans.three_integers_sender.clone();

                    match serde_json::from_slice::<ThreeIntegersSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into ThreeIntegersSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.single_string_signal.unwrap_or_default() {
                    let chan = sig_chans.single_string_sender.clone();

                    match serde_json::from_slice::<SingleStringSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleStringSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id
                    == sub_ids.single_optional_string_signal.unwrap_or_default()
                {
                    let chan = sig_chans.single_optional_string_sender.clone();

                    match serde_json::from_slice::<SingleOptionalStringSignalPayload>(&msg.payload)
                    {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleOptionalStringSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.three_strings_signal.unwrap_or_default() {
                    let chan = sig_chans.three_strings_sender.clone();

                    match serde_json::from_slice::<ThreeStringsSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into ThreeStringsSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.single_enum_signal.unwrap_or_default() {
                    let chan = sig_chans.single_enum_sender.clone();

                    match serde_json::from_slice::<SingleEnumSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SingleEnumSignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id
                    == sub_ids.single_optional_enum_signal.unwrap_or_default()
                {
                    let chan = sig_chans.single_optional_enum_sender.clone();

                    match serde_json::from_slice::<SingleOptionalEnumSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleOptionalEnumSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.three_enums_signal.unwrap_or_default() {
                    let chan = sig_chans.three_enums_sender.clone();

                    match serde_json::from_slice::<ThreeEnumsSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl);
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into ThreeEnumsSignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.single_struct_signal.unwrap_or_default() {
                    let chan = sig_chans.single_struct_sender.clone();

                    match serde_json::from_slice::<SingleStructSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleStructSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id
                    == sub_ids.single_optional_struct_signal.unwrap_or_default()
                {
                    let chan = sig_chans.single_optional_struct_sender.clone();

                    match serde_json::from_slice::<SingleOptionalStructSignalPayload>(&msg.payload)
                    {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleOptionalStructSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.three_structs_signal.unwrap_or_default() {
                    let chan = sig_chans.three_structs_sender.clone();

                    match serde_json::from_slice::<ThreeStructsSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into ThreeStructsSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.single_date_time_signal.unwrap_or_default()
                {
                    let chan = sig_chans.single_date_time_sender.clone();

                    match serde_json::from_slice::<SingleDateTimeSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleDateTimeSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id
                    == sub_ids.single_optional_datetime_signal.unwrap_or_default()
                {
                    let chan = sig_chans.single_optional_datetime_sender.clone();

                    match serde_json::from_slice::<SingleOptionalDatetimeSignalPayload>(
                        &msg.payload,
                    ) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleOptionalDatetimeSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.three_date_times_signal.unwrap_or_default()
                {
                    let chan = sig_chans.three_date_times_sender.clone();

                    match serde_json::from_slice::<ThreeDateTimesSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into ThreeDateTimesSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.single_duration_signal.unwrap_or_default()
                {
                    let chan = sig_chans.single_duration_sender.clone();

                    match serde_json::from_slice::<SingleDurationSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleDurationSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id
                    == sub_ids.single_optional_duration_signal.unwrap_or_default()
                {
                    let chan = sig_chans.single_optional_duration_sender.clone();

                    match serde_json::from_slice::<SingleOptionalDurationSignalPayload>(
                        &msg.payload,
                    ) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleOptionalDurationSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.three_durations_signal.unwrap_or_default()
                {
                    let chan = sig_chans.three_durations_sender.clone();

                    match serde_json::from_slice::<ThreeDurationsSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into ThreeDurationsSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.single_binary_signal.unwrap_or_default() {
                    let chan = sig_chans.single_binary_sender.clone();

                    match serde_json::from_slice::<SingleBinarySignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleBinarySignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id
                    == sub_ids.single_optional_binary_signal.unwrap_or_default()
                {
                    let chan = sig_chans.single_optional_binary_sender.clone();

                    match serde_json::from_slice::<SingleOptionalBinarySignalPayload>(&msg.payload)
                    {
                        Ok(pl) => {
                            let _send_result = chan.send(pl.value);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into SingleOptionalBinarySignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.three_binaries_signal.unwrap_or_default() {
                    let chan = sig_chans.three_binaries_sender.clone();

                    match serde_json::from_slice::<ThreeBinariesSignalPayload>(&msg.payload) {
                        Ok(pl) => {
                            let _send_result = chan.send(pl);
                        }
                        Err(e) => {
                            eprintln!(
                                "Failed to deserialize into ThreeBinariesSignalPayload: {}",
                                e
                            );
                            continue;
                        }
                    }
                }

                if msg.subscription_id == sub_ids.read_write_integer_property_value {
                    match serde_json::from_slice::<ReadWriteIntegerProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard =
                                props.read_write_integer.lock().expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_write_integer_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_only_integer_property_value {
                    match serde_json::from_slice::<ReadOnlyIntegerProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard =
                                props.read_only_integer.lock().expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_only_integer_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_optional_integer_property_value
                {
                    match serde_json::from_slice::<ReadWriteOptionalIntegerProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_optional_integer
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props
                                .read_write_optional_integer_tx_channel
                                .send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_two_integers_property_value {
                    match serde_json::from_slice::<ReadWriteTwoIntegersProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_two_integers
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.clone());
                            let _ = props.read_write_two_integers_tx_channel.send(Some(pl));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_only_string_property_value {
                    match serde_json::from_slice::<ReadOnlyStringProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard =
                                props.read_only_string.lock().expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_only_string_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_string_property_value {
                    match serde_json::from_slice::<ReadWriteStringProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard =
                                props.read_write_string.lock().expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_write_string_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_optional_string_property_value {
                    match serde_json::from_slice::<ReadWriteOptionalStringProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_optional_string
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props
                                .read_write_optional_string_tx_channel
                                .send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_two_strings_property_value {
                    match serde_json::from_slice::<ReadWriteTwoStringsProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_two_strings
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.clone());
                            let _ = props.read_write_two_strings_tx_channel.send(Some(pl));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_struct_property_value {
                    match serde_json::from_slice::<ReadWriteStructProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard =
                                props.read_write_struct.lock().expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_write_struct_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_optional_struct_property_value {
                    match serde_json::from_slice::<ReadWriteOptionalStructProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_optional_struct
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props
                                .read_write_optional_struct_tx_channel
                                .send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_two_structs_property_value {
                    match serde_json::from_slice::<ReadWriteTwoStructsProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_two_structs
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.clone());
                            let _ = props.read_write_two_structs_tx_channel.send(Some(pl));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_only_enum_property_value {
                    match serde_json::from_slice::<ReadOnlyEnumProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard =
                                props.read_only_enum.lock().expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_only_enum_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_enum_property_value {
                    match serde_json::from_slice::<ReadWriteEnumProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard =
                                props.read_write_enum.lock().expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_write_enum_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_optional_enum_property_value {
                    match serde_json::from_slice::<ReadWriteOptionalEnumProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_optional_enum
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props
                                .read_write_optional_enum_tx_channel
                                .send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_two_enums_property_value {
                    match serde_json::from_slice::<ReadWriteTwoEnumsProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_two_enums
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.clone());
                            let _ = props.read_write_two_enums_tx_channel.send(Some(pl));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_datetime_property_value {
                    match serde_json::from_slice::<ReadWriteDatetimeProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_datetime
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_write_datetime_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_optional_datetime_property_value
                {
                    match serde_json::from_slice::<ReadWriteOptionalDatetimeProperty>(&msg.payload)
                    {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_optional_datetime
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props
                                .read_write_optional_datetime_tx_channel
                                .send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_two_datetimes_property_value {
                    match serde_json::from_slice::<ReadWriteTwoDatetimesProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_two_datetimes
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.clone());
                            let _ = props.read_write_two_datetimes_tx_channel.send(Some(pl));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_duration_property_value {
                    match serde_json::from_slice::<ReadWriteDurationProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_duration
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_write_duration_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_optional_duration_property_value
                {
                    match serde_json::from_slice::<ReadWriteOptionalDurationProperty>(&msg.payload)
                    {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_optional_duration
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props
                                .read_write_optional_duration_tx_channel
                                .send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_two_durations_property_value {
                    match serde_json::from_slice::<ReadWriteTwoDurationsProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_two_durations
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.clone());
                            let _ = props.read_write_two_durations_tx_channel.send(Some(pl));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_binary_property_value {
                    match serde_json::from_slice::<ReadWriteBinaryProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard =
                                props.read_write_binary.lock().expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props.read_write_binary_tx_channel.send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_optional_binary_property_value {
                    match serde_json::from_slice::<ReadWriteOptionalBinaryProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_optional_binary
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.value.clone());
                            let _ = props
                                .read_write_optional_binary_tx_channel
                                .send(Some(pl.value));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                } else if msg.subscription_id == sub_ids.read_write_two_binaries_property_value {
                    match serde_json::from_slice::<ReadWriteTwoBinariesProperty>(&msg.payload) {
                        Ok(pl) => {
                            let mut guard = props
                                .read_write_two_binaries
                                .lock()
                                .expect("Mutex was poisoned");

                            *guard = Some(pl.clone());
                            let _ = props.read_write_two_binaries_tx_channel.send(Some(pl));
                        }
                        Err(e) => {
                            eprintln!("Failed to deserialize into SignalPayload: {}", e);
                            continue;
                        }
                    }
                }
            }
        });

        println!("Started client receive task");
        Ok(())
    }
}
