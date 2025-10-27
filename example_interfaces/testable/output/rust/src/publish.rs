use crate::payloads::MethodReturnCode;
use serde::Serialize;
use stinger_mqtt_trait::message::{MqttMessage, MqttMessageBuilder, QoS};
use uuid::Uuid;

impl MqttMessage {
    pub fn property_message<T: Serialize>(
        topic: &str,
        payload: &T,
        property_version: String,
    ) -> Self {
        MqttMessageBuilder::new()
            .topic(topic)
            .payload_object(payload)
            .qos(QoS::AtLeastOnce)
            .retain(true)
            .property_version("Version", property_version)
            .build()
    }

    #[cfg(feature = "client")]
    pub fn request<T: Serialize>(
        topic: &str,
        payload: &T,
        correlation_id: Uuid,
        response_topic: String,
    ) -> Self {
        MqttMessageBuilder::new()
            .topic(topic)
            .payload_object(payload)
            .qos(QoS::ExactlyOnce)
            .retain(false)
            .correlation_id(correlation_id.to_string())
            .response_topic(response_topic)
            .build()
    }

    #[cfg(feature = "server")]
    pub fn response<T: Serialize>(
        topic: &str,
        payload: &T,
        correlation_id: Uuid,
        return_code: Option<MethodReturnCode>,
        debug_info: Option<String>,
    ) -> Self {
        let builder = MqttMessageBuilder::new()
            .topic(topic)
            .payload_object(payload)
            .qos(QoS::AtLeastOnce)
            .retain(false)
            .correlation_id(correlation_id.to_string());
        if let Some(code) = return_code {
            builder.user_property("ReturnCode", code as u8);
        }
        if let Some(info) = debug_info {
            builder.user_property("DebugInfo", info);
        }
        builder.build()
    }

    pub fn signal<T: Serialize>(topic: &str, payload: &T) -> Self {
        MqttMessageBuilder::new()
            .topic(topic)
            .payload_object(payload)
            .qos(QoS::ExactlyOnce)
            .retain(false)
            .build()
    }
}
