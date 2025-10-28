/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/
use std::collections::HashMap;
use std::fmt;
use std::sync::{Arc, RwLock};

use crate::interface::InterfaceInfo;
use stinger_mqtt_trait::message::{MqttMessage, QoS};
use stinger_mqtt_trait::{MqttClient, MqttError};
use tokio::sync::broadcast;
use tokio::task::JoinHandle;
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};

#[derive(Debug)]
pub enum FullDiscoveryError {
    Subscribe(MqttError),
}

impl fmt::Display for FullDiscoveryError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            FullDiscoveryError::Subscribe(err) => {
                write!(f, "failed to subscribe for discovery: {err}")
            }
        }
    }
}

impl std::error::Error for FullDiscoveryError {}

impl From<MqttError> for FullDiscoveryError {
    fn from(value: MqttError) -> Self {
        FullDiscoveryError::Subscribe(value)
    }
}

pub struct FullDiscovery {
    service_name: String,
    subscription_id: u32,
    discovered_interfaces: Arc<RwLock<HashMap<String, InterfaceInfo>>>,
    listener_handle: JoinHandle<()>,
    notification_tx: broadcast::Sender<InterfaceInfo>,
}

/// Event receiver for new interface discovery notifications
pub type FullDiscoveryReceiver = broadcast::Receiver<InterfaceInfo>;

impl FullDiscovery {
    pub async fn new(connection: &mut impl MqttClient) -> Result<Self, FullDiscoveryError> {
        debug!("Starting client loop if not already started.");
        let _ = connection.start().await;

        let service_name = "Full".to_string();
        let discovery_topic = format!("full/{}/interface", "+");

        let (message_tx, message_rx) = broadcast::channel::<MqttMessage>(32);
        debug!("Subscribing to discovery topic: {discovery_topic}");
        let subscription_id = connection
            .subscribe(discovery_topic, QoS::AtLeastOnce, message_tx.clone())
            .await
            .map_err(FullDiscoveryError::from)?;
        let discovered_interfaces = Arc::new(RwLock::new(HashMap::new()));

        // Clients can get a notification receiver by calling the subscribe() method.
        let (notification_tx, _notification_rx) = broadcast::channel::<InterfaceInfo>(32);

        let listener_handle = Self::spawn_listener(
            message_rx,
            discovered_interfaces.clone(),
            notification_tx.clone(),
        );

        Ok(Self {
            service_name,
            subscription_id,
            discovered_interfaces,
            listener_handle,
            notification_tx,
        })
    }

    pub fn service_name(&self) -> &str {
        &self.service_name
    }

    pub fn discovered_interfaces(&self) -> Vec<InterfaceInfo> {
        let guard = self
            .discovered_interfaces
            .read()
            .expect("interfaces poisoned");
        guard.values().cloned().collect()
    }

    pub async fn get_singleton_service(&self) -> InterfaceInfo {
        // First check if we already have an interface
        {
            let guard = self
                .discovered_interfaces
                .read()
                .expect("interfaces poisoned");
            if let Some(info) = guard.values().next() {
                return info.clone();
            }
        }

        // No interfaces yet, wait for the first one to be discovered
        let mut receiver = self.notification_tx.subscribe();
        receiver.recv().await.expect("notification channel closed")
    }

    pub fn subscription_id(&self) -> u32 {
        self.subscription_id
    }

    /// Subscribe to notifications for newly discovered interfaces.
    ///
    /// Returns a receiver that will be notified when a new interface is discovered.
    /// Notifications are only sent for new interfaces, not for updates to existing ones.
    ///
    /// # Example
    ///
    /// ```no_run
    /// use full_ipc::discovery::FullDiscovery;
    /// use mqttier::{Connection, MqttierClient, MqttierOptions};
    ///
    /// #[tokio::main]
    /// async fn main() {
    ///     let options = MqttierOptions::new()
    ///         .connection(Connection::TcpLocalhost(1883))
    ///         .build();
    ///     let mut client = MqttierClient::new(options).unwrap();
    ///
    ///     let discovery = FullDiscovery::new(&mut client).await.unwrap();
    ///     let mut notifications = discovery.subscribe();
    ///     
    ///     tokio::spawn(async move {
    ///         while let Ok(interface_info) = notifications.recv().await {
    ///             println!("New interface discovered: {}", interface_info.instance);
    ///             println!("  Connection topic: {}", interface_info.connection_topic);
    ///         }
    ///     });
    ///     
    ///     // ... rest of your application
    /// }
    /// ```
    pub fn subscribe(&self) -> FullDiscoveryReceiver {
        self.notification_tx.subscribe()
    }

