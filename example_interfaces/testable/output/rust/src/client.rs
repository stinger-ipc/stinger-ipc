//! Client module for Test Able IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Test Able interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/
use crate::discovery::DiscoveredService;
use crate::message;
#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
#[allow(unused_imports)]
use iso8601_duration::Duration as IsoDuration;
use serde_json;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use stinger_mqtt_trait::message::{MqttMessage, QoS};
#[cfg(feature = "client")]
use stinger_mqtt_trait::Mqtt5PubSub;
use tokio::sync::{broadcast, oneshot, watch};
use tokio::task::JoinError;
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};
use uuid::Uuid;

use std::sync::atomic::{AtomicU32, Ordering};
#[allow(unused_imports)]
use stinger_rwlock_watch::ReadOnlyLockWatch;
use stinger_rwlock_watch::RwLockWatch;
#[allow(unused_imports)]
use stinger_rwlock_watch::WriteRequestLockWatch;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct TestAbleSubscriptionIds {
    call_with_nothing_method_resp: u32,
    call_one_integer_method_resp: u32,
    call_optional_integer_method_resp: u32,
    call_three_integers_method_resp: u32,
    call_one_string_method_resp: u32,
    call_optional_string_method_resp: u32,
    call_three_strings_method_resp: u32,
    call_one_enum_method_resp: u32,
    call_optional_enum_method_resp: u32,
    call_three_enums_method_resp: u32,
    call_one_struct_method_resp: u32,
    call_optional_struct_method_resp: u32,
    call_three_structs_method_resp: u32,
    call_one_date_time_method_resp: u32,
    call_optional_date_time_method_resp: u32,
    call_three_date_times_method_resp: u32,
    call_one_duration_method_resp: u32,
    call_optional_duration_method_resp: u32,
    call_three_durations_method_resp: u32,
    call_one_binary_method_resp: u32,
    call_optional_binary_method_resp: u32,
    call_three_binaries_method_resp: u32,
    call_one_list_of_integers_method_resp: u32,
    call_optional_list_of_floats_method_resp: u32,
    call_two_lists_method_resp: u32,

    empty_signal: Option<u32>,
    single_int_signal: Option<u32>,
    single_optional_int_signal: Option<u32>,
    three_integers_signal: Option<u32>,
    single_string_signal: Option<u32>,
    single_optional_string_signal: Option<u32>,
    three_strings_signal: Option<u32>,
    single_enum_signal: Option<u32>,
    single_optional_enum_signal: Option<u32>,
    three_enums_signal: Option<u32>,
    single_struct_signal: Option<u32>,
    single_optional_struct_signal: Option<u32>,
    three_structs_signal: Option<u32>,
    single_date_time_signal: Option<u32>,
    single_optional_datetime_signal: Option<u32>,
    three_date_times_signal: Option<u32>,
    single_duration_signal: Option<u32>,
    single_optional_duration_signal: Option<u32>,
    three_durations_signal: Option<u32>,
    single_binary_signal: Option<u32>,
    single_optional_binary_signal: Option<u32>,
    three_binaries_signal: Option<u32>,
    single_array_of_integers_signal: Option<u32>,
    single_optional_array_of_strings_signal: Option<u32>,
    array_of_every_type_signal: Option<u32>,
    read_write_integer_property_value: u32,
    read_only_integer_property_value: u32,
    read_write_optional_integer_property_value: u32,
    read_write_two_integers_property_value: u32,
    read_only_string_property_value: u32,
    read_write_string_property_value: u32,
    read_write_optional_string_property_value: u32,
    read_write_two_strings_property_value: u32,
    read_write_struct_property_value: u32,
    read_write_optional_struct_property_value: u32,
    read_write_two_structs_property_value: u32,
    read_only_enum_property_value: u32,
    read_write_enum_property_value: u32,
    read_write_optional_enum_property_value: u32,
    read_write_two_enums_property_value: u32,
    read_write_datetime_property_value: u32,
    read_write_optional_datetime_property_value: u32,
    read_write_two_datetimes_property_value: u32,
    read_write_duration_property_value: u32,
    read_write_optional_duration_property_value: u32,
    read_write_two_durations_property_value: u32,
    read_write_binary_property_value: u32,
    read_write_optional_binary_property_value: u32,
    read_write_two_binaries_property_value: u32,
    read_write_list_of_strings_property_value: u32,
    read_write_lists_property_value: u32,
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
    single_optional_struct_sender: broadcast::Sender<Option<AllTypes>>,
    three_structs_sender: broadcast::Sender<ThreeStructsSignalPayload>,
    single_date_time_sender: broadcast::Sender<chrono::DateTime<chrono::Utc>>,
    single_optional_datetime_sender: broadcast::Sender<Option<chrono::DateTime<chrono::Utc>>>,
    three_date_times_sender: broadcast::Sender<ThreeDateTimesSignalPayload>,
    single_duration_sender: broadcast::Sender<chrono::Duration>,
    single_optional_duration_sender: broadcast::Sender<Option<chrono::Duration>>,
    three_durations_sender: broadcast::Sender<ThreeDurationsSignalPayload>,
    single_binary_sender: broadcast::Sender<Vec<u8>>,
    single_optional_binary_sender: broadcast::Sender<Option<Vec<u8>>>,
    three_binaries_sender: broadcast::Sender<ThreeBinariesSignalPayload>,
    single_array_of_integers_sender: broadcast::Sender<Vec<i32>>,
    single_optional_array_of_strings_sender: broadcast::Sender<Option<Vec<String>>>,
    array_of_every_type_sender: broadcast::Sender<ArrayOfEveryTypeSignalPayload>,
}

#[derive(Clone)]
struct TestAbleProperties {
    pub read_write_integer: Arc<RwLockWatch<i32>>,
    pub read_write_integer_version: Arc<AtomicU32>,

    pub read_only_integer: Arc<RwLockWatch<i32>>,
    pub read_only_integer_version: Arc<AtomicU32>,

    pub read_write_optional_integer: Arc<RwLockWatch<Option<i32>>>,
    pub read_write_optional_integer_version: Arc<AtomicU32>,

    pub read_write_two_integers: Arc<RwLockWatch<ReadWriteTwoIntegersProperty>>,
    pub read_write_two_integers_version: Arc<AtomicU32>,

    pub read_only_string: Arc<RwLockWatch<String>>,
    pub read_only_string_version: Arc<AtomicU32>,

    pub read_write_string: Arc<RwLockWatch<String>>,
    pub read_write_string_version: Arc<AtomicU32>,

    pub read_write_optional_string: Arc<RwLockWatch<Option<String>>>,
    pub read_write_optional_string_version: Arc<AtomicU32>,

    pub read_write_two_strings: Arc<RwLockWatch<ReadWriteTwoStringsProperty>>,
    pub read_write_two_strings_version: Arc<AtomicU32>,

    pub read_write_struct: Arc<RwLockWatch<AllTypes>>,
    pub read_write_struct_version: Arc<AtomicU32>,

    pub read_write_optional_struct: Arc<RwLockWatch<Option<AllTypes>>>,
    pub read_write_optional_struct_version: Arc<AtomicU32>,

    pub read_write_two_structs: Arc<RwLockWatch<ReadWriteTwoStructsProperty>>,
    pub read_write_two_structs_version: Arc<AtomicU32>,

    pub read_only_enum: Arc<RwLockWatch<Numbers>>,
    pub read_only_enum_version: Arc<AtomicU32>,

    pub read_write_enum: Arc<RwLockWatch<Numbers>>,
    pub read_write_enum_version: Arc<AtomicU32>,

    pub read_write_optional_enum: Arc<RwLockWatch<Option<Numbers>>>,
    pub read_write_optional_enum_version: Arc<AtomicU32>,

    pub read_write_two_enums: Arc<RwLockWatch<ReadWriteTwoEnumsProperty>>,
    pub read_write_two_enums_version: Arc<AtomicU32>,

    pub read_write_datetime: Arc<RwLockWatch<chrono::DateTime<chrono::Utc>>>,
    pub read_write_datetime_version: Arc<AtomicU32>,

    pub read_write_optional_datetime: Arc<RwLockWatch<Option<chrono::DateTime<chrono::Utc>>>>,
    pub read_write_optional_datetime_version: Arc<AtomicU32>,

    pub read_write_two_datetimes: Arc<RwLockWatch<ReadWriteTwoDatetimesProperty>>,
    pub read_write_two_datetimes_version: Arc<AtomicU32>,

    pub read_write_duration: Arc<RwLockWatch<chrono::Duration>>,
    pub read_write_duration_version: Arc<AtomicU32>,

    pub read_write_optional_duration: Arc<RwLockWatch<Option<chrono::Duration>>>,
    pub read_write_optional_duration_version: Arc<AtomicU32>,

    pub read_write_two_durations: Arc<RwLockWatch<ReadWriteTwoDurationsProperty>>,
    pub read_write_two_durations_version: Arc<AtomicU32>,

    pub read_write_binary: Arc<RwLockWatch<Vec<u8>>>,
    pub read_write_binary_version: Arc<AtomicU32>,

    pub read_write_optional_binary: Arc<RwLockWatch<Option<Vec<u8>>>>,
    pub read_write_optional_binary_version: Arc<AtomicU32>,

    pub read_write_two_binaries: Arc<RwLockWatch<ReadWriteTwoBinariesProperty>>,
    pub read_write_two_binaries_version: Arc<AtomicU32>,

    pub read_write_list_of_strings: Arc<RwLockWatch<Vec<String>>>,
    pub read_write_list_of_strings_version: Arc<AtomicU32>,

    pub read_write_lists: Arc<RwLockWatch<ReadWriteListsProperty>>,
    pub read_write_lists_version: Arc<AtomicU32>,
}

/// This is the struct for our API client.
#[derive(Clone)]
pub struct TestAbleClient<C: Mqtt5PubSub> {
    mqtt_client: C,
    /// Temporarily holds oneshot channels for responses to method calls.
    pending_responses: Arc<Mutex<HashMap<Uuid, oneshot::Sender<MethodReturnCode>>>>,

    /// Temporarily holds the receiver for the broadcast channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<broadcast::Receiver<MqttMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: broadcast::Sender<MqttMessage>,

    /// Struct contains all the properties.
    properties: TestAbleProperties,

    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: TestAbleSubscriptionIds,
    /// Holds the channels used for sending signals to the application.
    signal_channels: TestAbleSignalChannels,

    /// Copy of MQTT Client ID
    pub client_id: String,

    /// Instance ID of the server
    service_instance_id: String,
}

