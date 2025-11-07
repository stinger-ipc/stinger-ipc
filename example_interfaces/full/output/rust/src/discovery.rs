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
use stinger_mqtt_trait::{Mqtt5PubSub, Mqtt5PubSubError};
use tokio::sync::broadcast;
use tokio::task::JoinHandle;
#[allow(unused_imports)]
use tracing::{debug, error, info, warn};

use crate::property::{FullInitialPropertyValues, FullInitialPropertyValuesBuilder};

#[allow(unused_imports)]
use crate::payloads::*;
#[cfg(feature = "metrics")]
use std::sync::Mutex;

#[derive(Debug)]
pub enum FullDiscoveryError {
    Subscribe(Mqtt5PubSubError),
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

impl From<Mqtt5PubSubError> for FullDiscoveryError {
    fn from(value: Mqtt5PubSubError) -> Self {
        FullDiscoveryError::Subscribe(value)
    }
}

struct ServiceInDiscovery {
    pub interface_info: Option<InterfaceInfo>,

    pub property_builder: FullInitialPropertyValuesBuilder,
    pub property_count: u32,

    pub fully_discovered: std::sync::atomic::AtomicBool,
}

impl Default for ServiceInDiscovery {
    fn default() -> Self {
        Self {
            interface_info: None,

            property_builder: FullInitialPropertyValuesBuilder::default(),
            property_count: 0,

            fully_discovered: std::sync::atomic::AtomicBool::new(false),
        }
    }
}

#[derive(Clone, Debug)]
pub struct DiscoveredService {
    pub interface_info: InterfaceInfo,

    pub properties: FullInitialPropertyValues,
}

impl ServiceInDiscovery {
    /// Attempts to convert a ServiceInDiscovery into a DiscoveredService
    pub fn to_discovered_service(&self) -> Option<DiscoveredService> {
        let built_properties_result = self.property_builder.build();
        match (&self.interface_info, built_properties_result) {
            (Some(info), Ok(props)) => Some(DiscoveredService {
                interface_info: info.clone(),
                properties: props,
            }),
            _ => None,
        }
    }
}

#[cfg(feature = "metrics")]
#[derive(Debug)]
pub struct FullDiscoveryMetrics {
    pub discovery_start_time: std::time::Instant,
    pub time_of_first_discovery: Option<std::time::Instant>,
    pub received_property_values: std::sync::atomic::AtomicU32,
}

#[cfg(feature = "metrics")]
impl Default for FullDiscoveryMetrics {
    fn default() -> Self {
        Self {
            discovery_start_time: std::time::Instant::now(),
            time_of_first_discovery: None,
            received_property_values: std::sync::atomic::AtomicU32::new(0),
        }
    }
}

#[cfg(feature = "metrics")]
impl FullDiscoveryMetrics {
    /// Sets the time_of_first_discovery if it hasn't been set yet
    pub fn set_time_of_first_discovery(&mut self) {
        if self.time_of_first_discovery.is_none() {
            self.time_of_first_discovery = Some(std::time::Instant::now());
        }
    }

    /// Increments received_property_values by 1
    pub fn increment_received_property_values(&self) {
        self.received_property_values
            .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
    }

    /// Returns the time in milliseconds between `discovery_start_time` and
    /// `time_of_first_discovery`, or `None` if `time_of_first_discovery` is not set.
    pub fn time_to_first_discovery_ms(&self) -> Option<u128> {
        self.time_of_first_discovery
            .as_ref()
            .map(|t| t.duration_since(self.discovery_start_time).as_millis())
    }
}

pub struct FullDiscovery {
    service_name: String,
    instances_in_discovery: Arc<RwLock<HashMap<String, ServiceInDiscovery>>>,
    info_listener_handle: JoinHandle<()>,

    prop_listener_handle: JoinHandle<()>,

