/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
*/

extern crate paho_mqtt as mqtt;
use connection::{MessagePublisher, Connection, ReceivedMessage};

use std::sync::{Arc, Mutex};
use tokio::sync::mpsc::{self, Sender, Receiver};

#[derive(Clone, Debug)]
struct SignalOnlySubscriptionIds {
    
    another_signal: Option<i32>,
    
}

pub struct SignalOnlyClient {
    connection: Connection,
    signal_recv_callback_for_another_signal: Box<dyn FnMut(f32, bool, String)->()>,
    
    msg_streamer_rx: Option<Receiver<ReceivedMessage>>,
    msg_streamer_tx: Sender<ReceivedMessage>,
    msg_publisher: MessagePublisher,
    subscription_ids: SignalOnlySubscriptionIds,
}

impl SignalOnlyClient {
    pub async fn new(mut connection: Connection) -> SignalOnlyClient {
        let _ = connection.connect().await;
        let (rcvr_tx, rcvr_rx) = mpsc::channel(64);
        let publisher = connection.get_publisher();
        
        let sub_ids = SignalOnlySubscriptionIds {
            
            another_signal: None,
            
        };
        let inst = SignalOnlyClient {
            connection: connection,
            signal_recv_callback_for_another_signal: Box::new( |_1, _2, _3| {} ),
            
            
            msg_streamer_rx: Some(rcvr_rx),
            msg_streamer_tx: rcvr_tx,
            msg_publisher: publisher,
            subscription_ids: sub_ids,
        };
        inst
    }

    pub async fn set_signal_recv_callbacks_for_another_signal(&mut self, cb: impl FnMut(f32, bool, String)->() + 'static) {
        self.signal_recv_callback_for_another_signal = Box::new(cb);
        let sub_id = self.connection.subscribe("SignalOnly/signal/anotherSignal", self.msg_streamer_tx.clone()).await;
        self.subscription_ids.another_signal = sub_id.ok();
    }
    

    

    pub async fn process_loop(&mut self) {
        let resp_map = self.pending_responses.clone();
        let mut receiver = self.msg_streamer_rx.take().expect("msg_streamer_rx should be Some");
        let mut streamer = self.connection.get_streamer().await;
        let task1 = tokio::spawn(async move {
            streamer.receive_loop().await;
        });

        let sub_ids = self.subscription_ids.clone();
        let task2 = tokio::spawn(async move {
            while let Some(msg) = receiver.recv().await {
                println!("Received message: {:?}", msg.message.payload_str());
            }
        });

        task1.await;
        task2.await;
    }
}