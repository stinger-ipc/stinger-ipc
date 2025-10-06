/*
DO NOT MODIFY THIS FILE.  It is automatically generated and changes will be over-written
on the next generation.

This is the Client for the Full interface.
*/
use std::collections::{HashMap, HashSet};
use std::fmt;
use std::sync::{Arc, RwLock};

use mqttier::{MqttierClient, MqttierError, ReceivedMessage};
use tokio::sync::mpsc;
use tokio::task::JoinHandle;

use crate::interface::InterfaceInfo;

#[derive(Debug)]
pub enum DiscoveryError {
	Subscribe(MqttierError),
}

impl fmt::Display for DiscoveryError {
	fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
		match self {
			DiscoveryError::Subscribe(err) => write!(f, "failed to subscribe for discovery: {err}"),
		}
	}
}

impl std::error::Error for DiscoveryError {}

impl From<MqttierError> for DiscoveryError {
	fn from(value: MqttierError) -> Self {
		DiscoveryError::Subscribe(value)
	}
}

pub struct Discovery {
	service_name: String,
	mqtt_client: MqttierClient,
	subscription_id: usize,
	discovered_interfaces: Arc<RwLock<HashMap<String, InterfaceInfo>>>,
	listener_handle: JoinHandle<()>,
}

impl Discovery {
	pub async fn new(
		connection: &mut MqttierClient,
	) -> Result<Self, DiscoveryError> {
		let service_name = "Full".to_string();
		let discovery_topic = format!("full/{}/interface", "+");

		let (message_tx, message_rx) = mpsc::channel::<ReceivedMessage>(32);
		let subscription_id = connection
			.subscribe(discovery_topic, 1, message_tx.clone())
			.await
			.map_err(DiscoveryError::from)?;

		let discovered_interfaces = Arc::new(RwLock::new(HashMap::new()));

		let listener_handle = Self::spawn_listener(
			message_rx,
			discovered_interfaces.clone(),
		);

		Ok(Self {
			service_name,
			mqtt_client: connection.clone(),
			subscription_id,
			discovered_interfaces,
			listener_handle,
		})
	}

	pub fn service_name(&self) -> &str {
		&self.service_name
	}

	pub fn discovered_interfaces(&self) -> Vec<InterfaceInfo> {
		let guard = self.discovered_interfaces.read().expect("interfaces poisoned");
		guard.values().cloned().collect()
	}

	pub fn first_service(&self) -> Option<InterfaceInfo> {
		let order_guard = self.discovered_order.read().expect("discovery order poisoned");
		let first_instance = order_guard.first()?.clone();
		drop(order_guard);

		let interfaces_guard = self
			.discovered_interfaces
			.read()
			.expect("interfaces poisoned");
		interfaces_guard.get(&first_instance).cloned()
	}

	pub fn subscription_id(&self) -> usize {
		self.subscription_id
	}

	fn spawn_listener(
		mut message_rx: mpsc::Receiver<ReceivedMessage>,
		discovered_interfaces: Arc<RwLock<HashMap<String, InterfaceInfo>>>,
		discovered_order: Arc<RwLock<Vec<String>>>,
		discovered_topics: Arc<RwLock<HashSet<String>>>,
	) -> JoinHandle<()> {
		tokio::spawn(async move {
			while let Some(message) = message_rx.recv().await {
				Self::handle_message(
					message,
					&discovered_interfaces,
					&discovered_order,
					&discovered_topics,
				);
			}
		})
	}

	fn handle_message(
		message: ReceivedMessage,
		discovered_interfaces: &Arc<RwLock<HashMap<String, InterfaceInfo>>>,
		discovered_order: &Arc<RwLock<Vec<String>>>,
		discovered_topics: &Arc<RwLock<HashSet<String>>>,
	) {
		if let Ok(info) = serde_json::from_slice::<InterfaceInfo>(&message.payload) {
			let mut interfaces_guard = discovered_interfaces
				.write()
				.expect("interfaces write lock poisoned");
			let instance_id = info.instance.clone();
			let is_new_instance = interfaces_guard.insert(instance_id.clone(), info).is_none();
			drop(interfaces_guard);

			if is_new_instance {
				let mut order_guard = discovered_order
					.write()
					.expect("discovery order write lock poisoned");
				order_guard.push(instance_id);
			}

			let mut topic_guard = discovered_topics
				.write()
				.expect("topics write lock poisoned");
			topic_guard.insert(message.topic);
		}
	}
}

impl Drop for Discovery {
	fn drop(&mut self) {
		self.listener_handle.abort();
	}
}

#[cfg(test)]
mod tests {
	use super::*;

	fn sample_message(topic: &str, instance: &str) -> ReceivedMessage {
		let info = InterfaceInfo {
			interface_name: "sample".into(),
			title: "Sample".into(),
			version: "1.0".into(),
			instance: instance.into(),
			connection_topic: format!("sample/{instance}"),
			timestamp: "2024-01-01T00:00:00Z".into(),
		};
		let payload = serde_json::to_vec(&info).expect("serialize");

		ReceivedMessage {
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
		let order = Arc::new(RwLock::new(Vec::new()));
		let topics = Arc::new(RwLock::new(HashSet::new()));

		Discovery::handle_message(
			sample_message("service/alpha/interface", "alpha"),
			&interfaces,
			&order,
			&topics,
		);
		Discovery::handle_message(
			sample_message("service/beta/interface", "beta"),
			&interfaces,
			&order,
			&topics,
		);
		Discovery::handle_message(
			sample_message("service/alpha/interface", "alpha"),
			&interfaces,
			&order,
			&topics,
		);

		let order_guard = order.read().unwrap();
		assert_eq!(order_guard.len(), 2);
		assert_eq!(order_guard[0], "alpha");
		assert_eq!(order_guard[1], "beta");

		let topics_guard = topics.read().unwrap();
		assert_eq!(topics_guard.len(), 2);
		assert!(topics_guard.contains("service/alpha/interface"));
		assert!(topics_guard.contains("service/beta/interface"));
	}
}