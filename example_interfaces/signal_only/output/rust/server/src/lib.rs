/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.
*/

extern crate paho_mqtt as mqtt;
use connection::{MessagePublisher, Connection, ReceivedMessage};

#[allow(unused_imports)]
use connection::payloads::{*, MethodResultCode};

use std::sync::{Arc, Mutex};
use tokio::sync::{mpsc};
use tokio::join;
use tokio::task::JoinError;

/// This struct is used to store all the MQTTv5 subscription ids
/// for the subscriptions the client will make.
#[derive(Clone, Debug)]
struct SignalOnlyServerSubscriptionIds {
    
    
}

#[derive(Clone)]
struct SignalOnlyServerMethodHandlers {
    
}

#[derive(Clone)]
struct SignalOnlyProperties {
    
}

pub struct SignalOnlyServer {
    /// Temporarily holds the receiver for the MPSC channel.  The Receiver will be moved
    /// to a process loop when it is needed.  MQTT messages will be received with this.
    msg_streamer_rx: Option<mpsc::Receiver<ReceivedMessage>>,

    /// The Sender side of MQTT messages that are received from the broker.  This tx
    /// side is cloned for each subscription made.
    msg_streamer_tx: mpsc::Sender<ReceivedMessage>,

    /// Through this MessagePublisher object, we can publish messages to MQTT.
    msg_publisher: MessagePublisher,

    /// Struct contains all the handlers for the various methods.
    method_handlers: SignalOnlyServerMethodHandlers,
    
    /// Subscription IDs for all the subscriptions this makes.
    subscription_ids: SignalOnlyServerSubscriptionIds,

    /// Copy of MQTT Client ID
    client_id: String,
}

impl SignalOnlyServer {
    pub async fn new(connection: &mut Connection) -> Self {
        let _ = connection.connect().await.expect("Could not connect to MQTT broker");

        //let interface_info = String::from(r#"{"name": "SignalOnly", "summary": "", "title": "SignalOnly", "version": "0.0.1"}"#);
        //connection.publish("SignalOnly/interface".to_string(), interface_info, 1).await;

        // Create a channel for messages to get from the Connection object to this SignalOnlyClient object.
        // The Connection object uses a clone of the tx side of the channel.
        let (message_received_tx, message_received_rx) = mpsc::channel(64);

        let publisher = connection.get_publisher();

        // Create method handler struct
        

        

        // Create structure for method handlers.
        let method_handlers = SignalOnlyServerMethodHandlers {
        };

        // Create structure for subscription ids.
        let sub_ids = SignalOnlyServerSubscriptionIds {
            
            
        };

        

        SignalOnlyServer {

            msg_streamer_rx: Some(message_received_rx),
            msg_streamer_tx: message_received_tx,
            msg_publisher: publisher,
            method_handlers: method_handlers,
            subscription_ids: sub_ids,
            client_id: connection.client_id.to_string(),
        }
    }

    pub async fn emit_another_signal(&mut self, one: f32, two: bool, three: String) {
        let data = connection::payloads::AnotherSignalSignalPayload {
            
            one: one,
            
            two: two,
            
            three: three,
            
        };
        self.msg_publisher.publish_structure("SignalOnly/signal/anotherSignal".to_string(), &data).await;
    }
    

    


    

     /// Starts the tasks that process messages received.
    pub async fn receive_loop(&mut self) -> Result<(), JoinError> {

        // Take ownership of the RX channel that receives MQTT messages.  This will be moved into the loop_task.
        let mut message_receiver = self.msg_streamer_rx.take().expect("msg_streamer_rx should be Some");
        let mut method_handlers = self.method_handlers.clone();
        let sub_ids = self.subscription_ids.clone();
        let mut publisher = self.msg_publisher.clone();

        let _loop_task = tokio::spawn(async move {
            while let Some(msg) = message_receiver.recv().await {
                println!("Got a new message");
            }   
        });

        println!("Started client receive task");
        Ok(())
    }
}