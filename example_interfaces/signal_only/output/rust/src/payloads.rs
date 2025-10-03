//! Payloads module for SignalOnly IPC
//! 
//! Contains all the data structures, enums, and return codes used by the SignalOnly IPC system.

/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/

use num_derive::{FromPrimitive, ToPrimitive};
use num_traits::FromPrimitive;

use serde::{Deserialize, Serialize};
use iso8601_duration::Duration as IsoDuration;
use base64::prelude::*;

pub mod base64_binary_format {
    use serde::{Deserialize, Deserializer, Serializer};

    pub fn serialize<S>(bytes: &Vec<u8>, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let b64_string = BASE64_STANDARD.encode(bytes);
        serializer.serialize_str(&b64_string)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<Vec<u8>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let b64_string = String::deserialize(deserializer)?;
        BASE64_STANDARD
            .decode(b64_string.as_bytes())
            .map_err(serde::de::Error::custom)
    }

    // For Option<Vec<u8>>
    pub fn serialize_option<S>(bytes: &Option<Vec<u8>>, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match bytes {
            Some(b) => serialize(b, serializer),
            None => serializer.serialize_none(),
        }
    }

    pub fn deserialize_option<'de, D>(deserializer: D) -> Result<Option<Vec<u8>>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let opt = Option::<String>::deserialize(deserializer)?;
        match opt {
            Some(b64_string) => {
                let decoded = BASE64_STANDARD
                    .decode(b64_string.as_bytes())
                    .map_err(serde::de::Error::custom)?;
                Ok(Some(decoded))
            }
            None => Ok(None),
        }
    }
}

// Helper functions for DateTime serialization/deserialization
pub mod datetime_iso_format {
    use chrono::{DateTime, Utc};
    use serde::{Deserialize, Deserializer, Serializer};

    pub fn serialize<S>(dt: &DateTime<Utc>, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let iso_string = dt.to_rfc3339();
        serializer.serialize_str(&iso_string)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<DateTime<Utc>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let iso_string = String::deserialize(deserializer)?;
        DateTime::parse_from_rfc3339(&iso_string)
            .map(|dt| dt.with_timezone(&Utc))
            .map_err(serde::de::Error::custom)
    }
}

pub mod duration_iso_format {
    // Serialization and deserialization for Duration as ISO 8601 string
    pub fn serialize<S>(duration: &Duration, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let seconds = duration.num_seconds();
        let iso_string = format!("PT{}S", seconds);
        serializer.serialize_str(&iso_string)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<Duration, D::Error>
    where
        D: Deserializer<'de>,
    {
        let iso_string = String::deserialize(deserializer)?;
        let iso_dur = iso_string.parse::<IsoDuration>().unwrap();
        iso_dur.to_chrono()
    }
}


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








// Structures for `anotherSignal` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct AnotherSignalSignalPayload {
    pub one: f32,
    
    pub two: bool,
    
    pub three: String,
    
}

// Structures for `bark` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct BarkSignalPayload {
    pub word: String,
    
}

// Structures for `maybe_number` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct MaybeNumberSignalPayload {
    pub number: Option<i32>,
    
}

// Structures for `maybe_name` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct MaybeNameSignalPayload {
    pub name: Option<String>,
    
}

// Structures for `now` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct NowSignalPayload {
    #[serde(with = "datetime_iso_format")]
    pub timestamp: chrono::DateTime<chrono::Utc>,
    
}





#[cfg(test)]
mod tests {
    use super::*;
    use chrono::{DateTime, Utc};

    

    #[test]
    fn test_base64_binary_format_serialization() {
        use serde::{Deserialize, Serialize};
        
        #[derive(Serialize, Deserialize, Debug, PartialEq)]
        struct TestStruct {
            #[serde(with = "base64_binary_format")]
            data: Vec<u8>,
        }

        // Test with various binary data
        let test_data = vec![0x00, 0x01, 0x02, 0xFF, 0xFE, 0x42, 0x13, 0x37];
        let test_struct = TestStruct { data: test_data.clone() };

        // Test serialization
        let serialized = serde_json::to_string(&test_struct).unwrap();
        
        // The base64 encoded value of [0x00, 0x01, 0x02, 0xFF, 0xFE, 0x42, 0x13, 0x37] should be "AAEC//5CEzc="
        assert!(serialized.contains("AAEC//5CEzc="));

        // Test deserialization
        let deserialized: TestStruct = serde_json::from_str(&serialized).unwrap();
        assert_eq!(deserialized.data, test_data);
    }

    #[test]
    fn test_base64_binary_format_option_serialization() {
        use serde::{Deserialize, Serialize};
        
        #[derive(Serialize, Deserialize, Debug, PartialEq)]
        struct TestStruct {
            #[serde(with = "base64_binary_format")]
            #[serde(serialize_with = "base64_binary_format::serialize_option")]
            #[serde(deserialize_with = "base64_binary_format::deserialize_option")]
            data: Option<Vec<u8>>,
        }

        // Test with Some data
        let test_data = vec![0x48, 0x65, 0x6C, 0x6C, 0x6F]; // "Hello" in bytes
        let test_struct_some = TestStruct { data: Some(test_data.clone()) };

        let serialized_some = serde_json::to_string(&test_struct_some).unwrap();
        let deserialized_some: TestStruct = serde_json::from_str(&serialized_some).unwrap();
        assert_eq!(deserialized_some.data, Some(test_data));

        // Test with None
        let test_struct_none = TestStruct { data: None };
        let serialized_none = serde_json::to_string(&test_struct_none).unwrap();
        let deserialized_none: TestStruct = serde_json::from_str(&serialized_none).unwrap();
        assert_eq!(deserialized_none.data, None);
    }

    #[test]
    fn test_base64_binary_format_round_trip() {
        use serde::{Deserialize, Serialize};
        
        #[derive(Serialize, Deserialize, Debug, PartialEq)]
        struct BinaryData {
            #[serde(with = "base64_binary_format")]
            payload: Vec<u8>,
            name: String,
        }

        // Test with empty data
        let empty_data = BinaryData {
            payload: vec![],
            name: "empty".to_string(),
        };
        let json = serde_json::to_string(&empty_data).unwrap();
        let parsed: BinaryData = serde_json::from_str(&json).unwrap();
        assert_eq!(parsed, empty_data);

        // Test with random binary data
        let random_data = BinaryData {
            payload: vec![0xDE, 0xAD, 0xBE, 0xEF, 0xCA, 0xFE, 0xBA, 0xBE],
            name: "random".to_string(),
        };
        let json = serde_json::to_string(&random_data).unwrap();
        let parsed: BinaryData = serde_json::from_str(&json).unwrap();
        assert_eq!(parsed, random_data);
    }
}