    fn spawn_listener(
        mut message_rx: broadcast::Receiver<MqttMessage>,
        discovered_interfaces: Arc<RwLock<HashMap<String, InterfaceInfo>>>,
        notification_tx: broadcast::Sender<InterfaceInfo>,
    ) -> JoinHandle<()> {
        tokio::spawn(async move {
            debug!("Listening for discovery messages");
            while let Ok(message) = message_rx.recv().await {
                Self::handle_message(message, &discovered_interfaces, &notification_tx);
            }
        })
    }

    fn handle_message(
        message: MqttMessage,
        discovered_interfaces: &Arc<RwLock<HashMap<String, InterfaceInfo>>>,
        notification_tx: &broadcast::Sender<InterfaceInfo>,
    ) {
        if message.payload.is_empty() {
            info!("Service represented by {} is now offline", message.topic);
            // Parse instance_id from topic (format: full/{instance_id}/interface)
            let topic_parts: Vec<&str> = message.topic.split('/').collect();
            if topic_parts.len() >= 2 {
                let instance_id = topic_parts[topic_parts.len() - 2].to_string();
                let mut interfaces_guard = discovered_interfaces
                    .write()
                    .expect("interfaces write lock poisoned");
                interfaces_guard.remove(&instance_id);
                drop(interfaces_guard);
            }
        } else {
            let deserialized = serde_json::from_slice::<InterfaceInfo>(&message.payload);
            match deserialized {
                Ok(info) => {
                    info!("Discovered service instance: {:?}", info);
                    let mut interfaces_guard = discovered_interfaces
                        .write()
                        .expect("interfaces write lock poisoned");
                    let instance_id = info.instance.clone();
                    let is_new_instance = interfaces_guard
                        .insert(instance_id.clone(), info.clone())
                        .is_none();
                    drop(interfaces_guard);

                    // Send notification only for new interfaces
                    if is_new_instance {
                        let _ = notification_tx.send(info);
                    }
                }
                Err(err) => {
                    error!(
                        "Failed to deserialize InterfaceInfo from {}: {}",
                        message.topic, err
                    );
                }
            }
        }
    }
}

impl Drop for FullDiscovery {
    fn drop(&mut self) {
        self.listener_handle.abort();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_message(topic: &str, instance: &str) -> MqttMessage {
        let info = InterfaceInfo {
            interface_name: "sample".into(),
            title: "Sample".into(),
            version: "1.0".into(),
            instance: instance.into(),
            connection_topic: format!("sample/{instance}"),
            timestamp: "2024-01-01T00:00:00Z".into(),
        };
        let payload = serde_json::to_vec(&info).expect("serialize");

        MqttMessage {
            topic: topic.into(),
            payload,
            qos: 1,
            subscription_id: 42,
            response_topic: None,
            content_type: None,
            correlation_data: None,
            user_properties: HashMap::new(),
        }
    }

    #[tokio::test]
    async fn collects_unique_instances_and_topics() {
        let interfaces = Arc::new(RwLock::new(HashMap::new()));
        let (notification_tx, mut notification_rx) = broadcast::channel::<InterfaceInfo>(32);

        FullDiscovery::handle_message(
            sample_message("service/alpha/interface", "alpha"),
            &interfaces,
            &notification_tx,
        );
        FullDiscovery::handle_message(
            sample_message("service/beta/interface", "beta"),
            &interfaces,
            &notification_tx,
        );
        FullDiscovery::handle_message(
            sample_message("service/alpha/interface", "alpha"),
            &interfaces,
            &notification_tx,
        );

        let interfaces_guard = interfaces.read().unwrap();
        assert_eq!(interfaces_guard.len(), 2);
        assert!(interfaces_guard.contains_key("alpha"));
        assert!(interfaces_guard.contains_key("beta"));

        // Check that we received exactly 2 notifications (only for new interfaces)
        let info1 = notification_rx
            .try_recv()
            .expect("should have first notification");
        assert_eq!(info1.instance, "alpha");
        let info2 = notification_rx
            .try_recv()
            .expect("should have second notification");
        assert_eq!(info2.instance, "beta");
        assert!(
            notification_rx.try_recv().is_err(),
            "should not have third notification"
        );
    }
}
