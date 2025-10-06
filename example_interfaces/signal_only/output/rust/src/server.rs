//! Server module for SignalOnly IPC
//!
//! This module is only available when the "server" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.
*/

use mqttier::{MqttierClient, PublishResult};

#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
use std::any::Any;

use std::future::Future;
use std::pin::Pin;
use tokio::task::JoinError;
type SentMessageFuture = Pin<Box<dyn Future<Output = Result<(), MethodReturnCode>> + Send>>;
#[cfg(feature = "server")]
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};

#[derive(Clone)]
pub struct SignalOnlyServer {
    mqttier_client: MqttierClient,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,

    pub instance_id: String,
}

impl SignalOnlyServer {
    pub async fn new(connection: &mut MqttierClient, instance_id: String) -> Self {
        SignalOnlyServer {
            mqttier_client: connection.clone(),

            client_id: connection.client_id.to_string(),
            instance_id,
        }
    }

    /// Converts a oneshot receiver for the publish result into a Future that resolves to
    pub async fn oneshot_to_future(
        publish_oneshot: tokio::sync::oneshot::Receiver<PublishResult>,
    ) -> SentMessageFuture {
        Box::pin(async move {
            let publish_result = publish_oneshot.await;
            match publish_result {
                Ok(PublishResult::Acknowledged(_))
                | Ok(PublishResult::Completed(_))
                | Ok(PublishResult::Sent(_)) => Ok(()),

                Ok(PublishResult::TimedOut) => Err(MethodReturnCode::Timeout(
                    "Timed out publishing signal".to_string(),
                )),

                Ok(PublishResult::SerializationError(s)) => {
                    Err(MethodReturnCode::SerializationError(s))
                }

                Ok(PublishResult::Error(s)) => Err(MethodReturnCode::TransportError(s)),

                Err(_) => Err(MethodReturnCode::UnknownError(
                    "Error publishing signal".to_string(),
                )),
            }
        })
    }

    pub async fn wrap_return_code_in_future(rc: MethodReturnCode) -> SentMessageFuture {
        Box::pin(async move {
            match rc {
                MethodReturnCode::Success => Ok(()),
                _ => Err(rc),
            }
        })
    }
    /// Emits the anotherSignal signal with the given arguments.
    pub async fn emit_another_signal(
        &mut self,
        one: f32,
        two: bool,
        three: String,
    ) -> SentMessageFuture {
        let data = AnotherSignalSignalPayload {
            one: one,

            two: two,

            three: three,
        };
        let published_oneshot = self
            .mqttier_client
            .publish_structure(
                format!("signalOnly/{}/signal/anotherSignal", self.instance_id),
                &data,
            )
            .await;
        SignalOnlyServer::oneshot_to_future(published_oneshot).await
    }
    /// Emits the bark signal with the given arguments.
    pub async fn emit_bark(&mut self, word: String) -> SentMessageFuture {
        let data = BarkSignalPayload { word: word };
        let published_oneshot = self
            .mqttier_client
            .publish_structure(
                format!("signalOnly/{}/signal/bark", self.instance_id),
                &data,
            )
            .await;
        SignalOnlyServer::oneshot_to_future(published_oneshot).await
    }
    /// Emits the maybe_number signal with the given arguments.
    pub async fn emit_maybe_number(&mut self, number: Option<i32>) -> SentMessageFuture {
        let data = MaybeNumberSignalPayload { number: number };
        let published_oneshot = self
            .mqttier_client
            .publish_structure(
                format!("signalOnly/{}/signal/maybeNumber", self.instance_id),
                &data,
            )
            .await;
        SignalOnlyServer::oneshot_to_future(published_oneshot).await
    }
    /// Emits the maybe_name signal with the given arguments.
    pub async fn emit_maybe_name(&mut self, name: Option<String>) -> SentMessageFuture {
        let data = MaybeNameSignalPayload { name: name };
        let published_oneshot = self
            .mqttier_client
            .publish_structure(
                format!("signalOnly/{}/signal/maybeName", self.instance_id),
                &data,
            )
            .await;
        SignalOnlyServer::oneshot_to_future(published_oneshot).await
    }
    /// Emits the now signal with the given arguments.
    pub async fn emit_now(
        &mut self,
        timestamp: chrono::DateTime<chrono::Utc>,
    ) -> SentMessageFuture {
        let data = NowSignalPayload {
            timestamp: timestamp,
        };
        let published_oneshot = self
            .mqttier_client
            .publish_structure(format!("signalOnly/{}/signal/now", self.instance_id), &data)
            .await;
        SignalOnlyServer::oneshot_to_future(published_oneshot).await
    }

    /// Starts the tasks that process messages received.
    /// In the task, it loops over messages received from the rx side of the message_receiver channel.
    /// Based on the subscription id of the received message, it will call a function to handle the
    /// received message.
    pub async fn run_loop(&mut self) -> Result<(), JoinError> {
        // Make sure the MqttierClient is connected and running.
        let _ = self.mqttier_client.run_loop().await;

        warn!("Server receive loop completed. Exiting run_loop.");
        Ok(())
    }
}
