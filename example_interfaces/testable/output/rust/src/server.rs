//! Server module for Test Able IPC
//!
//! This module is only available when the "server" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the Test Able interface.

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

use std::sync::atomic::{AtomicU32, Ordering};

use std::future::Future;
use std::pin::Pin;
use stinger_mqtt_trait::message::{MqttMessage, QoS};
use stinger_mqtt_trait::{Mqtt5PubSub, Mqtt5PubSubError, MqttPublishSuccess};
use tokio::task::JoinError;
type SentMessageFuture = Pin<Box<dyn Future<Output = Result<(), MethodReturnCode>> + Send>>;
use crate::message;
#[cfg(feature = "server")]
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct TestAbleServerSubscriptionIds {
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
struct TestAbleProperties {
    read_write_integer: Arc<AsyncMutex<Option<ReadWriteIntegerProperty>>>,
    read_write_integer_tx_channel: watch::Sender<Option<i32>>,
    read_write_integer_version: Arc<AtomicU32>,
    read_only_integer: Arc<AsyncMutex<Option<ReadOnlyIntegerProperty>>>,
    read_only_integer_tx_channel: watch::Sender<Option<i32>>,
    read_only_integer_version: Arc<AtomicU32>,
    read_write_optional_integer: Arc<AsyncMutex<Option<ReadWriteOptionalIntegerProperty>>>,
    read_write_optional_integer_tx_channel: watch::Sender<Option<Option<i32>>>,
    read_write_optional_integer_version: Arc<AtomicU32>,
    read_write_two_integers: Arc<AsyncMutex<Option<ReadWriteTwoIntegersProperty>>>,
    read_write_two_integers_tx_channel: watch::Sender<Option<ReadWriteTwoIntegersProperty>>,
    read_write_two_integers_version: Arc<AtomicU32>,
    read_only_string: Arc<AsyncMutex<Option<ReadOnlyStringProperty>>>,
    read_only_string_tx_channel: watch::Sender<Option<String>>,
    read_only_string_version: Arc<AtomicU32>,
    read_write_string: Arc<AsyncMutex<Option<ReadWriteStringProperty>>>,
    read_write_string_tx_channel: watch::Sender<Option<String>>,
    read_write_string_version: Arc<AtomicU32>,
    read_write_optional_string: Arc<AsyncMutex<Option<ReadWriteOptionalStringProperty>>>,
    read_write_optional_string_tx_channel: watch::Sender<Option<Option<String>>>,
    read_write_optional_string_version: Arc<AtomicU32>,
    read_write_two_strings: Arc<AsyncMutex<Option<ReadWriteTwoStringsProperty>>>,
    read_write_two_strings_tx_channel: watch::Sender<Option<ReadWriteTwoStringsProperty>>,
    read_write_two_strings_version: Arc<AtomicU32>,
    read_write_struct: Arc<AsyncMutex<Option<ReadWriteStructProperty>>>,
    read_write_struct_tx_channel: watch::Sender<Option<AllTypes>>,
    read_write_struct_version: Arc<AtomicU32>,
    read_write_optional_struct: Arc<AsyncMutex<Option<ReadWriteOptionalStructProperty>>>,
    read_write_optional_struct_tx_channel: watch::Sender<Option<Option<AllTypes>>>,
    read_write_optional_struct_version: Arc<AtomicU32>,
    read_write_two_structs: Arc<AsyncMutex<Option<ReadWriteTwoStructsProperty>>>,
    read_write_two_structs_tx_channel: watch::Sender<Option<ReadWriteTwoStructsProperty>>,
    read_write_two_structs_version: Arc<AtomicU32>,
    read_only_enum: Arc<AsyncMutex<Option<ReadOnlyEnumProperty>>>,
    read_only_enum_tx_channel: watch::Sender<Option<Numbers>>,
    read_only_enum_version: Arc<AtomicU32>,
    read_write_enum: Arc<AsyncMutex<Option<ReadWriteEnumProperty>>>,
    read_write_enum_tx_channel: watch::Sender<Option<Numbers>>,
    read_write_enum_version: Arc<AtomicU32>,
    read_write_optional_enum: Arc<AsyncMutex<Option<ReadWriteOptionalEnumProperty>>>,
    read_write_optional_enum_tx_channel: watch::Sender<Option<Option<Numbers>>>,
    read_write_optional_enum_version: Arc<AtomicU32>,
    read_write_two_enums: Arc<AsyncMutex<Option<ReadWriteTwoEnumsProperty>>>,
    read_write_two_enums_tx_channel: watch::Sender<Option<ReadWriteTwoEnumsProperty>>,
    read_write_two_enums_version: Arc<AtomicU32>,
    read_write_datetime: Arc<AsyncMutex<Option<ReadWriteDatetimeProperty>>>,
    read_write_datetime_tx_channel: watch::Sender<Option<chrono::DateTime<chrono::Utc>>>,
    read_write_datetime_version: Arc<AtomicU32>,
    read_write_optional_datetime: Arc<AsyncMutex<Option<ReadWriteOptionalDatetimeProperty>>>,
    read_write_optional_datetime_tx_channel:
        watch::Sender<Option<Option<chrono::DateTime<chrono::Utc>>>>,
    read_write_optional_datetime_version: Arc<AtomicU32>,
    read_write_two_datetimes: Arc<AsyncMutex<Option<ReadWriteTwoDatetimesProperty>>>,
    read_write_two_datetimes_tx_channel: watch::Sender<Option<ReadWriteTwoDatetimesProperty>>,
    read_write_two_datetimes_version: Arc<AtomicU32>,
    read_write_duration: Arc<AsyncMutex<Option<ReadWriteDurationProperty>>>,
    read_write_duration_tx_channel: watch::Sender<Option<chrono::Duration>>,
    read_write_duration_version: Arc<AtomicU32>,
    read_write_optional_duration: Arc<AsyncMutex<Option<ReadWriteOptionalDurationProperty>>>,
    read_write_optional_duration_tx_channel: watch::Sender<Option<Option<chrono::Duration>>>,
    read_write_optional_duration_version: Arc<AtomicU32>,
    read_write_two_durations: Arc<AsyncMutex<Option<ReadWriteTwoDurationsProperty>>>,
    read_write_two_durations_tx_channel: watch::Sender<Option<ReadWriteTwoDurationsProperty>>,
    read_write_two_durations_version: Arc<AtomicU32>,
    read_write_binary: Arc<AsyncMutex<Option<ReadWriteBinaryProperty>>>,
    read_write_binary_tx_channel: watch::Sender<Option<Vec<u8>>>,
    read_write_binary_version: Arc<AtomicU32>,
    read_write_optional_binary: Arc<AsyncMutex<Option<ReadWriteOptionalBinaryProperty>>>,
    read_write_optional_binary_tx_channel: watch::Sender<Option<Option<Vec<u8>>>>,
    read_write_optional_binary_version: Arc<AtomicU32>,
    read_write_two_binaries: Arc<AsyncMutex<Option<ReadWriteTwoBinariesProperty>>>,
    read_write_two_binaries_tx_channel: watch::Sender<Option<ReadWriteTwoBinariesProperty>>,
    read_write_two_binaries_version: Arc<AtomicU32>,
    read_write_list_of_strings: Arc<AsyncMutex<Option<ReadWriteListOfStringsProperty>>>,
    read_write_list_of_strings_tx_channel: watch::Sender<Option<Vec<String>>>,
    read_write_list_of_strings_version: Arc<AtomicU32>,
    read_write_lists: Arc<AsyncMutex<Option<ReadWriteListsProperty>>>,
    read_write_lists_tx_channel: watch::Sender<Option<ReadWriteListsProperty>>,
    read_write_lists_version: Arc<AtomicU32>,
}

#[derive(Clone)]
pub struct TestAbleServer<C: Mqtt5PubSub> {
    mqtt_client: C,

    /// Temporarily holds the receiver for the broadcast channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<broadcast::Receiver<MqttMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: broadcast::Sender<MqttMessage>,

    /// Struct contains all the method handlers.
    method_handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,

    /// Struct contains all the properties.
    properties: TestAbleProperties,

    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: TestAbleServerSubscriptionIds,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,

    pub instance_id: String,
}

impl<C: Mqtt5PubSub + Clone + Send> TestAbleServer<C> {
    pub async fn new(
        mut connection: C,
        method_handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
        instance_id: String,
    ) -> Self {
        // Create a channel for messages to get from the Mqtt5PubSub object to this TestAbleServer object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = broadcast::channel::<MqttMessage>(64);

        // Create method handler struct
        let subscription_id_call_with_nothing_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callWithNothing", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_with_nothing_method_req =
            subscription_id_call_with_nothing_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_one_integer_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOneInteger", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_integer_method_req =
            subscription_id_call_one_integer_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_optional_integer_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOptionalInteger", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_integer_method_req =
            subscription_id_call_optional_integer_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_three_integers_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callThreeIntegers", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_integers_method_req =
            subscription_id_call_three_integers_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_one_string_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOneString", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_string_method_req =
            subscription_id_call_one_string_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_optional_string_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOptionalString", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_string_method_req =
            subscription_id_call_optional_string_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_three_strings_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callThreeStrings", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_strings_method_req =
            subscription_id_call_three_strings_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_one_enum_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOneEnum", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_enum_method_req =
            subscription_id_call_one_enum_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_optional_enum_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOptionalEnum", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_enum_method_req =
            subscription_id_call_optional_enum_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_three_enums_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callThreeEnums", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_enums_method_req =
            subscription_id_call_three_enums_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_one_struct_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOneStruct", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_struct_method_req =
            subscription_id_call_one_struct_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_optional_struct_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOptionalStruct", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_struct_method_req =
            subscription_id_call_optional_struct_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_three_structs_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callThreeStructs", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_structs_method_req =
            subscription_id_call_three_structs_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_one_date_time_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOneDateTime", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_date_time_method_req =
            subscription_id_call_one_date_time_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_optional_date_time_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOptionalDateTime", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_date_time_method_req =
            subscription_id_call_optional_date_time_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_three_date_times_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callThreeDateTimes", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_date_times_method_req =
            subscription_id_call_three_date_times_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_one_duration_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOneDuration", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_duration_method_req =
            subscription_id_call_one_duration_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_optional_duration_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOptionalDuration", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_duration_method_req =
            subscription_id_call_optional_duration_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_three_durations_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callThreeDurations", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_durations_method_req =
            subscription_id_call_three_durations_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_one_binary_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOneBinary", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_binary_method_req =
            subscription_id_call_one_binary_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_optional_binary_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOptionalBinary", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_binary_method_req =
            subscription_id_call_optional_binary_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_three_binaries_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callThreeBinaries", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_three_binaries_method_req =
            subscription_id_call_three_binaries_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_one_list_of_integers_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOneListOfIntegers", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_one_list_of_integers_method_req =
            subscription_id_call_one_list_of_integers_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_optional_list_of_floats_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callOptionalListOfFloats", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_optional_list_of_floats_method_req =
            subscription_id_call_optional_list_of_floats_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_call_two_lists_method_req = connection
            .subscribe(
                format!("testAble/{}/method/callTwoLists", instance_id),
                QoS::ExactlyOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_call_two_lists_method_req =
            subscription_id_call_two_lists_method_req.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_integer_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteInteger/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_integer_property_update =
            subscription_id_read_write_integer_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_optional_integer_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteOptionalInteger/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_integer_property_update =
            subscription_id_read_write_optional_integer_property_update
                .unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_two_integers_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteTwoIntegers/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_integers_property_update =
            subscription_id_read_write_two_integers_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_string_property_update = connection
            .subscribe(
                format!("testAble/{}/property/readWriteString/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_string_property_update =
            subscription_id_read_write_string_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_optional_string_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteOptionalString/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_string_property_update =
            subscription_id_read_write_optional_string_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_two_strings_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteTwoStrings/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_strings_property_update =
            subscription_id_read_write_two_strings_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_struct_property_update = connection
            .subscribe(
                format!("testAble/{}/property/readWriteStruct/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_struct_property_update =
            subscription_id_read_write_struct_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_optional_struct_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteOptionalStruct/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_struct_property_update =
            subscription_id_read_write_optional_struct_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_two_structs_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteTwoStructs/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_structs_property_update =
            subscription_id_read_write_two_structs_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_enum_property_update = connection
            .subscribe(
                format!("testAble/{}/property/readWriteEnum/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_enum_property_update =
            subscription_id_read_write_enum_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_optional_enum_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteOptionalEnum/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_enum_property_update =
            subscription_id_read_write_optional_enum_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_two_enums_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteTwoEnums/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_enums_property_update =
            subscription_id_read_write_two_enums_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_datetime_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteDatetime/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_datetime_property_update =
            subscription_id_read_write_datetime_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_optional_datetime_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteOptionalDatetime/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_datetime_property_update =
            subscription_id_read_write_optional_datetime_property_update
                .unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_two_datetimes_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteTwoDatetimes/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_datetimes_property_update =
            subscription_id_read_write_two_datetimes_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_duration_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteDuration/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_duration_property_update =
            subscription_id_read_write_duration_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_optional_duration_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteOptionalDuration/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_duration_property_update =
            subscription_id_read_write_optional_duration_property_update
                .unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_two_durations_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteTwoDurations/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_durations_property_update =
            subscription_id_read_write_two_durations_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_binary_property_update = connection
            .subscribe(
                format!("testAble/{}/property/readWriteBinary/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_binary_property_update =
            subscription_id_read_write_binary_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_optional_binary_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteOptionalBinary/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_optional_binary_property_update =
            subscription_id_read_write_optional_binary_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_two_binaries_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteTwoBinaries/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_two_binaries_property_update =
            subscription_id_read_write_two_binaries_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_list_of_strings_property_update = connection
            .subscribe(
                format!(
                    "testAble/{}/property/readWriteListOfStrings/setValue",
                    instance_id
                ),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_list_of_strings_property_update =
            subscription_id_read_write_list_of_strings_property_update.unwrap_or_else(|_| u32::MAX);

        let subscription_id_read_write_lists_property_update = connection
            .subscribe(
                format!("testAble/{}/property/readWriteLists/setValue", instance_id),
                QoS::AtLeastOnce,
                message_received_tx.clone(),
            )
            .await;
        let subscription_id_read_write_lists_property_update =
            subscription_id_read_write_lists_property_update.unwrap_or_else(|_| u32::MAX);

        // Create structure for subscription ids.
        let sub_ids = TestAbleServerSubscriptionIds {
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

        let property_values = TestAbleProperties {
            read_write_integer: Arc::new(AsyncMutex::new(None)),
            read_write_integer_tx_channel: watch::channel(None).0,
            read_write_integer_version: Arc::new(AtomicU32::new(0)),
            read_only_integer: Arc::new(AsyncMutex::new(None)),
            read_only_integer_tx_channel: watch::channel(None).0,
            read_only_integer_version: Arc::new(AtomicU32::new(0)),
            read_write_optional_integer: Arc::new(AsyncMutex::new(None)),
            read_write_optional_integer_tx_channel: watch::channel(None).0,
            read_write_optional_integer_version: Arc::new(AtomicU32::new(0)),
            read_write_two_integers: Arc::new(AsyncMutex::new(None)),
            read_write_two_integers_tx_channel: watch::channel(None).0,
            read_write_two_integers_version: Arc::new(AtomicU32::new(0)),
            read_only_string: Arc::new(AsyncMutex::new(None)),
            read_only_string_tx_channel: watch::channel(None).0,
            read_only_string_version: Arc::new(AtomicU32::new(0)),
            read_write_string: Arc::new(AsyncMutex::new(None)),
            read_write_string_tx_channel: watch::channel(None).0,
            read_write_string_version: Arc::new(AtomicU32::new(0)),
            read_write_optional_string: Arc::new(AsyncMutex::new(None)),
            read_write_optional_string_tx_channel: watch::channel(None).0,
            read_write_optional_string_version: Arc::new(AtomicU32::new(0)),
            read_write_two_strings: Arc::new(AsyncMutex::new(None)),
            read_write_two_strings_tx_channel: watch::channel(None).0,
            read_write_two_strings_version: Arc::new(AtomicU32::new(0)),
            read_write_struct: Arc::new(AsyncMutex::new(None)),
            read_write_struct_tx_channel: watch::channel(None).0,
            read_write_struct_version: Arc::new(AtomicU32::new(0)),
            read_write_optional_struct: Arc::new(AsyncMutex::new(None)),
            read_write_optional_struct_tx_channel: watch::channel(None).0,
            read_write_optional_struct_version: Arc::new(AtomicU32::new(0)),
            read_write_two_structs: Arc::new(AsyncMutex::new(None)),
            read_write_two_structs_tx_channel: watch::channel(None).0,
            read_write_two_structs_version: Arc::new(AtomicU32::new(0)),
            read_only_enum: Arc::new(AsyncMutex::new(None)),
            read_only_enum_tx_channel: watch::channel(None).0,
            read_only_enum_version: Arc::new(AtomicU32::new(0)),
            read_write_enum: Arc::new(AsyncMutex::new(None)),
            read_write_enum_tx_channel: watch::channel(None).0,
            read_write_enum_version: Arc::new(AtomicU32::new(0)),
            read_write_optional_enum: Arc::new(AsyncMutex::new(None)),
            read_write_optional_enum_tx_channel: watch::channel(None).0,
            read_write_optional_enum_version: Arc::new(AtomicU32::new(0)),
            read_write_two_enums: Arc::new(AsyncMutex::new(None)),
            read_write_two_enums_tx_channel: watch::channel(None).0,
            read_write_two_enums_version: Arc::new(AtomicU32::new(0)),
            read_write_datetime: Arc::new(AsyncMutex::new(None)),
            read_write_datetime_tx_channel: watch::channel(None).0,
            read_write_datetime_version: Arc::new(AtomicU32::new(0)),
            read_write_optional_datetime: Arc::new(AsyncMutex::new(None)),
            read_write_optional_datetime_tx_channel: watch::channel(None).0,
            read_write_optional_datetime_version: Arc::new(AtomicU32::new(0)),
            read_write_two_datetimes: Arc::new(AsyncMutex::new(None)),
            read_write_two_datetimes_tx_channel: watch::channel(None).0,
            read_write_two_datetimes_version: Arc::new(AtomicU32::new(0)),
            read_write_duration: Arc::new(AsyncMutex::new(None)),
            read_write_duration_tx_channel: watch::channel(None).0,
            read_write_duration_version: Arc::new(AtomicU32::new(0)),
            read_write_optional_duration: Arc::new(AsyncMutex::new(None)),
            read_write_optional_duration_tx_channel: watch::channel(None).0,
            read_write_optional_duration_version: Arc::new(AtomicU32::new(0)),
            read_write_two_durations: Arc::new(AsyncMutex::new(None)),
            read_write_two_durations_tx_channel: watch::channel(None).0,
            read_write_two_durations_version: Arc::new(AtomicU32::new(0)),
            read_write_binary: Arc::new(AsyncMutex::new(None)),
            read_write_binary_tx_channel: watch::channel(None).0,
            read_write_binary_version: Arc::new(AtomicU32::new(0)),
            read_write_optional_binary: Arc::new(AsyncMutex::new(None)),
            read_write_optional_binary_tx_channel: watch::channel(None).0,
            read_write_optional_binary_version: Arc::new(AtomicU32::new(0)),
            read_write_two_binaries: Arc::new(AsyncMutex::new(None)),
            read_write_two_binaries_tx_channel: watch::channel(None).0,
            read_write_two_binaries_version: Arc::new(AtomicU32::new(0)),
            read_write_list_of_strings: Arc::new(AsyncMutex::new(None)),
            read_write_list_of_strings_tx_channel: watch::channel(None).0,
            read_write_list_of_strings_version: Arc::new(AtomicU32::new(0)),
            read_write_lists: Arc::new(AsyncMutex::new(None)),
            read_write_lists_tx_channel: watch::channel(None).0,
            read_write_lists_version: Arc::new(AtomicU32::new(0)),
        };

        TestAbleServer {
            mqtt_client: connection.clone(),

            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,
            method_handlers: method_handlers,
            properties: property_values,
            subscription_ids: sub_ids,

            client_id: connection.get_client_id(),
            instance_id,
        }
    }

    pub async fn oneshot_to_future(
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

    pub async fn wrap_return_code_in_future(rc: MethodReturnCode) -> SentMessageFuture {
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
        let topic = format!("testAble/{}/signal/empty", self.instance_id);
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
        let topic = format!("testAble/{}/signal/empty", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleInt signal with the given arguments.
    pub async fn emit_single_int(&mut self, value: i32) -> SentMessageFuture {
        let data = SingleIntSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleInt", self.instance_id);
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
        let data = SingleIntSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleInt", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalInt signal with the given arguments.
    pub async fn emit_single_optional_int(&mut self, value: Option<i32>) -> SentMessageFuture {
        let data = SingleOptionalIntSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalInt", self.instance_id);
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
        let data = SingleOptionalIntSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalInt", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeIntegers", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeIntegers", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleString signal with the given arguments.
    pub async fn emit_single_string(&mut self, value: String) -> SentMessageFuture {
        let data = SingleStringSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleString", self.instance_id);
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
        let data = SingleStringSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleString", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalString signal with the given arguments.
    pub async fn emit_single_optional_string(
        &mut self,
        value: Option<String>,
    ) -> SentMessageFuture {
        let data = SingleOptionalStringSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalString", self.instance_id);
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
        let data = SingleOptionalStringSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalString", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeStrings", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeStrings", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleEnum signal with the given arguments.
    pub async fn emit_single_enum(&mut self, value: Numbers) -> SentMessageFuture {
        let data = SingleEnumSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleEnum", self.instance_id);
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
        let data = SingleEnumSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleEnum", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalEnum signal with the given arguments.
    pub async fn emit_single_optional_enum(&mut self, value: Option<Numbers>) -> SentMessageFuture {
        let data = SingleOptionalEnumSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalEnum", self.instance_id);
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
        let data = SingleOptionalEnumSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalEnum", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeEnums", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeEnums", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleStruct signal with the given arguments.
    pub async fn emit_single_struct(&mut self, value: AllTypes) -> SentMessageFuture {
        let data = SingleStructSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleStruct", self.instance_id);
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
        let data = SingleStructSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleStruct", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalStruct signal with the given arguments.
    pub async fn emit_single_optional_struct(
        &mut self,
        value: Option<AllTypes>,
    ) -> SentMessageFuture {
        let data = SingleOptionalStructSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalStruct", self.instance_id);
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
        let data = SingleOptionalStructSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalStruct", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeStructs", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeStructs", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleDateTime signal with the given arguments.
    pub async fn emit_single_date_time(
        &mut self,
        value: chrono::DateTime<chrono::Utc>,
    ) -> SentMessageFuture {
        let data = SingleDateTimeSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleDateTime", self.instance_id);
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
        let data = SingleDateTimeSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleDateTime", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalDatetime signal with the given arguments.
    pub async fn emit_single_optional_datetime(
        &mut self,
        value: Option<chrono::DateTime<chrono::Utc>>,
    ) -> SentMessageFuture {
        let data = SingleOptionalDatetimeSignalPayload { value: value };
        let topic = format!(
            "testAble/{}/signal/singleOptionalDatetime",
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
        let data = SingleOptionalDatetimeSignalPayload { value: value };
        let topic = format!(
            "testAble/{}/signal/singleOptionalDatetime",
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeDateTimes", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeDateTimes", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleDuration signal with the given arguments.
    pub async fn emit_single_duration(&mut self, value: chrono::Duration) -> SentMessageFuture {
        let data = SingleDurationSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleDuration", self.instance_id);
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
        let data = SingleDurationSignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleDuration", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalDuration signal with the given arguments.
    pub async fn emit_single_optional_duration(
        &mut self,
        value: Option<chrono::Duration>,
    ) -> SentMessageFuture {
        let data = SingleOptionalDurationSignalPayload { value: value };
        let topic = format!(
            "testAble/{}/signal/singleOptionalDuration",
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
        let data = SingleOptionalDurationSignalPayload { value: value };
        let topic = format!(
            "testAble/{}/signal/singleOptionalDuration",
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeDurations", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeDurations", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleBinary signal with the given arguments.
    pub async fn emit_single_binary(&mut self, value: Vec<u8>) -> SentMessageFuture {
        let data = SingleBinarySignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleBinary", self.instance_id);
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
        let data = SingleBinarySignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleBinary", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalBinary signal with the given arguments.
    pub async fn emit_single_optional_binary(
        &mut self,
        value: Option<Vec<u8>>,
    ) -> SentMessageFuture {
        let data = SingleOptionalBinarySignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalBinary", self.instance_id);
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
        let data = SingleOptionalBinarySignalPayload { value: value };
        let topic = format!("testAble/{}/signal/singleOptionalBinary", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeBinaries", self.instance_id);
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
            first: first,

            second: second,

            third: third,
        };
        let topic = format!("testAble/{}/signal/threeBinaries", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleArrayOfIntegers signal with the given arguments.
    pub async fn emit_single_array_of_integers(&mut self, values: Vec<i32>) -> SentMessageFuture {
        let data = SingleArrayOfIntegersSignalPayload { values: values };
        let topic = format!("testAble/{}/signal/singleArrayOfIntegers", self.instance_id);
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
        let data = SingleArrayOfIntegersSignalPayload { values: values };
        let topic = format!("testAble/{}/signal/singleArrayOfIntegers", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the singleOptionalArrayOfStrings signal with the given arguments.
    pub async fn emit_single_optional_array_of_strings(
        &mut self,
        values: Option<Vec<String>>,
    ) -> SentMessageFuture {
        let data = SingleOptionalArrayOfStringsSignalPayload { values: values };
        let topic = format!(
            "testAble/{}/signal/singleOptionalArrayOfStrings",
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
        let data = SingleOptionalArrayOfStringsSignalPayload { values: values };
        let topic = format!(
            "testAble/{}/signal/singleOptionalArrayOfStrings",
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
            first_of_integers: first_of_integers,

            second_of_floats: second_of_floats,

            third_of_strings: third_of_strings,

            fourth_of_enums: fourth_of_enums,

            fifth_of_structs: fifth_of_structs,

            sixth_of_datetimes: sixth_of_datetimes,

            seventh_of_durations: seventh_of_durations,

            eighth_of_binaries: eighth_of_binaries,
        };
        let topic = format!("testAble/{}/signal/arrayOfEveryType", self.instance_id);
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
            first_of_integers: first_of_integers,

            second_of_floats: second_of_floats,

            third_of_strings: third_of_strings,

            fourth_of_enums: fourth_of_enums,

            fifth_of_structs: fifth_of_structs,

            sixth_of_datetimes: sixth_of_datetimes,

            seventh_of_durations: seventh_of_durations,

            eighth_of_binaries: eighth_of_binaries,
        };
        let topic = format!("testAble/{}/signal/arrayOfEveryType", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }

    /// Handles a request message for the callWithNothing method.
    async fn handle_call_with_nothing_request(
        mut publisher: C,
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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
        handlers: Arc<AsyncMutex<Box<dyn TestAbleMethodHandlers<C>>>>,
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
            TestAbleServer::<C>::publish_error_response(
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
                    TestAbleServer::<C>::publish_error_response(
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

    async fn publish_read_write_integer_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteIntegerProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_integer_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteIntegerProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<i32>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteIntegerProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_integer' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_integer' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_integer' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_integer_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_integer(&self) -> watch::Receiver<Option<i32>> {
        self.properties.read_write_integer_tx_channel.subscribe()
    }

    /// Sets the value of the read_write_integer property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_integer(&mut self, data: i32) -> SentMessageFuture {
        let prop = self.properties.read_write_integer.clone();

        let new_prop_obj = ReadWriteIntegerProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_integer_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_integer' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteInteger/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_integer_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_integer_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_only_integer_value(
        mut publisher: C,
        topic: String,
        data: ReadOnlyIntegerProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// Sets the value of the read_only_integer property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_only_integer(&mut self, data: i32) -> SentMessageFuture {
        let prop = self.properties.read_only_integer.clone();

        let new_prop_obj = ReadOnlyIntegerProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_only_integer_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_only_integer' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readOnlyInteger/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_only_integer_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_only_integer_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_optional_integer_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteOptionalIntegerProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_integer_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteOptionalIntegerProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Option<i32>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteOptionalIntegerProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_optional_integer' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_integer' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'read_write_optional_integer' property: {:?}", e);
            }
        };

        TestAbleServer::publish_read_write_optional_integer_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_optional_integer(&self) -> watch::Receiver<Option<Option<i32>>> {
        self.properties
            .read_write_optional_integer_tx_channel
            .subscribe()
    }

    /// Sets the value of the read_write_optional_integer property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_optional_integer(
        &mut self,
        data: Option<i32>,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_optional_integer.clone();

        let new_prop_obj = ReadWriteOptionalIntegerProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_optional_integer_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_optional_integer' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteOptionalInteger/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_optional_integer_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_optional_integer_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_two_integers_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteTwoIntegersProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_integers_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteTwoIntegersProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<ReadWriteTwoIntegersProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteTwoIntegersProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_two_integers' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_integers' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_two_integers' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_two_integers_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_two_integers(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoIntegersProperty>> {
        self.properties
            .read_write_two_integers_tx_channel
            .subscribe()
    }

    /// Sets the values of the read_write_two_integers property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_two_integers(
        &mut self,
        data: ReadWriteTwoIntegersProperty,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_two_integers.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result = self
            .properties
            .read_write_two_integers_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!(
                "Property 'read_write_two_integers' value not changed, so not notifying watchers."
            );
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteTwoIntegers/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_two_integers_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_two_integers_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_only_string_value(
        mut publisher: C,
        topic: String,
        data: ReadOnlyStringProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// Sets the value of the read_only_string property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_only_string(&mut self, data: String) -> SentMessageFuture {
        let prop = self.properties.read_only_string.clone();

        let new_prop_obj = ReadOnlyStringProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_only_string_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_only_string' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readOnlyString/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_only_string_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_only_string_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_string_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteStringProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_string_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteStringProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<String>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteStringProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_string' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_string' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_string' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_string_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_string(&self) -> watch::Receiver<Option<String>> {
        self.properties.read_write_string_tx_channel.subscribe()
    }

    /// Sets the value of the read_write_string property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_string(&mut self, data: String) -> SentMessageFuture {
        let prop = self.properties.read_write_string.clone();

        let new_prop_obj = ReadWriteStringProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_string_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_string' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteString/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_string_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_string_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_optional_string_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteOptionalStringProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_string_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteOptionalStringProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Option<String>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteOptionalStringProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_optional_string' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_string' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'read_write_optional_string' property: {:?}", e);
            }
        };

        TestAbleServer::publish_read_write_optional_string_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_optional_string(
        &self,
    ) -> watch::Receiver<Option<Option<String>>> {
        self.properties
            .read_write_optional_string_tx_channel
            .subscribe()
    }

    /// Sets the value of the read_write_optional_string property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_optional_string(
        &mut self,
        data: Option<String>,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_optional_string.clone();

        let new_prop_obj = ReadWriteOptionalStringProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_optional_string_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_optional_string' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteOptionalString/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_optional_string_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_optional_string_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_two_strings_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteTwoStringsProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_strings_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteTwoStringsProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<ReadWriteTwoStringsProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteTwoStringsProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_two_strings' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_strings' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_two_strings' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_two_strings_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_two_strings(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoStringsProperty>> {
        self.properties
            .read_write_two_strings_tx_channel
            .subscribe()
    }

    /// Sets the values of the read_write_two_strings property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_two_strings(
        &mut self,
        data: ReadWriteTwoStringsProperty,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_two_strings.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result = self
            .properties
            .read_write_two_strings_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!(
                "Property 'read_write_two_strings' value not changed, so not notifying watchers."
            );
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteTwoStrings/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_two_strings_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_two_strings_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_struct_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteStructProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_struct_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteStructProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<AllTypes>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteStructProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_struct' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_struct' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_struct' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_struct_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_struct(&self) -> watch::Receiver<Option<AllTypes>> {
        self.properties.read_write_struct_tx_channel.subscribe()
    }

    /// Sets the value of the read_write_struct property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_struct(&mut self, data: AllTypes) -> SentMessageFuture {
        let prop = self.properties.read_write_struct.clone();

        let new_prop_obj = ReadWriteStructProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_struct_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_struct' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteStruct/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_struct_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_struct_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_optional_struct_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteOptionalStructProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_struct_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteOptionalStructProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Option<AllTypes>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteOptionalStructProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_optional_struct' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_struct' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'read_write_optional_struct' property: {:?}", e);
            }
        };

        TestAbleServer::publish_read_write_optional_struct_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_optional_struct(
        &self,
    ) -> watch::Receiver<Option<Option<AllTypes>>> {
        self.properties
            .read_write_optional_struct_tx_channel
            .subscribe()
    }

    /// Sets the value of the read_write_optional_struct property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_optional_struct(
        &mut self,
        data: Option<AllTypes>,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_optional_struct.clone();

        let new_prop_obj = ReadWriteOptionalStructProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_optional_struct_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_optional_struct' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteOptionalStruct/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_optional_struct_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_optional_struct_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_two_structs_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteTwoStructsProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_structs_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteTwoStructsProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<ReadWriteTwoStructsProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteTwoStructsProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_two_structs' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_structs' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_two_structs' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_two_structs_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_two_structs(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoStructsProperty>> {
        self.properties
            .read_write_two_structs_tx_channel
            .subscribe()
    }

    /// Sets the values of the read_write_two_structs property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_two_structs(
        &mut self,
        data: ReadWriteTwoStructsProperty,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_two_structs.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result = self
            .properties
            .read_write_two_structs_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!(
                "Property 'read_write_two_structs' value not changed, so not notifying watchers."
            );
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteTwoStructs/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_two_structs_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_two_structs_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_only_enum_value(
        mut publisher: C,
        topic: String,
        data: ReadOnlyEnumProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// Sets the value of the read_only_enum property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_only_enum(&mut self, data: Numbers) -> SentMessageFuture {
        let prop = self.properties.read_only_enum.clone();

        let new_prop_obj = ReadOnlyEnumProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result =
            self.properties
                .read_only_enum_tx_channel
                .send_if_modified(|current_data| {
                    if current_data != &data_to_send_to_watchers {
                        *current_data = data_to_send_to_watchers;
                        true
                    } else {
                        false
                    }
                });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_only_enum' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!("testAble/{}/property/readOnlyEnum/value", self.instance_id);
                let new_version = self
                    .properties
                    .read_only_enum_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_only_enum_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_enum_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteEnumProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_enum_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteEnumProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Numbers>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteEnumProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_enum' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_enum' payload".to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_enum' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_enum_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_enum(&self) -> watch::Receiver<Option<Numbers>> {
        self.properties.read_write_enum_tx_channel.subscribe()
    }

    /// Sets the value of the read_write_enum property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_enum(&mut self, data: Numbers) -> SentMessageFuture {
        let prop = self.properties.read_write_enum.clone();

        let new_prop_obj = ReadWriteEnumProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result =
            self.properties
                .read_write_enum_tx_channel
                .send_if_modified(|current_data| {
                    if current_data != &data_to_send_to_watchers {
                        *current_data = data_to_send_to_watchers;
                        true
                    } else {
                        false
                    }
                });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_enum' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!("testAble/{}/property/readWriteEnum/value", self.instance_id);
                let new_version = self
                    .properties
                    .read_write_enum_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_enum_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_optional_enum_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteOptionalEnumProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_enum_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteOptionalEnumProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Option<Numbers>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteOptionalEnumProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_optional_enum' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_enum' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_optional_enum' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_optional_enum_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_optional_enum(&self) -> watch::Receiver<Option<Option<Numbers>>> {
        self.properties
            .read_write_optional_enum_tx_channel
            .subscribe()
    }

    /// Sets the value of the read_write_optional_enum property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_optional_enum(
        &mut self,
        data: Option<Numbers>,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_optional_enum.clone();

        let new_prop_obj = ReadWriteOptionalEnumProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_optional_enum_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!(
                "Property 'read_write_optional_enum' value not changed, so not notifying watchers."
            );
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteOptionalEnum/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_optional_enum_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_optional_enum_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_two_enums_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteTwoEnumsProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_enums_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteTwoEnumsProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<ReadWriteTwoEnumsProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteTwoEnumsProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_two_enums' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_enums' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_two_enums' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_two_enums_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_two_enums(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoEnumsProperty>> {
        self.properties.read_write_two_enums_tx_channel.subscribe()
    }

    /// Sets the values of the read_write_two_enums property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_two_enums(
        &mut self,
        data: ReadWriteTwoEnumsProperty,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_two_enums.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result = self
            .properties
            .read_write_two_enums_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_two_enums' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteTwoEnums/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_two_enums_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_two_enums_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_datetime_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteDatetimeProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_datetime_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteDatetimeProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<chrono::DateTime<chrono::Utc>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteDatetimeProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_datetime' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_datetime' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_datetime' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_datetime_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_datetime(
        &self,
    ) -> watch::Receiver<Option<chrono::DateTime<chrono::Utc>>> {
        self.properties.read_write_datetime_tx_channel.subscribe()
    }

    /// Sets the value of the read_write_datetime property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_datetime(
        &mut self,
        data: chrono::DateTime<chrono::Utc>,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_datetime.clone();

        let new_prop_obj = ReadWriteDatetimeProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_datetime_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_datetime' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteDatetime/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_datetime_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_datetime_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_optional_datetime_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteOptionalDatetimeProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_datetime_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteOptionalDatetimeProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Option<chrono::DateTime<chrono::Utc>>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteOptionalDatetimeProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_optional_datetime' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_datetime' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'read_write_optional_datetime' property: {:?}", e);
            }
        };

        TestAbleServer::publish_read_write_optional_datetime_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_optional_datetime(
        &self,
    ) -> watch::Receiver<Option<Option<chrono::DateTime<chrono::Utc>>>> {
        self.properties
            .read_write_optional_datetime_tx_channel
            .subscribe()
    }

    /// Sets the value of the read_write_optional_datetime property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_optional_datetime(
        &mut self,
        data: Option<chrono::DateTime<chrono::Utc>>,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_optional_datetime.clone();

        let new_prop_obj = ReadWriteOptionalDatetimeProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_optional_datetime_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_optional_datetime' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteOptionalDatetime/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_optional_datetime_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_optional_datetime_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_two_datetimes_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteTwoDatetimesProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_datetimes_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteTwoDatetimesProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<ReadWriteTwoDatetimesProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteTwoDatetimesProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_two_datetimes' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_datetimes' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_two_datetimes' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_two_datetimes_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_two_datetimes(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoDatetimesProperty>> {
        self.properties
            .read_write_two_datetimes_tx_channel
            .subscribe()
    }

    /// Sets the values of the read_write_two_datetimes property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_two_datetimes(
        &mut self,
        data: ReadWriteTwoDatetimesProperty,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_two_datetimes.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result = self
            .properties
            .read_write_two_datetimes_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!(
                "Property 'read_write_two_datetimes' value not changed, so not notifying watchers."
            );
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteTwoDatetimes/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_two_datetimes_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_two_datetimes_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_duration_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteDurationProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_duration_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteDurationProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<chrono::Duration>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteDurationProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_duration' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_duration' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_duration' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_duration_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_duration(&self) -> watch::Receiver<Option<chrono::Duration>> {
        self.properties.read_write_duration_tx_channel.subscribe()
    }

    /// Sets the value of the read_write_duration property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_duration(&mut self, data: chrono::Duration) -> SentMessageFuture {
        let prop = self.properties.read_write_duration.clone();

        let new_prop_obj = ReadWriteDurationProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_duration_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_duration' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteDuration/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_duration_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_duration_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_optional_duration_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteOptionalDurationProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_duration_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteOptionalDurationProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Option<chrono::Duration>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteOptionalDurationProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_optional_duration' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_duration' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'read_write_optional_duration' property: {:?}", e);
            }
        };

        TestAbleServer::publish_read_write_optional_duration_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_optional_duration(
        &self,
    ) -> watch::Receiver<Option<Option<chrono::Duration>>> {
        self.properties
            .read_write_optional_duration_tx_channel
            .subscribe()
    }

    /// Sets the value of the read_write_optional_duration property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_optional_duration(
        &mut self,
        data: Option<chrono::Duration>,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_optional_duration.clone();

        let new_prop_obj = ReadWriteOptionalDurationProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_optional_duration_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_optional_duration' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteOptionalDuration/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_optional_duration_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_optional_duration_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_two_durations_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteTwoDurationsProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_durations_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteTwoDurationsProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<ReadWriteTwoDurationsProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteTwoDurationsProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_two_durations' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_durations' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_two_durations' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_two_durations_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_two_durations(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoDurationsProperty>> {
        self.properties
            .read_write_two_durations_tx_channel
            .subscribe()
    }

    /// Sets the values of the read_write_two_durations property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_two_durations(
        &mut self,
        data: ReadWriteTwoDurationsProperty,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_two_durations.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result = self
            .properties
            .read_write_two_durations_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!(
                "Property 'read_write_two_durations' value not changed, so not notifying watchers."
            );
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteTwoDurations/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_two_durations_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_two_durations_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_binary_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteBinaryProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_binary_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteBinaryProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Vec<u8>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteBinaryProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_binary' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_binary' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_binary' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_binary_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_binary(&self) -> watch::Receiver<Option<Vec<u8>>> {
        self.properties.read_write_binary_tx_channel.subscribe()
    }

    /// Sets the value of the read_write_binary property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_binary(&mut self, data: Vec<u8>) -> SentMessageFuture {
        let prop = self.properties.read_write_binary.clone();

        let new_prop_obj = ReadWriteBinaryProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_binary_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_binary' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteBinary/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_binary_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_binary_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_optional_binary_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteOptionalBinaryProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_optional_binary_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteOptionalBinaryProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Option<Vec<u8>>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteOptionalBinaryProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_optional_binary' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_optional_binary' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'read_write_optional_binary' property: {:?}", e);
            }
        };

        TestAbleServer::publish_read_write_optional_binary_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_optional_binary(
        &self,
    ) -> watch::Receiver<Option<Option<Vec<u8>>>> {
        self.properties
            .read_write_optional_binary_tx_channel
            .subscribe()
    }

    /// Sets the value of the read_write_optional_binary property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_optional_binary(
        &mut self,
        data: Option<Vec<u8>>,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_optional_binary.clone();

        let new_prop_obj = ReadWriteOptionalBinaryProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_optional_binary_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_optional_binary' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteOptionalBinary/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_optional_binary_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_optional_binary_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_two_binaries_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteTwoBinariesProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_two_binaries_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteTwoBinariesProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<ReadWriteTwoBinariesProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteTwoBinariesProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_two_binaries' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_two_binaries' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_two_binaries' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_two_binaries_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_two_binaries(
        &self,
    ) -> watch::Receiver<Option<ReadWriteTwoBinariesProperty>> {
        self.properties
            .read_write_two_binaries_tx_channel
            .subscribe()
    }

    /// Sets the values of the read_write_two_binaries property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_two_binaries(
        &mut self,
        data: ReadWriteTwoBinariesProperty,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_two_binaries.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result = self
            .properties
            .read_write_two_binaries_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!(
                "Property 'read_write_two_binaries' value not changed, so not notifying watchers."
            );
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteTwoBinaries/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_two_binaries_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_two_binaries_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_list_of_strings_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteListOfStringsProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_list_of_strings_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteListOfStringsProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<Vec<String>>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteListOfStringsProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_list_of_strings' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_list_of_strings' payload"
                                .to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.value.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!("Failed to notify local watchers for 'read_write_list_of_strings' property: {:?}", e);
            }
        };

        TestAbleServer::publish_read_write_list_of_strings_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_list_of_strings(&self) -> watch::Receiver<Option<Vec<String>>> {
        self.properties
            .read_write_list_of_strings_tx_channel
            .subscribe()
    }

    /// Sets the value of the read_write_list_of_strings property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_list_of_strings(&mut self, data: Vec<String>) -> SentMessageFuture {
        let prop = self.properties.read_write_list_of_strings.clone();

        let new_prop_obj = ReadWriteListOfStringsProperty {
            value: data.clone(),
        };

        // Set the server's copy of the property value.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = Some(data.clone());
        let send_result = self
            .properties
            .read_write_list_of_strings_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_list_of_strings' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteListOfStrings/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_list_of_strings_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_list_of_strings_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
    }

    async fn publish_read_write_lists_value(
        mut publisher: C,
        topic: String,
        data: ReadWriteListsProperty,
        property_version: u32,
    ) -> SentMessageFuture {
        let msg = message::property_value_message(&topic, &data, property_version).unwrap();
        let ch = publisher.publish_noblock(msg).await;
        TestAbleServer::<C>::oneshot_to_future(ch).await
    }

    /// This is called because of an MQTT request to update the property value.
    /// It updates the local value, notifies any watchers, and publishes the new value.
    /// If there is an error, it can publish back if a response topic was provided.
    async fn update_read_write_lists_value(
        publisher: C,
        topic: String,
        property_pointer: Arc<AsyncMutex<Option<ReadWriteListsProperty>>>,
        property_version: Arc<AtomicU32>,
        watch_sender: watch::Sender<Option<ReadWriteListsProperty>>,
        msg: MqttMessage,
    ) -> SentMessageFuture {
        let payload_str = String::from_utf8_lossy(&msg.payload).to_string();
        let new_version = property_version.fetch_add(1, Ordering::SeqCst);
        let new_property_structure: ReadWriteListsProperty = {
            match serde_json::from_str(&payload_str) {
                Ok(obj) => obj,
                Err(e) => {
                    error!("Failed to parse JSON received over MQTT to update 'read_write_lists' property: {:?}", e);
                    return TestAbleServer::<C>::wrap_return_code_in_future(
                        MethodReturnCode::ServerDeserializationError(
                            "Failed to deserialize property 'read_write_lists' payload".to_string(),
                        ),
                    )
                    .await;
                }
            }
        };

        let mut property_guard = property_pointer.lock().await;
        *property_guard = Some(new_property_structure.clone());
        drop(property_guard);

        let topic2: String = topic.clone();
        let data_to_send_to_watchers = new_property_structure.clone();
        match watch_sender.send(Some(data_to_send_to_watchers)) {
            Ok(_) => {}
            Err(e) => {
                error!(
                    "Failed to notify local watchers for 'read_write_lists' property: {:?}",
                    e
                );
            }
        };

        TestAbleServer::publish_read_write_lists_value(
            publisher,
            topic2,
            new_property_structure,
            new_version,
        )
        .await
    }

    pub async fn watch_read_write_lists(&self) -> watch::Receiver<Option<ReadWriteListsProperty>> {
        self.properties.read_write_lists_tx_channel.subscribe()
    }

    /// Sets the values of the read_write_lists property.
    /// As a consequence, it notifies any watchers and publishes the new value to MQTT.
    pub async fn set_read_write_lists(
        &mut self,
        data: ReadWriteListsProperty,
    ) -> SentMessageFuture {
        let prop = self.properties.read_write_lists.clone();

        let new_prop_obj = data.clone();

        // Set the server's copy of the property values.
        let mut property_data_guard = prop.lock().await;
        *property_data_guard = Some(new_prop_obj.clone());
        let property_obj = property_data_guard.clone();
        drop(property_data_guard);

        // Notify watchers of the new property value.
        let data_to_send_to_watchers = property_obj.clone();
        let send_result = self
            .properties
            .read_write_lists_tx_channel
            .send_if_modified(|current_data| {
                if current_data != &data_to_send_to_watchers {
                    *current_data = data_to_send_to_watchers;
                    true
                } else {
                    false
                }
            });

        // Send value to MQTT if it has changed.
        if !send_result {
            debug!("Property 'read_write_lists' value not changed, so not notifying watchers.");
            return TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::Success(
                None,
            ))
            .await;
        } else {
            if let Some(prop_obj) = property_obj {
                let publisher2 = self.mqtt_client.clone();
                let topic2 = format!(
                    "testAble/{}/property/readWriteLists/value",
                    self.instance_id
                );
                let new_version = self
                    .properties
                    .read_write_lists_version
                    .fetch_add(1, std::sync::atomic::Ordering::SeqCst);
                TestAbleServer::<C>::publish_read_write_lists_value(
                    publisher2,
                    topic2,
                    prop_obj,
                    new_version,
                )
                .await
            } else {
                TestAbleServer::<C>::wrap_return_code_in_future(MethodReturnCode::UnknownError(
                    "Could not find property object".to_string(),
                ))
                .await
            }
        }
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

        let properties = self.properties.clone();

        // Spawn a task to periodically publish interface info.
        let mut interface_publisher = self.mqtt_client.clone();
        let instance_id = self.instance_id.clone();
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(std::time::Duration::from_secs(120));
            loop {
                interval.tick().await;
                let topic = format!("testAble/{}/interface", instance_id);
                let info = crate::interface::InterfaceInfoBuilder::default()
                    .interface_name("Test Able".to_string())
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

        let instance_id = self.instance_id.clone();
        let loop_task = tokio::spawn(async move {
            loop {
                match message_receiver.recv().await {
                    Ok(msg) => {
                        let opt_resp_topic = msg.response_topic.clone();
                        let opt_corr_data = msg.correlation_data.clone();

                        if let Some(subscription_id) = msg.subscription_id {
                            if subscription_id == sub_ids.call_with_nothing_method_req {
                                TestAbleServer::<C>::handle_call_with_nothing_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_one_integer_method_req {
                                TestAbleServer::<C>::handle_call_one_integer_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_optional_integer_method_req {
                                TestAbleServer::<C>::handle_call_optional_integer_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_three_integers_method_req {
                                TestAbleServer::<C>::handle_call_three_integers_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_one_string_method_req {
                                TestAbleServer::<C>::handle_call_one_string_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_optional_string_method_req {
                                TestAbleServer::<C>::handle_call_optional_string_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_three_strings_method_req {
                                TestAbleServer::<C>::handle_call_three_strings_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_one_enum_method_req {
                                TestAbleServer::<C>::handle_call_one_enum_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_optional_enum_method_req {
                                TestAbleServer::<C>::handle_call_optional_enum_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_three_enums_method_req {
                                TestAbleServer::<C>::handle_call_three_enums_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_one_struct_method_req {
                                TestAbleServer::<C>::handle_call_one_struct_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_optional_struct_method_req {
                                TestAbleServer::<C>::handle_call_optional_struct_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_three_structs_method_req {
                                TestAbleServer::<C>::handle_call_three_structs_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_one_date_time_method_req {
                                TestAbleServer::<C>::handle_call_one_date_time_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_optional_date_time_method_req
                            {
                                TestAbleServer::<C>::handle_call_optional_date_time_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_three_date_times_method_req {
                                TestAbleServer::<C>::handle_call_three_date_times_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_one_duration_method_req {
                                TestAbleServer::<C>::handle_call_one_duration_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_optional_duration_method_req {
                                TestAbleServer::<C>::handle_call_optional_duration_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_three_durations_method_req {
                                TestAbleServer::<C>::handle_call_three_durations_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_one_binary_method_req {
                                TestAbleServer::<C>::handle_call_one_binary_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_optional_binary_method_req {
                                TestAbleServer::<C>::handle_call_optional_binary_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_three_binaries_method_req {
                                TestAbleServer::<C>::handle_call_three_binaries_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id
                                == sub_ids.call_one_list_of_integers_method_req
                            {
                                TestAbleServer::<C>::handle_call_one_list_of_integers_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id
                                == sub_ids.call_optional_list_of_floats_method_req
                            {
                                TestAbleServer::<C>::handle_call_optional_list_of_floats_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else if subscription_id == sub_ids.call_two_lists_method_req {
                                TestAbleServer::<C>::handle_call_two_lists_request(
                                    publisher.clone(),
                                    method_handlers.clone(),
                                    msg,
                                )
                                .await;
                            } else {
                                let update_prop_future = {
                                    if subscription_id == sub_ids.read_write_integer_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteInteger/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_integer_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_integer.clone(),
                                            properties.read_write_integer_version.clone(),
                                            properties.read_write_integer_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_optional_integer_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteOptionalInteger/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_optional_integer_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.read_write_optional_integer.clone(),
                                                    properties.read_write_optional_integer_version.clone(),
                                                    properties.read_write_optional_integer_tx_channel.clone(),
                                                    msg).await
                                    } else if subscription_id
                                        == sub_ids.read_write_two_integers_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteTwoIntegers/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_two_integers_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_two_integers.clone(),
                                            properties.read_write_two_integers_version.clone(),
                                            properties.read_write_two_integers_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_string_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteString/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_string_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_string.clone(),
                                            properties.read_write_string_version.clone(),
                                            properties.read_write_string_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_optional_string_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteOptionalString/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_optional_string_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.read_write_optional_string.clone(),
                                                    properties.read_write_optional_string_version.clone(),
                                                    properties.read_write_optional_string_tx_channel.clone(),
                                                    msg).await
                                    } else if subscription_id
                                        == sub_ids.read_write_two_strings_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteTwoStrings/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_two_strings_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_two_strings.clone(),
                                            properties.read_write_two_strings_version.clone(),
                                            properties.read_write_two_strings_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_struct_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteStruct/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_struct_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_struct.clone(),
                                            properties.read_write_struct_version.clone(),
                                            properties.read_write_struct_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_optional_struct_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteOptionalStruct/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_optional_struct_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.read_write_optional_struct.clone(),
                                                    properties.read_write_optional_struct_version.clone(),
                                                    properties.read_write_optional_struct_tx_channel.clone(),
                                                    msg).await
                                    } else if subscription_id
                                        == sub_ids.read_write_two_structs_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteTwoStructs/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_two_structs_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_two_structs.clone(),
                                            properties.read_write_two_structs_version.clone(),
                                            properties.read_write_two_structs_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_enum_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteEnum/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_enum_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_enum.clone(),
                                            properties.read_write_enum_version.clone(),
                                            properties.read_write_enum_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_optional_enum_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteOptionalEnum/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_optional_enum_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_optional_enum.clone(),
                                            properties.read_write_optional_enum_version.clone(),
                                            properties.read_write_optional_enum_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_two_enums_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteTwoEnums/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_two_enums_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_two_enums.clone(),
                                            properties.read_write_two_enums_version.clone(),
                                            properties.read_write_two_enums_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_datetime_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteDatetime/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_datetime_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_datetime.clone(),
                                            properties.read_write_datetime_version.clone(),
                                            properties.read_write_datetime_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_optional_datetime_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteOptionalDatetime/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_optional_datetime_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.read_write_optional_datetime.clone(),
                                                    properties.read_write_optional_datetime_version.clone(),
                                                    properties.read_write_optional_datetime_tx_channel.clone(),
                                                    msg).await
                                    } else if subscription_id
                                        == sub_ids.read_write_two_datetimes_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteTwoDatetimes/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_two_datetimes_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_two_datetimes.clone(),
                                            properties.read_write_two_datetimes_version.clone(),
                                            properties.read_write_two_datetimes_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_duration_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteDuration/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_duration_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_duration.clone(),
                                            properties.read_write_duration_version.clone(),
                                            properties.read_write_duration_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_optional_duration_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteOptionalDuration/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_optional_duration_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.read_write_optional_duration.clone(),
                                                    properties.read_write_optional_duration_version.clone(),
                                                    properties.read_write_optional_duration_tx_channel.clone(),
                                                    msg).await
                                    } else if subscription_id
                                        == sub_ids.read_write_two_durations_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteTwoDurations/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_two_durations_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_two_durations.clone(),
                                            properties.read_write_two_durations_version.clone(),
                                            properties.read_write_two_durations_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_binary_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteBinary/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_binary_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_binary.clone(),
                                            properties.read_write_binary_version.clone(),
                                            properties.read_write_binary_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_optional_binary_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteOptionalBinary/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_optional_binary_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.read_write_optional_binary.clone(),
                                                    properties.read_write_optional_binary_version.clone(),
                                                    properties.read_write_optional_binary_tx_channel.clone(),
                                                    msg).await
                                    } else if subscription_id
                                        == sub_ids.read_write_two_binaries_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteTwoBinaries/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_two_binaries_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_two_binaries.clone(),
                                            properties.read_write_two_binaries_version.clone(),
                                            properties.read_write_two_binaries_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else if subscription_id
                                        == sub_ids.read_write_list_of_strings_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteListOfStrings/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_list_of_strings_value(
                                                    publisher.clone(),
                                                    prop_topic,
                                                    properties.read_write_list_of_strings.clone(),
                                                    properties.read_write_list_of_strings_version.clone(),
                                                    properties.read_write_list_of_strings_tx_channel.clone(),
                                                    msg).await
                                    } else if subscription_id
                                        == sub_ids.read_write_lists_property_update
                                    {
                                        let prop_topic = format!(
                                            "testAble/{}/property/readWriteLists/value",
                                            instance_id
                                        );
                                        TestAbleServer::<C>::update_read_write_lists_value(
                                            publisher.clone(),
                                            prop_topic,
                                            properties.read_write_lists.clone(),
                                            properties.read_write_lists_version.clone(),
                                            properties.read_write_lists_tx_channel.clone(),
                                            msg,
                                        )
                                        .await
                                    } else {
                                        TestAbleServer::<C>::wrap_return_code_in_future(
                                            MethodReturnCode::NotImplemented(
                                                "Could not find a property matching the request"
                                                    .to_string(),
                                            ),
                                        )
                                        .await
                                    }
                                };
                                match update_prop_future.await {
                                    Ok(_) => debug!("Successfully processed update  property"),
                                    Err(e) => {
                                        error!("Error processing update to '' property: {:?}", e);
                                        if let Some(resp_topic) = opt_resp_topic {
                                            TestAbleServer::<C>::publish_error_response(
                                                publisher.clone(),
                                                Some(resp_topic),
                                                opt_corr_data,
                                                e,
                                            )
                                            .await;
                                        } else {
                                            warn!("No response topic found in message properties; cannot send error response.");
                                        }
                                    }
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
pub trait TestAbleMethodHandlers<C: Mqtt5PubSub>: Send + Sync {
    async fn initialize(&mut self, server: TestAbleServer<C>) -> Result<(), MethodReturnCode>;

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
