//! Payloads module for Simple IPC
//!
//! Contains all the data structures, enums, and return codes used by the Simple IPC system.

/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Simple interface.

LICENSE: This generated code is not subject to any license restrictions from the generator itself.
TODO: Get license text from stinger file
*/

use num_derive::{FromPrimitive, ToPrimitive};
use num_traits::FromPrimitive;
use std::fmt;

use serde::{Deserialize, Serialize};

pub mod base64_binary_format {
    use base64::engine::general_purpose::STANDARD as BASE64_STANDARD;
    use base64::Engine;
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

    // For Vec<Vec<u8>> - serializes as array of base64 strings
    pub fn serialize_vec<S>(bytes_vec: &Vec<Vec<u8>>, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        use serde::ser::SerializeSeq;
        let mut seq = serializer.serialize_seq(Some(bytes_vec.len()))?;
        for bytes in bytes_vec {
            let b64_string = BASE64_STANDARD.encode(bytes);
            seq.serialize_element(&b64_string)?;
        }
        seq.end()
    }

    pub fn deserialize_vec<'de, D>(deserializer: D) -> Result<Vec<Vec<u8>>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let b64_strings = Vec::<String>::deserialize(deserializer)?;
        b64_strings
            .into_iter()
            .map(|b64_string| {
                BASE64_STANDARD
                    .decode(b64_string.as_bytes())
                    .map_err(serde::de::Error::custom)
            })
            .collect()
    }

    // For Option<Vec<Vec<u8>>>
    pub fn serialize_option_vec<S>(
        bytes_vec: &Option<Vec<Vec<u8>>>,
        serializer: S,
    ) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match bytes_vec {
            Some(v) => serialize_vec(v, serializer),
            None => serializer.serialize_none(),
        }
    }

    pub fn deserialize_option_vec<'de, D>(deserializer: D) -> Result<Option<Vec<Vec<u8>>>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let opt = Option::<Vec<String>>::deserialize(deserializer)?;
        match opt {
            Some(b64_strings) => {
                let decoded: Result<Vec<Vec<u8>>, _> = b64_strings
                    .into_iter()
                    .map(|b64_string| {
                        BASE64_STANDARD
                            .decode(b64_string.as_bytes())
                            .map_err(serde::de::Error::custom)
                    })
                    .collect();
                Ok(Some(decoded?))
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

    // For Option<DateTime<Utc>>
    pub fn serialize_option<S>(dt: &Option<DateTime<Utc>>, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match dt {
            Some(d) => serialize(d, serializer),
            None => serializer.serialize_none(),
        }
    }

    pub fn deserialize_option<'de, D>(deserializer: D) -> Result<Option<DateTime<Utc>>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let opt = Option::<String>::deserialize(deserializer)?;
        match opt {
            Some(iso_string) => {
                let dt = DateTime::parse_from_rfc3339(&iso_string)
                    .map(|dt| dt.with_timezone(&Utc))
                    .map_err(serde::de::Error::custom)?;
                Ok(Some(dt))
            }
            None => Ok(None),
        }
    }
    // For Vec<DateTime<Utc>> - serializes as array of ISO 8601 strings
    pub fn serialize_vec<S>(dt_vec: &Vec<DateTime<Utc>>, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        use serde::ser::SerializeSeq;
        let mut seq = serializer.serialize_seq(Some(dt_vec.len()))?;
        for dt in dt_vec {
            let iso_string = dt.to_rfc3339();
            seq.serialize_element(&iso_string)?;
        }
        seq.end()
    }

    pub fn deserialize_vec<'de, D>(deserializer: D) -> Result<Vec<DateTime<Utc>>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let iso_strings = Vec::<String>::deserialize(deserializer)?;
        iso_strings
            .into_iter()
            .map(|iso_string| {
                DateTime::parse_from_rfc3339(&iso_string)
                    .map(|dt| dt.with_timezone(&Utc))
                    .map_err(serde::de::Error::custom)
            })
            .collect()
    }

    // For Option<Vec<DateTime<Utc>>>
    pub fn serialize_option_vec<S>(
        dt_vec: &Option<Vec<DateTime<Utc>>>,
        serializer: S,
    ) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match dt_vec {
            Some(v) => serialize_vec(v, serializer),
            None => serializer.serialize_none(),
        }
    }

    pub fn deserialize_option_vec<'de, D>(
        deserializer: D,
    ) -> Result<Option<Vec<DateTime<Utc>>>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let opt = Option::<Vec<String>>::deserialize(deserializer)?;
        match opt {
            Some(iso_strings) => {
                let decoded: Result<Vec<DateTime<Utc>>, _> = iso_strings
                    .into_iter()
                    .map(|iso_string| {
                        DateTime::parse_from_rfc3339(&iso_string)
                            .map(|dt| dt.with_timezone(&Utc))
                            .map_err(serde::de::Error::custom)
                    })
                    .collect();
                Ok(Some(decoded?))
            }
            None => Ok(None),
        }
    }
}

