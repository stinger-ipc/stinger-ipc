/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.
*/

use mqttier::MqttierClient;

#[allow(unused_imports)]
use signal_only_types::payloads::{MethodResultCode, *};
use std::sync::{Arc, Mutex};

use tokio::task::JoinError;

#[derive(Clone)]
pub struct SignalOnlyServer {
    mqttier_client: MqttierClient,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,
}

impl SignalOnlyServer {
    pub async fn new(connection: &mut MqttierClient) -> Self {
        SignalOnlyServer {
            mqttier_client: connection.clone(),

            client_id: connection.client_id.to_string(),
        }
    }

    /// Emits the anotherSignal signal with the given arguments.
    pub async fn emit_another_signal(&mut self, one: f32, two: bool, three: String) {
        let data = AnotherSignalSignalPayload {
            one: one,

            two: two,

            three: three,
        };
        let _ = self
            .mqttier_client
            .publish_structure("signalOnly/signal/anotherSignal".to_string(), &data)
            .await;
    }

    /// Starts the tasks that process messages received.
    /// In the task, it loops over messages received from the rx side of the message_receiver channel.
    /// Based on the subscription id of the received message, it will call a function to handle the
    /// received message.
    pub async fn receive_loop(&mut self) -> Result<(), JoinError> {
        // Make sure the MqttierClient is connected and running.
        let _ = self.mqttier_client.run_loop().await;

        println!("Server receive loop completed [error?]");
        Ok(())
    }
}