    notification_tx: broadcast::Sender<DiscoveredService>,
    #[cfg(feature = "metrics")]
    pub metrics: Arc<Mutex<FullDiscoveryMetrics>>,
}

/// Event receiver for new interface discovery notifications
pub type FullDiscoveryReceiver = broadcast::Receiver<DiscoveredService>;

impl FullDiscovery {
    pub async fn new(connection: &mut impl Mqtt5PubSub) -> Result<Self, FullDiscoveryError> {
        let service_name = "Full".to_string();
        let discovery_topic = format!("full/{}/interface", "+");

        let (info_tx, info_rx) = broadcast::channel::<MqttMessage>(32);
        debug!("Subscribing to discovery topic: {discovery_topic}");
        let _subscription_id = connection
            .subscribe(discovery_topic, QoS::AtLeastOnce, info_tx.clone())
            .await
            .map_err(FullDiscoveryError::from)?;

        let (prop_tx, prop_rx) = broadcast::channel::<MqttMessage>(32);
        let _property_subscription_id = connection
            .subscribe(
                "full/+/property/+/value".to_string(),
                QoS::AtLeastOnce,
                prop_tx.clone(),
            )
            .await
            .map_err(FullDiscoveryError::from)?;

        let instances_in_discovery = Arc::new(RwLock::new(HashMap::new()));

        // Clients can get a notification receiver by calling the subscribe() method.
        let (notification_tx, _notification_rx) = broadcast::channel::<DiscoveredService>(32);

        #[cfg(feature = "metrics")]
        let metrics = Arc::new(Mutex::new(FullDiscoveryMetrics::default()));

        let info_listener_handle = Self::spawn_listener(
            info_rx,
            instances_in_discovery.clone(),
            notification_tx.clone(),
            #[cfg(feature = "metrics")]
            metrics.clone(),
        );

        let prop_listener_handle = Self::spawn_property_listener(
            prop_rx,
            instances_in_discovery.clone(),
            notification_tx.clone(),
            #[cfg(feature = "metrics")]
            metrics.clone(),
        );

        Ok(Self {
            service_name,
            instances_in_discovery,
            info_listener_handle,

            prop_listener_handle,

            notification_tx,
            #[cfg(feature = "metrics")]
            metrics,
        })
    }

    pub fn service_name(&self) -> &str {
        &self.service_name
    }

    pub fn instances_in_discovery(&self) -> Vec<DiscoveredService> {
        let guard = self
            .instances_in_discovery
            .read()
            .expect("interfaces poisoned");
        guard
            .values()
            .filter(|sd| {
                sd.fully_discovered
                    .load(std::sync::atomic::Ordering::Relaxed)
            })
            .filter_map(|sd| sd.to_discovered_service())
            .collect()
    }

    pub async fn get_singleton_service(&self) -> DiscoveredService {
        // First check if we already have an interface
        {
            let instance_map = self
                .instances_in_discovery
                .read()
                .expect("interfaces poisoned");
            if let Some(entry) = instance_map.values().next() {
                if entry.interface_info.is_some() {
                    let prop_build_result = entry.property_builder.build();
                    if prop_build_result.is_ok() {
                        return DiscoveredService {
                            interface_info: entry.interface_info.clone().unwrap(),

                            properties: prop_build_result.unwrap(),
                        };
                    }
                }
            }
        }

        // No interfaces yet, wait for the first one to be discovered
        let mut receiver = self.notification_tx.subscribe();
        receiver.recv().await.expect("notification channel closed")
    }

    pub fn subscribe(&self) -> FullDiscoveryReceiver {
        self.notification_tx.subscribe()
    }

    fn try_publish_discovered_service(
        service_in_discovery: &ServiceInDiscovery,
        notification_tx: &broadcast::Sender<DiscoveredService>,
        #[cfg(feature = "metrics")] metrics: &Arc<Mutex<SimpleDiscoveryMetrics>>,
    ) {
        // Check if this completes the discovery

        if service_in_discovery.property_count >= 7 {
            if let Some(discovered) = service_in_discovery.to_discovered_service() {
                service_in_discovery
                    .fully_discovered
                    .store(true, std::sync::atomic::Ordering::Relaxed);
                let _ = notification_tx.send(discovered);
                #[cfg(feature = "metrics")]
                {
                    let mut metrics_guard = metrics.lock().unwrap();
                    metrics_guard.set_time_of_first_discovery();
                }
            }
        }
    }