pub mod duration_iso_format {
    use chrono::Duration;
    use iso8601_duration::Duration as IsoDuration;
    use serde::{Deserialize, Deserializer, Serializer};

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
        let iso_dur: IsoDuration = iso_string
            .parse::<IsoDuration>()
            .map_err(|e| serde::de::Error::custom(format!("{:?}", e)))?;
        let std_duration: std::time::Duration = iso_dur.to_std().ok_or_else(|| {
            serde::de::Error::custom("Failed to convert ISO duration to std::time::Duration")
        })?;
        chrono::Duration::from_std(std_duration).map_err(serde::de::Error::custom)
    }

    // For Option<Duration>
    pub fn serialize_option<S>(
        duration: &Option<Duration>,
        serializer: S,
    ) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match duration {
            Some(d) => serialize(d, serializer),
            None => serializer.serialize_none(),
        }
    }

    pub fn deserialize_option<'de, D>(deserializer: D) -> Result<Option<Duration>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let opt = Option::<String>::deserialize(deserializer)?;
        match opt {
            Some(iso_string) => {
                let iso_dur: IsoDuration = iso_string
                    .parse::<IsoDuration>()
                    .map_err(|e| serde::de::Error::custom(format!("{:?}", e)))?;
                let std_duration: std::time::Duration = iso_dur.to_std().ok_or_else(|| {
                    serde::de::Error::custom(
                        "Failed to convert ISO duration to std::time::Duration",
                    )
                })?;
                let chrono_duration =
                    chrono::Duration::from_std(std_duration).map_err(serde::de::Error::custom)?;
                Ok(Some(chrono_duration))
            }
            None => Ok(None),
        }
    }

    // For Vec<Duration> - serializes as array of ISO 8601 duration strings
    pub fn serialize_vec<S>(duration_vec: &Vec<Duration>, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        use serde::ser::SerializeSeq;
        let mut seq = serializer.serialize_seq(Some(duration_vec.len()))?;
        for duration in duration_vec {
            let seconds = duration.num_seconds();
            let iso_string = format!("PT{}S", seconds);
            seq.serialize_element(&iso_string)?;
        }
        seq.end()
    }

    pub fn deserialize_vec<'de, D>(deserializer: D) -> Result<Vec<Duration>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let iso_strings = Vec::<String>::deserialize(deserializer)?;
        iso_strings
            .into_iter()
            .map(|iso_string| {
                let iso_dur: IsoDuration = iso_string
                    .parse::<IsoDuration>()
                    .map_err(|e| serde::de::Error::custom(format!("{:?}", e)))?;
                let std_duration: std::time::Duration = iso_dur.to_std().ok_or_else(|| {
                    serde::de::Error::custom(
                        "Failed to convert ISO duration to std::time::Duration",
                    )
                })?;
                chrono::Duration::from_std(std_duration).map_err(serde::de::Error::custom)
            })
            .collect()
    }

    // For Option<Vec<Duration>>
    pub fn serialize_option_vec<S>(
        duration_vec: &Option<Vec<Duration>>,
        serializer: S,
    ) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match duration_vec {
            Some(v) => serialize_vec(v, serializer),
            None => serializer.serialize_none(),
        }
    }

    pub fn deserialize_option_vec<'de, D>(
        deserializer: D,
    ) -> Result<Option<Vec<Duration>>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let opt = Option::<Vec<String>>::deserialize(deserializer)?;
        match opt {
            Some(iso_strings) => {
                let decoded: Result<Vec<Duration>, _> = iso_strings
                    .into_iter()
                    .map(|iso_string| {
                        let iso_dur: IsoDuration = iso_string
                            .parse::<IsoDuration>()
                            .map_err(|e| serde::de::Error::custom(format!("{:?}", e)))?;
                        let std_duration: std::time::Duration =
                            iso_dur.to_std().ok_or_else(|| {
                                serde::de::Error::custom(
                                    "Failed to convert ISO duration to std::time::Duration",
                                )
                            })?;
                        chrono::Duration::from_std(std_duration).map_err(serde::de::Error::custom)
                    })
                    .collect();
                Ok(Some(decoded?))
            }
            None => Ok(None),
        }
    }
}

