use crate::payloads::MethodReturnCode;
use bytes::Bytes;
use serde::Serialize;
use stinger_mqtt_trait::message::{MqttMessage, MqttMessageBuilder, QoS};
#[cfg(feature = "client")]
use uuid::Uuid;

#[cfg(feature = "server")]
pub fn interface_online(
    topic: &str,
    payload: &crate::interface::InterfaceInfo,
    message_expiry_seconds: u32,
) -> Result<MqttMessage, MethodReturnCode> {
    MqttMessageBuilder::default()
        .topic(topic)
        .object_payload(payload)
        .map_err(|e| MethodReturnCode::ServerSerializationError(e.to_string()))?
        .qos(QoS::AtLeastOnce)
        .retain(true)
        .message_expiry_interval(message_expiry_seconds)
        .build()
        .map_err(|e| MethodReturnCode::PayloadError(e.to_string()))
}

#[cfg(feature = "client")]
pub fn request<T: Serialize>(
    topic: &str,
    payload: &T,
    correlation_id: Uuid,
    response_topic: String,
) -> Result<MqttMessage, MethodReturnCode> {
    MqttMessageBuilder::default()
        .topic(topic)
        .object_payload(payload)
        .map_err(|e| MethodReturnCode::ClientSerializationError(e.to_string()))?
        .qos(QoS::ExactlyOnce)
        .retain(false)
        .correlation_data(Bytes::from(correlation_id.to_string()))
        .response_topic(response_topic)
        .build()
        .map_err(|e| MethodReturnCode::PayloadError(e.to_string()))
}

#[cfg(feature = "server")]
pub fn response<T: Serialize>(
    topic: &str,
    payload: &T,
    correlation_data: Bytes,
    debug_info: Option<String>,
) -> Result<MqttMessage, MethodReturnCode> {
    let mut builder = MqttMessageBuilder::default();
    builder
        .topic(topic)
        .object_payload(payload)
        .map_err(|e| MethodReturnCode::ServerSerializationError(e.to_string()))?
        .qos(QoS::AtLeastOnce)
        .retain(false)
        .correlation_data(correlation_data);
    if let Some(info) = debug_info {
        builder.user_property("DebugInfo", info);
    }
    builder
        .build()
        .map_err(|e| MethodReturnCode::PayloadError(e.to_string()))
}

#[cfg(feature = "server")]
pub fn error_response(
    topic: &str,
    correlation_data: Option<Bytes>,
    return_code: MethodReturnCode,
) -> Result<MqttMessage, MethodReturnCode> {
    let (code_num, debug_info) = return_code.to_code();
    let mut builder = MqttMessageBuilder::default();
    builder
        .topic(topic)
        .payload("{}")
        .qos(QoS::AtLeastOnce)
        .retain(false)
        .correlation_data(correlation_data)
        .user_property("ReturnCode", code_num.to_string());
    if let Some(info) = debug_info {
        builder.user_property("DebugInfo", info);
    }
    builder
        .build()
        .map_err(|e| MethodReturnCode::PayloadError(e.to_string()))
}

#[cfg(feature = "server")]
pub fn signal<T: Serialize>(topic: &str, payload: &T) -> Result<MqttMessage, MethodReturnCode> {
    MqttMessageBuilder::default()
        .topic(topic)
        .object_payload(payload)
        .map_err(|e| MethodReturnCode::ServerSerializationError(e.to_string()))?
        .qos(QoS::ExactlyOnce)
        .retain(false)
        .build()
        .map_err(|e| MethodReturnCode::PayloadError(e.to_string()))
}
