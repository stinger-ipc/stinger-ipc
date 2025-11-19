//! Server module for testable IPC
//!
//! This module is only available when the "server" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the testable interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
use bytes::Bytes;
use tokio::sync::oneshot;

use async_trait::async_trait;
use std::any::Any;
use std::sync::{Arc, Mutex};
use tokio::sync::Mutex as AsyncMutex;

use serde_json;
use tokio::sync::{broadcast, watch};

use crate::property::TestableInitialPropertyValues;
use std::sync::atomic::{AtomicU32, Ordering};

use std::future::Future;
use std::pin::Pin;
use stinger_mqtt_trait::message::{MqttMessage, QoS};
use stinger_mqtt_trait::{Mqtt5PubSub, Mqtt5PubSubError, MqttPublishSuccess};
use stinger_rwlock_watch::RwLockWatch;
#[allow(unused_imports)]
use stinger_rwlock_watch::{CommitResult, WriteRequestLockWatch};
use tokio::task::JoinError;
type SentMessageFuture = Pin<Box<dyn Future<Output = Result<(), MethodReturnCode>> + Send>>;
use crate::message;
#[cfg(feature = "metrics")]
use serde::Serialize;
#[cfg(feature = "server")]
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct TestableServerSubscriptionIds {
    call_with_nothing_method_req: u32,
    call_one_integer_method_req: u32,
    call_optional_integer_method_req: u32,
    call_three_integers_method_req: u32,
    call_one_string_method_req: u32,
    call_optional_string_method_req: u32,
    call_three_strings_method_req: u32,
    call_one_enum_method_req: u32,
    call_optional_enum_method_req: u32,
    call_three_enums_method_req: u32,
    call_one_struct_method_req: u32,
    call_optional_struct_method_req: u32,
    call_three_structs_method_req: u32,
    call_one_date_time_method_req: u32,
    call_optional_date_time_method_req: u32,
    call_three_date_times_method_req: u32,
    call_one_duration_method_req: u32,
    call_optional_duration_method_req: u32,
    call_three_durations_method_req: u32,
    call_one_binary_method_req: u32,
    call_optional_binary_method_req: u32,
    call_three_binaries_method_req: u32,
    call_one_list_of_integers_method_req: u32,
    call_optional_list_of_floats_method_req: u32,
    call_two_lists_method_req: u32,

    read_write_integer_property_update: u32,

    read_write_optional_integer_property_update: u32,

    read_write_two_integers_property_update: u32,

    read_write_string_property_update: u32,

    read_write_optional_string_property_update: u32,

    read_write_two_strings_property_update: u32,

    read_write_struct_property_update: u32,

    read_write_optional_struct_property_update: u32,

    read_write_two_structs_property_update: u32,

    read_write_enum_property_update: u32,

    read_write_optional_enum_property_update: u32,

    read_write_two_enums_property_update: u32,

    read_write_datetime_property_update: u32,

    read_write_optional_datetime_property_update: u32,

    read_write_two_datetimes_property_update: u32,

    read_write_duration_property_update: u32,

    read_write_optional_duration_property_update: u32,

    read_write_two_durations_property_update: u32,

    read_write_binary_property_update: u32,

    read_write_optional_binary_property_update: u32,

    read_write_two_binaries_property_update: u32,

    read_write_list_of_strings_property_update: u32,

    read_write_lists_property_update: u32,
}

#[derive(Clone)]
struct TestableProperties {
    pub read_write_integer: Arc<RwLockWatch<i32>>,
    read_write_integer_version: Arc<AtomicU32>,
    pub read_only_integer: Arc<RwLockWatch<i32>>,
    read_only_integer_version: Arc<AtomicU32>,
    pub read_write_optional_integer: Arc<RwLockWatch<Option<i32>>>,
    read_write_optional_integer_version: Arc<AtomicU32>,
    pub read_write_two_integers: Arc<RwLockWatch<ReadWriteTwoIntegersProperty>>,
    read_write_two_integers_version: Arc<AtomicU32>,
    pub read_only_string: Arc<RwLockWatch<String>>,
    read_only_string_version: Arc<AtomicU32>,
    pub read_write_string: Arc<RwLockWatch<String>>,
    read_write_string_version: Arc<AtomicU32>,
    pub read_write_optional_string: Arc<RwLockWatch<Option<String>>>,
    read_write_optional_string_version: Arc<AtomicU32>,
    pub read_write_two_strings: Arc<RwLockWatch<ReadWriteTwoStringsProperty>>,
    read_write_two_strings_version: Arc<AtomicU32>,
    pub read_write_struct: Arc<RwLockWatch<AllTypes>>,
    read_write_struct_version: Arc<AtomicU32>,
    pub read_write_optional_struct: Arc<RwLockWatch<Option<AllTypes>>>,
    read_write_optional_struct_version: Arc<AtomicU32>,
    pub read_write_two_structs: Arc<RwLockWatch<ReadWriteTwoStructsProperty>>,
    read_write_two_structs_version: Arc<AtomicU32>,
    pub read_only_enum: Arc<RwLockWatch<Numbers>>,
    read_only_enum_version: Arc<AtomicU32>,
    pub read_write_enum: Arc<RwLockWatch<Numbers>>,
    read_write_enum_version: Arc<AtomicU32>,
    pub read_write_optional_enum: Arc<RwLockWatch<Option<Numbers>>>,
    read_write_optional_enum_version: Arc<AtomicU32>,
    pub read_write_two_enums: Arc<RwLockWatch<ReadWriteTwoEnumsProperty>>,
    read_write_two_enums_version: Arc<AtomicU32>,
    pub read_write_datetime: Arc<RwLockWatch<chrono::DateTime<chrono::Utc>>>,
    read_write_datetime_version: Arc<AtomicU32>,
    pub read_write_optional_datetime: Arc<RwLockWatch<Option<chrono::DateTime<chrono::Utc>>>>,
    read_write_optional_datetime_version: Arc<AtomicU32>,
    pub read_write_two_datetimes: Arc<RwLockWatch<ReadWriteTwoDatetimesProperty>>,
    read_write_two_datetimes_version: Arc<AtomicU32>,
    pub read_write_duration: Arc<RwLockWatch<chrono::Duration>>,
    read_write_duration_version: Arc<AtomicU32>,
    pub read_write_optional_duration: Arc<RwLockWatch<Option<chrono::Duration>>>,
    read_write_optional_duration_version: Arc<AtomicU32>,
    pub read_write_two_durations: Arc<RwLockWatch<ReadWriteTwoDurationsProperty>>,
    read_write_two_durations_version: Arc<AtomicU32>,
    pub read_write_binary: Arc<RwLockWatch<Vec<u8>>>,
    read_write_binary_version: Arc<AtomicU32>,
    pub read_write_optional_binary: Arc<RwLockWatch<Option<Vec<u8>>>>,
    read_write_optional_binary_version: Arc<AtomicU32>,
    pub read_write_two_binaries: Arc<RwLockWatch<ReadWriteTwoBinariesProperty>>,
    read_write_two_binaries_version: Arc<AtomicU32>,
    pub read_write_list_of_strings: Arc<RwLockWatch<Vec<String>>>,
    read_write_list_of_strings_version: Arc<AtomicU32>,
    pub read_write_lists: Arc<RwLockWatch<ReadWriteListsProperty>>,
    read_write_lists_version: Arc<AtomicU32>,
}

#[cfg(feature = "metrics")]
#[derive(Debug, Serialize)]
pub struct TestableServerMetrics {
    pub call_with_nothing_calls: u64,
    pub call_with_nothing_errors: u64,
    pub call_one_integer_calls: u64,
    pub call_one_integer_errors: u64,
    pub call_optional_integer_calls: u64,
    pub call_optional_integer_errors: u64,
    pub call_three_integers_calls: u64,
    pub call_three_integers_errors: u64,
    pub call_one_string_calls: u64,
    pub call_one_string_errors: u64,
    pub call_optional_string_calls: u64,
    pub call_optional_string_errors: u64,
    pub call_three_strings_calls: u64,
    pub call_three_strings_errors: u64,
    pub call_one_enum_calls: u64,
    pub call_one_enum_errors: u64,
    pub call_optional_enum_calls: u64,
    pub call_optional_enum_errors: u64,
    pub call_three_enums_calls: u64,
    pub call_three_enums_errors: u64,
    pub call_one_struct_calls: u64,
    pub call_one_struct_errors: u64,
    pub call_optional_struct_calls: u64,
    pub call_optional_struct_errors: u64,
    pub call_three_structs_calls: u64,
    pub call_three_structs_errors: u64,
    pub call_one_date_time_calls: u64,
    pub call_one_date_time_errors: u64,
    pub call_optional_date_time_calls: u64,
    pub call_optional_date_time_errors: u64,
    pub call_three_date_times_calls: u64,
    pub call_three_date_times_errors: u64,
    pub call_one_duration_calls: u64,
    pub call_one_duration_errors: u64,
    pub call_optional_duration_calls: u64,
    pub call_optional_duration_errors: u64,
    pub call_three_durations_calls: u64,
    pub call_three_durations_errors: u64,
    pub call_one_binary_calls: u64,
    pub call_one_binary_errors: u64,
    pub call_optional_binary_calls: u64,
    pub call_optional_binary_errors: u64,
    pub call_three_binaries_calls: u64,
    pub call_three_binaries_errors: u64,
    pub call_one_list_of_integers_calls: u64,
    pub call_one_list_of_integers_errors: u64,
    pub call_optional_list_of_floats_calls: u64,
    pub call_optional_list_of_floats_errors: u64,
    pub call_two_lists_calls: u64,
    pub call_two_lists_errors: u64,

    pub initial_property_publish_time: std::time::Duration,
}

#[cfg(feature = "metrics")]
impl Default for TestableServerMetrics {
    fn default() -> Self {
        TestableServerMetrics {
            call_with_nothing_calls: 0,
            call_with_nothing_errors: 0,
            call_one_integer_calls: 0,
            call_one_integer_errors: 0,
            call_optional_integer_calls: 0,
            call_optional_integer_errors: 0,
            call_three_integers_calls: 0,
            call_three_integers_errors: 0,
            call_one_string_calls: 0,
            call_one_string_errors: 0,
            call_optional_string_calls: 0,
            call_optional_string_errors: 0,
            call_three_strings_calls: 0,
            call_three_strings_errors: 0,
            call_one_enum_calls: 0,
            call_one_enum_errors: 0,
            call_optional_enum_calls: 0,
            call_optional_enum_errors: 0,
            call_three_enums_calls: 0,
            call_three_enums_errors: 0,
            call_one_struct_calls: 0,
            call_one_struct_errors: 0,
            call_optional_struct_calls: 0,
            call_optional_struct_errors: 0,
            call_three_structs_calls: 0,
            call_three_structs_errors: 0,
            call_one_date_time_calls: 0,
            call_one_date_time_errors: 0,
            call_optional_date_time_calls: 0,
            call_optional_date_time_errors: 0,
            call_three_date_times_calls: 0,
            call_three_date_times_errors: 0,
            call_one_duration_calls: 0,
            call_one_duration_errors: 0,
            call_optional_duration_calls: 0,
            call_optional_duration_errors: 0,
            call_three_durations_calls: 0,
            call_three_durations_errors: 0,
            call_one_binary_calls: 0,
            call_one_binary_errors: 0,
            call_optional_binary_calls: 0,
            call_optional_binary_errors: 0,
            call_three_binaries_calls: 0,
            call_three_binaries_errors: 0,
            call_one_list_of_integers_calls: 0,
            call_one_list_of_integers_errors: 0,
            call_optional_list_of_floats_calls: 0,
            call_optional_list_of_floats_errors: 0,
            call_two_lists_calls: 0,
            call_two_lists_errors: 0,

            initial_property_publish_time: std::time::Duration::from_secs(0),
        }
    }
}

#[derive(Clone)]
pub struct TestableServer<C: Mqtt5PubSub> {
    mqtt_client: C,

    /// Temporarily holds the receiver for the broadcast channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<broadcast::Receiver<MqttMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: broadcast::Sender<MqttMessage>,

    /// Struct contains all the method handlers.
    method_handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,

    /// Struct contains all the properties.
    properties: TestableProperties,

    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: TestableServerSubscriptionIds,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,

    pub instance_id: String,

    #[cfg(feature = "metrics")]
    metrics: Arc<AsyncMutex<TestableServerMetrics>>,
}