    fn spawn_listener(
        mut message_rx: broadcast::Receiver<MqttMessage>,
        instances_in_discovery: Arc<RwLock<HashMap<String, ServiceInDiscovery>>>,
        notification_tx: broadcast::Sender<DiscoveredService>,
        #[cfg(feature = "metrics")] metrics: Arc<Mutex<SimpleDiscoveryMetrics>>,
    ) -> JoinHandle<()> {
        tokio::spawn(async move {
            debug!("Listening for discovery messages");
            while let Ok(message) = message_rx.recv().await {
                Self::handle_message(
                    message,
                    &instances_in_discovery,
                    &notification_tx,
                    #[cfg(feature = "metrics")]
                    metrics.clone(),
                );
            }
        })
    }

    fn spawn_property_listener(
        mut message_rx: broadcast::Receiver<MqttMessage>,
        instances_in_discovery: Arc<RwLock<HashMap<String, ServiceInDiscovery>>>,
        notification_tx: broadcast::Sender<DiscoveredService>,
        #[cfg(feature = "metrics")] metrics: Arc<Mutex<FullDiscoveryMetrics>>,
    ) -> JoinHandle<()> {
        tokio::spawn(async move {
            debug!("Listening for property value messages");
            while let Ok(message) = message_rx.recv().await {
                #[cfg(feature = "metrics")]
                {
                    let metrics_guard = metrics.lock().unwrap();
                    metrics_guard.increment_received_property_values();
                }

                // Parse property topic (format: service/{instance_id}/property/{property_name}/value)
                let topic_parts: Vec<&str> = message.topic.split('/').collect();
                if topic_parts.len() == 5 {
                    let instance_id = topic_parts[1];
                    let property_name = topic_parts[3];

                    let mut instance_map = instances_in_discovery
                        .write()
                        .expect("interfaces write lock poisoned");
                    let service_in_discovery = instance_map
                        .entry(instance_id.to_string())
                        .or_insert_with(ServiceInDiscovery::default);

                    match property_name {
                        "favoriteNumber" => {
                            let deserialized_property =
                                serde_json::from_slice::<FavoriteNumberProperty>(&message.payload);
                            let version = message
                                .user_properties
                                .get("Version")
                                .and_then(|v| v.parse::<u32>().ok())
                                .unwrap_or(0);
                            match deserialized_property {
                                Ok(prop_value) => {
                                    service_in_discovery
                                        .property_builder
                                        .favorite_number(prop_value.number);

                                    service_in_discovery
                                        .property_builder
                                        .favorite_number_version(version);
                                    service_in_discovery.property_count += 1;
                                }
                                Err(e) => {
                                    error!("Failed to deserialize property 'favorite_number' for instance '{}': {}", instance_id, e);
                                }
                            }
                        }

                        "favoriteFoods" => {
                            let deserialized_property =
                                serde_json::from_slice::<FavoriteFoodsProperty>(&message.payload);
                            let version = message
                                .user_properties
                                .get("Version")
                                .and_then(|v| v.parse::<u32>().ok())
                                .unwrap_or(0);
                            match deserialized_property {
                                Ok(prop_value) => {
                                    service_in_discovery
                                        .property_builder
                                        .favorite_foods(prop_value);

                                    service_in_discovery
                                        .property_builder
                                        .favorite_foods_version(version);
                                    service_in_discovery.property_count += 1;
                                }
                                Err(e) => {
                                    error!("Failed to deserialize property 'favorite_foods' for instance '{}': {}", instance_id, e);
                                }
                            }
                        }

                        "lunchMenu" => {
                            let deserialized_property =
                                serde_json::from_slice::<LunchMenuProperty>(&message.payload);
                            let version = message
                                .user_properties
                                .get("Version")
                                .and_then(|v| v.parse::<u32>().ok())
                                .unwrap_or(0);
                            match deserialized_property {
                                Ok(prop_value) => {
                                    service_in_discovery.property_builder.lunch_menu(prop_value);

                                    service_in_discovery
                                        .property_builder
                                        .lunch_menu_version(version);
                                    service_in_discovery.property_count += 1;
                                }
                                Err(e) => {
                                    error!("Failed to deserialize property 'lunch_menu' for instance '{}': {}", instance_id, e);
                                }
                            }
                        }

                        "familyName" => {
                            let deserialized_property =
                                serde_json::from_slice::<FamilyNameProperty>(&message.payload);
                            let version = message
                                .user_properties
                                .get("Version")
                                .and_then(|v| v.parse::<u32>().ok())
                                .unwrap_or(0);
                            match deserialized_property {
                                Ok(prop_value) => {
                                    service_in_discovery
                                        .property_builder
                                        .family_name(prop_value.family_name);

                                    service_in_discovery
                                        .property_builder
                                        .family_name_version(version);
                                    service_in_discovery.property_count += 1;
                                }
                                Err(e) => {
                                    error!("Failed to deserialize property 'family_name' for instance '{}': {}", instance_id, e);
                                }
                            }
                        }

                        "lastBreakfastTime" => {
                            let deserialized_property =
                                serde_json::from_slice::<LastBreakfastTimeProperty>(
                                    &message.payload,
                                );
                            let version = message
                                .user_properties
                                .get("Version")
                                .and_then(|v| v.parse::<u32>().ok())
                                .unwrap_or(0);
                            match deserialized_property {
                                Ok(prop_value) => {
                                    service_in_discovery
                                        .property_builder
                                        .last_breakfast_time(prop_value.timestamp);

                                    service_in_discovery
                                        .property_builder
                                        .last_breakfast_time_version(version);
                                    service_in_discovery.property_count += 1;
                                }
                                Err(e) => {
                                    error!("Failed to deserialize property 'last_breakfast_time' for instance '{}': {}", instance_id, e);
                                }
                            }
                        }

                        "breakfastLength" => {
                            let deserialized_property =
                                serde_json::from_slice::<BreakfastLengthProperty>(&message.payload);
                            let version = message
                                .user_properties
                                .get("Version")
                                .and_then(|v| v.parse::<u32>().ok())
                                .unwrap_or(0);
                            match deserialized_property {
                                Ok(prop_value) => {
                                    service_in_discovery
                                        .property_builder
                                        .breakfast_length(prop_value.length);

                                    service_in_discovery
                                        .property_builder
                                        .breakfast_length_version(version);
                                    service_in_discovery.property_count += 1;
                                }
                                Err(e) => {
                                    error!("Failed to deserialize property 'breakfast_length' for instance '{}': {}", instance_id, e);
                                }
                            }
                        }

                        "lastBirthdays" => {
                            let deserialized_property =
                                serde_json::from_slice::<LastBirthdaysProperty>(&message.payload);
                            let version = message
                                .user_properties
                                .get("Version")
                                .and_then(|v| v.parse::<u32>().ok())
                                .unwrap_or(0);
                            match deserialized_property {
                                Ok(prop_value) => {
                                    service_in_discovery
                                        .property_builder
                                        .last_birthdays(prop_value);

                                    service_in_discovery
                                        .property_builder
                                        .last_birthdays_version(version);
                                    service_in_discovery.property_count += 1;
                                }
                                Err(e) => {
                                    error!("Failed to deserialize property 'last_birthdays' for instance '{}': {}", instance_id, e);
                                }
                            }
                        }

                        _ => {
                            // Ignore unknown properties
                        }
                    }
                    Self::try_publish_discovered_service(
                        service_in_discovery,
                        &notification_tx,
                        #[cfg(feature = "metrics")]
                        &metrics,
                    );
                }
            }
        })
    }

