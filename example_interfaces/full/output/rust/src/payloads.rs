//! Payloads module for Full IPC
//!
//! Contains all the data structures, enums, and return codes used by the Full IPC system.

/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/

use num_derive::{FromPrimitive, ToPrimitive};
use num_traits::FromPrimitive;
use std::fmt;

use serde::{Deserialize, Serialize};

pub mod base64_binary_format {
    use base64::Engine;
    use base64::engine::general_purpose::STANDARD as BASE64_STANDARD;
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
}

#[allow(dead_code)]
#[derive(Debug)]
pub enum MethodReturnCode {
    Success,
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
            0 => MethodReturnCode::Success,
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
            MethodReturnCode::Success => (0, None),
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
pub enum DayOfTheWeek {
    Sunday = 1,
    Monday = 2,
    Tuesday = 3,
    Wednesday = 4,
    Thursday = 5,
    Friday = 6,
    Saturday = 7,
}

#[allow(dead_code)]
impl DayOfTheWeek {
    pub fn from_u32(value: u32) -> Option<Self> {
        FromPrimitive::from_u32(value)
    }
}

impl From<DayOfTheWeek> for u32 {
    fn from(s: DayOfTheWeek) -> u32 {
        s as u32
    }
}

impl TryFrom<u32> for DayOfTheWeek {
    type Error = String;
    fn try_from(v: u32) -> Result<Self, Self::Error> {
        DayOfTheWeek::from_u32(v).ok_or_else(|| format!("Invalid DayOfTheWeek value: {}", v))
    }
}

impl fmt::Display for DayOfTheWeek {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

// --- INTERFACE STRUCTURES ---

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Lunch {
    pub drink: bool,
    pub sandwich: String,
    pub crackers: f32,
    pub day: DayOfTheWeek,

    pub order_number: Option<i32>,
    #[serde(with = "datetime_iso_format")]
    pub time_of_lunch: chrono::DateTime<chrono::Utc>,
    #[serde(with = "duration_iso_format")]
    pub duration_of_lunch: chrono::Duration,
}

// ---- METHODS ----

// Structures for `addNumbers` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `addNumbers` method.
pub struct AddNumbersRequestObject {
    pub first: i32,
    pub second: i32,
    pub third: Option<i32>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `addNumbers` method.
pub struct AddNumbersReturnValues {
    pub sum: i32,
}

// Structures for `doSomething` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `doSomething` method.
pub struct DoSomethingRequestObject {
    #[serde(rename = "aString")]
    pub a_string: String,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `doSomething` method.
pub struct DoSomethingReturnValues {
    pub label: String,
    pub identifier: i32,
    pub day: DayOfTheWeek,
}

// Structures for `echo` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `echo` method.
pub struct EchoRequestObject {
    pub message: String,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `echo` method.
pub struct EchoReturnValues {
    pub message: String,
}

// Structures for `what_time_is_it` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `what_time_is_it` method.
pub struct WhatTimeIsItRequestObject {
    #[serde(with = "datetime_iso_format")]
    pub the_first_time: chrono::DateTime<chrono::Utc>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `what_time_is_it` method.
pub struct WhatTimeIsItReturnValues {
    #[serde(with = "datetime_iso_format")]
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

// Structures for `set_the_time` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `set_the_time` method.
pub struct SetTheTimeRequestObject {
    #[serde(with = "datetime_iso_format")]
    pub the_first_time: chrono::DateTime<chrono::Utc>,
    #[serde(with = "datetime_iso_format")]
    pub the_second_time: chrono::DateTime<chrono::Utc>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `set_the_time` method.
pub struct SetTheTimeReturnValues {
    #[serde(with = "datetime_iso_format")]
    pub timestamp: chrono::DateTime<chrono::Utc>,
    pub confirmation_message: String,
}

// Structures for `forward_time` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `forward_time` method.
pub struct ForwardTimeRequestObject {
    #[serde(with = "duration_iso_format")]
    pub adjustment: chrono::Duration,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `forward_time` method.
pub struct ForwardTimeReturnValues {
    #[serde(with = "datetime_iso_format")]
    pub new_time: chrono::DateTime<chrono::Utc>,
}

// Structures for `how_off_is_the_clock` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `how_off_is_the_clock` method.
pub struct HowOffIsTheClockRequestObject {
    #[serde(with = "datetime_iso_format")]
    pub actual_time: chrono::DateTime<chrono::Utc>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `how_off_is_the_clock` method.
pub struct HowOffIsTheClockReturnValues {
    #[serde(with = "duration_iso_format")]
    pub difference: chrono::Duration,
}

// ---- SIGNALS ----

// Structures for `todayIs` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct TodayIsSignalPayload {
    #[serde(rename = "dayOfMonth")]
    pub day_of_month: i32,
    #[serde(rename = "dayOfWeek")]
    pub day_of_week: Option<DayOfTheWeek>,