#[allow(dead_code)]
#[derive(Debug, Clone)]
pub enum MethodReturnCode {
    Success(Option<String>),
    ClientError(String),
    ServerError(String),
    TransportError(String),
    PayloadError(String),
    ClientSerializationError(String),
    ClientDeserializationError(String),
    ServerSerializationError(String),
    ServerDeserializationError(String),
    MethodNotFound(String),
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
            0 => MethodReturnCode::Success(message),
            1 => MethodReturnCode::ClientError(message.unwrap_or_default()),
            2 => MethodReturnCode::ServerError(message.unwrap_or_default()),
            3 => MethodReturnCode::TransportError(message.unwrap_or_default()),
            4 => MethodReturnCode::PayloadError(message.unwrap_or_default()),
            5 => MethodReturnCode::ClientSerializationError(message.unwrap_or_default()),
            6 => MethodReturnCode::ClientDeserializationError(message.unwrap_or_default()),
            7 => MethodReturnCode::ServerSerializationError(message.unwrap_or_default()),
            8 => MethodReturnCode::ServerDeserializationError(message.unwrap_or_default()),
            9 => MethodReturnCode::MethodNotFound(message.unwrap_or_default()),
            10 => MethodReturnCode::Unauthorized(message.unwrap_or_default()),
            11 => MethodReturnCode::Timeout(message.unwrap_or_default()),
            12 => MethodReturnCode::OutOfSync(message.unwrap_or_default()),
            13 => MethodReturnCode::UnknownError(message.unwrap_or_default()),
            14 => MethodReturnCode::NotImplemented(message.unwrap_or_default()),
            15 => MethodReturnCode::ServiceUnavailable(message.unwrap_or_default()),
            _ => MethodReturnCode::UnknownError(message.unwrap_or_default()),
        }
    }

    pub fn to_code(&self) -> (u32, Option<String>) {
        match self {
            MethodReturnCode::Success(opt_msg) => (0, opt_msg.clone()),
            MethodReturnCode::ClientError(msg) => (1, Some(msg.clone())),
            MethodReturnCode::ServerError(msg) => (2, Some(msg.clone())),
            MethodReturnCode::TransportError(msg) => (3, Some(msg.clone())),
            MethodReturnCode::PayloadError(msg) => (4, Some(msg.clone())),
            MethodReturnCode::ClientSerializationError(msg) => (5, Some(msg.clone())),
            MethodReturnCode::ClientDeserializationError(msg) => (6, Some(msg.clone())),
            MethodReturnCode::ServerSerializationError(msg) => (7, Some(msg.clone())),
            MethodReturnCode::ServerDeserializationError(msg) => (8, Some(msg.clone())),
            MethodReturnCode::MethodNotFound(msg) => (9, Some(msg.clone())),
            MethodReturnCode::Unauthorized(msg) => (10, Some(msg.clone())),
            MethodReturnCode::Timeout(msg) => (11, Some(msg.clone())),
            MethodReturnCode::OutOfSync(msg) => (12, Some(msg.clone())),
            MethodReturnCode::UnknownError(msg) => (13, Some(msg.clone())),
            MethodReturnCode::NotImplemented(msg) => (14, Some(msg.clone())),
            MethodReturnCode::ServiceUnavailable(msg) => (15, Some(msg.clone())),
        }
    }
}

// --- ENUMERATIONS ---

#[repr(u32)]
#[derive(Debug, FromPrimitive, ToPrimitive, Clone, Serialize, Deserialize, PartialEq)]
#[serde(into = "u32", try_from = "u32")]
pub enum Gender {
    Male = 1,
    Female = 2,
    Other = 3,
}

#[allow(dead_code)]
impl Gender {
    pub fn from_u32(value: u32) -> Option<Self> {
        FromPrimitive::from_u32(value)
    }
}

impl From<Gender> for u32 {
    fn from(s: Gender) -> u32 {
        s as u32
    }
}

impl TryFrom<u32> for Gender {
    type Error = String;
    fn try_from(v: u32) -> Result<Self, Self::Error> {
        Gender::from_u32(v).ok_or_else(|| format!("Invalid Gender value: {}", v))
    }
}

impl fmt::Display for Gender {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

// --- INTERFACE STRUCTURES ---

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Person {
    pub name: String,
    pub gender: Gender,
}

// ---- METHODS ----

// Structures for `trade_numbers` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `trade_numbers` method.
pub struct TradeNumbersRequestObject {
    pub your_number: i32,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `trade_numbers` method.
pub struct TradeNumbersReturnValues {
    pub my_number: i32,
}

// ---- SIGNALS ----

// Structures for `person_entered` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct PersonEnteredSignalPayload {
    pub person: Person,
}

// `school` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct SchoolProperty {
    pub name: String,
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::{DateTime, Utc};

    #[test]
    fn test_school_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "name": "apples" 
        }"#;

        let parsed: SchoolProperty = serde_json::from_str(json_str).unwrap();
    }

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
        let test_struct = TestStruct {
            data: test_data.clone(),
        };

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
        let test_struct_some = TestStruct {
            data: Some(test_data.clone()),
        };

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