    fn handle_message(
        message: MqttMessage,
        instances_in_discovery: &Arc<RwLock<HashMap<String, ServiceInDiscovery>>>,
        notification_tx: &broadcast::Sender<DiscoveredService>,
        #[cfg(feature = "metrics")] metrics: Arc<Mutex<SimpleDiscoveryMetrics>>,
    ) {
        if message.payload.is_empty() {
            info!("Service represented by {} is now offline", message.topic);
            // Parse instance_id from topic (format: full/{instance_id}/interface)
            let topic_parts: Vec<&str> = message.topic.split('/').collect();
            if topic_parts.len() >= 2 {
                let instance_id = topic_parts[topic_parts.len() - 2].to_string();
                let mut interfaces_guard = instances_in_discovery
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
                    {
                        let mut instance_map = instances_in_discovery
                            .write()
                            .expect("interfaces write lock poisoned");
                        let service_in_discovery = instance_map
                            .entry(info.instance.clone())
                            .or_insert_with(ServiceInDiscovery::default);
                        service_in_discovery.interface_info = Some(info);
                        Self::try_publish_discovered_service(
                            service_in_discovery,
                            &notification_tx,
                            #[cfg(feature = "metrics")]
                            &metrics,
                        );
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
        self.info_listener_handle.abort();

        self.prop_listener_handle.abort();
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