impl<C: Mqtt5PubSub + Clone + Send> TestableServer<C> {
    pub async fn new(
        mut connection: C,
        method_handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        instance_id: String,
        initial_property_values: TestableInitialPropertyValues,
    ) -> Self {
        #[cfg(feature = "metrics")]
        let mut metrics = TestableServerMetrics::default();

        // Create a channel for messages to get from the Mqtt5PubSub object to this TestableServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = broadcast::channel::<MqttMessage>(64);

        // Create method handler struct
        let subscription_id_call_with_nothing_method_req = connection
            .subscribe(
                format!("testable/{}/method/callWithNothing", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_with_nothing_method_req =
            subscription_id_call_with_nothing_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_one_integer_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOneInteger", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_integer_method_req =
            subscription_id_call_one_integer_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_optional_integer_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOptionalInteger", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_integer_method_req =
            subscription_id_call_optional_integer_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_three_integers_method_req = connection
            .subscribe(
                format!("testable/{}/method/callThreeIntegers", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_integers_method_req =
            subscription_id_call_three_integers_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_one_string_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOneString", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_string_method_req =
            subscription_id_call_one_string_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_optional_string_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOptionalString", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_string_method_req =
            subscription_id_call_optional_string_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_three_strings_method_req = connection
            .subscribe(
                format!("testable/{}/method/callThreeStrings", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_strings_method_req =
            subscription_id_call_three_strings_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_one_enum_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOneEnum", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_enum_method_req =
            subscription_id_call_one_enum_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_optional_enum_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOptionalEnum", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_enum_method_req =
            subscription_id_call_optional_enum_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_three_enums_method_req = connection
            .subscribe(
                format!("testable/{}/method/callThreeEnums", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_enums_method_req =
            subscription_id_call_three_enums_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_one_struct_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOneStruct", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_struct_method_req =
            subscription_id_call_one_struct_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_optional_struct_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOptionalStruct", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_struct_method_req =
            subscription_id_call_optional_struct_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_three_structs_method_req = connection
            .subscribe(
                format!("testable/{}/method/callThreeStructs", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_structs_method_req =
            subscription_id_call_three_structs_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_one_date_time_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOneDateTime", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_date_time_method_req =
            subscription_id_call_one_date_time_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_optional_date_time_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOptionalDateTime", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_date_time_method_req =
            subscription_id_call_optional_date_time_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_three_date_times_method_req = connection
            .subscribe(
                format!("testable/{}/method/callThreeDateTimes", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_date_times_method_req =
            subscription_id_call_three_date_times_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_one_duration_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOneDuration", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_duration_method_req =
            subscription_id_call_one_duration_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_optional_duration_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOptionalDuration", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_duration_method_req =
            subscription_id_call_optional_duration_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_three_durations_method_req = connection
            .subscribe(
                format!("testable/{}/method/callThreeDurations", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_durations_method_req =
            subscription_id_call_three_durations_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_one_binary_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOneBinary", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_binary_method_req =
            subscription_id_call_one_binary_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_optional_binary_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOptionalBinary", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_binary_method_req =
            subscription_id_call_optional_binary_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_three_binaries_method_req = connection
            .subscribe(
                format!("testable/{}/method/callThreeBinaries", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_binaries_method_req =
            subscription_id_call_three_binaries_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_one_list_of_integers_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOneListOfIntegers", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_list_of_integers_method_req =
            subscription_id_call_one_list_of_integers_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_optional_list_of_floats_method_req = connection
            .subscribe(
                format!("testable/{}/method/callOptionalListOfFloats", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_list_of_floats_method_req =
            subscription_id_call_optional_list_of_floats_method_req.unwrap_or(u32::MAX);

        let subscription_id_call_two_lists_method_req = connection
            .subscribe(
                format!("testable/{}/method/callTwoLists", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_two_lists_method_req =
            subscription_id_call_two_lists_method_req.unwrap_or(u32::MAX);

        let subscription_id_read_write_integer_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteInteger/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_integer_property_update =
            subscription_id_read_write_integer_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_optional_integer_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteOptionalInteger/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_integer_property_update =
            subscription_id_read_write_optional_integer_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_two_integers_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteTwoIntegers/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_integers_property_update =
            subscription_id_read_write_two_integers_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_string_property_update = connection
            .subscribe(
                format!("testable/{}/property/readWriteString/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_string_property_update =
            subscription_id_read_write_string_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_optional_string_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteOptionalString/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_string_property_update =
            subscription_id_read_write_optional_string_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_two_strings_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteTwoStrings/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_strings_property_update =
            subscription_id_read_write_two_strings_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_struct_property_update = connection
            .subscribe(
                format!("testable/{}/property/readWriteStruct/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_struct_property_update =
            subscription_id_read_write_struct_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_optional_struct_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteOptionalStruct/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_struct_property_update =
            subscription_id_read_write_optional_struct_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_two_structs_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteTwoStructs/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_structs_property_update =
            subscription_id_read_write_two_structs_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_enum_property_update = connection
            .subscribe(
                format!("testable/{}/property/readWriteEnum/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_enum_property_update =
            subscription_id_read_write_enum_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_optional_enum_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteOptionalEnum/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_enum_property_update =
            subscription_id_read_write_optional_enum_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_two_enums_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteTwoEnums/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_enums_property_update =
            subscription_id_read_write_two_enums_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_datetime_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteDatetime/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_datetime_property_update =
            subscription_id_read_write_datetime_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_optional_datetime_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteOptionalDatetime/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_datetime_property_update =
            subscription_id_read_write_optional_datetime_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_two_datetimes_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteTwoDatetimes/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_datetimes_property_update =
            subscription_id_read_write_two_datetimes_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_duration_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteDuration/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_duration_property_update =
            subscription_id_read_write_duration_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_optional_duration_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteOptionalDuration/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_duration_property_update =
            subscription_id_read_write_optional_duration_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_two_durations_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteTwoDurations/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_durations_property_update =
            subscription_id_read_write_two_durations_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_binary_property_update = connection
            .subscribe(
                format!("testable/{}/property/readWriteBinary/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_binary_property_update =
            subscription_id_read_write_binary_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_optional_binary_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteOptionalBinary/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_binary_property_update =
            subscription_id_read_write_optional_binary_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_two_binaries_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteTwoBinaries/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_binaries_property_update =
            subscription_id_read_write_two_binaries_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_list_of_strings_property_update = connection
            .subscribe(
                format!(
                    "testable/{}/property/readWriteListOfStrings/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_list_of_strings_property_update =
            subscription_id_read_write_list_of_strings_property_update.unwrap_or(u32::MAX);

        let subscription_id_read_write_lists_property_update = connection
            .subscribe(
                format!("testable/{}/property/readWriteLists/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_lists_property_update =
            subscription_id_read_write_lists_property_update.unwrap_or(u32::MAX);

        // Create structure for subscription ids.
        let sub_ids = TestableServerSubscriptionIds {
            call_with_nothing_method_req: subscription_id_call_with_nothing_method_req,
            call_one_integer_method_req: subscription_id_call_one_integer_method_req,
            call_optional_integer_method_req: subscription_id_call_optional_integer_method_req,
            call_three_integers_method_req: subscription_id_call_three_integers_method_req,
            call_one_string_method_req: subscription_id_call_one_string_method_req,
            call_optional_string_method_req: subscription_id_call_optional_string_method_req,
            call_three_strings_method_req: subscription_id_call_three_strings_method_req,
            call_one_enum_method_req: subscription_id_call_one_enum_method_req,
            call_optional_enum_method_req: subscription_id_call_optional_enum_method_req,
            call_three_enums_method_req: subscription_id_call_three_enums_method_req,
            call_one_struct_method_req: subscription_id_call_one_struct_method_req,
            call_optional_struct_method_req: subscription_id_call_optional_struct_method_req,
            call_three_structs_method_req: subscription_id_call_three_structs_method_req,
            call_one_date_time_method_req: subscription_id_call_one_date_time_method_req,
            call_optional_date_time_method_req: subscription_id_call_optional_date_time_method_req,
            call_three_date_times_method_req: subscription_id_call_three_date_times_method_req,
            call_one_duration_method_req: subscription_id_call_one_duration_method_req,
            call_optional_duration_method_req: subscription_id_call_optional_duration_method_req,
            call_three_durations_method_req: subscription_id_call_three_durations_method_req,
            call_one_binary_method_req: subscription_id_call_one_binary_method_req,
            call_optional_binary_method_req: subscription_id_call_optional_binary_method_req,
            call_three_binaries_method_req: subscription_id_call_three_binaries_method_req,
            call_one_list_of_integers_method_req:
                subscription_id_call_one_list_of_integers_method_req,
            call_optional_list_of_floats_method_req:
                subscription_id_call_optional_list_of_floats_method_req,
            call_two_lists_method_req: subscription_id_call_two_lists_method_req,

            read_write_integer_property_update: subscription_id_read_write_integer_property_update,
            read_write_optional_integer_property_update:
                subscription_id_read_write_optional_integer_property_update,
            read_write_two_integers_property_update:
                subscription_id_read_write_two_integers_property_update,
            read_write_string_property_update: subscription_id_read_write_string_property_update,
            read_write_optional_string_property_update:
                subscription_id_read_write_optional_string_property_update,
            read_write_two_strings_property_update:
                subscription_id_read_write_two_strings_property_update,
            read_write_struct_property_update: subscription_id_read_write_struct_property_update,
            read_write_optional_struct_property_update:
                subscription_id_read_write_optional_struct_property_update,
            read_write_two_structs_property_update:
                subscription_id_read_write_two_structs_property_update,
            read_write_enum_property_update: subscription_id_read_write_enum_property_update,
            read_write_optional_enum_property_update:
                subscription_id_read_write_optional_enum_property_update,
            read_write_two_enums_property_update:
                subscription_id_read_write_two_enums_property_update,
            read_write_datetime_property_update:
                subscription_id_read_write_datetime_property_update,
            read_write_optional_datetime_property_update:
                subscription_id_read_write_optional_datetime_property_update,
            read_write_two_datetimes_property_update:
                subscription_id_read_write_two_datetimes_property_update,
            read_write_duration_property_update:
                subscription_id_read_write_duration_property_update,
            read_write_optional_duration_property_update:
                subscription_id_read_write_optional_duration_property_update,
            read_write_two_durations_property_update:
                subscription_id_read_write_two_durations_property_update,
            read_write_binary_property_update: subscription_id_read_write_binary_property_update,
            read_write_optional_binary_property_update:
                subscription_id_read_write_optional_binary_property_update,
            read_write_two_binaries_property_update:
                subscription_id_read_write_two_binaries_property_update,
            read_write_list_of_strings_property_update:
                subscription_id_read_write_list_of_strings_property_update,
            read_write_lists_property_update: subscription_id_read_write_lists_property_update,
        };

        let property_values = TestableProperties {
            read_write_integer: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_integer.clone(),
            )),
            read_write_integer_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_integer_version,
            )),

            read_only_integer: Arc::new(RwLockWatch::new(
                initial_property_values.read_only_integer.clone(),
            )),
            read_only_integer_version: Arc::new(AtomicU32::new(
                initial_property_values.read_only_integer_version,
            )),

            read_write_optional_integer: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_optional_integer.clone(),
            )),
            read_write_optional_integer_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_optional_integer_version,
            )),
            read_write_two_integers: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_two_integers.clone(),
            )),
            read_write_two_integers_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_two_integers_version,
            )),

            read_only_string: Arc::new(RwLockWatch::new(
                initial_property_values.read_only_string.clone(),
            )),
            read_only_string_version: Arc::new(AtomicU32::new(
                initial_property_values.read_only_string_version,
            )),

            read_write_string: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_string.clone(),
            )),
            read_write_string_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_string_version,
            )),

            read_write_optional_string: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_optional_string.clone(),
            )),
            read_write_optional_string_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_optional_string_version,
            )),
            read_write_two_strings: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_two_strings.clone(),
            )),
            read_write_two_strings_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_two_strings_version,
            )),

            read_write_struct: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_struct.clone(),
            )),
            read_write_struct_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_struct_version,
            )),

            read_write_optional_struct: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_optional_struct.clone(),
            )),
            read_write_optional_struct_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_optional_struct_version,
            )),
            read_write_two_structs: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_two_structs.clone(),
            )),
            read_write_two_structs_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_two_structs_version,
            )),

            read_only_enum: Arc::new(RwLockWatch::new(
                initial_property_values.read_only_enum.clone(),
            )),
            read_only_enum_version: Arc::new(AtomicU32::new(
                initial_property_values.read_only_enum_version,
            )),

            read_write_enum: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_enum.clone(),
            )),
            read_write_enum_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_enum_version,
            )),

            read_write_optional_enum: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_optional_enum.clone(),
            )),
            read_write_optional_enum_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_optional_enum_version,
            )),
            read_write_two_enums: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_two_enums.clone(),
            )),
            read_write_two_enums_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_two_enums_version,
            )),

            read_write_datetime: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_datetime.clone(),
            )),
            read_write_datetime_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_datetime_version,
            )),

            read_write_optional_datetime: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_optional_datetime.clone(),
            )),
            read_write_optional_datetime_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_optional_datetime_version,
            )),
            read_write_two_datetimes: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_two_datetimes.clone(),
            )),
            read_write_two_datetimes_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_two_datetimes_version,
            )),

            read_write_duration: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_duration.clone(),
            )),
            read_write_duration_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_duration_version,
            )),

            read_write_optional_duration: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_optional_duration.clone(),
            )),
            read_write_optional_duration_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_optional_duration_version,
            )),
            read_write_two_durations: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_two_durations.clone(),
            )),
            read_write_two_durations_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_two_durations_version,
            )),

            read_write_binary: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_binary.clone(),
            )),
            read_write_binary_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_binary_version,
            )),

            read_write_optional_binary: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_optional_binary.clone(),
            )),
            read_write_optional_binary_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_optional_binary_version,
            )),
            read_write_two_binaries: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_two_binaries.clone(),
            )),
            read_write_two_binaries_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_two_binaries_version,
            )),

            read_write_list_of_strings: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_list_of_strings.clone(),
            )),
            read_write_list_of_strings_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_list_of_strings_version,
            )),
            read_write_lists: Arc::new(RwLockWatch::new(
                initial_property_values.read_write_lists.clone(),
            )),
            read_write_lists_version: Arc::new(AtomicU32::new(
                initial_property_values.read_write_lists_version,
            )),
        };

        // Publish the initial property values for all the properties.
        #[cfg(feature = "metrics")]
        let start_prop_publish_time = std::time::Instant::now();
        {
            let topic = format!("testable/{}/property/readWriteInteger/value", instance_id);

            let payload_obj = ReadWriteIntegerProperty {
                value: initial_property_values.read_write_integer,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_integer_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readOnlyInteger/value", instance_id);

            let payload_obj = ReadOnlyIntegerProperty {
                value: initial_property_values.read_only_integer,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_only_integer_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteOptionalInteger/value",
                instance_id
            );

            let payload_obj = ReadWriteOptionalIntegerProperty {
                value: initial_property_values.read_write_optional_integer,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_optional_integer_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteTwoIntegers/value",
                instance_id
            );
            let msg = message::property_value(
                &topic,
                &initial_property_values.read_write_two_integers,
                initial_property_values.read_write_two_integers_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readOnlyString/value", instance_id);

            let payload_obj = ReadOnlyStringProperty {
                value: initial_property_values.read_only_string,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_only_string_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readWriteString/value", instance_id);

            let payload_obj = ReadWriteStringProperty {
                value: initial_property_values.read_write_string,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_string_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteOptionalString/value",
                instance_id
            );

            let payload_obj = ReadWriteOptionalStringProperty {
                value: initial_property_values.read_write_optional_string,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_optional_string_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteTwoStrings/value",
                instance_id
            );
            let msg = message::property_value(
                &topic,
                &initial_property_values.read_write_two_strings,
                initial_property_values.read_write_two_strings_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readWriteStruct/value", instance_id);

            let payload_obj = ReadWriteStructProperty {
                value: initial_property_values.read_write_struct,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_struct_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteOptionalStruct/value",
                instance_id
            );

            let payload_obj = ReadWriteOptionalStructProperty {
                value: initial_property_values.read_write_optional_struct,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_optional_struct_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteTwoStructs/value",
                instance_id
            );
            let msg = message::property_value(
                &topic,
                &initial_property_values.read_write_two_structs,
                initial_property_values.read_write_two_structs_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readOnlyEnum/value", instance_id);

            let payload_obj = ReadOnlyEnumProperty {
                value: initial_property_values.read_only_enum,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_only_enum_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readWriteEnum/value", instance_id);

            let payload_obj = ReadWriteEnumProperty {
                value: initial_property_values.read_write_enum,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_enum_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteOptionalEnum/value",
                instance_id
            );

            let payload_obj = ReadWriteOptionalEnumProperty {
                value: initial_property_values.read_write_optional_enum,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_optional_enum_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readWriteTwoEnums/value", instance_id);
            let msg = message::property_value(
                &topic,
                &initial_property_values.read_write_two_enums,
                initial_property_values.read_write_two_enums_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readWriteDatetime/value", instance_id);

            let payload_obj = ReadWriteDatetimeProperty {
                value: initial_property_values.read_write_datetime,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_datetime_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteOptionalDatetime/value",
                instance_id
            );

            let payload_obj = ReadWriteOptionalDatetimeProperty {
                value: initial_property_values.read_write_optional_datetime,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_optional_datetime_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteTwoDatetimes/value",
                instance_id
            );
            let msg = message::property_value(
                &topic,
                &initial_property_values.read_write_two_datetimes,
                initial_property_values.read_write_two_datetimes_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readWriteDuration/value", instance_id);

            let payload_obj = ReadWriteDurationProperty {
                value: initial_property_values.read_write_duration,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_duration_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteOptionalDuration/value",
                instance_id
            );

            let payload_obj = ReadWriteOptionalDurationProperty {
                value: initial_property_values.read_write_optional_duration,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_optional_duration_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteTwoDurations/value",
                instance_id
            );
            let msg = message::property_value(
                &topic,
                &initial_property_values.read_write_two_durations,
                initial_property_values.read_write_two_durations_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readWriteBinary/value", instance_id);

            let payload_obj = ReadWriteBinaryProperty {
                value: initial_property_values.read_write_binary,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_binary_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteOptionalBinary/value",
                instance_id
            );

            let payload_obj = ReadWriteOptionalBinaryProperty {
                value: initial_property_values.read_write_optional_binary,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_optional_binary_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteTwoBinaries/value",
                instance_id
            );
            let msg = message::property_value(
                &topic,
                &initial_property_values.read_write_two_binaries,
                initial_property_values.read_write_two_binaries_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!(
                "testable/{}/property/readWriteListOfStrings/value",
                instance_id
            );

            let payload_obj = ReadWriteListOfStringsProperty {
                value: initial_property_values.read_write_list_of_strings,
            };
            let msg = message::property_value(
                &topic,
                &payload_obj,
                initial_property_values.read_write_list_of_strings_version,
            )
            .unwrap();

            let _ = connection.publish_nowait(msg);
        }

        {
            let topic = format!("testable/{}/property/readWriteLists/value", instance_id);
            let msg = message::property_value(
                &topic,
                &initial_property_values.read_write_lists,
                initial_property_values.read_write_lists_version,
            )
            .unwrap();
            let _ = connection.publish_nowait(msg);
        }

        #[cfg(feature = "metrics")]
        {
            metrics.initial_property_publish_time = start_prop_publish_time.elapsed();
            debug!(
                "Published 26 initial property values in {:?}",
                metrics.initial_property_publish_time
            );
        }

        TestableServer {
            mqtt_client: connection.clone(),

            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,
            method_handlers,
            properties: property_values,
            subscription_ids: sub_ids,

            client_id: connection.get_client_id(),
            instance_id,
            #[cfg(feature = "metrics")]
            metrics: Arc::new(AsyncMutex::new(metrics)),
        }
    }

    #[cfg(feature = "metrics")]
    pub fn get_metrics(&self) -> Arc<AsyncMutex<TestableServerMetrics>> {
        self.metrics.clone()
    }

    /// Converts a oneshot channel receiver into a future.
    async fn oneshot_to_future(
        ch: oneshot::Receiver<Result<MqttPublishSuccess, Mqtt5PubSubError>>,
    ) -> SentMessageFuture {
        Box::pin(async move {
            let chan_result = ch.await;
            match chan_result {
                Ok(transferred_result) => match transferred_result {
                    Ok(MqttPublishSuccess::Acknowledged) => Ok(()),
                    Ok(MqttPublishSuccess::Completed) => Ok(()),
                    Ok(MqttPublishSuccess::Sent) => Ok(()),
                    Ok(MqttPublishSuccess::Queued) => Ok(()),
                    Err(e) => Err(MethodReturnCode::TransportError(format!(
                        "MQTT publish error: {:?}",
                        e
                    ))),
                },
                Err(e) => Err(MethodReturnCode::TransportError(format!(
                    "MQTT publish oneshot receive error: {:?}",
                    e
                ))),
            }
        })
    }

    async fn wrap_return_code_in_future(rc: MethodReturnCode) -> SentMessageFuture {
        Box::pin(async move {
            match rc {
                MethodReturnCode::Success(_) => Ok(()),
                _ => Err(rc),
            }
        })
    }

    /// Publishes an error response to the given response topic with the given correlation data.
    async fn publish_error_response(
        mut publisher: C,
        response_topic: Option<String>,
        correlation_data: Option<Bytes>,
        err: MethodReturnCode,
    ) {
        if let Some(resp_topic) = response_topic {
            let msg = message::error_response(&resp_topic, correlation_data, err).unwrap();
            let _ = publisher.publish(msg).await;
        } else {
            info!("No response topic found in message properties; cannot send error response.");
        }
    }
    /// Emits the empty signal with the given arguments.
    pub async fn emit_empty(&mut self) -> SentMessageFuture {
        let data = EmptySignalPayload {};
        let topic = format!("testable/{}/signal/empty", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the empty signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_empty_nowait(
        &mut self,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = EmptySignalPayload {};
        let topic = format!("testable/{}/signal/empty", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleInt signal with the given arguments.
    pub async fn emit_single_int(&mut self, value: i32) -> SentMessageFuture {
        let data = SingleIntSignalPayload { value };
        let topic = format!("testable/{}/signal/singleInt", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleInt signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_int_nowait(
        &mut self,
        value: i32,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleIntSignalPayload { value };
        let topic = format!("testable/{}/signal/singleInt", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalInt signal with the given arguments.
    pub async fn emit_single_optional_int(&mut self, value: Option<i32>) -> SentMessageFuture {
        let data = SingleOptionalIntSignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalInt", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleOptionalInt signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_optional_int_nowait(
        &mut self,
        value: Option<i32>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleOptionalIntSignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalInt", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the threeIntegers signal with the given arguments.
    pub async fn emit_three_integers(
        &mut self,
        first: i32,
        second: i32,
        third: Option<i32>,
    ) -> SentMessageFuture {
        let data = ThreeIntegersSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeIntegers", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the threeIntegers signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_three_integers_nowait(
        &mut self,
        first: i32,
        second: i32,
        third: Option<i32>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = ThreeIntegersSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeIntegers", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleString signal with the given arguments.
    pub async fn emit_single_string(&mut self, value: String) -> SentMessageFuture {
        let data = SingleStringSignalPayload { value };
        let topic = format!("testable/{}/signal/singleString", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleString signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_string_nowait(
        &mut self,
        value: String,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleStringSignalPayload { value };
        let topic = format!("testable/{}/signal/singleString", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalString signal with the given arguments.
    pub async fn emit_single_optional_string(
        &mut self,
        value: Option<String>,
    ) -> SentMessageFuture {
        let data = SingleOptionalStringSignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalString", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleOptionalString signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_optional_string_nowait(
        &mut self,
        value: Option<String>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleOptionalStringSignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalString", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the threeStrings signal with the given arguments.
    pub async fn emit_three_strings(
        &mut self,
        first: String,
        second: String,
        third: Option<String>,
    ) -> SentMessageFuture {
        let data = ThreeStringsSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeStrings", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the threeStrings signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_three_strings_nowait(
        &mut self,
        first: String,
        second: String,
        third: Option<String>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = ThreeStringsSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeStrings", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleEnum signal with the given arguments.
    pub async fn emit_single_enum(&mut self, value: Numbers) -> SentMessageFuture {
        let data = SingleEnumSignalPayload { value };
        let topic = format!("testable/{}/signal/singleEnum", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleEnum signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_enum_nowait(
        &mut self,
        value: Numbers,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleEnumSignalPayload { value };
        let topic = format!("testable/{}/signal/singleEnum", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalEnum signal with the given arguments.
    pub async fn emit_single_optional_enum(&mut self, value: Option<Numbers>) -> SentMessageFuture {
        let data = SingleOptionalEnumSignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalEnum", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleOptionalEnum signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_optional_enum_nowait(
        &mut self,
        value: Option<Numbers>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleOptionalEnumSignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalEnum", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the threeEnums signal with the given arguments.
    pub async fn emit_three_enums(
        &mut self,
        first: Numbers,
        second: Numbers,
        third: Option<Numbers>,
    ) -> SentMessageFuture {
        let data = ThreeEnumsSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeEnums", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the threeEnums signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_three_enums_nowait(
        &mut self,
        first: Numbers,
        second: Numbers,
        third: Option<Numbers>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = ThreeEnumsSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeEnums", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleStruct signal with the given arguments.
    pub async fn emit_single_struct(&mut self, value: AllTypes) -> SentMessageFuture {
        let data = SingleStructSignalPayload { value };
        let topic = format!("testable/{}/signal/singleStruct", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleStruct signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_struct_nowait(
        &mut self,
        value: AllTypes,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleStructSignalPayload { value };
        let topic = format!("testable/{}/signal/singleStruct", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalStruct signal with the given arguments.
    pub async fn emit_single_optional_struct(
        &mut self,
        value: Option<AllTypes>,
    ) -> SentMessageFuture {
        let data = SingleOptionalStructSignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalStruct", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleOptionalStruct signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_optional_struct_nowait(
        &mut self,
        value: Option<AllTypes>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleOptionalStructSignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalStruct", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the threeStructs signal with the given arguments.
    pub async fn emit_three_structs(
        &mut self,
        first: AllTypes,
        second: AllTypes,
        third: Option<AllTypes>,
    ) -> SentMessageFuture {
        let data = ThreeStructsSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeStructs", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the threeStructs signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_three_structs_nowait(
        &mut self,
        first: AllTypes,
        second: AllTypes,
        third: Option<AllTypes>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = ThreeStructsSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeStructs", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleDateTime signal with the given arguments.
    pub async fn emit_single_date_time(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> SentMessageFuture {
        let data = SingleDateTimeSignalPayload { value };
        let topic = format!("testable/{}/signal/singleDateTime", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleDateTime signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_date_time_nowait(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleDateTimeSignalPayload { value };
        let topic = format!("testable/{}/signal/singleDateTime", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalDatetime signal with the given arguments.
    pub async fn emit_single_optional_datetime(
        &mut self,
        value: Option<chrono::DateTime<chrono::Utc>>,
    ) -> SentMessageFuture {
        let data = SingleOptionalDatetimeSignalPayload { value };
        let topic = format!(
            "testable/{}/signal/singleOptionalDatetime",
            self.instance_id
        );
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleOptionalDatetime signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_optional_datetime_nowait(
        &mut self,
        value: Option<chrono::DateTime<chrono::Utc>>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleOptionalDatetimeSignalPayload { value };
        let topic = format!(
            "testable/{}/signal/singleOptionalDatetime",
            self.instance_id
        );
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the threeDateTimes signal with the given arguments.
    pub async fn emit_three_date_times(
        &mut self,
        first: chrono::DateTime<chrono::Utc>,
        second: chrono::DateTime<chrono::Utc>,
        third: Option<chrono::DateTime<chrono::Utc>>,
    ) -> SentMessageFuture {
        let data = ThreeDateTimesSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeDateTimes", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the threeDateTimes signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_three_date_times_nowait(
        &mut self,
        first: chrono::DateTime<chrono::Utc>,
        second: chrono::DateTime<chrono::Utc>,
        third: Option<chrono::DateTime<chrono::Utc>>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = ThreeDateTimesSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeDateTimes", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleDuration signal with the given arguments.
    pub async fn emit_single_duration(&mut self, value: chrono::Duration) -> SentMessageFuture {
        let data = SingleDurationSignalPayload { value };
        let topic = format!("testable/{}/signal/singleDuration", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleDuration signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_duration_nowait(
        &mut self,
        value: chrono::Duration,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleDurationSignalPayload { value };
        let topic = format!("testable/{}/signal/singleDuration", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalDuration signal with the given arguments.
    pub async fn emit_single_optional_duration(
        &mut self,
        value: Option<chrono::Duration>,
    ) -> SentMessageFuture {
        let data = SingleOptionalDurationSignalPayload { value };
        let topic = format!(
            "testable/{}/signal/singleOptionalDuration",
            self.instance_id
        );
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleOptionalDuration signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_optional_duration_nowait(
        &mut self,
        value: Option<chrono::Duration>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleOptionalDurationSignalPayload { value };
        let topic = format!(
            "testable/{}/signal/singleOptionalDuration",
            self.instance_id
        );
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the threeDurations signal with the given arguments.
    pub async fn emit_three_durations(
        &mut self,
        first: chrono::Duration,
        second: chrono::Duration,
        third: Option<chrono::Duration>,
    ) -> SentMessageFuture {
        let data = ThreeDurationsSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeDurations", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the threeDurations signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_three_durations_nowait(
        &mut self,
        first: chrono::Duration,
        second: chrono::Duration,
        third: Option<chrono::Duration>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = ThreeDurationsSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeDurations", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleBinary signal with the given arguments.
    pub async fn emit_single_binary(&mut self, value: Vec<u8>) -> SentMessageFuture {
        let data = SingleBinarySignalPayload { value };
        let topic = format!("testable/{}/signal/singleBinary", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleBinary signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_binary_nowait(
        &mut self,
        value: Vec<u8>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleBinarySignalPayload { value };
        let topic = format!("testable/{}/signal/singleBinary", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalBinary signal with the given arguments.
    pub async fn emit_single_optional_binary(
        &mut self,
        value: Option<Vec<u8>>,
    ) -> SentMessageFuture {
        let data = SingleOptionalBinarySignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalBinary", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleOptionalBinary signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_optional_binary_nowait(
        &mut self,
        value: Option<Vec<u8>>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleOptionalBinarySignalPayload { value };
        let topic = format!("testable/{}/signal/singleOptionalBinary", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the threeBinaries signal with the given arguments.
    pub async fn emit_three_binaries(
        &mut self,
        first: Vec<u8>,
        second: Vec<u8>,
        third: Option<Vec<u8>>,
    ) -> SentMessageFuture {
        let data = ThreeBinariesSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeBinaries", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the threeBinaries signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_three_binaries_nowait(
        &mut self,
        first: Vec<u8>,
        second: Vec<u8>,
        third: Option<Vec<u8>>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = ThreeBinariesSignalPayload {
            first,

            second,

            third,
        };
        let topic = format!("testable/{}/signal/threeBinaries", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleArrayOfIntegers signal with the given arguments.
    pub async fn emit_single_array_of_integers(&mut self, values: Vec<i32>) -> SentMessageFuture {
        let data = SingleArrayOfIntegersSignalPayload { values };
        let topic = format!("testable/{}/signal/singleArrayOfIntegers", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleArrayOfIntegers signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_array_of_integers_nowait(
        &mut self,
        values: Vec<i32>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleArrayOfIntegersSignalPayload { values };
        let topic = format!("testable/{}/signal/singleArrayOfIntegers", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalArrayOfStrings signal with the given arguments.
    pub async fn emit_single_optional_array_of_strings(
        &mut self,
        values: Option<Vec<String>>,
    ) -> SentMessageFuture {
        let data = SingleOptionalArrayOfStringsSignalPayload { values };
        let topic = format!(
            "testable/{}/signal/singleOptionalArrayOfStrings",
            self.instance_id
        );
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the singleOptionalArrayOfStrings signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_single_optional_array_of_strings_nowait(
        &mut self,
        values: Option<Vec<String>>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = SingleOptionalArrayOfStringsSignalPayload { values };
        let topic = format!(
            "testable/{}/signal/singleOptionalArrayOfStrings",
            self.instance_id
        );
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the arrayOfEveryType signal with the given arguments.
    pub async fn emit_array_of_every_type(
        &mut self,
        first_of_integers: Vec<i32>,
        second_of_floats: Vec<f32>,
        third_of_strings: Vec<String>,
        fourth_of_enums: Vec<Numbers>,
        fifth_of_structs: Vec<Entry>,
        sixth_of_datetimes: Vec<chrono::DateTime<chrono::Utc>>,
        seventh_of_durations: Vec<chrono::Duration>,
        eighth_of_binaries: Vec<Vec<u8>>,
    ) -> SentMessageFuture {
        let data = ArrayOfEveryTypeSignalPayload {
            first_of_integers,

            second_of_floats,

            third_of_strings,

            fourth_of_enums,

            fifth_of_structs,

            sixth_of_datetimes,

            seventh_of_durations,

            eighth_of_binaries,
        };
        let topic = format!("testable/{}/signal/arrayOfEveryType", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the arrayOfEveryType signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_array_of_every_type_nowait(
        &mut self,
        first_of_integers: Vec<i32>,
        second_of_floats: Vec<f32>,
        third_of_strings: Vec<String>,
        fourth_of_enums: Vec<Numbers>,
        fifth_of_structs: Vec<Entry>,
        sixth_of_datetimes: Vec<chrono::DateTime<chrono::Utc>>,
        seventh_of_durations: Vec<chrono::Duration>,
        eighth_of_binaries: Vec<Vec<u8>>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = ArrayOfEveryTypeSignalPayload {
            first_of_integers,

            second_of_floats,

            third_of_strings,

            fourth_of_enums,

            fifth_of_structs,

            sixth_of_datetimes,

            seventh_of_durations,

            eighth_of_binaries,
        };
        let topic = format!("testable/{}/signal/arrayOfEveryType", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }

    /// Handles a request message for the callWithNothing method.
    async fn handle_call_with_nothing_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;

        // call the method handler
        let rc: Result<(), MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_call_with_nothing().await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(_retval) => {
                    let empty_resp = CallWithNothingReturnValues {};
                    let msg = message::response(&resp_topic, &empty_resp, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callWithNothing: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callWithNothing`.");
        }
    }

    /// Handles a request message for the callOneInteger method.
    async fn handle_call_one_integer_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOneIntegerRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOneInteger: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<i32, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_call_one_integer(payload.input1).await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOneIntegerReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callOneInteger: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOneInteger`.");
        }
    }

    /// Handles a request message for the callOptionalInteger method.
    async fn handle_call_optional_integer_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOptionalIntegerRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOptionalInteger: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Option<i32>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_optional_integer(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOptionalIntegerReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callOptionalInteger: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!(
                "No response topic provided, so no publishing response to `callOptionalInteger`."
            );
        }
    }

    /// Handles a request message for the callThreeIntegers method.
    async fn handle_call_three_integers_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallThreeIntegersRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callThreeIntegers: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<CallThreeIntegersReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_three_integers(payload.input1, payload.input2, payload.input3)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callThreeIntegers: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callThreeIntegers`.");
        }
    }

    /// Handles a request message for the callOneString method.
    async fn handle_call_one_string_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOneStringRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOneString: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<String, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_call_one_string(payload.input1).await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOneStringReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callOneString: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOneString`.");
        }
    }

    /// Handles a request message for the callOptionalString method.
    async fn handle_call_optional_string_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOptionalStringRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOptionalString: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Option<String>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_optional_string(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOptionalStringReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callOptionalString: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOptionalString`.");
        }
    }

    /// Handles a request message for the callThreeStrings method.
    async fn handle_call_three_strings_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallThreeStringsRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callThreeStrings: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<CallThreeStringsReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_three_strings(payload.input1, payload.input2, payload.input3)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callThreeStrings: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callThreeStrings`.");
        }
    }

    /// Handles a request message for the callOneEnum method.
    async fn handle_call_one_enum_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOneEnumRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOneEnum: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Numbers, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_call_one_enum(payload.input1).await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOneEnumReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callOneEnum: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOneEnum`.");
        }
    }

    /// Handles a request message for the callOptionalEnum method.
    async fn handle_call_optional_enum_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOptionalEnumRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOptionalEnum: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Option<Numbers>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_optional_enum(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOptionalEnumReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callOptionalEnum: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOptionalEnum`.");
        }
    }

    /// Handles a request message for the callThreeEnums method.
    async fn handle_call_three_enums_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallThreeEnumsRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callThreeEnums: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<CallThreeEnumsReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_three_enums(payload.input1, payload.input2, payload.input3)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callThreeEnums: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callThreeEnums`.");
        }
    }

    /// Handles a request message for the callOneStruct method.
    async fn handle_call_one_struct_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOneStructRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOneStruct: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<AllTypes, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_call_one_struct(payload.input1).await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOneStructReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callOneStruct: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOneStruct`.");
        }
    }

    /// Handles a request message for the callOptionalStruct method.
    async fn handle_call_optional_struct_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOptionalStructRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOptionalStruct: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Option<AllTypes>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_optional_struct(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOptionalStructReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callOptionalStruct: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOptionalStruct`.");
        }
    }

    /// Handles a request message for the callThreeStructs method.
    async fn handle_call_three_structs_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallThreeStructsRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callThreeStructs: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<CallThreeStructsReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_three_structs(payload.input1, payload.input2, payload.input3)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callThreeStructs: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callThreeStructs`.");
        }
    }

    /// Handles a request message for the callOneDateTime method.
    async fn handle_call_one_date_time_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOneDateTimeRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOneDateTime: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<chrono::DateTime<chrono::Utc>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_one_date_time(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOneDateTimeReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callOneDateTime: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOneDateTime`.");
        }
    }

    /// Handles a request message for the callOptionalDateTime method.
    async fn handle_call_optional_date_time_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOptionalDateTimeRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOptionalDateTime: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Option<chrono::DateTime<chrono::Utc>>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_optional_date_time(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOptionalDateTimeReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callOptionalDateTime: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!(
                "No response topic provided, so no publishing response to `callOptionalDateTime`."
            );
        }
    }

    /// Handles a request message for the callThreeDateTimes method.
    async fn handle_call_three_date_times_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallThreeDateTimesRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callThreeDateTimes: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<CallThreeDateTimesReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_three_date_times(payload.input1, payload.input2, payload.input3)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callThreeDateTimes: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callThreeDateTimes`.");
        }
    }

    /// Handles a request message for the callOneDuration method.
    async fn handle_call_one_duration_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOneDurationRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOneDuration: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<chrono::Duration, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_call_one_duration(payload.input1).await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOneDurationReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callOneDuration: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOneDuration`.");
        }
    }

    /// Handles a request message for the callOptionalDuration method.
    async fn handle_call_optional_duration_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOptionalDurationRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOptionalDuration: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Option<chrono::Duration>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_optional_duration(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOptionalDurationReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callOptionalDuration: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!(
                "No response topic provided, so no publishing response to `callOptionalDuration`."
            );
        }
    }

    /// Handles a request message for the callThreeDurations method.
    async fn handle_call_three_durations_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallThreeDurationsRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callThreeDurations: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<CallThreeDurationsReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_three_durations(payload.input1, payload.input2, payload.input3)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callThreeDurations: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callThreeDurations`.");
        }
    }

    /// Handles a request message for the callOneBinary method.
    async fn handle_call_one_binary_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOneBinaryRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOneBinary: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Vec<u8>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard.handle_call_one_binary(payload.input1).await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOneBinaryReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callOneBinary: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOneBinary`.");
        }
    }

    /// Handles a request message for the callOptionalBinary method.
    async fn handle_call_optional_binary_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallOptionalBinaryRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOptionalBinary: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Option<Vec<u8>>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_optional_binary(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOptionalBinaryReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callOptionalBinary: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOptionalBinary`.");
        }
    }

    /// Handles a request message for the callThreeBinaries method.
    async fn handle_call_three_binaries_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallThreeBinariesRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callThreeBinaries: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<CallThreeBinariesReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_three_binaries(payload.input1, payload.input2, payload.input3)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callThreeBinaries: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callThreeBinaries`.");
        }
    }

    /// Handles a request message for the callOneListOfIntegers method.
    async fn handle_call_one_list_of_integers_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj =
            serde_json::from_slice::<CallOneListOfIntegersRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOneListOfIntegers: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Vec<i32>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_one_list_of_integers(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOneListOfIntegersReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callOneListOfIntegers: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!(
                "No response topic provided, so no publishing response to `callOneListOfIntegers`."
            );
        }
    }

    /// Handles a request message for the callOptionalListOfFloats method.
    async fn handle_call_optional_list_of_floats_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj =
            serde_json::from_slice::<CallOptionalListOfFloatsRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callOptionalListOfFloats: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<Option<Vec<f32>>, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_optional_list_of_floats(payload.input1)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let resp_obj = CallOptionalListOfFloatsReturnValues { output1: retval };
                    let msg = message::response(&resp_topic, &resp_obj, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!(
                        "Error occurred while handling callOptionalListOfFloats: {:?}",
                        &err
                    );
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callOptionalListOfFloats`.");
        }
    }

    /// Handles a request message for the callTwoLists method.
    async fn handle_call_two_lists_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestableMethodHandlers<C>>>>,
        msg: MqttMessage,
    ) {
        let opt_corr_data = msg.correlation_data;
        let opt_resp_topic = msg.response_topic;
        let payload_vec = msg.payload;
        let payload_obj = serde_json::from_slice::<CallTwoListsRequestObject>(&payload_vec);
        if payload_obj.is_err() {
            error!(
                "Error deserializing request payload for callTwoLists: {:?}",
                payload_obj.err()
            );
            TestableServer::<C>::publish_error_response(
                publisher,
                opt_resp_topic,
                opt_corr_data,
                MethodReturnCode::ServerDeserializationError(
                    "Failed to deserialize request payload".to_string(),
                ),
            )
            .await;
            return;
        }
        // Unwrap is OK here because we just checked for error.
        let payload = payload_obj.unwrap();

        // call the method handler
        let rc: Result<CallTwoListsReturnValues, MethodReturnCode> = {
            let handler_guard = handlers.lock().await;
            handler_guard
                .handle_call_two_lists(payload.input1, payload.input2)
                .await
        };

        if let Some(resp_topic) = opt_resp_topic {
            let corr_data = opt_corr_data.unwrap_or_default();
            match rc {
                Ok(retval) => {
                    let msg = message::response(&resp_topic, &retval, corr_data, None).unwrap();
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    info!("Error occurred while handling callTwoLists: {:?}", &err);
                    TestableServer::<C>::publish_error_response(
                        publisher,
                        Some(resp_topic),
                        Some(corr_data),
                        err,
                    )
                    .await;
                }
            }
        } else {
            // Without a response topic, we cannot send a response.
            info!("No response topic provided, so no publishing response to `callTwoLists`.");
        }
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_integer_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<i32>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteIntegerProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_integer' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_integer' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteIntegerProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteIntegerProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_integer': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_integer'.");
        }
    }

    /// Watch for changes to the `read_write_integer` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_integer(&self) -> watch::Receiver<i32> {
        self.properties.read_write_integer.subscribe()
    }

    pub fn get_read_write_integer_handle(&self) -> WriteRequestLockWatch<i32> {
        self.properties.read_write_integer.write_request()
    }

    /// Sets the value of the read_write_integer property.
    pub async fn set_read_write_integer(&mut self, value: i32) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_integer_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// Watch for changes to the `read_only_integer` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_only_integer(&self) -> watch::Receiver<i32> {
        self.properties.read_only_integer.subscribe()
    }

    pub fn get_read_only_integer_handle(&self) -> WriteRequestLockWatch<i32> {
        self.properties.read_only_integer.write_request()
    }

    /// Sets the value of the read_only_integer property.
    pub async fn set_read_only_integer(&mut self, value: i32) -> SentMessageFuture {
        let write_request_lock = self.get_read_only_integer_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_integer_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Option<i32>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteOptionalIntegerProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_optional_integer' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_integer' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteOptionalIntegerProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteOptionalIntegerProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_optional_integer': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_optional_integer'.");
        }
    }

    /// Watch for changes to the `read_write_optional_integer` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_integer(&self) -> watch::Receiver<Option<i32>> {
        self.properties.read_write_optional_integer.subscribe()
    }

    pub fn get_read_write_optional_integer_handle(&self) -> WriteRequestLockWatch<Option<i32>> {
        self.properties.read_write_optional_integer.write_request()
    }

    /// Sets the value of the read_write_optional_integer property.
    pub async fn set_read_write_optional_integer(
        &mut self,
        value: Option<i32>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_optional_integer_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_integers_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<ReadWriteTwoIntegersProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 2 fields.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteTwoIntegersProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_two_integers' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_integers' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_two_integers': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_two_integers'.");
        }
    }

    /// Watch for changes to the `read_write_two_integers` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_integers(&self) -> watch::Receiver<ReadWriteTwoIntegersProperty> {
        self.properties.read_write_two_integers.subscribe()
    }

    pub fn get_read_write_two_integers_handle(
        &self,
    ) -> WriteRequestLockWatch<ReadWriteTwoIntegersProperty> {
        self.properties.read_write_two_integers.write_request()
    }

    /// Sets the values of the read_write_two_integers property.
    pub async fn set_read_write_two_integers(
        &mut self,
        value: ReadWriteTwoIntegersProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_two_integers_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// Watch for changes to the `read_only_string` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_only_string(&self) -> watch::Receiver<String> {
        self.properties.read_only_string.subscribe()
    }

    pub fn get_read_only_string_handle(&self) -> WriteRequestLockWatch<String> {
        self.properties.read_only_string.write_request()
    }

    /// Sets the value of the read_only_string property.
    pub async fn set_read_only_string(&mut self, value: String) -> SentMessageFuture {
        let write_request_lock = self.get_read_only_string_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_string_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<String>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteStringProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_string' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_string' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteStringProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteStringProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_string': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_string'.");
        }
    }

    /// Watch for changes to the `read_write_string` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_string(&self) -> watch::Receiver<String> {
        self.properties.read_write_string.subscribe()
    }

    pub fn get_read_write_string_handle(&self) -> WriteRequestLockWatch<String> {
        self.properties.read_write_string.write_request()
    }

    /// Sets the value of the read_write_string property.
    pub async fn set_read_write_string(&mut self, value: String) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_string_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_string_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Option<String>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteOptionalStringProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_optional_string' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_string' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteOptionalStringProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteOptionalStringProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_optional_string': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_optional_string'.");
        }
    }

    /// Watch for changes to the `read_write_optional_string` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_string(&self) -> watch::Receiver<Option<String>> {
        self.properties.read_write_optional_string.subscribe()
    }

    pub fn get_read_write_optional_string_handle(&self) -> WriteRequestLockWatch<Option<String>> {
        self.properties.read_write_optional_string.write_request()
    }

    /// Sets the value of the read_write_optional_string property.
    pub async fn set_read_write_optional_string(
        &mut self,
        value: Option<String>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_optional_string_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_strings_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<ReadWriteTwoStringsProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 2 fields.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteTwoStringsProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_two_strings' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_strings' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_two_strings': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_two_strings'.");
        }
    }

    /// Watch for changes to the `read_write_two_strings` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_strings(&self) -> watch::Receiver<ReadWriteTwoStringsProperty> {
        self.properties.read_write_two_strings.subscribe()
    }

    pub fn get_read_write_two_strings_handle(
        &self,
    ) -> WriteRequestLockWatch<ReadWriteTwoStringsProperty> {
        self.properties.read_write_two_strings.write_request()
    }

    /// Sets the values of the read_write_two_strings property.
    pub async fn set_read_write_two_strings(
        &mut self,
        value: ReadWriteTwoStringsProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_two_strings_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_struct_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<AllTypes>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteStructProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_struct' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_struct' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteStructProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteStructProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_struct': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_struct'.");
        }
    }

    /// Watch for changes to the `read_write_struct` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_struct(&self) -> watch::Receiver<AllTypes> {
        self.properties.read_write_struct.subscribe()
    }

    pub fn get_read_write_struct_handle(&self) -> WriteRequestLockWatch<AllTypes> {
        self.properties.read_write_struct.write_request()
    }

    /// Sets the value of the read_write_struct property.
    pub async fn set_read_write_struct(&mut self, value: AllTypes) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_struct_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_struct_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Option<AllTypes>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteOptionalStructProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_optional_struct' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_struct' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteOptionalStructProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteOptionalStructProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_optional_struct': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_optional_struct'.");
        }
    }

    /// Watch for changes to the `read_write_optional_struct` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_struct(&self) -> watch::Receiver<Option<AllTypes>> {
        self.properties.read_write_optional_struct.subscribe()
    }

    pub fn get_read_write_optional_struct_handle(&self) -> WriteRequestLockWatch<Option<AllTypes>> {
        self.properties.read_write_optional_struct.write_request()
    }

    /// Sets the value of the read_write_optional_struct property.
    pub async fn set_read_write_optional_struct(
        &mut self,
        value: Option<AllTypes>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_optional_struct_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_structs_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<ReadWriteTwoStructsProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 2 fields.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteTwoStructsProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_two_structs' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_structs' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_two_structs': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_two_structs'.");
        }
    }

    /// Watch for changes to the `read_write_two_structs` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_structs(&self) -> watch::Receiver<ReadWriteTwoStructsProperty> {
        self.properties.read_write_two_structs.subscribe()
    }

    pub fn get_read_write_two_structs_handle(
        &self,
    ) -> WriteRequestLockWatch<ReadWriteTwoStructsProperty> {
        self.properties.read_write_two_structs.write_request()
    }

    /// Sets the values of the read_write_two_structs property.
    pub async fn set_read_write_two_structs(
        &mut self,
        value: ReadWriteTwoStructsProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_two_structs_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// Watch for changes to the `read_only_enum` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_only_enum(&self) -> watch::Receiver<Numbers> {
        self.properties.read_only_enum.subscribe()
    }

    pub fn get_read_only_enum_handle(&self) -> WriteRequestLockWatch<Numbers> {
        self.properties.read_only_enum.write_request()
    }

    /// Sets the value of the read_only_enum property.
    pub async fn set_read_only_enum(&mut self, value: Numbers) -> SentMessageFuture {
        let write_request_lock = self.get_read_only_enum_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_enum_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Numbers>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteEnumProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_enum' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_enum' payload".to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteEnumProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteEnumProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!(
                        "Error occurred while handling property update for 'read_write_enum': {:?}",
                        &err
                    );
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_enum'.");
        }
    }

    /// Watch for changes to the `read_write_enum` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_enum(&self) -> watch::Receiver<Numbers> {
        self.properties.read_write_enum.subscribe()
    }

    pub fn get_read_write_enum_handle(&self) -> WriteRequestLockWatch<Numbers> {
        self.properties.read_write_enum.write_request()
    }

    /// Sets the value of the read_write_enum property.
    pub async fn set_read_write_enum(&mut self, value: Numbers) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_enum_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_enum_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Option<Numbers>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteOptionalEnumProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_optional_enum' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_enum' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteOptionalEnumProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteOptionalEnumProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_optional_enum': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_optional_enum'.");
        }
    }

    /// Watch for changes to the `read_write_optional_enum` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_enum(&self) -> watch::Receiver<Option<Numbers>> {
        self.properties.read_write_optional_enum.subscribe()
    }

    pub fn get_read_write_optional_enum_handle(&self) -> WriteRequestLockWatch<Option<Numbers>> {
        self.properties.read_write_optional_enum.write_request()
    }

    /// Sets the value of the read_write_optional_enum property.
    pub async fn set_read_write_optional_enum(
        &mut self,
        value: Option<Numbers>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_optional_enum_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_enums_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<ReadWriteTwoEnumsProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 2 fields.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteTwoEnumsProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_two_enums' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_enums' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_two_enums': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_two_enums'.");
        }
    }

    /// Watch for changes to the `read_write_two_enums` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_enums(&self) -> watch::Receiver<ReadWriteTwoEnumsProperty> {
        self.properties.read_write_two_enums.subscribe()
    }

    pub fn get_read_write_two_enums_handle(
        &self,
    ) -> WriteRequestLockWatch<ReadWriteTwoEnumsProperty> {
        self.properties.read_write_two_enums.write_request()
    }

    /// Sets the values of the read_write_two_enums property.
    pub async fn set_read_write_two_enums(
        &mut self,
        value: ReadWriteTwoEnumsProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_two_enums_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_datetime_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<chrono::DateTime<chrono::Utc>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteDatetimeProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_datetime' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_datetime' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteDatetimeProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteDatetimeProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_datetime': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_datetime'.");
        }
    }

    /// Watch for changes to the `read_write_datetime` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_datetime(&self) -> watch::Receiver<chrono::DateTime<chrono::Utc>> {
        self.properties.read_write_datetime.subscribe()
    }

    pub fn get_read_write_datetime_handle(
        &self,
    ) -> WriteRequestLockWatch<chrono::DateTime<chrono::Utc>> {
        self.properties.read_write_datetime.write_request()
    }

    /// Sets the value of the read_write_datetime property.
    pub async fn set_read_write_datetime(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_datetime_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_datetime_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Option<chrono::DateTime<chrono::Utc>>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteOptionalDatetimeProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_optional_datetime' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_datetime' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteOptionalDatetimeProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteOptionalDatetimeProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_optional_datetime': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_optional_datetime'.");
        }
    }

    /// Watch for changes to the `read_write_optional_datetime` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_datetime(
        &self,
    ) -> watch::Receiver<Option<chrono::DateTime<chrono::Utc>>> {
        self.properties.read_write_optional_datetime.subscribe()
    }

    pub fn get_read_write_optional_datetime_handle(
        &self,
    ) -> WriteRequestLockWatch<Option<chrono::DateTime<chrono::Utc>>> {
        self.properties.read_write_optional_datetime.write_request()
    }

    /// Sets the value of the read_write_optional_datetime property.
    pub async fn set_read_write_optional_datetime(
        &mut self,
        value: Option<chrono::DateTime<chrono::Utc>>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_optional_datetime_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_datetimes_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<ReadWriteTwoDatetimesProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 2 fields.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteTwoDatetimesProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_two_datetimes' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_datetimes' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_two_datetimes': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_two_datetimes'.");
        }
    }

    /// Watch for changes to the `read_write_two_datetimes` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_datetimes(&self) -> watch::Receiver<ReadWriteTwoDatetimesProperty> {
        self.properties.read_write_two_datetimes.subscribe()
    }

    pub fn get_read_write_two_datetimes_handle(
        &self,
    ) -> WriteRequestLockWatch<ReadWriteTwoDatetimesProperty> {
        self.properties.read_write_two_datetimes.write_request()
    }

    /// Sets the values of the read_write_two_datetimes property.
    pub async fn set_read_write_two_datetimes(
        &mut self,
        value: ReadWriteTwoDatetimesProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_two_datetimes_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_duration_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<chrono::Duration>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteDurationProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_duration' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_duration' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteDurationProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteDurationProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_duration': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_duration'.");
        }
    }

    /// Watch for changes to the `read_write_duration` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_duration(&self) -> watch::Receiver<chrono::Duration> {
        self.properties.read_write_duration.subscribe()
    }

    pub fn get_read_write_duration_handle(&self) -> WriteRequestLockWatch<chrono::Duration> {
        self.properties.read_write_duration.write_request()
    }

    /// Sets the value of the read_write_duration property.
    pub async fn set_read_write_duration(&mut self, value: chrono::Duration) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_duration_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_duration_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Option<chrono::Duration>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteOptionalDurationProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_optional_duration' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_duration' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteOptionalDurationProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteOptionalDurationProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_optional_duration': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_optional_duration'.");
        }
    }

    /// Watch for changes to the `read_write_optional_duration` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_duration(&self) -> watch::Receiver<Option<chrono::Duration>> {
        self.properties.read_write_optional_duration.subscribe()
    }

    pub fn get_read_write_optional_duration_handle(
        &self,
    ) -> WriteRequestLockWatch<Option<chrono::Duration>> {
        self.properties.read_write_optional_duration.write_request()
    }

    /// Sets the value of the read_write_optional_duration property.
    pub async fn set_read_write_optional_duration(
        &mut self,
        value: Option<chrono::Duration>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_optional_duration_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_durations_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<ReadWriteTwoDurationsProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 2 fields.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteTwoDurationsProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_two_durations' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_durations' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_two_durations': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_two_durations'.");
        }
    }

    /// Watch for changes to the `read_write_two_durations` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_durations(&self) -> watch::Receiver<ReadWriteTwoDurationsProperty> {
        self.properties.read_write_two_durations.subscribe()
    }

    pub fn get_read_write_two_durations_handle(
        &self,
    ) -> WriteRequestLockWatch<ReadWriteTwoDurationsProperty> {
        self.properties.read_write_two_durations.write_request()
    }

    /// Sets the values of the read_write_two_durations property.
    pub async fn set_read_write_two_durations(
        &mut self,
        value: ReadWriteTwoDurationsProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_two_durations_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_binary_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Vec<u8>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteBinaryProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_binary' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_binary' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteBinaryProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteBinaryProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_binary': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_binary'.");
        }
    }

    /// Watch for changes to the `read_write_binary` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_binary(&self) -> watch::Receiver<Vec<u8>> {
        self.properties.read_write_binary.subscribe()
    }

    pub fn get_read_write_binary_handle(&self) -> WriteRequestLockWatch<Vec<u8>> {
        self.properties.read_write_binary.write_request()
    }

    /// Sets the value of the read_write_binary property.
    pub async fn set_read_write_binary(&mut self, value: Vec<u8>) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_binary_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_binary_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Option<Vec<u8>>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteOptionalBinaryProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_optional_binary' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_binary' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteOptionalBinaryProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteOptionalBinaryProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_optional_binary': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_optional_binary'.");
        }
    }

    /// Watch for changes to the `read_write_optional_binary` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_optional_binary(&self) -> watch::Receiver<Option<Vec<u8>>> {
        self.properties.read_write_optional_binary.subscribe()
    }

    pub fn get_read_write_optional_binary_handle(&self) -> WriteRequestLockWatch<Option<Vec<u8>>> {
        self.properties.read_write_optional_binary.write_request()
    }

    /// Sets the value of the read_write_optional_binary property.
    pub async fn set_read_write_optional_binary(
        &mut self,
        value: Option<Vec<u8>>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_optional_binary_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_binaries_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<ReadWriteTwoBinariesProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 2 fields.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteTwoBinariesProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_two_binaries' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_binaries' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_two_binaries': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_two_binaries'.");
        }
    }

    /// Watch for changes to the `read_write_two_binaries` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_two_binaries(&self) -> watch::Receiver<ReadWriteTwoBinariesProperty> {
        self.properties.read_write_two_binaries.subscribe()
    }

    pub fn get_read_write_two_binaries_handle(
        &self,
    ) -> WriteRequestLockWatch<ReadWriteTwoBinariesProperty> {
        self.properties.read_write_two_binaries.write_request()
    }

    /// Sets the values of the read_write_two_binaries property.
    pub async fn set_read_write_two_binaries(
        &mut self,
        value: ReadWriteTwoBinariesProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_two_binaries_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_list_of_strings_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<Vec<String>>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 1 field.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteListOfStringsProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Single value property.  Use the value field of the struct.
                        *write_request = new_property_structure.value.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_list_of_strings' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_list_of_strings' payload"
                                .to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    ReadWriteListOfStringsProperty { value: new_value }
                } else {
                    let prop_lock = property_pointer.read().await;

                    ReadWriteListOfStringsProperty {
                        value: (*prop_lock).clone(),
                    }
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_list_of_strings': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_list_of_strings'.");
        }
    }

    /// Watch for changes to the `read_write_list_of_strings` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_list_of_strings(&self) -> watch::Receiver<Vec<String>> {
        self.properties.read_write_list_of_strings.subscribe()
    }

    pub fn get_read_write_list_of_strings_handle(&self) -> WriteRequestLockWatch<Vec<String>> {
        self.properties.read_write_list_of_strings.write_request()
    }

    /// Sets the value of the read_write_list_of_strings property.
    pub async fn set_read_write_list_of_strings(
        &mut self,
        value: Vec<String>,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_list_of_strings_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, which notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_lists_value(
        mut publisher: C,
        property_pointer: Arc<RwLockWatch<ReadWriteListsProperty>>, // Arc to the property value
        version_pointer: Arc<AtomicU32>,
        msg: MqttMessage,
    ) {
        // This is JSON encoding of an object with 2 fields.
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();

        let mut return_code = MethodReturnCode::Success(None);

        match msg.content_type.as_deref() {
            Some("application/json") => { /* OK */ }
            Some(ct) => {
                error!("Unexpected content-type for property update: {}", ct);
                return_code = MethodReturnCode::PayloadError(format!(
                    "Invalid Content-Type '{}', expected 'application/json'",
                    ct
                ));
            }
            None => {
                error!("Missing content-type for property update");
                return_code = MethodReturnCode::PayloadError(
                    "Missing Content-Type; expected 'application/json'".to_string(),
                );
            }
        }

        match return_code {
            MethodReturnCode::Success(_) => {
                let mut incoming_version: Option<u32> = None;
                if let Some(version_str) = msg.user_properties.get("PropertyVersion") {
                    match version_str.parse::<u32>() {
                        Ok(v) => incoming_version = Some(v),
                        Err(e) => {
                            error!(
                                "Failed to parse 'PropertyVersion' user property ('{}'): {:?}",
                                version_str, e
                            );
                            return_code = MethodReturnCode::PayloadError(
                                "Invalid 'PropertyVersion' user property".to_string(),
                            );
                        }
                    }
                }

                if let Some(v) = incoming_version {
                    let current = version_pointer.load(Ordering::SeqCst);
                    if v != current {
                        return_code = MethodReturnCode::OutOfSync(format!(
                            "PropertyVersion mismatch: incoming {}, current {}",
                            v, current
                        ));
                    }
                }
            }
            _ => { /* Do nothing, error already set. */ }
        }

        let opt_new_value = match return_code {
            MethodReturnCode::Success(_) => {
                match serde_json::from_str::<ReadWriteListsProperty>(&payload_str) {
                    Ok(new_property_structure) => {
                        let request_lock = property_pointer.write_request();
                        let mut write_request = request_lock.write().await;

                        // Multi-value property set as a struct.
                        *write_request = new_property_structure.clone();

                        // Committing the write request blocks until the message has been published to MQTT.
                        write_request
                            .commit(std::time::Duration::from_secs(2))
                            .await;
                        Some((*write_request).clone())
                    }
                    Err(e) => {
                        error!("Failed to parse JSON received over MQTT to update 'read_write_lists' property: {:?}", e);
                        return_code = MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_lists' payload".to_string(),
                        );
                        None
                    }
                }
            }
            _ => None,
        };

        if let Some(resp_topic) = msg.response_topic {
            let corr_data = msg.correlation_data.unwrap_or_default();
            let payload_obj = {
                if let Some(new_value) = opt_new_value {
                    new_value
                } else {
                    let prop_lock = property_pointer.read().await;

                    (*prop_lock).clone()
                }
            };
            match message::property_update_response(
                &resp_topic,
                &payload_obj,
                corr_data,
                return_code,
            ) {
                Ok(msg) => {
                    let _fut_publish_result = publisher.publish(msg).await;
                }
                Err(err) => {
                    error!("Error occurred while handling property update for 'read_write_lists': {:?}", &err);
                }
            }
        } else {
            debug!("No response topic provided, so no publishing response to property update for 'read_write_lists'.");
        }
    }

    /// Watch for changes to the `read_write_lists` property.
    /// This returns a watch::Receiver that can be awaited on for changes to the property value.
    pub fn watch_read_write_lists(&self) -> watch::Receiver<ReadWriteListsProperty> {
        self.properties.read_write_lists.subscribe()
    }

    pub fn get_read_write_lists_handle(&self) -> WriteRequestLockWatch<ReadWriteListsProperty> {
        self.properties.read_write_lists.write_request()
    }

    /// Sets the values of the read_write_lists property.
    pub async fn set_read_write_lists(
        &mut self,
        value: ReadWriteListsProperty,
    ) -> SentMessageFuture {
        let write_request_lock = self.get_read_write_lists_handle();
        Box::pin(async move {
            let mut write_request = write_request_lock.write().await;
            *write_request = value;
            match write_request
                .commit(std::time::Duration::from_secs(2))
                .await
            {
                CommitResult::Applied(_) => Ok(()),
                CommitResult::TimedOut => Err(MethodReturnCode::Timeout(
                    "Timeout committing property change".to_string(),
                )),
            }
        })
    }

    /// Starts the tasks that process messages received.
    /// In the task, it loops over messages received from the rx side of the message_receiver channel.
    /// Based on the subscription id of the received message, it will call a function to handle the
    /// received message.
    pub async fn run_loop(&mut self) -> Result<(), JoinError>
    where
        C: 'static,
    {
        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = {
            self.msg_streamer_rx
                .lock()
                .unwrap()
                .take()
                .expect("msg_streamer_rx should be Some")
        };

        let method_handlers = self.method_handlers.clone();
        let _ = self
            .method_handlers
            .lock()
            .await
            .initialize(self.clone())
            .await;
        let sub_ids = self.subscription_ids.clone();
        let publisher = self.mqtt_client.clone();

        let props = self.properties.clone();
        {
            // Set up property change request handling task
            let instance_id_for_read_write_integer_prop = self.instance_id.clone();
            let mut publisher_for_read_write_integer_prop = self.mqtt_client.clone();
            let read_write_integer_prop_version = props.read_write_integer_version.clone();
            if let Some(mut rx_for_read_write_integer_prop) =
                props.read_write_integer.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_integer_prop.recv().await
                    {
                        let payload_obj = ReadWriteIntegerProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_integer_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteInteger/value",
                            instance_id_for_read_write_integer_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_integer_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_integer' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_integer' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_only_integer_prop = self.instance_id.clone();
            let mut publisher_for_read_only_integer_prop = self.mqtt_client.clone();
            let read_only_integer_prop_version = props.read_only_integer_version.clone();
            if let Some(mut rx_for_read_only_integer_prop) =
                props.read_only_integer.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_only_integer_prop.recv().await
                    {
                        let payload_obj = ReadOnlyIntegerProperty {
                            value: request.clone(),
                        };

                        let version_value = read_only_integer_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readOnlyInteger/value",
                            instance_id_for_read_only_integer_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_only_integer_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_only_integer' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_only_integer' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_optional_integer_prop = self.instance_id.clone();
            let mut publisher_for_read_write_optional_integer_prop = self.mqtt_client.clone();
            let read_write_optional_integer_prop_version =
                props.read_write_optional_integer_version.clone();
            if let Some(mut rx_for_read_write_optional_integer_prop) =
                props.read_write_optional_integer.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_optional_integer_prop.recv().await
                    {
                        let payload_obj = ReadWriteOptionalIntegerProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_optional_integer_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteOptionalInteger/value",
                            instance_id_for_read_write_optional_integer_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_optional_integer_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_optional_integer' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_optional_integer' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_two_integers_prop = self.instance_id.clone();
            let mut publisher_for_read_write_two_integers_prop = self.mqtt_client.clone();
            let read_write_two_integers_prop_version =
                props.read_write_two_integers_version.clone();
            if let Some(mut rx_for_read_write_two_integers_prop) =
                props.read_write_two_integers.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_two_integers_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = read_write_two_integers_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteTwoIntegers/value",
                            instance_id_for_read_write_two_integers_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_two_integers_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_two_integers' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_two_integers' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_only_string_prop = self.instance_id.clone();
            let mut publisher_for_read_only_string_prop = self.mqtt_client.clone();
            let read_only_string_prop_version = props.read_only_string_version.clone();
            if let Some(mut rx_for_read_only_string_prop) =
                props.read_only_string.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_only_string_prop.recv().await
                    {
                        let payload_obj = ReadOnlyStringProperty {
                            value: request.clone(),
                        };

                        let version_value = read_only_string_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readOnlyString/value",
                            instance_id_for_read_only_string_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_only_string_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_only_string' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_only_string' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_string_prop = self.instance_id.clone();
            let mut publisher_for_read_write_string_prop = self.mqtt_client.clone();
            let read_write_string_prop_version = props.read_write_string_version.clone();
            if let Some(mut rx_for_read_write_string_prop) =
                props.read_write_string.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_string_prop.recv().await
                    {
                        let payload_obj = ReadWriteStringProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_string_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteString/value",
                            instance_id_for_read_write_string_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_string_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_string' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_string' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_optional_string_prop = self.instance_id.clone();
            let mut publisher_for_read_write_optional_string_prop = self.mqtt_client.clone();
            let read_write_optional_string_prop_version =
                props.read_write_optional_string_version.clone();
            if let Some(mut rx_for_read_write_optional_string_prop) =
                props.read_write_optional_string.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_optional_string_prop.recv().await
                    {
                        let payload_obj = ReadWriteOptionalStringProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_optional_string_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteOptionalString/value",
                            instance_id_for_read_write_optional_string_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_optional_string_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_optional_string' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_optional_string' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_two_strings_prop = self.instance_id.clone();
            let mut publisher_for_read_write_two_strings_prop = self.mqtt_client.clone();
            let read_write_two_strings_prop_version = props.read_write_two_strings_version.clone();
            if let Some(mut rx_for_read_write_two_strings_prop) =
                props.read_write_two_strings.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_two_strings_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = read_write_two_strings_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteTwoStrings/value",
                            instance_id_for_read_write_two_strings_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_two_strings_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_two_strings' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_two_strings' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_struct_prop = self.instance_id.clone();
            let mut publisher_for_read_write_struct_prop = self.mqtt_client.clone();
            let read_write_struct_prop_version = props.read_write_struct_version.clone();
            if let Some(mut rx_for_read_write_struct_prop) =
                props.read_write_struct.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_struct_prop.recv().await
                    {
                        let payload_obj = ReadWriteStructProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_struct_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteStruct/value",
                            instance_id_for_read_write_struct_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_struct_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_struct' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_struct' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_optional_struct_prop = self.instance_id.clone();
            let mut publisher_for_read_write_optional_struct_prop = self.mqtt_client.clone();
            let read_write_optional_struct_prop_version =
                props.read_write_optional_struct_version.clone();
            if let Some(mut rx_for_read_write_optional_struct_prop) =
                props.read_write_optional_struct.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_optional_struct_prop.recv().await
                    {
                        let payload_obj = ReadWriteOptionalStructProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_optional_struct_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteOptionalStruct/value",
                            instance_id_for_read_write_optional_struct_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_optional_struct_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_optional_struct' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_optional_struct' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_two_structs_prop = self.instance_id.clone();
            let mut publisher_for_read_write_two_structs_prop = self.mqtt_client.clone();
            let read_write_two_structs_prop_version = props.read_write_two_structs_version.clone();
            if let Some(mut rx_for_read_write_two_structs_prop) =
                props.read_write_two_structs.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_two_structs_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = read_write_two_structs_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteTwoStructs/value",
                            instance_id_for_read_write_two_structs_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_two_structs_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_two_structs' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_two_structs' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_only_enum_prop = self.instance_id.clone();
            let mut publisher_for_read_only_enum_prop = self.mqtt_client.clone();
            let read_only_enum_prop_version = props.read_only_enum_version.clone();
            if let Some(mut rx_for_read_only_enum_prop) =
                props.read_only_enum.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_only_enum_prop.recv().await
                    {
                        let payload_obj = ReadOnlyEnumProperty {
                            value: request.clone(),
                        };

                        let version_value = read_only_enum_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readOnlyEnum/value",
                            instance_id_for_read_only_enum_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_only_enum_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_only_enum' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_only_enum' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_enum_prop = self.instance_id.clone();
            let mut publisher_for_read_write_enum_prop = self.mqtt_client.clone();
            let read_write_enum_prop_version = props.read_write_enum_version.clone();
            if let Some(mut rx_for_read_write_enum_prop) =
                props.read_write_enum.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_enum_prop.recv().await
                    {
                        let payload_obj = ReadWriteEnumProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_enum_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteEnum/value",
                            instance_id_for_read_write_enum_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_enum_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_enum' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_enum' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_optional_enum_prop = self.instance_id.clone();
            let mut publisher_for_read_write_optional_enum_prop = self.mqtt_client.clone();
            let read_write_optional_enum_prop_version =
                props.read_write_optional_enum_version.clone();
            if let Some(mut rx_for_read_write_optional_enum_prop) =
                props.read_write_optional_enum.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_optional_enum_prop.recv().await
                    {
                        let payload_obj = ReadWriteOptionalEnumProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_optional_enum_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteOptionalEnum/value",
                            instance_id_for_read_write_optional_enum_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_optional_enum_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_optional_enum' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_optional_enum' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_two_enums_prop = self.instance_id.clone();
            let mut publisher_for_read_write_two_enums_prop = self.mqtt_client.clone();
            let read_write_two_enums_prop_version = props.read_write_two_enums_version.clone();
            if let Some(mut rx_for_read_write_two_enums_prop) =
                props.read_write_two_enums.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_two_enums_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = read_write_two_enums_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteTwoEnums/value",
                            instance_id_for_read_write_two_enums_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_two_enums_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_two_enums' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_two_enums' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_datetime_prop = self.instance_id.clone();
            let mut publisher_for_read_write_datetime_prop = self.mqtt_client.clone();
            let read_write_datetime_prop_version = props.read_write_datetime_version.clone();
            if let Some(mut rx_for_read_write_datetime_prop) =
                props.read_write_datetime.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_datetime_prop.recv().await
                    {
                        let payload_obj = ReadWriteDatetimeProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_datetime_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteDatetime/value",
                            instance_id_for_read_write_datetime_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_datetime_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_datetime' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_datetime' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_optional_datetime_prop = self.instance_id.clone();
            let mut publisher_for_read_write_optional_datetime_prop = self.mqtt_client.clone();
            let read_write_optional_datetime_prop_version =
                props.read_write_optional_datetime_version.clone();
            if let Some(mut rx_for_read_write_optional_datetime_prop) =
                props.read_write_optional_datetime.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_optional_datetime_prop.recv().await
                    {
                        let payload_obj = ReadWriteOptionalDatetimeProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_optional_datetime_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteOptionalDatetime/value",
                            instance_id_for_read_write_optional_datetime_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_optional_datetime_prop
                                        .publish(msg)
                                        .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_optional_datetime' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_optional_datetime' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_two_datetimes_prop = self.instance_id.clone();
            let mut publisher_for_read_write_two_datetimes_prop = self.mqtt_client.clone();
            let read_write_two_datetimes_prop_version =
                props.read_write_two_datetimes_version.clone();
            if let Some(mut rx_for_read_write_two_datetimes_prop) =
                props.read_write_two_datetimes.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_two_datetimes_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = read_write_two_datetimes_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteTwoDatetimes/value",
                            instance_id_for_read_write_two_datetimes_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_two_datetimes_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_two_datetimes' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_two_datetimes' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_duration_prop = self.instance_id.clone();
            let mut publisher_for_read_write_duration_prop = self.mqtt_client.clone();
            let read_write_duration_prop_version = props.read_write_duration_version.clone();
            if let Some(mut rx_for_read_write_duration_prop) =
                props.read_write_duration.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_duration_prop.recv().await
                    {
                        let payload_obj = ReadWriteDurationProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_duration_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteDuration/value",
                            instance_id_for_read_write_duration_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_duration_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_duration' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_duration' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_optional_duration_prop = self.instance_id.clone();
            let mut publisher_for_read_write_optional_duration_prop = self.mqtt_client.clone();
            let read_write_optional_duration_prop_version =
                props.read_write_optional_duration_version.clone();
            if let Some(mut rx_for_read_write_optional_duration_prop) =
                props.read_write_optional_duration.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_optional_duration_prop.recv().await
                    {
                        let payload_obj = ReadWriteOptionalDurationProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_optional_duration_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteOptionalDuration/value",
                            instance_id_for_read_write_optional_duration_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_optional_duration_prop
                                        .publish(msg)
                                        .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_optional_duration' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_optional_duration' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_two_durations_prop = self.instance_id.clone();
            let mut publisher_for_read_write_two_durations_prop = self.mqtt_client.clone();
            let read_write_two_durations_prop_version =
                props.read_write_two_durations_version.clone();
            if let Some(mut rx_for_read_write_two_durations_prop) =
                props.read_write_two_durations.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_two_durations_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = read_write_two_durations_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteTwoDurations/value",
                            instance_id_for_read_write_two_durations_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_two_durations_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_two_durations' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_two_durations' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_binary_prop = self.instance_id.clone();
            let mut publisher_for_read_write_binary_prop = self.mqtt_client.clone();
            let read_write_binary_prop_version = props.read_write_binary_version.clone();
            if let Some(mut rx_for_read_write_binary_prop) =
                props.read_write_binary.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_binary_prop.recv().await
                    {
                        let payload_obj = ReadWriteBinaryProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_binary_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteBinary/value",
                            instance_id_for_read_write_binary_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_binary_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_binary' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_binary' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_optional_binary_prop = self.instance_id.clone();
            let mut publisher_for_read_write_optional_binary_prop = self.mqtt_client.clone();
            let read_write_optional_binary_prop_version =
                props.read_write_optional_binary_version.clone();
            if let Some(mut rx_for_read_write_optional_binary_prop) =
                props.read_write_optional_binary.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_optional_binary_prop.recv().await
                    {
                        let payload_obj = ReadWriteOptionalBinaryProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_optional_binary_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteOptionalBinary/value",
                            instance_id_for_read_write_optional_binary_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_optional_binary_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_optional_binary' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_optional_binary' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_two_binaries_prop = self.instance_id.clone();
            let mut publisher_for_read_write_two_binaries_prop = self.mqtt_client.clone();
            let read_write_two_binaries_prop_version =
                props.read_write_two_binaries_version.clone();
            if let Some(mut rx_for_read_write_two_binaries_prop) =
                props.read_write_two_binaries.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_two_binaries_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = read_write_two_binaries_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteTwoBinaries/value",
                            instance_id_for_read_write_two_binaries_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_two_binaries_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_two_binaries' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_two_binaries' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_list_of_strings_prop = self.instance_id.clone();
            let mut publisher_for_read_write_list_of_strings_prop = self.mqtt_client.clone();
            let read_write_list_of_strings_prop_version =
                props.read_write_list_of_strings_version.clone();
            if let Some(mut rx_for_read_write_list_of_strings_prop) =
                props.read_write_list_of_strings.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_list_of_strings_prop.recv().await
                    {
                        let payload_obj = ReadWriteListOfStringsProperty {
                            value: request.clone(),
                        };

                        let version_value = read_write_list_of_strings_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteListOfStrings/value",
                            instance_id_for_read_write_list_of_strings_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result = publisher_for_read_write_list_of_strings_prop
                                    .publish(msg)
                                    .await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_list_of_strings' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_list_of_strings' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        {
            // Set up property change request handling task
            let instance_id_for_read_write_lists_prop = self.instance_id.clone();
            let mut publisher_for_read_write_lists_prop = self.mqtt_client.clone();
            let read_write_lists_prop_version = props.read_write_lists_version.clone();
            if let Some(mut rx_for_read_write_lists_prop) =
                props.read_write_lists.take_request_receiver()
            {
                tokio::spawn(async move {
                    while let Some((request, opt_responder)) =
                        rx_for_read_write_lists_prop.recv().await
                    {
                        let payload_obj = request.clone();

                        let version_value = read_write_lists_prop_version
                            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
                        let topic: String = format!(
                            "testable/{}/property/readWriteLists/value",
                            instance_id_for_read_write_lists_prop
                        );
                        match message::property_value(&topic, &payload_obj, version_value) {
                            Ok(msg) => {
                                let publish_result =
                                    publisher_for_read_write_lists_prop.publish(msg).await;
                                if let Some(responder) = opt_responder {
                                    match publish_result {
                                        Ok(_) => {
                                            let _ = responder.send(Some(request));
                                        }
                                        Err(_) => {
                                            error!("Error publishing updated value for 'read_write_lists' property");
                                            let _ = responder.send(None);
                                        }
                                    };
                                }
                            }
                            Err(e) => {
                                error!("Error creating property value message for 'read_write_lists' property: {:?}", e);
                                if let Some(responder) = opt_responder {
                                    let _ = responder.send(None);
                                }
                            }
                        }
                    }
                });
            }
        }

        // Spawn a task to periodically publish interface info.
        let mut interface_publisher = self.mqtt_client.clone();
        let instance_id = self.instance_id.clone();
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(std::time::Duration::from_secs(120));
            loop {
                interval.tick().await;
                let topic = format!("testable/{}/interface", instance_id);
                let info = crate::interface::InterfaceInfoBuilder::default()
                    .interface_name("testable".to_string())
                    .title("Interface for testing".to_string())
                    .version("0.0.1".to_string())
                    .instance(instance_id.clone())
                    .connection_topic(topic.clone())
                    .build()
                    .unwrap();
                let msg = message::interface_online(&topic, &info, 150 /*seconds*/).unwrap();
                let _ = interface_publisher.publish(msg).await;
            }
        });

        let properties = self.properties.clone();
        let loop_task = tokio::spawn(async move {
            loop {
                match message_receiver.recv().await {
                    Ok(msg) => {
                        if let Some(subscription_id) = msg.subscription_id {
                            match subscription_id {
                                _i if _i == sub_ids.call_with_nothing_method_req => {
                                    debug!("Received callWithNothing method invocation message.");
                                    TestableServer::<C>::handle_call_with_nothing_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_one_integer_method_req => {
                                    debug!("Received callOneInteger method invocation message.");
                                    TestableServer::<C>::handle_call_one_integer_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_optional_integer_method_req => {
                                    debug!(
                                        "Received callOptionalInteger method invocation message."
                                    );
                                    TestableServer::<C>::handle_call_optional_integer_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_three_integers_method_req => {
                                    debug!("Received callThreeIntegers method invocation message.");
                                    TestableServer::<C>::handle_call_three_integers_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_one_string_method_req => {
                                    debug!("Received callOneString method invocation message.");
                                    TestableServer::<C>::handle_call_one_string_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_optional_string_method_req => {
                                    debug!(
                                        "Received callOptionalString method invocation message."
                                    );
                                    TestableServer::<C>::handle_call_optional_string_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_three_strings_method_req => {
                                    debug!("Received callThreeStrings method invocation message.");
                                    TestableServer::<C>::handle_call_three_strings_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_one_enum_method_req => {
                                    debug!("Received callOneEnum method invocation message.");
                                    TestableServer::<C>::handle_call_one_enum_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_optional_enum_method_req => {
                                    debug!("Received callOptionalEnum method invocation message.");
                                    TestableServer::<C>::handle_call_optional_enum_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_three_enums_method_req => {
                                    debug!("Received callThreeEnums method invocation message.");
                                    TestableServer::<C>::handle_call_three_enums_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_one_struct_method_req => {
                                    debug!("Received callOneStruct method invocation message.");
                                    TestableServer::<C>::handle_call_one_struct_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_optional_struct_method_req => {
                                    debug!(
                                        "Received callOptionalStruct method invocation message."
                                    );
                                    TestableServer::<C>::handle_call_optional_struct_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_three_structs_method_req => {
                                    debug!("Received callThreeStructs method invocation message.");
                                    TestableServer::<C>::handle_call_three_structs_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_one_date_time_method_req => {
                                    debug!("Received callOneDateTime method invocation message.");
                                    TestableServer::<C>::handle_call_one_date_time_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_optional_date_time_method_req => {
                                    debug!(
                                        "Received callOptionalDateTime method invocation message."
                                    );
                                    TestableServer::<C>::handle_call_optional_date_time_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_three_date_times_method_req => {
                                    debug!(
                                        "Received callThreeDateTimes method invocation message."
                                    );
                                    TestableServer::<C>::handle_call_three_date_times_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_one_duration_method_req => {
                                    debug!("Received callOneDuration method invocation message.");
                                    TestableServer::<C>::handle_call_one_duration_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_optional_duration_method_req => {
                                    debug!(
                                        "Received callOptionalDuration method invocation message."
                                    );
                                    TestableServer::<C>::handle_call_optional_duration_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_three_durations_method_req => {
                                    debug!(
                                        "Received callThreeDurations method invocation message."
                                    );
                                    TestableServer::<C>::handle_call_three_durations_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_one_binary_method_req => {
                                    debug!("Received callOneBinary method invocation message.");
                                    TestableServer::<C>::handle_call_one_binary_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_optional_binary_method_req => {
                                    debug!(
                                        "Received callOptionalBinary method invocation message."
                                    );
                                    TestableServer::<C>::handle_call_optional_binary_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_three_binaries_method_req => {
                                    debug!("Received callThreeBinaries method invocation message.");
                                    TestableServer::<C>::handle_call_three_binaries_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_one_list_of_integers_method_req => {
                                    debug!(
                                        "Received callOneListOfIntegers method invocation message."
                                    );
                                    TestableServer::<C>::handle_call_one_list_of_integers_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.call_optional_list_of_floats_method_req => {
                                    debug!("Received callOptionalListOfFloats method invocation message.");
                                    TestableServer::<C>::handle_call_optional_list_of_floats_request(publisher.clone(), method_handlers.clone(), msg).await;
                                }
                                _i if _i == sub_ids.call_two_lists_method_req => {
                                    debug!("Received callTwoLists method invocation message.");
                                    TestableServer::<C>::handle_call_two_lists_request(
                                        publisher.clone(),
                                        method_handlers.clone(),
                                        msg,
                                    )
                                    .await;
                                }
                                _i if _i == sub_ids.read_write_integer_property_update => {
                                    debug!("Received read_write_integer property update request message.");
                                    TestableServer::<C>::update_read_write_integer_value(
                                        publisher.clone(),
                                        properties.read_write_integer.clone(),
                                        properties.read_write_integer_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_optional_integer_property_update => {
                                    debug!("Received read_write_optional_integer property update request message.");
                                    TestableServer::<C>::update_read_write_optional_integer_value(
                                        publisher.clone(),
                                        properties.read_write_optional_integer.clone(),
                                        properties.read_write_optional_integer_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_two_integers_property_update => {
                                    debug!("Received read_write_two_integers property update request message.");
                                    TestableServer::<C>::update_read_write_two_integers_value(
                                        publisher.clone(),
                                        properties.read_write_two_integers.clone(),
                                        properties.read_write_two_integers_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_string_property_update => {
                                    debug!("Received read_write_string property update request message.");
                                    TestableServer::<C>::update_read_write_string_value(
                                        publisher.clone(),
                                        properties.read_write_string.clone(),
                                        properties.read_write_string_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_optional_string_property_update => {
                                    debug!("Received read_write_optional_string property update request message.");
                                    TestableServer::<C>::update_read_write_optional_string_value(
                                        publisher.clone(),
                                        properties.read_write_optional_string.clone(),
                                        properties.read_write_optional_string_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_two_strings_property_update => {
                                    debug!("Received read_write_two_strings property update request message.");
                                    TestableServer::<C>::update_read_write_two_strings_value(
                                        publisher.clone(),
                                        properties.read_write_two_strings.clone(),
                                        properties.read_write_two_strings_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_struct_property_update => {
                                    debug!("Received read_write_struct property update request message.");
                                    TestableServer::<C>::update_read_write_struct_value(
                                        publisher.clone(),
                                        properties.read_write_struct.clone(),
                                        properties.read_write_struct_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_optional_struct_property_update => {
                                    debug!("Received read_write_optional_struct property update request message.");
                                    TestableServer::<C>::update_read_write_optional_struct_value(
                                        publisher.clone(),
                                        properties.read_write_optional_struct.clone(),
                                        properties.read_write_optional_struct_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_two_structs_property_update => {
                                    debug!("Received read_write_two_structs property update request message.");
                                    TestableServer::<C>::update_read_write_two_structs_value(
                                        publisher.clone(),
                                        properties.read_write_two_structs.clone(),
                                        properties.read_write_two_structs_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_enum_property_update => {
                                    debug!(
                                        "Received read_write_enum property update request message."
                                    );
                                    TestableServer::<C>::update_read_write_enum_value(
                                        publisher.clone(),
                                        properties.read_write_enum.clone(),
                                        properties.read_write_enum_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_optional_enum_property_update => {
                                    debug!("Received read_write_optional_enum property update request message.");
                                    TestableServer::<C>::update_read_write_optional_enum_value(
                                        publisher.clone(),
                                        properties.read_write_optional_enum.clone(),
                                        properties.read_write_optional_enum_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_two_enums_property_update => {
                                    debug!("Received read_write_two_enums property update request message.");
                                    TestableServer::<C>::update_read_write_two_enums_value(
                                        publisher.clone(),
                                        properties.read_write_two_enums.clone(),
                                        properties.read_write_two_enums_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_datetime_property_update => {
                                    debug!("Received read_write_datetime property update request message.");
                                    TestableServer::<C>::update_read_write_datetime_value(
                                        publisher.clone(),
                                        properties.read_write_datetime.clone(),
                                        properties.read_write_datetime_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i
                                    == sub_ids.read_write_optional_datetime_property_update =>
                                {
                                    debug!("Received read_write_optional_datetime property update request message.");
                                    TestableServer::<C>::update_read_write_optional_datetime_value(
                                        publisher.clone(),
                                        properties.read_write_optional_datetime.clone(),
                                        properties.read_write_optional_datetime_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_two_datetimes_property_update => {
                                    debug!("Received read_write_two_datetimes property update request message.");
                                    TestableServer::<C>::update_read_write_two_datetimes_value(
                                        publisher.clone(),
                                        properties.read_write_two_datetimes.clone(),
                                        properties.read_write_two_datetimes_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_duration_property_update => {
                                    debug!("Received read_write_duration property update request message.");
                                    TestableServer::<C>::update_read_write_duration_value(
                                        publisher.clone(),
                                        properties.read_write_duration.clone(),
                                        properties.read_write_duration_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i
                                    == sub_ids.read_write_optional_duration_property_update =>
                                {
                                    debug!("Received read_write_optional_duration property update request message.");
                                    TestableServer::<C>::update_read_write_optional_duration_value(
                                        publisher.clone(),
                                        properties.read_write_optional_duration.clone(),
                                        properties.read_write_optional_duration_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_two_durations_property_update => {
                                    debug!("Received read_write_two_durations property update request message.");
                                    TestableServer::<C>::update_read_write_two_durations_value(
                                        publisher.clone(),
                                        properties.read_write_two_durations.clone(),
                                        properties.read_write_two_durations_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_binary_property_update => {
                                    debug!("Received read_write_binary property update request message.");
                                    TestableServer::<C>::update_read_write_binary_value(
                                        publisher.clone(),
                                        properties.read_write_binary.clone(),
                                        properties.read_write_binary_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_optional_binary_property_update => {
                                    debug!("Received read_write_optional_binary property update request message.");
                                    TestableServer::<C>::update_read_write_optional_binary_value(
                                        publisher.clone(),
                                        properties.read_write_optional_binary.clone(),
                                        properties.read_write_optional_binary_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_two_binaries_property_update => {
                                    debug!("Received read_write_two_binaries property update request message.");
                                    TestableServer::<C>::update_read_write_two_binaries_value(
                                        publisher.clone(),
                                        properties.read_write_two_binaries.clone(),
                                        properties.read_write_two_binaries_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_list_of_strings_property_update => {
                                    debug!("Received read_write_list_of_strings property update request message.");
                                    TestableServer::<C>::update_read_write_list_of_strings_value(
                                        publisher.clone(),
                                        properties.read_write_list_of_strings.clone(),
                                        properties.read_write_list_of_strings_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _i if _i == sub_ids.read_write_lists_property_update => {
                                    debug!("Received read_write_lists property update request message.");
                                    TestableServer::<C>::update_read_write_lists_value(
                                        publisher.clone(),
                                        properties.read_write_lists.clone(),
                                        properties.read_write_lists_version.clone(),
                                        msg,
                                    )
                                    .await;
                                }

                                _ => {
                                    error!(
                                        "Received MQTT message with unknown subscription id: {}",
                                        subscription_id
                                    );
                                }
                            }
                        } else {
                            warn!("Received MQTT message without subscription id; cannot process.");
                        }
                    }
                    Err(e) => {
                        warn!("Error receiving MQTT message in server loop: {:?}", e);
                    }
                }
            }
        });

        let _ = tokio::join!(loop_task);

        warn!("Server receive loop completed. Exiting run_loop.");
        Ok(())
    }
}

#[async_trait]
pub trait TestableMethodHandlers<C: Mqtt5PubSub>: Send + Sync {
    async fn initialize(&mut self, server: TestableServer<C>) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the callWithNothing method request.
    async fn handle_call_with_nothing(&self) -> Result<(), MethodReturnCode>;

    /// Pointer to a function to handle the callOneInteger method request.
    async fn handle_call_one_integer(&self, input1: i32) -> Result<i32, MethodReturnCode>;

    /// Pointer to a function to handle the callOptionalInteger method request.
    async fn handle_call_optional_integer(
        &self,
        input1: Option<i32>,
    ) -> Result<Option<i32>, MethodReturnCode>;

    /// Pointer to a function to handle the callThreeIntegers method request.
    async fn handle_call_three_integers(
        &self,
        input1: i32,
        input2: i32,
        input3: Option<i32>,
    ) -> Result<CallThreeIntegersReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the callOneString method request.
    async fn handle_call_one_string(&self, input1: String) -> Result<String, MethodReturnCode>;

    /// Pointer to a function to handle the callOptionalString method request.
    async fn handle_call_optional_string(
        &self,
        input1: Option<String>,
    ) -> Result<Option<String>, MethodReturnCode>;

    /// Pointer to a function to handle the callThreeStrings method request.
    async fn handle_call_three_strings(
        &self,
        input1: String,
        input2: Option<String>,
        input3: String,
    ) -> Result<CallThreeStringsReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the callOneEnum method request.
    async fn handle_call_one_enum(&self, input1: Numbers) -> Result<Numbers, MethodReturnCode>;

    /// Pointer to a function to handle the callOptionalEnum method request.
    async fn handle_call_optional_enum(
        &self,
        input1: Option<Numbers>,
    ) -> Result<Option<Numbers>, MethodReturnCode>;

    /// Pointer to a function to handle the callThreeEnums method request.
    async fn handle_call_three_enums(
        &self,
        input1: Numbers,
        input2: Numbers,
        input3: Option<Numbers>,
    ) -> Result<CallThreeEnumsReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the callOneStruct method request.
    async fn handle_call_one_struct(&self, input1: AllTypes) -> Result<AllTypes, MethodReturnCode>;

    /// Pointer to a function to handle the callOptionalStruct method request.
    async fn handle_call_optional_struct(
        &self,
        input1: Option<AllTypes>,
    ) -> Result<Option<AllTypes>, MethodReturnCode>;

    /// Pointer to a function to handle the callThreeStructs method request.
    async fn handle_call_three_structs(
        &self,
        input1: Option<AllTypes>,
        input2: AllTypes,
        input3: AllTypes,
    ) -> Result<CallThreeStructsReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the callOneDateTime method request.
    async fn handle_call_one_date_time(
        &self,
        input1: chrono::DateTime<chrono::Utc>,
    ) -> Result<chrono::DateTime<chrono::Utc>, MethodReturnCode>;

    /// Pointer to a function to handle the callOptionalDateTime method request.
    async fn handle_call_optional_date_time(
        &self,
        input1: Option<chrono::DateTime<chrono::Utc>>,
    ) -> Result<Option<chrono::DateTime<chrono::Utc>>, MethodReturnCode>;

    /// Pointer to a function to handle the callThreeDateTimes method request.
    async fn handle_call_three_date_times(
        &self,
        input1: chrono::DateTime<chrono::Utc>,
        input2: chrono::DateTime<chrono::Utc>,
        input3: Option<chrono::DateTime<chrono::Utc>>,
    ) -> Result<CallThreeDateTimesReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the callOneDuration method request.
    async fn handle_call_one_duration(
        &self,
        input1: chrono::Duration,
    ) -> Result<chrono::Duration, MethodReturnCode>;

    /// Pointer to a function to handle the callOptionalDuration method request.
    async fn handle_call_optional_duration(
        &self,
        input1: Option<chrono::Duration>,
    ) -> Result<Option<chrono::Duration>, MethodReturnCode>;

    /// Pointer to a function to handle the callThreeDurations method request.
    async fn handle_call_three_durations(
        &self,
        input1: chrono::Duration,
        input2: chrono::Duration,
        input3: Option<chrono::Duration>,
    ) -> Result<CallThreeDurationsReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the callOneBinary method request.
    async fn handle_call_one_binary(&self, input1: Vec<u8>) -> Result<Vec<u8>, MethodReturnCode>;

    /// Pointer to a function to handle the callOptionalBinary method request.
    async fn handle_call_optional_binary(
        &self,
        input1: Option<Vec<u8>>,
    ) -> Result<Option<Vec<u8>>, MethodReturnCode>;

    /// Pointer to a function to handle the callThreeBinaries method request.
    async fn handle_call_three_binaries(
        &self,
        input1: Vec<u8>,
        input2: Vec<u8>,
        input3: Option<Vec<u8>>,
    ) -> Result<CallThreeBinariesReturnValues, MethodReturnCode>;

    /// Pointer to a function to handle the callOneListOfIntegers method request.
    async fn handle_call_one_list_of_integers(
        &self,
        input1: Vec<i32>,
    ) -> Result<Vec<i32>, MethodReturnCode>;

    /// Pointer to a function to handle the callOptionalListOfFloats method request.
    async fn handle_call_optional_list_of_floats(
        &self,
        input1: Option<Vec<f32>>,
    ) -> Result<Option<Vec<f32>>, MethodReturnCode>;

    /// Pointer to a function to handle the callTwoLists method request.
    async fn handle_call_two_lists(
        &self,
        input1: Vec<Numbers>,
        input2: Option<Vec<String>>,
    ) -> Result<CallTwoListsReturnValues, MethodReturnCode>;

    fn as_any(&self) -> &dyn Any;
}
