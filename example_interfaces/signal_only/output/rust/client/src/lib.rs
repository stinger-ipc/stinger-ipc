/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the SignalOnly interface.
*/

extern crate paho_mqtt as mqtt;
use futures::{StreamExt};
use connection::{MessageStreamer, MessagePublisher, Connection, ReceivedMessage};

use std::io::Error;
use tokio::sync::mpsc::{self};
use tokio::time::{self, Duration};
use serde::Serialize;



pub struct SignalOnlyClient {
    connection: Connection,
    signal_recv_callback_for_another_signal: Box<dyn FnMut(f32, bool, String)->()>,
    
    msg_streamer_rx: Receiver<ReceivedMessage>,
    msg_streamer_tx: Sender<ReceivedMessage>,
    msg_publisher: MessagePublisher, 
}

impl SignalOnlyClient {
    pub fn new(mut connection: Connection) -> SignalOnlyClient {
        let (rcvr_tx: Sender<ReceivedMessage>, mut rcvr_rx: Receiver<ReceivedMessage>) = mpsc.channel(64);
        let publihser = connection.get_publisher()
        
        
        let inst = SignalOnlyClient {
            connection: connection,
            subsc_id_start: subsc_id_start,
            signal_recv_callback_for_another_signal: Box::new( |_1, _2, _3| {} ),
            
            
            msg_streamer_rx: rcvr_rx,
            msg_streamer_tx: rcvr_tx,
            msg_publisher: publisher,
        };
        inst
    }

    async pub fn set_signal_recv_callbacks_for_another_signal(&mut self, cb: impl FnMut(f32, bool, String)->() + 'static) {
        self.signal_recv_callback_for_another_signal = Box::new(cb);
        self.connection.subscribe(String::from("SignalOnly/signal/anotherSignal"), self.msg_streamer_tx.clone()).await;
    }
    

    



}