    #[serde(with = "datetime_iso_format")]
    pub timestamp: chrono::DateTime<chrono::Utc>,
    #[serde(with = "duration_iso_format")]
    pub process_time: chrono::Duration,
    #[serde(with = "base64_binary_format")]
    pub memory_segment: Vec<u8>,
}

// `favorite_number` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct FavoriteNumberProperty {
    pub number: i32,
}

// `favorite_foods` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct FavoriteFoodsProperty {
    pub drink: String,
    pub slices_of_pizza: i32,
    pub breakfast: Option<String>,
}

// `lunch_menu` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct LunchMenuProperty {
    pub monday: Lunch,

    /// Tuesday's lunch menu.
    pub tuesday: Lunch,
}

// `family_name` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct FamilyNameProperty {
    pub family_name: String,
}

// `last_breakfast_time` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct LastBreakfastTimeProperty {
    #[serde(with = "datetime_iso_format")]
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

// `breakfast_length` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct BreakfastLengthProperty {
    #[serde(with = "duration_iso_format")]
    pub length: chrono::Duration,
}

// `last_birthdays` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct LastBirthdaysProperty {
    #[serde(with = "datetime_iso_format")]
    pub mom: chrono::DateTime<chrono::Utc>,
    #[serde(with = "datetime_iso_format")]
    pub dad: chrono::DateTime<chrono::Utc>,
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub sister: Option<chrono::DateTime<chrono::Utc>>,

    pub brothers_age: Option<i32>,
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::{DateTime, Utc};

    #[test]
    fn test_favorite_number_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "number": 42 
        }"#;

        let parsed: FavoriteNumberProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_favorite_foods_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "drink": "apples" ,
        
            "slices_of_pizza": 42 ,
        
            "breakfast": "apples" 
        }"#;

        let parsed: FavoriteFoodsProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_lunch_menu_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "monday": {"drink": true, "sandwich": "apples", "crackers": 3.14, "day": 7, "order_number": 42, "time_of_lunch": "1990-07-08T16:20:00Z", "duration_of_lunch": None} ,
        
            "tuesday": {"drink": true, "sandwich": "apples", "crackers": 3.14, "day": 7, "order_number": 42, "time_of_lunch": "1990-07-08T16:20:00Z", "duration_of_lunch": None} 
        }"#;

        let parsed: LunchMenuProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_family_name_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "family_name": "apples" 
        }"#;

        let parsed: FamilyNameProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_last_breakfast_time_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "timestamp": "1990-07-08T16:20:00Z" 
        }"#;

        let parsed: LastBreakfastTimeProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_breakfast_length_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "length": None 
        }"#;

        let parsed: BreakfastLengthProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_last_birthdays_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "mom": "1990-07-08T16:20:00Z" ,
        
            "dad": "1990-07-08T16:20:00Z" ,
        
            "sister": "1990-07-08T16:20:00Z" ,
        
            "brothers_age": 42 
        }"#;

        let parsed: LastBirthdaysProperty = serde_json::from_str(json_str).unwrap();
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
