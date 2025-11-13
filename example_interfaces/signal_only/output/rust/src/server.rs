//! Server module for SignalOnly IPC
//!
//! This module is only available when the "server" feature is enabled.

/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Server for the SignalOnly interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

#[allow(unused_imports)]
use crate::payloads::{MethodReturnCode, *};
use bytes::Bytes;
use tokio::sync::oneshot;

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
#[cfg(feature = "server")]
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};

#[derive(Clone)]
pub struct SignalOnlyServer<C: Mqtt5PubSub> {
    mqtt_client: C,

    /// Copy of MQTT Client ID
    #[allow(dead_code)]
    pub client_id: String,

    pub instance_id: String,
}

impl<C: Mqtt5PubSub + Clone + Send> SignalOnlyServer<C> {
    pub async fn new(mut connection: C, instance_id: String) -> Self {
        SignalOnlyServer {
            mqtt_client: connection.clone(),

            client_id: connection.get_client_id(),
            instance_id,
        }
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
    /// Emits the anotherSignal signal with the given arguments.
    pub async fn emit_another_signal(
        &mut self,
        one: f32,
        two: bool,
        three: String,
    ) -> SentMessageFuture {
        let data = AnotherSignalSignalPayload { one, two, three };
        let topic = format!("signalOnly/{}/signal/anotherSignal", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the anotherSignal signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_another_signal_nowait(
        &mut self,
        one: f32,
        two: bool,
        three: String,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = AnotherSignalSignalPayload { one, two, three };
        let topic = format!("signalOnly/{}/signal/anotherSignal", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the bark signal with the given arguments.
    pub async fn emit_bark(&mut self, word: String) -> SentMessageFuture {
        let data = BarkSignalPayload { word };
        let topic = format!("signalOnly/{}/signal/bark", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the bark signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_bark_nowait(
        &mut self,
        word: String,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = BarkSignalPayload { word };
        let topic = format!("signalOnly/{}/signal/bark", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the maybe_number signal with the given arguments.
    pub async fn emit_maybe_number(&mut self, number: Option<i32>) -> SentMessageFuture {
        let data = MaybeNumberSignalPayload { number };
        let topic = format!("signalOnly/{}/signal/maybeNumber", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the maybe_number signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_maybe_number_nowait(
        &mut self,
        number: Option<i32>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = MaybeNumberSignalPayload { number };
        let topic = format!("signalOnly/{}/signal/maybeNumber", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the maybe_name signal with the given arguments.
    pub async fn emit_maybe_name(&mut self, name: Option<String>) -> SentMessageFuture {
        let data = MaybeNameSignalPayload { name };
        let topic = format!("signalOnly/{}/signal/maybeName", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the maybe_name signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_maybe_name_nowait(
        &mut self,
        name: Option<String>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = MaybeNameSignalPayload { name };
        let topic = format!("signalOnly/{}/signal/maybeName", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }
    /// Emits the now signal with the given arguments.
    pub async fn emit_now(
        &mut self,
        timestamp: chrono::DateTime<chrono::Utc>,
    ) -> SentMessageFuture {
        let data = NowSignalPayload { timestamp };
        let topic = format!("signalOnly/{}/signal/now", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        let ch = publisher.publish_noblock(msg).await;
        Self::oneshot_to_future(ch).await
    }

    /// Emits the now signal with the given arguments, but this is a fire-and-forget version.
    pub fn emit_now_nowait(
        &mut self,
        timestamp: chrono::DateTime<chrono::Utc>,
    ) -> std::result::Result<MqttPublishSuccess, Mqtt5PubSubError> {
        let data = NowSignalPayload { timestamp };
        let topic = format!("signalOnly/{}/signal/now", self.instance_id);
        let msg = message::signal(&topic, &data).unwrap();
        let mut publisher = self.mqtt_client.clone();
        publisher.publish_nowait(msg)
    }

    /// Starts the tasks that process messages received.
    /// In the task, it loops over messages received from the rx side of the message_receiver channel.
    /// Based on the subscription id of the received message, it will call a function to handle the
    /// received message.
    pub async fn run_loop(&mut self) -> Result<(), JoinError>
    where
        C: 'static,
    {
        warn!("Server receive loop completed. Exiting run_loop.");
        Ok(())
    }
}