impl<C: Mqtt5PubSub + Clone + Send + 'static> TestAbleClient<C> {
    /// Creates a new TestAbleClient that uses an Mqtt5PubSub.
    pub async fn new(mut connection: C, discovery_info: DiscoveredService) -> Self {
        // Create a channel for messages to get from the Connection object to this TestAbleClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = broadcast::channel(64);

        let client_id = connection.get_client_id();

        let topic_call_with_nothing_method_resp =
            format!("client/{}/callWithNothing/response", client_id);
        let subscription_id_call_with_nothing_method_resp = connection
            .subscribe(
                topic_call_with_nothing_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_with_nothing_method_resp =
            subscription_id_call_with_nothing_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_one_integer_method_resp =
            format!("client/{}/callOneInteger/response", client_id);
        let subscription_id_call_one_integer_method_resp = connection
            .subscribe(
                topic_call_one_integer_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_integer_method_resp =
            subscription_id_call_one_integer_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_optional_integer_method_resp =
            format!("client/{}/callOptionalInteger/response", client_id);
        let subscription_id_call_optional_integer_method_resp = connection
            .subscribe(
                topic_call_optional_integer_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_integer_method_resp =
            subscription_id_call_optional_integer_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_three_integers_method_resp =
            format!("client/{}/callThreeIntegers/response", client_id);
        let subscription_id_call_three_integers_method_resp = connection
            .subscribe(
                topic_call_three_integers_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_integers_method_resp =
            subscription_id_call_three_integers_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_one_string_method_resp =
            format!("client/{}/callOneString/response", client_id);
        let subscription_id_call_one_string_method_resp = connection
            .subscribe(
                topic_call_one_string_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_string_method_resp =
            subscription_id_call_one_string_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_optional_string_method_resp =
            format!("client/{}/callOptionalString/response", client_id);
        let subscription_id_call_optional_string_method_resp = connection
            .subscribe(
                topic_call_optional_string_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_string_method_resp =
            subscription_id_call_optional_string_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_three_strings_method_resp =
            format!("client/{}/callThreeStrings/response", client_id);
        let subscription_id_call_three_strings_method_resp = connection
            .subscribe(
                topic_call_three_strings_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_strings_method_resp =
            subscription_id_call_three_strings_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_one_enum_method_resp = format!("client/{}/callOneEnum/response", client_id);
        let subscription_id_call_one_enum_method_resp = connection
            .subscribe(
                topic_call_one_enum_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_enum_method_resp =
            subscription_id_call_one_enum_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_optional_enum_method_resp =
            format!("client/{}/callOptionalEnum/response", client_id);
        let subscription_id_call_optional_enum_method_resp = connection
            .subscribe(
                topic_call_optional_enum_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_enum_method_resp =
            subscription_id_call_optional_enum_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_three_enums_method_resp =
            format!("client/{}/callThreeEnums/response", client_id);
        let subscription_id_call_three_enums_method_resp = connection
            .subscribe(
                topic_call_three_enums_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_enums_method_resp =
            subscription_id_call_three_enums_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_one_struct_method_resp =
            format!("client/{}/callOneStruct/response", client_id);
        let subscription_id_call_one_struct_method_resp = connection
            .subscribe(
                topic_call_one_struct_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_struct_method_resp =
            subscription_id_call_one_struct_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_optional_struct_method_resp =
            format!("client/{}/callOptionalStruct/response", client_id);
        let subscription_id_call_optional_struct_method_resp = connection
            .subscribe(
                topic_call_optional_struct_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_struct_method_resp =
            subscription_id_call_optional_struct_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_three_structs_method_resp =
            format!("client/{}/callThreeStructs/response", client_id);
        let subscription_id_call_three_structs_method_resp = connection
            .subscribe(
                topic_call_three_structs_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_structs_method_resp =
            subscription_id_call_three_structs_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_one_date_time_method_resp =
            format!("client/{}/callOneDateTime/response", client_id);
        let subscription_id_call_one_date_time_method_resp = connection
            .subscribe(
                topic_call_one_date_time_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_date_time_method_resp =
            subscription_id_call_one_date_time_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_optional_date_time_method_resp =
            format!("client/{}/callOptionalDateTime/response", client_id);
        let subscription_id_call_optional_date_time_method_resp = connection
            .subscribe(
                topic_call_optional_date_time_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_date_time_method_resp =
            subscription_id_call_optional_date_time_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_three_date_times_method_resp =
            format!("client/{}/callThreeDateTimes/response", client_id);
        let subscription_id_call_three_date_times_method_resp = connection
            .subscribe(
                topic_call_three_date_times_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_date_times_method_resp =
            subscription_id_call_three_date_times_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_one_duration_method_resp =
            format!("client/{}/callOneDuration/response", client_id);
        let subscription_id_call_one_duration_method_resp = connection
            .subscribe(
                topic_call_one_duration_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_duration_method_resp =
            subscription_id_call_one_duration_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_optional_duration_method_resp =
            format!("client/{}/callOptionalDuration/response", client_id);
        let subscription_id_call_optional_duration_method_resp = connection
            .subscribe(
                topic_call_optional_duration_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_duration_method_resp =
            subscription_id_call_optional_duration_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_three_durations_method_resp =
            format!("client/{}/callThreeDurations/response", client_id);
        let subscription_id_call_three_durations_method_resp = connection
            .subscribe(
                topic_call_three_durations_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_durations_method_resp =
            subscription_id_call_three_durations_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_one_binary_method_resp =
            format!("client/{}/callOneBinary/response", client_id);
        let subscription_id_call_one_binary_method_resp = connection
            .subscribe(
                topic_call_one_binary_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_binary_method_resp =
            subscription_id_call_one_binary_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_optional_binary_method_resp =
            format!("client/{}/callOptionalBinary/response", client_id);
        let subscription_id_call_optional_binary_method_resp = connection
            .subscribe(
                topic_call_optional_binary_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_binary_method_resp =
            subscription_id_call_optional_binary_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_three_binaries_method_resp =
            format!("client/{}/callThreeBinaries/response", client_id);
        let subscription_id_call_three_binaries_method_resp = connection
            .subscribe(
                topic_call_three_binaries_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_binaries_method_resp =
            subscription_id_call_three_binaries_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_one_list_of_integers_method_resp =
            format!("client/{}/callOneListOfIntegers/response", client_id);
        let subscription_id_call_one_list_of_integers_method_resp = connection
            .subscribe(
                topic_call_one_list_of_integers_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_list_of_integers_method_resp =
            subscription_id_call_one_list_of_integers_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_optional_list_of_floats_method_resp =
            format!("client/{}/callOptionalListOfFloats/response", client_id);
        let subscription_id_call_optional_list_of_floats_method_resp = connection
            .subscribe(
                topic_call_optional_list_of_floats_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_list_of_floats_method_resp =
            subscription_id_call_optional_list_of_floats_method_resp.unwrap_or_else(|_| u32::MAX);
        let topic_call_two_lists_method_resp =
            format!("client/{}/callTwoLists/response", client_id);
        let subscription_id_call_two_lists_method_resp = connection
            .subscribe(
                topic_call_two_lists_method_resp,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_two_lists_method_resp =
            subscription_id_call_two_lists_method_resp.unwrap_or_else(|_| u32::MAX);

        // Subscribe to all the topics needed for signals.
        let topic_empty_signal = format!(
            "testAble/{}/signal/empty",
            discovery_info.interface_info.instance
        );
        let subscription_id_empty_signal = connection
            .subscribe(
                topic_empty_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_empty_signal =
            subscription_id_empty_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_int_signal = format!(
            "testAble/{}/signal/singleInt",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_int_signal = connection
            .subscribe(
                topic_single_int_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_int_signal =
            subscription_id_single_int_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_optional_int_signal = format!(
            "testAble/{}/signal/singleOptionalInt",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_optional_int_signal = connection
            .subscribe(
                topic_single_optional_int_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_int_signal =
            subscription_id_single_optional_int_signal.unwrap_or_else(|_| u32::MAX);
        let topic_three_integers_signal = format!(
            "testAble/{}/signal/threeIntegers",
            discovery_info.interface_info.instance
        );
        let subscription_id_three_integers_signal = connection
            .subscribe(
                topic_three_integers_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_three_integers_signal =
            subscription_id_three_integers_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_string_signal = format!(
            "testAble/{}/signal/singleString",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_string_signal = connection
            .subscribe(
                topic_single_string_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_string_signal =
            subscription_id_single_string_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_optional_string_signal = format!(
            "testAble/{}/signal/singleOptionalString",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_optional_string_signal = connection
            .subscribe(
                topic_single_optional_string_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_string_signal =
            subscription_id_single_optional_string_signal.unwrap_or_else(|_| u32::MAX);
        let topic_three_strings_signal = format!(
            "testAble/{}/signal/threeStrings",
            discovery_info.interface_info.instance
        );
        let subscription_id_three_strings_signal = connection
            .subscribe(
                topic_three_strings_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_three_strings_signal =
            subscription_id_three_strings_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_enum_signal = format!(
            "testAble/{}/signal/singleEnum",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_enum_signal = connection
            .subscribe(
                topic_single_enum_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_enum_signal =
            subscription_id_single_enum_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_optional_enum_signal = format!(
            "testAble/{}/signal/singleOptionalEnum",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_optional_enum_signal = connection
            .subscribe(
                topic_single_optional_enum_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_enum_signal =
            subscription_id_single_optional_enum_signal.unwrap_or_else(|_| u32::MAX);
        let topic_three_enums_signal = format!(
            "testAble/{}/signal/threeEnums",
            discovery_info.interface_info.instance
        );
        let subscription_id_three_enums_signal = connection
            .subscribe(
                topic_three_enums_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_three_enums_signal =
            subscription_id_three_enums_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_struct_signal = format!(
            "testAble/{}/signal/singleStruct",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_struct_signal = connection
            .subscribe(
                topic_single_struct_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_struct_signal =
            subscription_id_single_struct_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_optional_struct_signal = format!(
            "testAble/{}/signal/singleOptionalStruct",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_optional_struct_signal = connection
            .subscribe(
                topic_single_optional_struct_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_struct_signal =
            subscription_id_single_optional_struct_signal.unwrap_or_else(|_| u32::MAX);
        let topic_three_structs_signal = format!(
            "testAble/{}/signal/threeStructs",
            discovery_info.interface_info.instance
        );
        let subscription_id_three_structs_signal = connection
            .subscribe(
                topic_three_structs_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_three_structs_signal =
            subscription_id_three_structs_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_date_time_signal = format!(
            "testAble/{}/signal/singleDateTime",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_date_time_signal = connection
            .subscribe(
                topic_single_date_time_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_date_time_signal =
            subscription_id_single_date_time_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_optional_datetime_signal = format!(
            "testAble/{}/signal/singleOptionalDatetime",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_optional_datetime_signal = connection
            .subscribe(
                topic_single_optional_datetime_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_datetime_signal =
            subscription_id_single_optional_datetime_signal.unwrap_or_else(|_| u32::MAX);
        let topic_three_date_times_signal = format!(
            "testAble/{}/signal/threeDateTimes",
            discovery_info.interface_info.instance
        );
        let subscription_id_three_date_times_signal = connection
            .subscribe(
                topic_three_date_times_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_three_date_times_signal =
            subscription_id_three_date_times_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_duration_signal = format!(
            "testAble/{}/signal/singleDuration",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_duration_signal = connection
            .subscribe(
                topic_single_duration_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_duration_signal =
            subscription_id_single_duration_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_optional_duration_signal = format!(
            "testAble/{}/signal/singleOptionalDuration",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_optional_duration_signal = connection
            .subscribe(
                topic_single_optional_duration_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_duration_signal =
            subscription_id_single_optional_duration_signal.unwrap_or_else(|_| u32::MAX);
        let topic_three_durations_signal = format!(
            "testAble/{}/signal/threeDurations",
            discovery_info.interface_info.instance
        );
        let subscription_id_three_durations_signal = connection
            .subscribe(
                topic_three_durations_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_three_durations_signal =
            subscription_id_three_durations_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_binary_signal = format!(
            "testAble/{}/signal/singleBinary",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_binary_signal = connection
            .subscribe(
                topic_single_binary_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_binary_signal =
            subscription_id_single_binary_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_optional_binary_signal = format!(
            "testAble/{}/signal/singleOptionalBinary",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_optional_binary_signal = connection
            .subscribe(
                topic_single_optional_binary_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_binary_signal =
            subscription_id_single_optional_binary_signal.unwrap_or_else(|_| u32::MAX);
        let topic_three_binaries_signal = format!(
            "testAble/{}/signal/threeBinaries",
            discovery_info.interface_info.instance
        );
        let subscription_id_three_binaries_signal = connection
            .subscribe(
                topic_three_binaries_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_three_binaries_signal =
            subscription_id_three_binaries_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_array_of_integers_signal = format!(
            "testAble/{}/signal/singleArrayOfIntegers",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_array_of_integers_signal = connection
            .subscribe(
                topic_single_array_of_integers_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_array_of_integers_signal =
            subscription_id_single_array_of_integers_signal.unwrap_or_else(|_| u32::MAX);
        let topic_single_optional_array_of_strings_signal = format!(
            "testAble/{}/signal/singleOptionalArrayOfStrings",
            discovery_info.interface_info.instance
        );
        let subscription_id_single_optional_array_of_strings_signal = connection
            .subscribe(
                topic_single_optional_array_of_strings_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_single_optional_array_of_strings_signal =
            subscription_id_single_optional_array_of_strings_signal.unwrap_or_else(|_| u32::MAX);
        let topic_array_of_every_type_signal = format!(
            "testAble/{}/signal/arrayOfEveryType",
            discovery_info.interface_info.instance
        );
        let subscription_id_array_of_every_type_signal = connection
            .subscribe(
                topic_array_of_every_type_signal,
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_array_of_every_type_signal =
            subscription_id_array_of_every_type_signal.unwrap_or_else(|_| u32::MAX);

        // Subscribe to all the topics needed for properties.

        let topic_read_write_integer_property_value = format!(
            "testAble/{}/property/readWriteInteger/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_integer_property_value = connection
            .subscribe(
                topic_read_write_integer_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_integer_property_value =
            subscription_id_read_write_integer_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_only_integer_property_value = format!(
            "testAble/{}/property/readOnlyInteger/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_only_integer_property_value = connection
            .subscribe(
                topic_read_only_integer_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_only_integer_property_value =
            subscription_id_read_only_integer_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_optional_integer_property_value = format!(
            "testAble/{}/property/readWriteOptionalInteger/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_optional_integer_property_value = connection
            .subscribe(
                topic_read_write_optional_integer_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_integer_property_value =
            subscription_id_read_write_optional_integer_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_two_integers_property_value = format!(
            "testAble/{}/property/readWriteTwoIntegers/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_two_integers_property_value = connection
            .subscribe(
                topic_read_write_two_integers_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_integers_property_value =
            subscription_id_read_write_two_integers_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_only_string_property_value = format!(
            "testAble/{}/property/readOnlyString/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_only_string_property_value = connection
            .subscribe(
                topic_read_only_string_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_only_string_property_value =
            subscription_id_read_only_string_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_string_property_value = format!(
            "testAble/{}/property/readWriteString/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_string_property_value = connection
            .subscribe(
                topic_read_write_string_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_string_property_value =
            subscription_id_read_write_string_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_optional_string_property_value = format!(
            "testAble/{}/property/readWriteOptionalString/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_optional_string_property_value = connection
            .subscribe(
                topic_read_write_optional_string_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_string_property_value =
            subscription_id_read_write_optional_string_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_two_strings_property_value = format!(
            "testAble/{}/property/readWriteTwoStrings/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_two_strings_property_value = connection
            .subscribe(
                topic_read_write_two_strings_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_strings_property_value =
            subscription_id_read_write_two_strings_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_struct_property_value = format!(
            "testAble/{}/property/readWriteStruct/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_struct_property_value = connection
            .subscribe(
                topic_read_write_struct_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_struct_property_value =
            subscription_id_read_write_struct_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_optional_struct_property_value = format!(
            "testAble/{}/property/readWriteOptionalStruct/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_optional_struct_property_value = connection
            .subscribe(
                topic_read_write_optional_struct_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_struct_property_value =
            subscription_id_read_write_optional_struct_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_two_structs_property_value = format!(
            "testAble/{}/property/readWriteTwoStructs/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_two_structs_property_value = connection
            .subscribe(
                topic_read_write_two_structs_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_structs_property_value =
            subscription_id_read_write_two_structs_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_only_enum_property_value = format!(
            "testAble/{}/property/readOnlyEnum/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_only_enum_property_value = connection
            .subscribe(
                topic_read_only_enum_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_only_enum_property_value =
            subscription_id_read_only_enum_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_enum_property_value = format!(
            "testAble/{}/property/readWriteEnum/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_enum_property_value = connection
            .subscribe(
                topic_read_write_enum_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_enum_property_value =
            subscription_id_read_write_enum_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_optional_enum_property_value = format!(
            "testAble/{}/property/readWriteOptionalEnum/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_optional_enum_property_value = connection
            .subscribe(
                topic_read_write_optional_enum_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_enum_property_value =
            subscription_id_read_write_optional_enum_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_two_enums_property_value = format!(
            "testAble/{}/property/readWriteTwoEnums/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_two_enums_property_value = connection
            .subscribe(
                topic_read_write_two_enums_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_enums_property_value =
            subscription_id_read_write_two_enums_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_datetime_property_value = format!(
            "testAble/{}/property/readWriteDatetime/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_datetime_property_value = connection
            .subscribe(
                topic_read_write_datetime_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_datetime_property_value =
            subscription_id_read_write_datetime_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_optional_datetime_property_value = format!(
            "testAble/{}/property/readWriteOptionalDatetime/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_optional_datetime_property_value = connection
            .subscribe(
                topic_read_write_optional_datetime_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_datetime_property_value =
            subscription_id_read_write_optional_datetime_property_value
                .unwrap_or_else(|_| u32::MAX);

        let topic_read_write_two_datetimes_property_value = format!(
            "testAble/{}/property/readWriteTwoDatetimes/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_two_datetimes_property_value = connection
            .subscribe(
                topic_read_write_two_datetimes_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_datetimes_property_value =
            subscription_id_read_write_two_datetimes_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_duration_property_value = format!(
            "testAble/{}/property/readWriteDuration/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_duration_property_value = connection
            .subscribe(
                topic_read_write_duration_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_duration_property_value =
            subscription_id_read_write_duration_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_optional_duration_property_value = format!(
            "testAble/{}/property/readWriteOptionalDuration/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_optional_duration_property_value = connection
            .subscribe(
                topic_read_write_optional_duration_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_duration_property_value =
            subscription_id_read_write_optional_duration_property_value
                .unwrap_or_else(|_| u32::MAX);

        let topic_read_write_two_durations_property_value = format!(
            "testAble/{}/property/readWriteTwoDurations/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_two_durations_property_value = connection
            .subscribe(
                topic_read_write_two_durations_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_durations_property_value =
            subscription_id_read_write_two_durations_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_binary_property_value = format!(
            "testAble/{}/property/readWriteBinary/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_binary_property_value = connection
            .subscribe(
                topic_read_write_binary_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_binary_property_value =
            subscription_id_read_write_binary_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_optional_binary_property_value = format!(
            "testAble/{}/property/readWriteOptionalBinary/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_optional_binary_property_value = connection
            .subscribe(
                topic_read_write_optional_binary_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_binary_property_value =
            subscription_id_read_write_optional_binary_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_two_binaries_property_value = format!(
            "testAble/{}/property/readWriteTwoBinaries/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_two_binaries_property_value = connection
            .subscribe(
                topic_read_write_two_binaries_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_binaries_property_value =
            subscription_id_read_write_two_binaries_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_list_of_strings_property_value = format!(
            "testAble/{}/property/readWriteListOfStrings/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_list_of_strings_property_value = connection
            .subscribe(
                topic_read_write_list_of_strings_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_list_of_strings_property_value =
            subscription_id_read_write_list_of_strings_property_value.unwrap_or_else(|_| u32::MAX);

        let topic_read_write_lists_property_value = format!(
            "testAble/{}/property/readWriteLists/value",
            discovery_info.interface_info.instance
        );
        let subscription_id_read_write_lists_property_value = connection
            .subscribe(
                topic_read_write_lists_property_value,
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_lists_property_value =
            subscription_id_read_write_lists_property_value.unwrap_or_else(|_| u32::MAX);

        let property_values = TestAbleProperties {
            read_write_integer: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_integer,
            )),
            read_write_integer_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_integer_version,
            )),

            read_only_integer: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_only_integer,
            )),
            read_only_integer_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_only_integer_version,
            )),

            read_write_optional_integer: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_optional_integer,
            )),
            read_write_optional_integer_version: Arc::new(AtomicU32::new(
                discovery_info
                    .properties
                    .read_write_optional_integer_version,
            )),
            read_write_two_integers: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_two_integers,
            )),
            read_write_two_integers_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_two_integers_version,
            )),

            read_only_string: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_only_string,
            )),
            read_only_string_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_only_string_version,
            )),

            read_write_string: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_string,
            )),
            read_write_string_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_string_version,
            )),

            read_write_optional_string: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_optional_string,
            )),
            read_write_optional_string_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_optional_string_version,
            )),
            read_write_two_strings: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_two_strings,
            )),
            read_write_two_strings_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_two_strings_version,
            )),

            read_write_struct: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_struct,
            )),
            read_write_struct_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_struct_version,
            )),

            read_write_optional_struct: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_optional_struct,
            )),
            read_write_optional_struct_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_optional_struct_version,
            )),
            read_write_two_structs: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_two_structs,
            )),
            read_write_two_structs_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_two_structs_version,
            )),

            read_only_enum: Arc::new(RwLockWatch::new(discovery_info.properties.read_only_enum)),
            read_only_enum_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_only_enum_version,
            )),

            read_write_enum: Arc::new(RwLockWatch::new(discovery_info.properties.read_write_enum)),
            read_write_enum_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_enum_version,
            )),

            read_write_optional_enum: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_optional_enum,
            )),
            read_write_optional_enum_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_optional_enum_version,
            )),
            read_write_two_enums: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_two_enums,
            )),
            read_write_two_enums_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_two_enums_version,
            )),

            read_write_datetime: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_datetime,
            )),
            read_write_datetime_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_datetime_version,
            )),

            read_write_optional_datetime: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_optional_datetime,
            )),
            read_write_optional_datetime_version: Arc::new(AtomicU32::new(
                discovery_info
                    .properties
                    .read_write_optional_datetime_version,
            )),
            read_write_two_datetimes: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_two_datetimes,
            )),
            read_write_two_datetimes_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_two_datetimes_version,
            )),

            read_write_duration: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_duration,
            )),
            read_write_duration_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_duration_version,
            )),

            read_write_optional_duration: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_optional_duration,
            )),
            read_write_optional_duration_version: Arc::new(AtomicU32::new(
                discovery_info
                    .properties
                    .read_write_optional_duration_version,
            )),
            read_write_two_durations: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_two_durations,
            )),
            read_write_two_durations_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_two_durations_version,
            )),

            read_write_binary: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_binary,
            )),
            read_write_binary_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_binary_version,
            )),

            read_write_optional_binary: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_optional_binary,
            )),
            read_write_optional_binary_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_optional_binary_version,
            )),
            read_write_two_binaries: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_two_binaries,
            )),
            read_write_two_binaries_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_two_binaries_version,
            )),

            read_write_list_of_strings: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_list_of_strings,
            )),
            read_write_list_of_strings_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_list_of_strings_version,
            )),
            read_write_lists: Arc::new(RwLockWatch::new(
                discovery_info.properties.read_write_lists,
            )),
            read_write_lists_version: Arc::new(AtomicU32::new(
                discovery_info.properties.read_write_lists_version,
            )),
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
            call_one_list_of_integers_method_resp:
                subscription_id_call_one_list_of_integers_method_resp,
            call_optional_list_of_floats_method_resp:
                subscription_id_call_optional_list_of_floats_method_resp,
            call_two_lists_method_resp: subscription_id_call_two_lists_method_resp,
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
            single_array_of_integers_signal: Some(subscription_id_single_array_of_integers_signal),
            single_optional_array_of_strings_signal: Some(
                subscription_id_single_optional_array_of_strings_signal,
            ),
            array_of_every_type_signal: Some(subscription_id_array_of_every_type_signal),
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
            read_write_list_of_strings_property_value:
                subscription_id_read_write_list_of_strings_property_value,
            read_write_lists_property_value: subscription_id_read_write_lists_property_value,
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
            single_array_of_integers_sender: broadcast::channel(64).0,
            single_optional_array_of_strings_sender: broadcast::channel(64).0,
            array_of_every_type_sender: broadcast::channel(64).0,
        };

        // Create TestAbleClient structure.
        let inst = TestAbleClient {
            mqtt_client: connection,
            pending_responses: Arc::new(Mutex::new(HashMap::new())),
            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,

            properties: property_values,

            subscription_ids: sub_ids,
            signal_channels: signal_channels,
            client_id: client_id,

            service_instance_id: discovery_info.interface_info.instance,
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
    pub fn get_single_optional_struct_receiver(&self) -> broadcast::Receiver<Option<AllTypes>> {
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
    ) -> broadcast::Receiver<Option<chrono::DateTime<chrono::Utc>>> {
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
    pub fn get_single_optional_duration_receiver(
        &self,
    ) -> broadcast::Receiver<Option<chrono::Duration>> {
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
    pub fn get_single_optional_binary_receiver(&self) -> broadcast::Receiver<Option<Vec<u8>>> {
        self.signal_channels
            .single_optional_binary_sender
            .subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the threeBinaries signal.
    /// The signal payload, `ThreeBinariesSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_three_binaries_receiver(&self) -> broadcast::Receiver<ThreeBinariesSignalPayload> {
        self.signal_channels.three_binaries_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleArrayOfIntegers signal.
    /// The signal payload, `SingleArrayOfIntegersSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_array_of_integers_receiver(&self) -> broadcast::Receiver<Vec<i32>> {
        self.signal_channels
            .single_array_of_integers_sender
            .subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the singleOptionalArrayOfStrings signal.
    /// The signal payload, `SingleOptionalArrayOfStringsSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_single_optional_array_of_strings_receiver(
        &self,
    ) -> broadcast::Receiver<Option<Vec<String>>> {
        self.signal_channels
            .single_optional_array_of_strings_sender
            .subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the arrayOfEveryType signal.
    /// The signal payload, `ArrayOfEveryTypeSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_array_of_every_type_receiver(
        &self,
    ) -> broadcast::Receiver<ArrayOfEveryTypeSignalPayload> {
        self.signal_channels.array_of_every_type_sender.subscribe()
    }

    async fn start_call_with_nothing(&mut self) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallWithNothingRequestObject {};

        let response_topic: String = format!("client/{}/callWithNothing/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callWithNothing",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callWithNothing` method.
    /// Method arguments are packed into a CallWithNothingRequestObject structure
    /// and published to the `testAble/{}/method/callWithNothing` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_with_nothing(&mut self) -> Result<(), MethodReturnCode> {
        let receiver = self.start_call_with_nothing().await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(_) => Ok(()),
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_one_integer(&mut self, input1: i32) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneIntegerRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneInteger/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOneInteger",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOneInteger` method.
    /// Method arguments are packed into a CallOneIntegerRequestObject structure
    /// and published to the `testAble/{}/method/callOneInteger` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_integer(&mut self, input1: i32) -> Result<i32, MethodReturnCode> {
        let receiver = self.start_call_one_integer(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOneIntegerReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_optional_integer(
        &mut self,
        input1: Option<i32>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalIntegerRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalInteger/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOptionalInteger",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOptionalIntegerReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_three_integers(
        &mut self,
        input1: i32,
        input2: i32,
        input3: Option<i32>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
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
        let msg = message::request(
            &format!(
                "testAble/{}/method/callThreeIntegers",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallThreeIntegersReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_one_string(
        &mut self,
        input1: String,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneStringRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneString/response", self.client_id);
        let msg = message::request(
            &format!("testAble/{}/method/callOneString", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOneString` method.
    /// Method arguments are packed into a CallOneStringRequestObject structure
    /// and published to the `testAble/{}/method/callOneString` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_string(&mut self, input1: String) -> Result<String, MethodReturnCode> {
        let receiver = self.start_call_one_string(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOneStringReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_optional_string(
        &mut self,
        input1: Option<String>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalStringRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalString/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOptionalString",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOptionalStringReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_three_strings(
        &mut self,
        input1: String,
        input2: Option<String>,
        input3: String,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
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
        let msg = message::request(
            &format!(
                "testAble/{}/method/callThreeStrings",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallThreeStringsReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_one_enum(
        &mut self,
        input1: Numbers,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneEnumRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneEnum/response", self.client_id);
        let msg = message::request(
            &format!("testAble/{}/method/callOneEnum", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOneEnum` method.
    /// Method arguments are packed into a CallOneEnumRequestObject structure
    /// and published to the `testAble/{}/method/callOneEnum` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_enum(&mut self, input1: Numbers) -> Result<Numbers, MethodReturnCode> {
        let receiver = self.start_call_one_enum(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOneEnumReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_optional_enum(
        &mut self,
        input1: Option<Numbers>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalEnumRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOptionalEnum/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOptionalEnum",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOptionalEnumReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_three_enums(
        &mut self,
        input1: Numbers,
        input2: Numbers,
        input3: Option<Numbers>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
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
        let msg = message::request(
            &format!(
                "testAble/{}/method/callThreeEnums",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallThreeEnumsReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_one_struct(
        &mut self,
        input1: AllTypes,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneStructRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneStruct/response", self.client_id);
        let msg = message::request(
            &format!("testAble/{}/method/callOneStruct", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOneStructReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_optional_struct(
        &mut self,
        input1: Option<AllTypes>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalStructRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalStruct/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOptionalStruct",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOptionalStruct` method.
    /// Method arguments are packed into a CallOptionalStructRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalStruct` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_struct(
        &mut self,
        input1: Option<AllTypes>,
    ) -> Result<Option<AllTypes>, MethodReturnCode> {
        let receiver = self.start_call_optional_struct(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOptionalStructReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_three_structs(
        &mut self,
        input1: Option<AllTypes>,
        input2: AllTypes,
        input3: AllTypes,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
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
        let msg = message::request(
            &format!(
                "testAble/{}/method/callThreeStructs",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callThreeStructs` method.
    /// Method arguments are packed into a CallThreeStructsRequestObject structure
    /// and published to the `testAble/{}/method/callThreeStructs` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_three_structs(
        &mut self,
        input1: Option<AllTypes>,
        input2: AllTypes,
        input3: AllTypes,
    ) -> Result<CallThreeStructsReturnValues, MethodReturnCode> {
        let receiver = self.start_call_three_structs(input1, input2, input3).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallThreeStructsReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_one_date_time(
        &mut self,
        input1: chrono::DateTime<chrono::Utc>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneDateTimeRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneDateTime/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOneDateTime",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOneDateTimeReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_optional_date_time(
        &mut self,
        input1: Option<chrono::DateTime<chrono::Utc>>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalDateTimeRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalDateTime/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOptionalDateTime",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOptionalDateTime` method.
    /// Method arguments are packed into a CallOptionalDateTimeRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalDateTime` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_date_time(
        &mut self,
        input1: Option<chrono::DateTime<chrono::Utc>>,
    ) -> Result<Option<chrono::DateTime<chrono::Utc>>, MethodReturnCode> {
        let receiver = self.start_call_optional_date_time(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOptionalDateTimeReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_three_date_times(
        &mut self,
        input1: chrono::DateTime<chrono::Utc>,
        input2: chrono::DateTime<chrono::Utc>,
        input3: Option<chrono::DateTime<chrono::Utc>>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
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
        let msg = message::request(
            &format!(
                "testAble/{}/method/callThreeDateTimes",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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
        input3: Option<chrono::DateTime<chrono::Utc>>,
    ) -> Result<CallThreeDateTimesReturnValues, MethodReturnCode> {
        let receiver = self
            .start_call_three_date_times(input1, input2, input3)
            .await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallThreeDateTimesReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_one_duration(
        &mut self,
        input1: chrono::Duration,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneDurationRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneDuration/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOneDuration",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOneDurationReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_optional_duration(
        &mut self,
        input1: Option<chrono::Duration>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalDurationRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalDuration/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOptionalDuration",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOptionalDuration` method.
    /// Method arguments are packed into a CallOptionalDurationRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalDuration` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_duration(
        &mut self,
        input1: Option<chrono::Duration>,
    ) -> Result<Option<chrono::Duration>, MethodReturnCode> {
        let receiver = self.start_call_optional_duration(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOptionalDurationReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_three_durations(
        &mut self,
        input1: chrono::Duration,
        input2: chrono::Duration,
        input3: Option<chrono::Duration>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
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
        let msg = message::request(
            &format!(
                "testAble/{}/method/callThreeDurations",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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
        input3: Option<chrono::Duration>,
    ) -> Result<CallThreeDurationsReturnValues, MethodReturnCode> {
        let receiver = self
            .start_call_three_durations(input1, input2, input3)
            .await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallThreeDurationsReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_one_binary(
        &mut self,
        input1: Vec<u8>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneBinaryRequestObject { input1: input1 };

        let response_topic: String = format!("client/{}/callOneBinary/response", self.client_id);
        let msg = message::request(
            &format!("testAble/{}/method/callOneBinary", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOneBinary` method.
    /// Method arguments are packed into a CallOneBinaryRequestObject structure
    /// and published to the `testAble/{}/method/callOneBinary` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_binary(&mut self, input1: Vec<u8>) -> Result<Vec<u8>, MethodReturnCode> {
        let receiver = self.start_call_one_binary(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOneBinaryReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_optional_binary(
        &mut self,
        input1: Option<Vec<u8>>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalBinaryRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOptionalBinary/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOptionalBinary",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOptionalBinary` method.
    /// Method arguments are packed into a CallOptionalBinaryRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalBinary` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_binary(
        &mut self,
        input1: Option<Vec<u8>>,
    ) -> Result<Option<Vec<u8>>, MethodReturnCode> {
        let receiver = self.start_call_optional_binary(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOptionalBinaryReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_three_binaries(
        &mut self,
        input1: Vec<u8>,
        input2: Vec<u8>,
        input3: Option<Vec<u8>>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
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
        let msg = message::request(
            &format!(
                "testAble/{}/method/callThreeBinaries",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
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
        input3: Option<Vec<u8>>,
    ) -> Result<CallThreeBinariesReturnValues, MethodReturnCode> {
        let receiver = self.start_call_three_binaries(input1, input2, input3).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallThreeBinariesReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_one_list_of_integers(
        &mut self,
        input1: Vec<i32>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOneListOfIntegersRequestObject { input1: input1 };

        let response_topic: String =
            format!("client/{}/callOneListOfIntegers/response", self.client_id);
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOneListOfIntegers",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOneListOfIntegers` method.
    /// Method arguments are packed into a CallOneListOfIntegersRequestObject structure
    /// and published to the `testAble/{}/method/callOneListOfIntegers` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_one_list_of_integers(
        &mut self,
        input1: Vec<i32>,
    ) -> Result<Vec<i32>, MethodReturnCode> {
        let receiver = self.start_call_one_list_of_integers(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOneListOfIntegersReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_optional_list_of_floats(
        &mut self,
        input1: Option<Vec<f32>>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallOptionalListOfFloatsRequestObject { input1: input1 };

        let response_topic: String = format!(
            "client/{}/callOptionalListOfFloats/response",
            self.client_id
        );
        let msg = message::request(
            &format!(
                "testAble/{}/method/callOptionalListOfFloats",
                self.service_instance_id
            ),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callOptionalListOfFloats` method.
    /// Method arguments are packed into a CallOptionalListOfFloatsRequestObject structure
    /// and published to the `testAble/{}/method/callOptionalListOfFloats` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_optional_list_of_floats(
        &mut self,
        input1: Option<Vec<f32>>,
    ) -> Result<Option<Vec<f32>>, MethodReturnCode> {
        let receiver = self.start_call_optional_list_of_floats(input1).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallOptionalListOfFloatsReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj.output1)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    async fn start_call_two_lists(
        &mut self,
        input1: Vec<Numbers>,
        input2: Option<Vec<String>>,
    ) -> oneshot::Receiver<MethodReturnCode> {
        // Setup tracking for the future response.
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }

        let data = CallTwoListsRequestObject {
            input1: input1,
            input2: input2,
        };

        let response_topic: String = format!("client/{}/callTwoLists/response", self.client_id);
        let msg = message::request(
            &format!("testAble/{}/method/callTwoLists", self.service_instance_id),
            &data,
            correlation_id,
            response_topic,
        )
        .unwrap();
        let _ = self.mqtt_client.publish(msg).await;
        receiver
    }

    /// The `callTwoLists` method.
    /// Method arguments are packed into a CallTwoListsRequestObject structure
    /// and published to the `testAble/{}/method/callTwoLists` MQTT topic.
    ///
    /// This method awaits on the response to the call before returning.
    pub async fn call_two_lists(
        &mut self,
        input1: Vec<Numbers>,
        input2: Option<Vec<String>>,
    ) -> Result<CallTwoListsReturnValues, MethodReturnCode> {
        let receiver = self.start_call_two_lists(input1, input2).await;

        let return_code: MethodReturnCode = receiver.await.unwrap();
        match return_code {
            MethodReturnCode::Success(payload_str) => {
                let return_obj: CallTwoListsReturnValues =
                    serde_json::from_str(payload_str.as_ref().map_or("{}", |v| v))
                        .map_err(|e| MethodReturnCode::ClientDeserializationError(e.to_string()))?;

                Ok(return_obj)
            }
            _ => {
                return Err(return_code);
            }
        }
    }

    /// Watch for changes to the `read_write_integer` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_integer(&self) -> watch::Receiver<i32> {
        self.properties.read_write_integer.subscribe()
    }

    /// Sets the `read_write_integer` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_integer(&mut self, value: i32) -> MethodReturnCode {
        let data = ReadWriteIntegerProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteInteger/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_integer_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_integer_handle(&self) -> Arc<WriteRequestLockWatch<i32>> {
        self.properties.read_write_integer.write_request().into()
    }

    /// Watch for changes to the `read_only_integer` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_only_integer(&self) -> watch::Receiver<i32> {
        self.properties.read_only_integer.subscribe()
    }

    pub fn get_read_only_integer_handle(&self) -> Arc<ReadOnlyLockWatch<i32>> {
        self.properties.read_only_integer.read_only().into()
    }

    /// Watch for changes to the `read_write_optional_integer` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_integer(&self) -> watch::Receiver<Option<i32>> {
        self.properties.read_write_optional_integer.subscribe()
    }

    /// Sets the `read_write_optional_integer` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_optional_integer(
        &mut self,
        value: Option<i32>,
    ) -> MethodReturnCode {
        let data = ReadWriteOptionalIntegerProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteOptionalInteger/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_optional_integer_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_optional_integer_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<i32>>> {
        self.properties
            .read_write_optional_integer
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_two_integers` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_integers(&self) -> watch::Receiver<ReadWriteTwoIntegersProperty> {
        self.properties.read_write_two_integers.subscribe()
    }

    /// Sets the `read_write_two_integers` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_two_integers(
        &mut self,
        value: ReadWriteTwoIntegersProperty,
    ) -> MethodReturnCode {
        let data = value;
        let topic: String = format!(
            "testAble/{}/property/readWriteTwoIntegers/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_two_integers_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_two_integers_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<ReadWriteTwoIntegersProperty>> {
        self.properties
            .read_write_two_integers
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_only_string` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_only_string(&self) -> watch::Receiver<String> {
        self.properties.read_only_string.subscribe()
    }

    pub fn get_read_only_string_handle(&self) -> Arc<ReadOnlyLockWatch<String>> {
        self.properties.read_only_string.read_only().into()
    }

    /// Watch for changes to the `read_write_string` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_string(&self) -> watch::Receiver<String> {
        self.properties.read_write_string.subscribe()
    }

    /// Sets the `read_write_string` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_string(&mut self, value: String) -> MethodReturnCode {
        let data = ReadWriteStringProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteString/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_string_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_string_handle(&self) -> Arc<WriteRequestLockWatch<String>> {
        self.properties.read_write_string.write_request().into()
    }

    /// Watch for changes to the `read_write_optional_string` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_string(&self) -> watch::Receiver<Option<String>> {
        self.properties.read_write_optional_string.subscribe()
    }

    /// Sets the `read_write_optional_string` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_optional_string(
        &mut self,
        value: Option<String>,
    ) -> MethodReturnCode {
        let data = ReadWriteOptionalStringProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteOptionalString/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_optional_string_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_optional_string_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<String>>> {
        self.properties
            .read_write_optional_string
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_two_strings` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_strings(&self) -> watch::Receiver<ReadWriteTwoStringsProperty> {
        self.properties.read_write_two_strings.subscribe()
    }

    /// Sets the `read_write_two_strings` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_two_strings(
        &mut self,
        value: ReadWriteTwoStringsProperty,
    ) -> MethodReturnCode {
        let data = value;
        let topic: String = format!(
            "testAble/{}/property/readWriteTwoStrings/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_two_strings_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_two_strings_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<ReadWriteTwoStringsProperty>> {
        self.properties
            .read_write_two_strings
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_struct` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_struct(&self) -> watch::Receiver<AllTypes> {
        self.properties.read_write_struct.subscribe()
    }

    /// Sets the `read_write_struct` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_struct(&mut self, value: AllTypes) -> MethodReturnCode {
        let data = ReadWriteStructProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteStruct/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_struct_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_struct_handle(&self) -> Arc<WriteRequestLockWatch<AllTypes>> {
        self.properties.read_write_struct.write_request().into()
    }

    /// Watch for changes to the `read_write_optional_struct` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_struct(&self) -> watch::Receiver<Option<AllTypes>> {
        self.properties.read_write_optional_struct.subscribe()
    }

    /// Sets the `read_write_optional_struct` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_optional_struct(
        &mut self,
        value: Option<AllTypes>,
    ) -> MethodReturnCode {
        let data = ReadWriteOptionalStructProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteOptionalStruct/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_optional_struct_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_optional_struct_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<AllTypes>>> {
        self.properties
            .read_write_optional_struct
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_two_structs` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_structs(&self) -> watch::Receiver<ReadWriteTwoStructsProperty> {
        self.properties.read_write_two_structs.subscribe()
    }

    /// Sets the `read_write_two_structs` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_two_structs(
        &mut self,
        value: ReadWriteTwoStructsProperty,
    ) -> MethodReturnCode {
        let data = value;
        let topic: String = format!(
            "testAble/{}/property/readWriteTwoStructs/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_two_structs_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_two_structs_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<ReadWriteTwoStructsProperty>> {
        self.properties
            .read_write_two_structs
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_only_enum` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_only_enum(&self) -> watch::Receiver<Numbers> {
        self.properties.read_only_enum.subscribe()
    }

    pub fn get_read_only_enum_handle(&self) -> Arc<ReadOnlyLockWatch<Numbers>> {
        self.properties.read_only_enum.read_only().into()
    }

    /// Watch for changes to the `read_write_enum` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_enum(&self) -> watch::Receiver<Numbers> {
        self.properties.read_write_enum.subscribe()
    }

    /// Sets the `read_write_enum` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_enum(&mut self, value: Numbers) -> MethodReturnCode {
        let data = ReadWriteEnumProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteEnum/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_enum_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_enum_handle(&self) -> Arc<WriteRequestLockWatch<Numbers>> {
        self.properties.read_write_enum.write_request().into()
    }

    /// Watch for changes to the `read_write_optional_enum` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_enum(&self) -> watch::Receiver<Option<Numbers>> {
        self.properties.read_write_optional_enum.subscribe()
    }

    /// Sets the `read_write_optional_enum` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_optional_enum(
        &mut self,
        value: Option<Numbers>,
    ) -> MethodReturnCode {
        let data = ReadWriteOptionalEnumProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteOptionalEnum/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_optional_enum_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_optional_enum_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<Numbers>>> {
        self.properties
            .read_write_optional_enum
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_two_enums` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_enums(&self) -> watch::Receiver<ReadWriteTwoEnumsProperty> {
        self.properties.read_write_two_enums.subscribe()
    }

    /// Sets the `read_write_two_enums` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_two_enums(
        &mut self,
        value: ReadWriteTwoEnumsProperty,
    ) -> MethodReturnCode {
        let data = value;
        let topic: String = format!(
            "testAble/{}/property/readWriteTwoEnums/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_two_enums_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_two_enums_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<ReadWriteTwoEnumsProperty>> {
        self.properties.read_write_two_enums.write_request().into()
    }

    /// Watch for changes to the `read_write_datetime` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_datetime(&self) -> watch::Receiver<chrono::DateTime<chrono::Utc>> {
        self.properties.read_write_datetime.subscribe()
    }

    /// Sets the `read_write_datetime` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_datetime(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> MethodReturnCode {
        let data = ReadWriteDatetimeProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteDatetime/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_datetime_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_datetime_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<chrono::DateTime<chrono::Utc>>> {
        self.properties.read_write_datetime.write_request().into()
    }

    /// Watch for changes to the `read_write_optional_datetime` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_datetime(
        &self,
    ) -> watch::Receiver<Option<chrono::DateTime<chrono::Utc>>> {
        self.properties.read_write_optional_datetime.subscribe()
    }

    /// Sets the `read_write_optional_datetime` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_optional_datetime(
        &mut self,
        value: Option<chrono::DateTime<chrono::Utc>>,
    ) -> MethodReturnCode {
        let data = ReadWriteOptionalDatetimeProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteOptionalDatetime/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_optional_datetime_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_optional_datetime_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<chrono::DateTime<chrono::Utc>>>> {
        self.properties
            .read_write_optional_datetime
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_two_datetimes` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_datetimes(&self) -> watch::Receiver<ReadWriteTwoDatetimesProperty> {
        self.properties.read_write_two_datetimes.subscribe()
    }

    /// Sets the `read_write_two_datetimes` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_two_datetimes(
        &mut self,
        value: ReadWriteTwoDatetimesProperty,
    ) -> MethodReturnCode {
        let data = value;
        let topic: String = format!(
            "testAble/{}/property/readWriteTwoDatetimes/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_two_datetimes_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_two_datetimes_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<ReadWriteTwoDatetimesProperty>> {
        self.properties
            .read_write_two_datetimes
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_duration` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_duration(&self) -> watch::Receiver<chrono::Duration> {
        self.properties.read_write_duration.subscribe()
    }

    /// Sets the `read_write_duration` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_duration(&mut self, value: chrono::Duration) -> MethodReturnCode {
        let data = ReadWriteDurationProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteDuration/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_duration_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_duration_handle(&self) -> Arc<WriteRequestLockWatch<chrono::Duration>> {
        self.properties.read_write_duration.write_request().into()
    }

    /// Watch for changes to the `read_write_optional_duration` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_duration(&self) -> watch::Receiver<Option<chrono::Duration>> {
        self.properties.read_write_optional_duration.subscribe()
    }

    /// Sets the `read_write_optional_duration` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_optional_duration(
        &mut self,
        value: Option<chrono::Duration>,
    ) -> MethodReturnCode {
        let data = ReadWriteOptionalDurationProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteOptionalDuration/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_optional_duration_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_optional_duration_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<chrono::Duration>>> {
        self.properties
            .read_write_optional_duration
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_two_durations` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_durations(&self) -> watch::Receiver<ReadWriteTwoDurationsProperty> {
        self.properties.read_write_two_durations.subscribe()
    }

    /// Sets the `read_write_two_durations` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_two_durations(
        &mut self,
        value: ReadWriteTwoDurationsProperty,
    ) -> MethodReturnCode {
        let data = value;
        let topic: String = format!(
            "testAble/{}/property/readWriteTwoDurations/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_two_durations_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_two_durations_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<ReadWriteTwoDurationsProperty>> {
        self.properties
            .read_write_two_durations
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_binary` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_binary(&self) -> watch::Receiver<Vec<u8>> {
        self.properties.read_write_binary.subscribe()
    }

    /// Sets the `read_write_binary` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_binary(&mut self, value: Vec<u8>) -> MethodReturnCode {
        let data = ReadWriteBinaryProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteBinary/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_binary_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_binary_handle(&self) -> Arc<WriteRequestLockWatch<Vec<u8>>> {
        self.properties.read_write_binary.write_request().into()
    }

    /// Watch for changes to the `read_write_optional_binary` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_binary(&self) -> watch::Receiver<Option<Vec<u8>>> {
        self.properties.read_write_optional_binary.subscribe()
    }

    /// Sets the `read_write_optional_binary` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_optional_binary(
        &mut self,
        value: Option<Vec<u8>>,
    ) -> MethodReturnCode {
        let data = ReadWriteOptionalBinaryProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteOptionalBinary/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_optional_binary_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_optional_binary_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<Option<Vec<u8>>>> {
        self.properties
            .read_write_optional_binary
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_two_binaries` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_binaries(&self) -> watch::Receiver<ReadWriteTwoBinariesProperty> {
        self.properties.read_write_two_binaries.subscribe()
    }

    /// Sets the `read_write_two_binaries` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_two_binaries(
        &mut self,
        value: ReadWriteTwoBinariesProperty,
    ) -> MethodReturnCode {
        let data = value;
        let topic: String = format!(
            "testAble/{}/property/readWriteTwoBinaries/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_two_binaries_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_two_binaries_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<ReadWriteTwoBinariesProperty>> {
        self.properties
            .read_write_two_binaries
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_list_of_strings` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_list_of_strings(&self) -> watch::Receiver<Vec<String>> {
        self.properties.read_write_list_of_strings.subscribe()
    }

    /// Sets the `read_write_list_of_strings` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_list_of_strings(&mut self, value: Vec<String>) -> MethodReturnCode {
        let data = ReadWriteListOfStringsProperty { value: value };
        let topic: String = format!(
            "testAble/{}/property/readWriteListOfStrings/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_list_of_strings_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_list_of_strings_handle(&self) -> Arc<WriteRequestLockWatch<Vec<String>>> {
        self.properties
            .read_write_list_of_strings
            .write_request()
            .into()
    }

    /// Watch for changes to the `read_write_lists` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_lists(&self) -> watch::Receiver<ReadWriteListsProperty> {
        self.properties.read_write_lists.subscribe()
    }

    /// Sets the `read_write_lists` property and returns a oneshot that receives the acknowledgment back from the server.
    pub async fn set_read_write_lists(
        &mut self,
        value: ReadWriteListsProperty,
    ) -> MethodReturnCode {
        let data = value;
        let topic: String = format!(
            "testAble/{}/property/readWriteLists/setValue",
            self.client_id
        );
        let correlation_id = Uuid::new_v4();
        let (sender, receiver) = oneshot::channel();
        {
            let mut hashmap = self.pending_responses.lock().expect("Mutex was poisoned");
            hashmap.insert(correlation_id.clone(), sender);
        }
        let msg = message::property_update_request_message(
            &topic,
            &data,
            self.properties
                .read_write_lists_version
                .load(Ordering::Relaxed),
            correlation_id,
        )
        .unwrap();
        let _publish_result = self.mqtt_client.publish(msg);

        receiver.await.unwrap_or_else(|_| {
            MethodReturnCode::ClientError(
                "Failed to receive property set acknowledgment".to_string(),
            )
        })
    }

    pub fn get_read_write_lists_handle(
        &self,
    ) -> Arc<WriteRequestLockWatch<ReadWriteListsProperty>> {
        self.properties.read_write_lists.write_request().into()
    }

    fn get_return_code_from_message(msg: &MqttMessage) -> MethodReturnCode {
        let payload = String::from_utf8_lossy(&msg.payload).to_string();
        let mut return_code: MethodReturnCode = MethodReturnCode::Success(None);
        if let Some(retval) = msg.user_properties.get("ReturnCode") {
            let opt_dbg_info = msg.user_properties.get("DebugInfo").cloned();
            if let Ok(return_code_u32) = retval.parse::<u32>() {
                if return_code_u32 == 0 {
                    return_code = MethodReturnCode::from_code(return_code_u32, Some(payload));
                } else {
                    return_code = MethodReturnCode::from_code(return_code_u32, opt_dbg_info);
                }
            }
        }
        return_code
    }

    /// Starts the tasks that process messages received.
    pub async fn run_loop(&mut self) -> Result<(), JoinError> {
        // Clone the Arc pointer to the map.  This will be moved into the loop_task.
        let resp_map: Arc<Mutex<HashMap<Uuid, oneshot::Sender<MethodReturnCode>>>> =
            self.pending_responses.clone();

        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = {
            let mut guard = self.msg_streamer_rx.lock().expect("Mutex was poisoned");
            guard.take().expect("msg_streamer_rx should be Some")
        };

        let sig_chans = self.signal_channels.clone();

        let sub_ids = self.subscription_ids.clone();
        let props = self.properties.clone();
        {
            // Set up property change request handling task
            let client_id_for_read_write_integer_prop = self.client_id.clone();
            let mut publisher_for_read_write_integer_prop = self.mqtt_client.clone();
            let read_write_integer_prop_version = props.read_write_integer_version.clone();
            if let Some(mut rx_for_read_write_integer_prop) =
                props.read_write_integer.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_integer_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteInteger/setValue",
                            client_id_for_read_write_integer_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_integer_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_integer_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_only_integer_prop = self.client_id.clone();
            let mut publisher_for_read_only_integer_prop = self.mqtt_client.clone();
            let read_only_integer_prop_version = props.read_only_integer_version.clone();
            if let Some(mut rx_for_read_only_integer_prop) =
                props.read_only_integer.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_only_integer_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readOnlyInteger/setValue",
                            client_id_for_read_only_integer_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_only_integer_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_only_integer_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_optional_integer_prop = self.client_id.clone();
            let mut publisher_for_read_write_optional_integer_prop = self.mqtt_client.clone();
            let read_write_optional_integer_prop_version =
                props.read_write_optional_integer_version.clone();
            if let Some(mut rx_for_read_write_optional_integer_prop) =
                props.read_write_optional_integer.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_optional_integer_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteOptionalInteger/setValue",
                            client_id_for_read_write_optional_integer_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_optional_integer_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_optional_integer_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_two_integers_prop = self.client_id.clone();
            let mut publisher_for_read_write_two_integers_prop = self.mqtt_client.clone();
            let read_write_two_integers_prop_version =
                props.read_write_two_integers_version.clone();
            if let Some(mut rx_for_read_write_two_integers_prop) =
                props.read_write_two_integers.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_two_integers_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteTwoIntegers/setValue",
                            client_id_for_read_write_two_integers_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_two_integers_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_two_integers_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_only_string_prop = self.client_id.clone();
            let mut publisher_for_read_only_string_prop = self.mqtt_client.clone();
            let read_only_string_prop_version = props.read_only_string_version.clone();
            if let Some(mut rx_for_read_only_string_prop) =
                props.read_only_string.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_only_string_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readOnlyString/setValue",
                            client_id_for_read_only_string_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_only_string_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_only_string_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_string_prop = self.client_id.clone();
            let mut publisher_for_read_write_string_prop = self.mqtt_client.clone();
            let read_write_string_prop_version = props.read_write_string_version.clone();
            if let Some(mut rx_for_read_write_string_prop) =
                props.read_write_string.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_string_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteString/setValue",
                            client_id_for_read_write_string_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_string_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_string_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_optional_string_prop = self.client_id.clone();
            let mut publisher_for_read_write_optional_string_prop = self.mqtt_client.clone();
            let read_write_optional_string_prop_version =
                props.read_write_optional_string_version.clone();
            if let Some(mut rx_for_read_write_optional_string_prop) =
                props.read_write_optional_string.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_optional_string_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteOptionalString/setValue",
                            client_id_for_read_write_optional_string_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_optional_string_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_optional_string_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_two_strings_prop = self.client_id.clone();
            let mut publisher_for_read_write_two_strings_prop = self.mqtt_client.clone();
            let read_write_two_strings_prop_version = props.read_write_two_strings_version.clone();
            if let Some(mut rx_for_read_write_two_strings_prop) =
                props.read_write_two_strings.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_two_strings_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteTwoStrings/setValue",
                            client_id_for_read_write_two_strings_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_two_strings_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_two_strings_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_struct_prop = self.client_id.clone();
            let mut publisher_for_read_write_struct_prop = self.mqtt_client.clone();
            let read_write_struct_prop_version = props.read_write_struct_version.clone();
            if let Some(mut rx_for_read_write_struct_prop) =
                props.read_write_struct.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_struct_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteStruct/setValue",
                            client_id_for_read_write_struct_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_struct_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_struct_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_optional_struct_prop = self.client_id.clone();
            let mut publisher_for_read_write_optional_struct_prop = self.mqtt_client.clone();
            let read_write_optional_struct_prop_version =
                props.read_write_optional_struct_version.clone();
            if let Some(mut rx_for_read_write_optional_struct_prop) =
                props.read_write_optional_struct.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_optional_struct_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteOptionalStruct/setValue",
                            client_id_for_read_write_optional_struct_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_optional_struct_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_optional_struct_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_two_structs_prop = self.client_id.clone();
            let mut publisher_for_read_write_two_structs_prop = self.mqtt_client.clone();
            let read_write_two_structs_prop_version = props.read_write_two_structs_version.clone();
            if let Some(mut rx_for_read_write_two_structs_prop) =
                props.read_write_two_structs.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_two_structs_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteTwoStructs/setValue",
                            client_id_for_read_write_two_structs_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_two_structs_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_two_structs_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_only_enum_prop = self.client_id.clone();
            let mut publisher_for_read_only_enum_prop = self.mqtt_client.clone();
            let read_only_enum_prop_version = props.read_only_enum_version.clone();
            if let Some(mut rx_for_read_only_enum_prop) =
                props.read_only_enum.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_only_enum_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readOnlyEnum/setValue",
                            client_id_for_read_only_enum_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_only_enum_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_only_enum_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_enum_prop = self.client_id.clone();
            let mut publisher_for_read_write_enum_prop = self.mqtt_client.clone();
            let read_write_enum_prop_version = props.read_write_enum_version.clone();
            if let Some(mut rx_for_read_write_enum_prop) =
                props.read_write_enum.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_enum_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteEnum/setValue",
                            client_id_for_read_write_enum_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_enum_prop_version.load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_enum_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_optional_enum_prop = self.client_id.clone();
            let mut publisher_for_read_write_optional_enum_prop = self.mqtt_client.clone();
            let read_write_optional_enum_prop_version =
                props.read_write_optional_enum_version.clone();
            if let Some(mut rx_for_read_write_optional_enum_prop) =
                props.read_write_optional_enum.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_optional_enum_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteOptionalEnum/setValue",
                            client_id_for_read_write_optional_enum_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_optional_enum_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_optional_enum_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_two_enums_prop = self.client_id.clone();
            let mut publisher_for_read_write_two_enums_prop = self.mqtt_client.clone();
            let read_write_two_enums_prop_version = props.read_write_two_enums_version.clone();
            if let Some(mut rx_for_read_write_two_enums_prop) =
                props.read_write_two_enums.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_two_enums_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteTwoEnums/setValue",
                            client_id_for_read_write_two_enums_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_two_enums_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_two_enums_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_datetime_prop = self.client_id.clone();
            let mut publisher_for_read_write_datetime_prop = self.mqtt_client.clone();
            let read_write_datetime_prop_version = props.read_write_datetime_version.clone();
            if let Some(mut rx_for_read_write_datetime_prop) =
                props.read_write_datetime.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_datetime_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteDatetime/setValue",
                            client_id_for_read_write_datetime_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_datetime_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_datetime_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_optional_datetime_prop = self.client_id.clone();
            let mut publisher_for_read_write_optional_datetime_prop = self.mqtt_client.clone();
            let read_write_optional_datetime_prop_version =
                props.read_write_optional_datetime_version.clone();
            if let Some(mut rx_for_read_write_optional_datetime_prop) =
                props.read_write_optional_datetime.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_optional_datetime_prop.recv().await
                    {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteOptionalDatetime/setValue",
                            client_id_for_read_write_optional_datetime_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_optional_datetime_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_optional_datetime_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_two_datetimes_prop = self.client_id.clone();
            let mut publisher_for_read_write_two_datetimes_prop = self.mqtt_client.clone();
            let read_write_two_datetimes_prop_version =
                props.read_write_two_datetimes_version.clone();
            if let Some(mut rx_for_read_write_two_datetimes_prop) =
                props.read_write_two_datetimes.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_two_datetimes_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteTwoDatetimes/setValue",
                            client_id_for_read_write_two_datetimes_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_two_datetimes_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_two_datetimes_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_duration_prop = self.client_id.clone();
            let mut publisher_for_read_write_duration_prop = self.mqtt_client.clone();
            let read_write_duration_prop_version = props.read_write_duration_version.clone();
            if let Some(mut rx_for_read_write_duration_prop) =
                props.read_write_duration.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_duration_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteDuration/setValue",
                            client_id_for_read_write_duration_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_duration_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_duration_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_optional_duration_prop = self.client_id.clone();
            let mut publisher_for_read_write_optional_duration_prop = self.mqtt_client.clone();
            let read_write_optional_duration_prop_version =
                props.read_write_optional_duration_version.clone();
            if let Some(mut rx_for_read_write_optional_duration_prop) =
                props.read_write_optional_duration.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_optional_duration_prop.recv().await
                    {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteOptionalDuration/setValue",
                            client_id_for_read_write_optional_duration_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_optional_duration_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_optional_duration_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_two_durations_prop = self.client_id.clone();
            let mut publisher_for_read_write_two_durations_prop = self.mqtt_client.clone();
            let read_write_two_durations_prop_version =
                props.read_write_two_durations_version.clone();
            if let Some(mut rx_for_read_write_two_durations_prop) =
                props.read_write_two_durations.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_two_durations_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteTwoDurations/setValue",
                            client_id_for_read_write_two_durations_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_two_durations_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_two_durations_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_binary_prop = self.client_id.clone();
            let mut publisher_for_read_write_binary_prop = self.mqtt_client.clone();
            let read_write_binary_prop_version = props.read_write_binary_version.clone();
            if let Some(mut rx_for_read_write_binary_prop) =
                props.read_write_binary.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_binary_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteBinary/setValue",
                            client_id_for_read_write_binary_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_binary_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_binary_prop.publish(msg).await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_optional_binary_prop = self.client_id.clone();
            let mut publisher_for_read_write_optional_binary_prop = self.mqtt_client.clone();
            let read_write_optional_binary_prop_version =
                props.read_write_optional_binary_version.clone();
            if let Some(mut rx_for_read_write_optional_binary_prop) =
                props.read_write_optional_binary.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_optional_binary_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteOptionalBinary/setValue",
                            client_id_for_read_write_optional_binary_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_optional_binary_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_optional_binary_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_two_binaries_prop = self.client_id.clone();
            let mut publisher_for_read_write_two_binaries_prop = self.mqtt_client.clone();
            let read_write_two_binaries_prop_version =
                props.read_write_two_binaries_version.clone();
            if let Some(mut rx_for_read_write_two_binaries_prop) =
                props.read_write_two_binaries.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_two_binaries_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteTwoBinaries/setValue",
                            client_id_for_read_write_two_binaries_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_two_binaries_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_two_binaries_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_list_of_strings_prop = self.client_id.clone();
            let mut publisher_for_read_write_list_of_strings_prop = self.mqtt_client.clone();
            let read_write_list_of_strings_prop_version =
                props.read_write_list_of_strings_version.clone();
            if let Some(mut rx_for_read_write_list_of_strings_prop) =
                props.read_write_list_of_strings.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_list_of_strings_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteListOfStrings/setValue",
                            client_id_for_read_write_list_of_strings_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_list_of_strings_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result = publisher_for_read_write_list_of_strings_prop
                            .publish(msg)
                            .await;
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let client_id_for_read_write_lists_prop = self.client_id.clone();
            let mut publisher_for_read_write_lists_prop = self.mqtt_client.clone();
            let read_write_lists_prop_version = props.read_write_lists_version.clone();
            if let Some(mut rx_for_read_write_lists_prop) =
                props.read_write_lists.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some(request) = rx_for_read_write_lists_prop.recv().await {
                        let topic: String = format!(
                            "testAble/{}/property/readWriteLists/setValue",
                            client_id_for_read_write_lists_prop
                        );
                        let msg = message::property_update_message(
                            &topic,
                            &request,
                            read_write_lists_prop_version
                                .load(std::sync::atomic::Ordering::Relaxed),
                        )
                        .unwrap();
                        let _publish_result =
                            publisher_for_read_write_lists_prop.publish(msg).await;
                    }
                });
            }
        }

        let _loop_task = tokio::spawn(async move {
            while let Ok(msg) = message_receiver.recv().await {
                let opt_corr_data: Option<Vec<u8>> =
                    msg.correlation_data.clone().map(|b| b.to_vec());
                let opt_corr_id: Option<Uuid> =
                    opt_corr_data.and_then(|b| Uuid::from_slice(b.as_slice()).ok());

                if let Some(subscription_id) = msg.subscription_id {
                    let return_code = TestAbleClient::<C>::get_return_code_from_message(&msg);
                    if subscription_id == sub_ids.call_with_nothing_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callWithNothing method response handling
                    else if subscription_id == sub_ids.call_one_integer_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOneInteger method response handling
                    else if subscription_id == sub_ids.call_optional_integer_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOptionalInteger method response handling
                    else if subscription_id == sub_ids.call_three_integers_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callThreeIntegers method response handling
                    else if subscription_id == sub_ids.call_one_string_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOneString method response handling
                    else if subscription_id == sub_ids.call_optional_string_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOptionalString method response handling
                    else if subscription_id == sub_ids.call_three_strings_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callThreeStrings method response handling
                    else if subscription_id == sub_ids.call_one_enum_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOneEnum method response handling
                    else if subscription_id == sub_ids.call_optional_enum_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOptionalEnum method response handling
                    else if subscription_id == sub_ids.call_three_enums_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callThreeEnums method response handling
                    else if subscription_id == sub_ids.call_one_struct_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOneStruct method response handling
                    else if subscription_id == sub_ids.call_optional_struct_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOptionalStruct method response handling
                    else if subscription_id == sub_ids.call_three_structs_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callThreeStructs method response handling
                    else if subscription_id == sub_ids.call_one_date_time_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOneDateTime method response handling
                    else if subscription_id == sub_ids.call_optional_date_time_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOptionalDateTime method response handling
                    else if subscription_id == sub_ids.call_three_date_times_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callThreeDateTimes method response handling
                    else if subscription_id == sub_ids.call_one_duration_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOneDuration method response handling
                    else if subscription_id == sub_ids.call_optional_duration_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOptionalDuration method response handling
                    else if subscription_id == sub_ids.call_three_durations_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callThreeDurations method response handling
                    else if subscription_id == sub_ids.call_one_binary_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOneBinary method response handling
                    else if subscription_id == sub_ids.call_optional_binary_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOptionalBinary method response handling
                    else if subscription_id == sub_ids.call_three_binaries_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callThreeBinaries method response handling
                    else if subscription_id == sub_ids.call_one_list_of_integers_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOneListOfIntegers method response handling
                    else if subscription_id == sub_ids.call_optional_list_of_floats_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    }
                    // end callOptionalListOfFloats method response handling
                    else if subscription_id == sub_ids.call_two_lists_method_resp {
                        if opt_corr_id.is_some() {
                            let opt_sender = opt_corr_id.and_then(|uuid| {
                                let mut hashmap = resp_map.lock().expect("Mutex was poisoned");
                                hashmap.remove(&uuid)
                            });
                            if let Some(sender) = opt_sender {
                                let oss: oneshot::Sender<MethodReturnCode> = sender;
                                match oss.send(return_code.clone()) {
                                    Ok(_) => (),
                                    Err(_) => (),
                                }
                            }
                        }
                    } // end callTwoLists method response handling
                    if Some(subscription_id) == sub_ids.empty_signal {
                        let chan = sig_chans.empty_sender.clone();

                        let _send_result = chan.send(());
                    }
                    // end empty signal handling
                    else if Some(subscription_id) == sub_ids.single_int_signal {
                        let chan = sig_chans.single_int_sender.clone();

                        match serde_json::from_slice::<SingleIntSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SingleIntSignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end singleInt signal handling
                    else if Some(subscription_id) == sub_ids.single_optional_int_signal {
                        let chan = sig_chans.single_optional_int_sender.clone();

                        match serde_json::from_slice::<SingleOptionalIntSignalPayload>(&msg.payload)
                        {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleOptionalIntSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleOptionalInt signal handling
                    else if Some(subscription_id) == sub_ids.three_integers_signal {
                        let chan = sig_chans.three_integers_sender.clone();

                        match serde_json::from_slice::<ThreeIntegersSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into ThreeIntegersSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end threeIntegers signal handling
                    else if Some(subscription_id) == sub_ids.single_string_signal {
                        let chan = sig_chans.single_string_sender.clone();

                        match serde_json::from_slice::<SingleStringSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SingleStringSignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end singleString signal handling
                    else if Some(subscription_id) == sub_ids.single_optional_string_signal {
                        let chan = sig_chans.single_optional_string_sender.clone();

                        match serde_json::from_slice::<SingleOptionalStringSignalPayload>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleOptionalStringSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleOptionalString signal handling
                    else if Some(subscription_id) == sub_ids.three_strings_signal {
                        let chan = sig_chans.three_strings_sender.clone();

                        match serde_json::from_slice::<ThreeStringsSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into ThreeStringsSignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end threeStrings signal handling
                    else if Some(subscription_id) == sub_ids.single_enum_signal {
                        let chan = sig_chans.single_enum_sender.clone();

                        match serde_json::from_slice::<SingleEnumSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SingleEnumSignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end singleEnum signal handling
                    else if Some(subscription_id) == sub_ids.single_optional_enum_signal {
                        let chan = sig_chans.single_optional_enum_sender.clone();

                        match serde_json::from_slice::<SingleOptionalEnumSignalPayload>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleOptionalEnumSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleOptionalEnum signal handling
                    else if Some(subscription_id) == sub_ids.three_enums_signal {
                        let chan = sig_chans.three_enums_sender.clone();

                        match serde_json::from_slice::<ThreeEnumsSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into ThreeEnumsSignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end threeEnums signal handling
                    else if Some(subscription_id) == sub_ids.single_struct_signal {
                        let chan = sig_chans.single_struct_sender.clone();

                        match serde_json::from_slice::<SingleStructSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SingleStructSignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end singleStruct signal handling
                    else if Some(subscription_id) == sub_ids.single_optional_struct_signal {
                        let chan = sig_chans.single_optional_struct_sender.clone();

                        match serde_json::from_slice::<SingleOptionalStructSignalPayload>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleOptionalStructSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleOptionalStruct signal handling
                    else if Some(subscription_id) == sub_ids.three_structs_signal {
                        let chan = sig_chans.three_structs_sender.clone();

                        match serde_json::from_slice::<ThreeStructsSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into ThreeStructsSignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end threeStructs signal handling
                    else if Some(subscription_id) == sub_ids.single_date_time_signal {
                        let chan = sig_chans.single_date_time_sender.clone();

                        match serde_json::from_slice::<SingleDateTimeSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleDateTimeSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleDateTime signal handling
                    else if Some(subscription_id) == sub_ids.single_optional_datetime_signal {
                        let chan = sig_chans.single_optional_datetime_sender.clone();

                        match serde_json::from_slice::<SingleOptionalDatetimeSignalPayload>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleOptionalDatetimeSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleOptionalDatetime signal handling
                    else if Some(subscription_id) == sub_ids.three_date_times_signal {
                        let chan = sig_chans.three_date_times_sender.clone();

                        match serde_json::from_slice::<ThreeDateTimesSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into ThreeDateTimesSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end threeDateTimes signal handling
                    else if Some(subscription_id) == sub_ids.single_duration_signal {
                        let chan = sig_chans.single_duration_sender.clone();

                        match serde_json::from_slice::<SingleDurationSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleDurationSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleDuration signal handling
                    else if Some(subscription_id) == sub_ids.single_optional_duration_signal {
                        let chan = sig_chans.single_optional_duration_sender.clone();

                        match serde_json::from_slice::<SingleOptionalDurationSignalPayload>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleOptionalDurationSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleOptionalDuration signal handling
                    else if Some(subscription_id) == sub_ids.three_durations_signal {
                        let chan = sig_chans.three_durations_sender.clone();

                        match serde_json::from_slice::<ThreeDurationsSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into ThreeDurationsSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end threeDurations signal handling
                    else if Some(subscription_id) == sub_ids.single_binary_signal {
                        let chan = sig_chans.single_binary_sender.clone();

                        match serde_json::from_slice::<SingleBinarySignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SingleBinarySignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end singleBinary signal handling
                    else if Some(subscription_id) == sub_ids.single_optional_binary_signal {
                        let chan = sig_chans.single_optional_binary_sender.clone();

                        match serde_json::from_slice::<SingleOptionalBinarySignalPayload>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.value);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleOptionalBinarySignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleOptionalBinary signal handling
                    else if Some(subscription_id) == sub_ids.three_binaries_signal {
                        let chan = sig_chans.three_binaries_sender.clone();

                        match serde_json::from_slice::<ThreeBinariesSignalPayload>(&msg.payload) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into ThreeBinariesSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end threeBinaries signal handling
                    else if Some(subscription_id) == sub_ids.single_array_of_integers_signal {
                        let chan = sig_chans.single_array_of_integers_sender.clone();

                        match serde_json::from_slice::<SingleArrayOfIntegersSignalPayload>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.values);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleArrayOfIntegersSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleArrayOfIntegers signal handling
                    else if Some(subscription_id)
                        == sub_ids.single_optional_array_of_strings_signal
                    {
                        let chan = sig_chans.single_optional_array_of_strings_sender.clone();

                        match serde_json::from_slice::<SingleOptionalArrayOfStringsSignalPayload>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let _send_result = chan.send(pl.values);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into SingleOptionalArrayOfStringsSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    }
                    // end singleOptionalArrayOfStrings signal handling
                    else if Some(subscription_id) == sub_ids.array_of_every_type_signal {
                        let chan = sig_chans.array_of_every_type_sender.clone();

                        match serde_json::from_slice::<ArrayOfEveryTypeSignalPayload>(&msg.payload)
                        {
                            Ok(pl) => {
                                let _send_result = chan.send(pl);
                            }
                            Err(e) => {
                                warn!("Failed to deserialize '{}' into ArrayOfEveryTypeSignalPayload: {}", String::from_utf8_lossy(&msg.payload), e);
                                continue;
                            }
                        }
                    } // end arrayOfEveryType signal handling

                    if subscription_id == sub_ids.read_write_integer_property_value {
                        match serde_json::from_slice::<ReadWriteIntegerProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_integer.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_integer_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_integer property value update
                    else if subscription_id == sub_ids.read_only_integer_property_value {
                        match serde_json::from_slice::<ReadOnlyIntegerProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_only_integer.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_only_integer_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_only_integer property value update
                    else if subscription_id == sub_ids.read_write_optional_integer_property_value
                    {
                        match serde_json::from_slice::<ReadWriteOptionalIntegerProperty>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let mut guard = props.read_write_optional_integer.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_optional_integer_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_optional_integer property value update
                    else if subscription_id == sub_ids.read_write_two_integers_property_value {
                        match serde_json::from_slice::<ReadWriteTwoIntegersProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_two_integers.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_two_integers_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_two_integers property value update
                    else if subscription_id == sub_ids.read_only_string_property_value {
                        match serde_json::from_slice::<ReadOnlyStringProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_only_string.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_only_string_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_only_string property value update
                    else if subscription_id == sub_ids.read_write_string_property_value {
                        match serde_json::from_slice::<ReadWriteStringProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_string.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_string_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_string property value update
                    else if subscription_id == sub_ids.read_write_optional_string_property_value {
                        match serde_json::from_slice::<ReadWriteOptionalStringProperty>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let mut guard = props.read_write_optional_string.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_optional_string_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_optional_string property value update
                    else if subscription_id == sub_ids.read_write_two_strings_property_value {
                        match serde_json::from_slice::<ReadWriteTwoStringsProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_two_strings.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_two_strings_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_two_strings property value update
                    else if subscription_id == sub_ids.read_write_struct_property_value {
                        match serde_json::from_slice::<ReadWriteStructProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_struct.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_struct_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_struct property value update
                    else if subscription_id == sub_ids.read_write_optional_struct_property_value {
                        match serde_json::from_slice::<ReadWriteOptionalStructProperty>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let mut guard = props.read_write_optional_struct.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_optional_struct_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_optional_struct property value update
                    else if subscription_id == sub_ids.read_write_two_structs_property_value {
                        match serde_json::from_slice::<ReadWriteTwoStructsProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_two_structs.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_two_structs_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_two_structs property value update
                    else if subscription_id == sub_ids.read_only_enum_property_value {
                        match serde_json::from_slice::<ReadOnlyEnumProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_only_enum.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_only_enum_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_only_enum property value update
                    else if subscription_id == sub_ids.read_write_enum_property_value {
                        match serde_json::from_slice::<ReadWriteEnumProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_enum.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_enum_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_enum property value update
                    else if subscription_id == sub_ids.read_write_optional_enum_property_value {
                        match serde_json::from_slice::<ReadWriteOptionalEnumProperty>(&msg.payload)
                        {
                            Ok(pl) => {
                                let mut guard = props.read_write_optional_enum.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_optional_enum_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_optional_enum property value update
                    else if subscription_id == sub_ids.read_write_two_enums_property_value {
                        match serde_json::from_slice::<ReadWriteTwoEnumsProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_two_enums.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_two_enums_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_two_enums property value update
                    else if subscription_id == sub_ids.read_write_datetime_property_value {
                        match serde_json::from_slice::<ReadWriteDatetimeProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_datetime.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_datetime_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_datetime property value update
                    else if subscription_id == sub_ids.read_write_optional_datetime_property_value
                    {
                        match serde_json::from_slice::<ReadWriteOptionalDatetimeProperty>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let mut guard = props.read_write_optional_datetime.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_optional_datetime_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_optional_datetime property value update
                    else if subscription_id == sub_ids.read_write_two_datetimes_property_value {
                        match serde_json::from_slice::<ReadWriteTwoDatetimesProperty>(&msg.payload)
                        {
                            Ok(pl) => {
                                let mut guard = props.read_write_two_datetimes.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_two_datetimes_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_two_datetimes property value update
                    else if subscription_id == sub_ids.read_write_duration_property_value {
                        match serde_json::from_slice::<ReadWriteDurationProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_duration.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_duration_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_duration property value update
                    else if subscription_id == sub_ids.read_write_optional_duration_property_value
                    {
                        match serde_json::from_slice::<ReadWriteOptionalDurationProperty>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let mut guard = props.read_write_optional_duration.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_optional_duration_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_optional_duration property value update
                    else if subscription_id == sub_ids.read_write_two_durations_property_value {
                        match serde_json::from_slice::<ReadWriteTwoDurationsProperty>(&msg.payload)
                        {
                            Ok(pl) => {
                                let mut guard = props.read_write_two_durations.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_two_durations_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_two_durations property value update
                    else if subscription_id == sub_ids.read_write_binary_property_value {
                        match serde_json::from_slice::<ReadWriteBinaryProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_binary.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_binary_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_binary property value update
                    else if subscription_id == sub_ids.read_write_optional_binary_property_value {
                        match serde_json::from_slice::<ReadWriteOptionalBinaryProperty>(
                            &msg.payload,
                        ) {
                            Ok(pl) => {
                                let mut guard = props.read_write_optional_binary.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_optional_binary_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_optional_binary property value update
                    else if subscription_id == sub_ids.read_write_two_binaries_property_value {
                        match serde_json::from_slice::<ReadWriteTwoBinariesProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_two_binaries.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_two_binaries_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_two_binaries property value update
                    else if subscription_id == sub_ids.read_write_list_of_strings_property_value {
                        match serde_json::from_slice::<ReadWriteListOfStringsProperty>(&msg.payload)
                        {
                            Ok(pl) => {
                                let mut guard = props.read_write_list_of_strings.write().await;

                                *guard = pl.value.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_list_of_strings_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    }
                    // end read_write_list_of_strings property value update
                    else if subscription_id == sub_ids.read_write_lists_property_value {
                        match serde_json::from_slice::<ReadWriteListsProperty>(&msg.payload) {
                            Ok(pl) => {
                                let mut guard = props.read_write_lists.write().await;

                                *guard = pl.clone();

                                if let Some(version_str) = msg.user_properties.get("Version") {
                                    if let Ok(version_num) = version_str.parse::<u32>() {
                                        props.read_write_lists_version.store(
                                            version_num,
                                            std::sync::atomic::Ordering::Relaxed,
                                        );
                                    }
                                }
                                if opt_corr_id.is_some() {
                                    let opt_sender = opt_corr_id.and_then(|uuid| {
                                        let mut hashmap =
                                            resp_map.lock().expect("Mutex was poisoned");
                                        hashmap.remove(&uuid)
                                    });
                                    if let Some(sender) = opt_sender {
                                        let oss: oneshot::Sender<MethodReturnCode> = sender;
                                        match oss.send(return_code) {
                                            Ok(_) => (),
                                            Err(_) => (),
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                warn!(
                                    "Failed to deserialize '{}' into SignalPayload: {}",
                                    String::from_utf8_lossy(&msg.payload),
                                    e
                                );
                                continue;
                            }
                        }
                    } // end read_write_lists property value update
                }
            }
        });

        Ok(())
    }
}
