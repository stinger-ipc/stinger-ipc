/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
*/

extern crate paho_mqtt as mqtt;
use connection::{MessagePublisher, Connection, ReceivedMessage};

use json::{JsonValue};
use std::collections::HashMap;
use uuid::Uuid;
use serde_json;

#[allow(unused_imports)]
use connection::payloads::{*, MethodResultCode};

use std::sync::{Arc, Mutex};
use tokio::sync::{mpsc, broadcast, oneshot};
use tokio::join;
use tokio::task::JoinError;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct SignalOnlySubscriptionIds {
    
    another_signal_signal: Option<i32>,
}

/// This struct holds the tx side of a broadcast channels used when receiving signals.
/// The rx side of the broadcast channels can be created from the tx side later.
/// When SignalOnlyClient gets a message and determines that it
/// is a signal, it will send the signal payload via the tx channel that is in this struct.
#[derive(Clone)]
struct SignalOnlySignalChannels {
    another_signal_sender: broadcast::Sender<AnotherSignalSignalPayload>,
    
}

/// This is the struct for our API client.
pub struct SignalOnlyClient {
    

    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Option<mpsc::Receiver<ReceivedMessage>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    
    /// Contains all the MQTTv5 subscription ids.
    subscription_ids: SignalOnlySubscriptionIds,

    /// Holds the channels used for sending signals to the application.
    signal_channels: SignalOnlySignalChannels,
    
    /// Copy of MQTT Client ID
    client_id: String,
}

impl SignalOnlyClient {

    /// Creates a new SignalOnlyClient that uses elements from the provided Connection object.
    pub async fn new(connection: &mut Connection) -> Self {
        let _ = connection.connect().await.expect("Could not connect to MQTT broker");

        // Create a channel for messages to get from the Connection object to this SignalOnlyClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        

        // Subscribe to all the topics needed for signals.
        let topic_another_signal_signal = "signalOnly/signal/anotherSignal";
        let subscription_id_another_signal_signal = connection.subscribe(&topic_another_signal_signal, message_received_tx.clone()).await;
        let subscription_id_another_signal_signal = subscription_id_another_signal_signal.unwrap_or_else(|_| -1);
        

        // Create structure for subscription ids.
        let sub_ids = SignalOnlySubscriptionIds {
            another_signal_signal: Some(subscription_id_another_signal_signal),
            
        };

        // Create structure for the tx side of broadcast channels for signals.
        let signal_channels = SignalOnlySignalChannels {
            another_signal_sender: broadcast::channel(64).0,
            
        };

        // Create SignalOnlyClient structure.
        let inst = SignalOnlyClient {
            
            msg_streamer_rx: Some(message_received_rx),
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
    

    

    /// Starts the tasks that process messages received.
    pub async fn receive_loop(&mut self) -> Result<(), JoinError> {
        
        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = self.msg_streamer_rx.take().expect("msg_streamer_rx should be Some");

        let sig_chans = self.signal_channels.clone();
        let sub_ids = self.subscription_ids.clone();

        let loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                let msg_props = msg.message.properties();
                let opt_corr_id_bin: Option<Vec<u8>> = msg_props.get_binary(mqtt::PropertyCode::CorrelationData);
                let corr_id: Option<Uuid> = opt_corr_id_bin.and_then(|b| Uuid::from_slice(&b).ok());
                if msg.subscription_id == sub_ids.another_signal_signal.unwrap_or_default() {
                    let chan = sig_chans.another_signal_sender.clone();
                    let pl: connection::payloads::AnotherSignalSignalPayload =  serde_json::from_str(&msg.message.payload_str()).expect("Failed to deserialize");
                    let _send_result = chan.send(pl);
                }
                
            }   
        });

        println!("Started client receive task");
        Ok(())
    }
}