pub mod payloads;

// Re-export all public types from payloads
pub use payloads::*;

#[allow(dead_code)]
#[derive(Debug)]
pub enum MethodReturnCode {
    Success,
    ClientError(String),
    ServerError(String),
    TransportError(String),
    PayloadError(String),
    SerializationError(String),
    DeserializationError(String),
    Unauthorized(String),
    Timeout(String),
    OutOfSync(String),
    UnknownError(String),
    NotImplemented(String),
    ServiceUnavailable(String),
}

impl MethodReturnCode {
    pub fn from_code(code: u32, message: Option<String>) -> Self {
        match code {
            0 => MethodReturnCode::Success,
            1 => MethodReturnCode::ClientError(message.unwrap_or_default()),
            2 => MethodReturnCode::ServerError(message.unwrap_or_default()),
            3 => MethodReturnCode::TransportError(message.unwrap_or_default()),
            4 => MethodReturnCode::PayloadError(message.unwrap_or_default()),
            5 => MethodReturnCode::SerializationError(message.unwrap_or_default()),
            6 => MethodReturnCode::DeserializationError(message.unwrap_or_default()),
            7 => MethodReturnCode::Unauthorized(message.unwrap_or_default()),
            8 => MethodReturnCode::Timeout(message.unwrap_or_default()),
            9 => MethodReturnCode::OutOfSync(message.unwrap_or_default()),
            10 => MethodReturnCode::UnknownError(message.unwrap_or_default()),
            11 => MethodReturnCode::NotImplemented(message.unwrap_or_default()),
            12 => MethodReturnCode::ServiceUnavailable(message.unwrap_or_default()),
            _ => MethodReturnCode::UnknownError(message.unwrap_or_default()),
        }
    }

    pub fn to_code(&self) -> (u32, Option<String>) {
        match self {
            MethodReturnCode::Success => (0, None),
            MethodReturnCode::ClientError(msg) => (1, Some(msg.clone())),
            MethodReturnCode::ServerError(msg) => (2, Some(msg.clone())),
            MethodReturnCode::TransportError(msg) => (3, Some(msg.clone())),
            MethodReturnCode::PayloadError(msg) => (4, Some(msg.clone())),
            MethodReturnCode::SerializationError(msg) => (5, Some(msg.clone())),
            MethodReturnCode::DeserializationError(msg) => (6, Some(msg.clone())),
            MethodReturnCode::Unauthorized(msg) => (7, Some(msg.clone())),
            MethodReturnCode::Timeout(msg) => (8, Some(msg.clone())),
            MethodReturnCode::OutOfSync(msg) => (9, Some(msg.clone())),
            MethodReturnCode::UnknownError(msg) => (10, Some(msg.clone())),
            MethodReturnCode::NotImplemented(msg) => (11, Some(msg.clone())),
            MethodReturnCode::ServiceUnavailable(msg) => (12, Some(msg.clone())),
        }
    }
}
