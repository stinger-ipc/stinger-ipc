//! Client module for SignalOnly IPC
//!
//! This module is only available when the "client" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
*/
#[cfg(feature = "client")]
use mqttier::{MqttierClient, ReceivedMessage};
use serde_json;

#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
#[allow(unused_imports)]
use iso8601_duration::Duration as IsoDuration;
use std::sync::{Arc, Mutex};
use tokio::sync::{broadcast, mpsc};
use tokio::task::JoinError;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct SignalOnlySubscriptionIds {
    another_signal_signal: Option<usize>,
    bark_signal: Option<usize>,
    maybe_number_signal: Option<usize>,
    maybe_name_signal: Option<usize>,
    now_signal: Option<usize>,
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When SignalOnlyClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct SignalOnlySignalChannels {
    another_signal_sender: broadcast::Sender<AnotherSignalSignalPayload>,
    bark_sender: broadcast::Sender<String>,
    maybe_number_sender: broadcast::Sender<Option<i32>>,
    maybe_name_sender: broadcast::Sender<Option<String>>,
    now_sender: broadcast::Sender<chrono::DateTime<chrono::Utc>>,
}

/// This is the struct for our API client.
#[derive(Clone)]
pub struct SignalOnlyClient {
    mqttier_client: MqttierClient,

    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Arc<Mutex<Option<mpsc::Receiver<ReceivedMessage>>>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    #[allow(dead_code)]
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: SignalOnlySubscriptionIds,
    /// Holds the channels used for sending signals to the application.
    signal_channels: SignalOnlySignalChannels,

    /// Copy of MQTT Client ID
    pub client_id: String,
}

impl SignalOnlyClient {
    /// Creates a new SignalOnlyClient that uses an MqttierClient.
    pub async fn new(connection: &mut MqttierClient, service_id: String) -> Self {
        // Create a channel for messages to get from the Connection object to this SignalOnlyClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        // Subscribe to all the topics needed for signals.
        let topic_another_signal_signal = format!("signalOnly/{}/signal/anotherSignal", service_id);
        let subscription_id_another_signal_signal = connection
            .subscribe(topic_another_signal_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_another_signal_signal =
            subscription_id_another_signal_signal.unwrap_or_else(|_| usize::MAX);
        let topic_bark_signal = format!("signalOnly/{}/signal/bark", service_id);
        let subscription_id_bark_signal = connection
            .subscribe(topic_bark_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_bark_signal =
            subscription_id_bark_signal.unwrap_or_else(|_| usize::MAX);
        let topic_maybe_number_signal = format!("signalOnly/{}/signal/maybeNumber", service_id);
        let subscription_id_maybe_number_signal = connection
            .subscribe(topic_maybe_number_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_maybe_number_signal =
            subscription_id_maybe_number_signal.unwrap_or_else(|_| usize::MAX);
        let topic_maybe_name_signal = format!("signalOnly/{}/signal/maybeName", service_id);
        let subscription_id_maybe_name_signal = connection
            .subscribe(topic_maybe_name_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_maybe_name_signal =
            subscription_id_maybe_name_signal.unwrap_or_else(|_| usize::MAX);
        let topic_now_signal = format!("signalOnly/{}/signal/now", service_id);
        let subscription_id_now_signal = connection
            .subscribe(topic_now_signal, 2, message_received_tx.clone())
            .await;
        let subscription_id_now_signal = subscription_id_now_signal.unwrap_or_else(|_| usize::MAX);

        // Subscribe to all the topics needed for properties.

        // Create structure for subscription ids.
        let sub_ids = SignalOnlySubscriptionIds {
            another_signal_signal: Some(subscription_id_another_signal_signal),
            bark_signal: Some(subscription_id_bark_signal),
            maybe_number_signal: Some(subscription_id_maybe_number_signal),
            maybe_name_signal: Some(subscription_id_maybe_name_signal),
            now_signal: Some(subscription_id_now_signal),
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = SignalOnlySignalChannels {
            another_signal_sender: broadcast::channel(64).0,
            bark_sender: broadcast::channel(64).0,
            maybe_number_sender: broadcast::channel(64).0,
            maybe_name_sender: broadcast::channel(64).0,
            now_sender: broadcast::channel(64).0,
        };

        // Create SignalOnlyClient structure.
        let inst = SignalOnlyClient {
            mqttier_client: connection.clone(),

            msg_streamer_rx: Arc::new(Mutex::new(Some(message_received_rx))),
            msg_streamer_tx: message_received_tx,

            subscription_ids: sub_ids,
            signal_channels: signal_channels,
            client_id: connection.client_id.to_string(),
        };
        inst
    }

    /// Get the RX receiver side of the broadcast channel for the anotherSignal signal.
    /// The signal payload, `AnotherSignalSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_another_signal_receiver(&self) -> broadcast::Receiver<AnotherSignalSignalPayload> {
        self.signal_channels.another_signal_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the bark signal.
    /// The signal payload, `BarkSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_bark_receiver(&self) -> broadcast::Receiver<String> {
        self.signal_channels.bark_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the maybe_number signal.
    /// The signal payload, `MaybeNumberSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_maybe_number_receiver(&self) -> broadcast::Receiver<Option<i32>> {
        self.signal_channels.maybe_number_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the maybe_name signal.
    /// The signal payload, `MaybeNameSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_maybe_name_receiver(&self) -> broadcast::Receiver<Option<String>> {
        self.signal_channels.maybe_name_sender.subscribe()
    }
    /// Get the RX receiver side of the broadcast channel for the now signal.
    /// The signal payload, `NowSignalPayload`, will be put onto the channel whenever it is received.
    pub fn get_now_receiver(&self) -> broadcast::Receiver<chrono::DateTime<chrono::Utc>> {
        self.signal_channels.now_sender.subscribe()
    }

    /// Starts the tasks that process messages received.
    pub async fn run_loop(&self) -> Result<(), JoinError> {
        // Make sure the MqttierClient is connected and running.
        let _ = self.mqttier_client.run_loop().await;

        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = {
            let mut guard = self.msg_streamer_rx.lock().expect("Mutex was poisoned");
            guard.take().expect("msg_streamer_rx should be Some")
        };

        let sig_chans = self.signal_channels.clone();

        let sub_ids = self.subscription_ids.clone();
        let _loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                if msg.subscription_id == sub_ids.another_signal_signal.unwrap_or_default() {
                    let chan = sig_chans.another_signal_sender.clone();

                    let pl: AnotherSignalSignalPayload =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let _send_result = chan.send(pl);
                } else if msg.subscription_id == sub_ids.bark_signal.unwrap_or_default() {
                    let chan = sig_chans.bark_sender.clone();

                    let pl: BarkSignalPayload =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let _send_result = chan.send(pl.word);
                } else if msg.subscription_id == sub_ids.maybe_number_signal.unwrap_or_default() {
                    let chan = sig_chans.maybe_number_sender.clone();

                    let pl: MaybeNumberSignalPayload =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let _send_result = chan.send(pl.number);
                } else if msg.subscription_id == sub_ids.maybe_name_signal.unwrap_or_default() {
                    let chan = sig_chans.maybe_name_sender.clone();

                    let pl: MaybeNameSignalPayload =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let _send_result = chan.send(pl.name);
                } else if msg.subscription_id == sub_ids.now_signal.unwrap_or_default() {
                    let chan = sig_chans.now_sender.clone();

                    let pl: NowSignalPayload =
                        serde_json::from_slice(&msg.payload).expect("Failed to deserialize");
                    let _send_result = chan.send(pl.timestamp);
                }
            }
        });

        println!("Started client receive task");
        Ok(())
    }
}
