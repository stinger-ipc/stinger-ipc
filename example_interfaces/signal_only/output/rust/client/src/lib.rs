/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
*/

extern crate paho_mqtt as mqtt;
use connection::{MessagePublisher, Connection, ReceivedMessage};

use std::sync::{Arc, Mutex};
use tokio::sync::{mpsc, broadcast, oneshot};

#[derive(Clone, Debug)]
struct SignalOnlySubscriptionIds {
    
    another_signal_signal: Option<i32>,
}

#[derive(Clone)]
struct SignalOnlySignalChannels {
    another_signal_sender: broadcast::Sender<AnotherSignalSignalPayload>,
    
}

pub struct SignalOnlyClient {
    connection: Connection,
    msg_streamer_rx: Option<mpsc::Receiver<ReceivedMessage>>,
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,
    msg_publisher: MessagePublisher,
    subscription_ids: SignalOnlySubscriptionIds,
    signal_channels: SignalOnlySignalChannels,
}

impl SignalOnlyClient {
    pub async fn new(mut connection: Connection) -> SignalOnlyClient {
        let _ = connection.connect().await;
        let (rcvr_tx, rcvr_rx) = mpsc::channel(64);
        let publisher = connection.get_publisher();
        
        // Signal subscriptions here are temporary.  Eventually, we'll subscribe when registering the callback.
        let topic_another_signal_signal = "SignalOnly/signal/anotherSignal";
        let subscription_id_another_signal_signal = connection.subscribe(&topic_another_signal_signal, rcvr_tx.clone()).await;
        let subscription_id_another_signal_signal = subscription_id_another_signal_signal.unwrap_or_else(|_| -1);
        
        let sub_ids = SignalOnlySubscriptionIds {
            
            another_signal_signal: Some(subscription_id_another_signal_signal),
            
        };
        let signal_channels = SignalOnlySignalChannels {
            another_signal_sender: broadcast::channel(64).0,
            
        };
        let inst = SignalOnlyClient {
            connection: connection,
            
            msg_streamer_rx: Some(rcvr_rx),
            msg_streamer_tx: rcvr_tx,
            msg_publisher: publisher,
            subscription_ids: sub_ids,
            signal_channels: signal_channels,
        };
        inst
    }

    pub async fn get_another_signal_receiver() {

    }
    

    

    pub async fn process_loop(&mut self) {
        let resp_map = self.pending_responses.clone();
        let mut receiver = self.msg_streamer_rx.take().expect("msg_streamer_rx should be Some");
        let mut streamer = self.connection.get_streamer().await;
        let sig_chans = self.signal_channels.clone();
        let task1 = tokio::spawn(async move {
            streamer.receive_loop().await;
        });

        let sub_ids = self.subscription_ids.clone();
        let task2 = tokio::spawn(async move {
            while let Some(msg) = receiver.recv().await {
                println!("Received mqtt message: {:?} against subscription id {}", msg.message.payload_str(), msg.subscription_id);
                println!("Our subscriptions are: {:?}", sub_ids);
                if msg.subscription_id == sub_ids.another_signal_signal.unwrap_or_default() {
                    println!("Found subscription match for {}({:?}) as a anotherSignal signal", msg.message.topic(), sub_ids.another_signal_signal);
                    let chan = sig_chans.another_signal_sender.clone();
                    let send_result = chan.send(AnotherSignalSignalPayload {
                        
                        one: 1,
                        
                        two: 1,
                        
                        three: 1,
                        
                    });
                    println!("Sent anotherSignal signal with payload: {:?}", msg.message.payload_str());
                }
                
            }   
        });

        task1.await;
        task2.await;
    }
}