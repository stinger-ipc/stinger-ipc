//! Payloads module for Test Able IPC
//!
//! Contains all the data structures, enums, and return codes used by the Test Able IPC system.

/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Test Able interface.
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

// --- ENUMERATIONS ---

#[repr(u32)]
#[derive(Debug, FromPrimitive, ToPrimitive, Clone, Serialize, Deserialize, PartialEq)]
#[serde(into = "u32", try_from = "u32")]
pub enum Numbers {
    One = 1,
    Two = 2,
    Three = 3,
}

#[allow(dead_code)]
impl Numbers {
    pub fn from_u32(value: u32) -> Option<Self> {
        FromPrimitive::from_u32(value)
    }
}

impl From<Numbers> for u32 {
    fn from(s: Numbers) -> u32 {
        s as u32
    }
}

impl TryFrom<u32> for Numbers {
    type Error = String;
    fn try_from(v: u32) -> Result<Self, Self::Error> {
        Numbers::from_u32(v).ok_or_else(|| format!("Invalid Numbers value: {}", v))
    }
}

impl fmt::Display for Numbers {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

// --- INTERFACE STRUCTURES ---

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct AllTypes {
    pub the_bool: bool,

    pub the_int: i32,
    /// A floating point number.  Bool and int do not have descriptions.
    pub the_number: f32,
    /// A string type.
    pub the_str: String,
    /// An enum type
    pub the_enum: Numbers,

    /// A date and time type.
    #[serde(with = "datetime_iso_format")]
    pub date_and_time: chrono::DateTime<chrono::Utc>,

    /// A duration type.
    #[serde(with = "duration_iso_format")]
    pub time_duration: chrono::Duration,

    /// A binary type.
    #[serde(with = "base64_binary_format")]
    pub data: Vec<u8>,

    /// An optional integer type.#[serde(rename = "OptionalInteger")]
    pub optional_integer: Option<i32>,
    /// An optional string type.#[serde(rename = "OptionalString")]
    pub optional_string: Option<String>,
    /// An optional enum type, one of the numbers.#[serde(rename = "OptionalEnum")]
    pub optional_enum: Option<Numbers>,

    /// An optional date and time type.#[serde(rename = "OptionalDateTime")]
    #[serde(with = "datetime_iso_format")]
    pub optional_date_time: chrono::DateTime<chrono::Utc>,

    /// An optional duration type.#[serde(rename = "OptionalDuration")]
    #[serde(with = "duration_iso_format")]
    pub optional_duration: chrono::Duration,

    /// An optional binary type.#[serde(rename = "OptionalBinary")]
    #[serde(with = "base64_binary_format")]
    pub optional_binary: Vec<u8>,
}

// ---- METHODS ----

// Structures for `callWithNothing` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callWithNothing` method.
pub struct CallWithNothingRequestObject {}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callWithNothing` method.
pub struct CallWithNothingReturnValues {}

// Structures for `callOneInteger` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOneInteger` method.
pub struct CallOneIntegerRequestObject {
    pub input1: i32,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOneInteger` method.
pub struct CallOneIntegerReturnValues {
    pub output1: i32,
}

// Structures for `callOptionalInteger` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOptionalInteger` method.
pub struct CallOptionalIntegerRequestObject {
    pub input1: Option<i32>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalInteger` method.
pub struct CallOptionalIntegerReturnValues {
    pub output1: Option<i32>,
}

// Structures for `callThreeIntegers` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callThreeIntegers` method.
pub struct CallThreeIntegersRequestObject {
    /// The first integer input.  The other two don't have descriptions.
    pub input1: i32,

    pub input2: i32,

    pub input3: Option<i32>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeIntegers` method.
pub struct CallThreeIntegersReturnValues {
    /// The first integer output.  The other two don't have descriptions.
    pub output1: i32,

    pub output2: i32,

    pub output3: Option<i32>,
}

// Structures for `callOneString` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOneString` method.
pub struct CallOneStringRequestObject {
    pub input1: String,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOneString` method.
pub struct CallOneStringReturnValues {
    pub output1: String,
}

// Structures for `callOptionalString` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOptionalString` method.
pub struct CallOptionalStringRequestObject {
    pub input1: Option<String>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalString` method.
pub struct CallOptionalStringReturnValues {
    pub output1: Option<String>,
}

// Structures for `callThreeStrings` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callThreeStrings` method.
pub struct CallThreeStringsRequestObject {
    /// The first string input.  The other two don't have descriptions.
    pub input1: String,

    pub input2: Option<String>,

    pub input3: String,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeStrings` method.
pub struct CallThreeStringsReturnValues {
    /// The first string output.  The other two don't have descriptions.
    pub output1: String,

    pub output2: Option<String>,

    pub output3: String,
}

// Structures for `callOneEnum` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOneEnum` method.
pub struct CallOneEnumRequestObject {
    pub input1: Numbers,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOneEnum` method.
pub struct CallOneEnumReturnValues {
    pub output1: Numbers,
}

// Structures for `callOptionalEnum` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOptionalEnum` method.
pub struct CallOptionalEnumRequestObject {
    pub input1: Option<Numbers>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalEnum` method.
pub struct CallOptionalEnumReturnValues {
    pub output1: Option<Numbers>,
}

// Structures for `callThreeEnums` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callThreeEnums` method.
pub struct CallThreeEnumsRequestObject {
    /// The first enum input.  The other two don't have descriptions.
    pub input1: Numbers,

    pub input2: Numbers,

    pub input3: Option<Numbers>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeEnums` method.
pub struct CallThreeEnumsReturnValues {
    /// The first enum output.  The other two don't have descriptions.
    pub output1: Numbers,

    pub output2: Numbers,

    pub output3: Option<Numbers>,
}

// Structures for `callOneStruct` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOneStruct` method.
pub struct CallOneStructRequestObject {
    pub input1: AllTypes,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOneStruct` method.
pub struct CallOneStructReturnValues {
    pub output1: AllTypes,
}

// Structures for `callOptionalStruct` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOptionalStruct` method.
pub struct CallOptionalStructRequestObject {
    pub input1: AllTypes,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalStruct` method.
pub struct CallOptionalStructReturnValues {
    pub output1: AllTypes,
}

// Structures for `callThreeStructs` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callThreeStructs` method.
pub struct CallThreeStructsRequestObject {
    /// The first struct input.  The other two don't have descriptions.
    pub input1: AllTypes,

    pub input2: AllTypes,

    pub input3: AllTypes,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeStructs` method.
pub struct CallThreeStructsReturnValues {
    /// The first struct output.  The other two don't have descriptions.
    pub output1: AllTypes,

    pub output2: AllTypes,

    pub output3: AllTypes,
}

// Structures for `callOneDateTime` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOneDateTime` method.
pub struct CallOneDateTimeRequestObject {
    #[serde(with = "datetime_iso_format")]
    pub input1: chrono::DateTime<chrono::Utc>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOneDateTime` method.
pub struct CallOneDateTimeReturnValues {
    #[serde(with = "datetime_iso_format")]
    pub output1: chrono::DateTime<chrono::Utc>,
}

// Structures for `callOptionalDateTime` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOptionalDateTime` method.
pub struct CallOptionalDateTimeRequestObject {
    #[serde(with = "datetime_iso_format")]
    pub input1: chrono::DateTime<chrono::Utc>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalDateTime` method.
pub struct CallOptionalDateTimeReturnValues {
    #[serde(with = "datetime_iso_format")]
    pub output1: chrono::DateTime<chrono::Utc>,
}

// Structures for `callThreeDateTimes` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callThreeDateTimes` method.
pub struct CallThreeDateTimesRequestObject {
    /// The first date and time input.  The other two don't have descriptions.
    #[serde(with = "datetime_iso_format")]
    pub input1: chrono::DateTime<chrono::Utc>,

    #[serde(with = "datetime_iso_format")]
    pub input2: chrono::DateTime<chrono::Utc>,

    #[serde(with = "datetime_iso_format")]
    pub input3: chrono::DateTime<chrono::Utc>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeDateTimes` method.
pub struct CallThreeDateTimesReturnValues {
    #[serde(with = "datetime_iso_format")]
    /// The first date and time output.  The other two don't have descriptions.
    pub output1: chrono::DateTime<chrono::Utc>,
    #[serde(with = "datetime_iso_format")]
    pub output2: chrono::DateTime<chrono::Utc>,
    #[serde(with = "datetime_iso_format")]
    pub output3: chrono::DateTime<chrono::Utc>,
}

// Structures for `callOneDuration` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOneDuration` method.
pub struct CallOneDurationRequestObject {
    #[serde(with = "duration_iso_format")]
    pub input1: chrono::Duration,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOneDuration` method.
pub struct CallOneDurationReturnValues {
    #[serde(with = "duration_iso_format")]
    pub output1: chrono::Duration,
}

// Structures for `callOptionalDuration` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOptionalDuration` method.
pub struct CallOptionalDurationRequestObject {
    #[serde(with = "duration_iso_format")]
    pub input1: chrono::Duration,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalDuration` method.
pub struct CallOptionalDurationReturnValues {
    #[serde(with = "duration_iso_format")]
    pub output1: chrono::Duration,
}

// Structures for `callThreeDurations` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callThreeDurations` method.
pub struct CallThreeDurationsRequestObject {
    /// The first duration input.  The other two don't have descriptions.
    #[serde(with = "duration_iso_format")]
    pub input1: chrono::Duration,

    #[serde(with = "duration_iso_format")]
    pub input2: chrono::Duration,

    #[serde(with = "duration_iso_format")]
    pub input3: chrono::Duration,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeDurations` method.
pub struct CallThreeDurationsReturnValues {
    #[serde(with = "duration_iso_format")]
    /// The first duration output.  The other two don't have descriptions.
    pub output1: chrono::Duration,
    #[serde(with = "duration_iso_format")]
    pub output2: chrono::Duration,
    #[serde(with = "duration_iso_format")]
    pub output3: chrono::Duration,
}

// Structures for `callOneBinary` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOneBinary` method.
pub struct CallOneBinaryRequestObject {
    #[serde(with = "base64_binary_format")]
    pub input1: Vec<u8>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOneBinary` method.
pub struct CallOneBinaryReturnValues {
    #[serde(with = "base64_binary_format")]
    pub output1: Vec<u8>,
}

// Structures for `callOptionalBinary` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOptionalBinary` method.
pub struct CallOptionalBinaryRequestObject {
    #[serde(with = "base64_binary_format")]
    pub input1: Vec<u8>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalBinary` method.
pub struct CallOptionalBinaryReturnValues {
    #[serde(with = "base64_binary_format")]
    pub output1: Vec<u8>,
}

// Structures for `callThreeBinaries` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callThreeBinaries` method.
pub struct CallThreeBinariesRequestObject {
    /// The first binary input.  The other two don't have descriptions.
    #[serde(with = "base64_binary_format")]
    pub input1: Vec<u8>,

    #[serde(with = "base64_binary_format")]
    pub input2: Vec<u8>,

    #[serde(with = "base64_binary_format")]
    pub input3: Vec<u8>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeBinaries` method.
pub struct CallThreeBinariesReturnValues {
    #[serde(with = "base64_binary_format")]
    /// The first binary output.  The other two don't have descriptions.
    pub output1: Vec<u8>,
    #[serde(with = "base64_binary_format")]
    pub output2: Vec<u8>,
    #[serde(with = "base64_binary_format")]
    pub output3: Vec<u8>,
}

// ---- SIGNALS ----

// Structures for `empty` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct EmptySignalPayload {}

// Structures for `singleInt` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleIntSignalPayload {
    /// The integer value.
    pub value: i32,
}

// Structures for `singleOptionalInt` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleOptionalIntSignalPayload {
    /// The integer value.
    pub value: Option<i32>,
}

// Structures for `threeIntegers` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ThreeIntegersSignalPayload {
    /// The first integer value.
    pub first: i32,
    /// The second integer value.
    pub second: i32,
    /// The third integer value.
    pub third: Option<i32>,
}

// Structures for `singleString` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleStringSignalPayload {
    /// The string value.
    pub value: String,
}

// Structures for `singleOptionalString` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleOptionalStringSignalPayload {
    /// The string value.
    pub value: Option<String>,
}

// Structures for `threeStrings` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ThreeStringsSignalPayload {
    /// The first string value.
    pub first: String,
    /// The second string value.
    pub second: String,
    /// The third string value.
    pub third: Option<String>,
}

// Structures for `singleEnum` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleEnumSignalPayload {
    /// The enum value.
    pub value: Numbers,
}

// Structures for `singleOptionalEnum` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleOptionalEnumSignalPayload {
    /// The enum value.
    pub value: Option<Numbers>,
}

// Structures for `threeEnums` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ThreeEnumsSignalPayload {
    /// The first enum value.
    pub first: Numbers,
    /// The second enum value.
    pub second: Numbers,
    /// The third enum value.
    pub third: Option<Numbers>,
}

// Structures for `singleStruct` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleStructSignalPayload {
    /// The struct value.
    pub value: AllTypes,
}

// Structures for `singleOptionalStruct` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleOptionalStructSignalPayload {
    /// The struct value.
    pub value: AllTypes,
}

// Structures for `threeStructs` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ThreeStructsSignalPayload {
    /// The first struct value.
    pub first: AllTypes,
    /// The second struct value.
    pub second: AllTypes,
    /// The third struct value.
    pub third: AllTypes,
}

// Structures for `singleDateTime` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleDateTimeSignalPayload {
    /// The date and time value.
    #[serde(with = "datetime_iso_format")]
    pub value: chrono::DateTime<chrono::Utc>,
}

// Structures for `singleOptionalDatetime` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleOptionalDatetimeSignalPayload {
    /// The date and time value.
    #[serde(with = "datetime_iso_format")]
    pub value: chrono::DateTime<chrono::Utc>,
}

// Structures for `threeDateTimes` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ThreeDateTimesSignalPayload {
    /// The first date and time value.
    #[serde(with = "datetime_iso_format")]
    pub first: chrono::DateTime<chrono::Utc>,
    /// The second date and time value.
    #[serde(with = "datetime_iso_format")]
    pub second: chrono::DateTime<chrono::Utc>,
    /// The third date and time value.
    #[serde(with = "datetime_iso_format")]
    pub third: chrono::DateTime<chrono::Utc>,
}

// Structures for `singleDuration` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleDurationSignalPayload {
    /// The duration value.
    #[serde(with = "duration_iso_format")]
    pub value: chrono::Duration,
}

// Structures for `singleOptionalDuration` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleOptionalDurationSignalPayload {
    /// The duration value.
    #[serde(with = "duration_iso_format")]
    pub value: chrono::Duration,
}

// Structures for `threeDurations` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ThreeDurationsSignalPayload {
    /// The first duration value.
    #[serde(with = "duration_iso_format")]
    pub first: chrono::Duration,
    /// The second duration value.
    #[serde(with = "duration_iso_format")]
    pub second: chrono::Duration,
    /// The third duration value.
    #[serde(with = "duration_iso_format")]
    pub third: chrono::Duration,
}

// Structures for `singleBinary` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleBinarySignalPayload {
    /// The binary value.
    #[serde(with = "base64_binary_format")]
    pub value: Vec<u8>,
}

// Structures for `singleOptionalBinary` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleOptionalBinarySignalPayload {
    /// The binary value.
    #[serde(with = "base64_binary_format")]
    pub value: Vec<u8>,
}

// Structures for `threeBinaries` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ThreeBinariesSignalPayload {
    /// The first binary value.
    #[serde(with = "base64_binary_format")]
    pub first: Vec<u8>,
    /// The second binary value.
    #[serde(with = "base64_binary_format")]
    pub second: Vec<u8>,
    /// The third binary value.
    #[serde(with = "base64_binary_format")]
    pub third: Vec<u8>,
}

// `read_write_integer` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteIntegerProperty {
    pub value: i32,
}

// `read_only_integer` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadOnlyIntegerProperty {
    pub value: i32,
}

// `read_write_optional_integer` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteOptionalIntegerProperty {
    pub value: Option<i32>,
}

// `read_write_two_integers` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoIntegersProperty {
    pub first: i32,
    pub second: Option<i32>,
}

// `read_only_string` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadOnlyStringProperty {
    pub value: String,
}

// `read_write_string` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteStringProperty {
    pub value: String,
}

// `read_write_optional_string` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteOptionalStringProperty {
    pub value: Option<String>,
}

// `read_write_two_strings` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoStringsProperty {
    pub first: String,
    pub second: Option<String>,
}

// `read_write_struct` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteStructProperty {
    pub value: AllTypes,
}

// `read_write_optional_struct` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteOptionalStructProperty {
    pub value: AllTypes,
}

// `read_write_two_structs` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoStructsProperty {
    pub first: AllTypes,
    pub second: AllTypes,
}

// `read_only_enum` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadOnlyEnumProperty {
    pub value: Numbers,
}

// `read_write_enum` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteEnumProperty {
    pub value: Numbers,
}

// `read_write_optional_enum` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteOptionalEnumProperty {
    pub value: Option<Numbers>,
}

// `read_write_two_enums` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoEnumsProperty {
    pub first: Numbers,
    pub second: Option<Numbers>,
}

// `read_write_datetime` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteDatetimeProperty {
    #[serde(with = "datetime_iso_format")]
    pub value: chrono::DateTime<chrono::Utc>,
}

// `read_write_optional_datetime` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteOptionalDatetimeProperty {
    #[serde(with = "datetime_iso_format")]
    pub value: chrono::DateTime<chrono::Utc>,
}

// `read_write_two_datetimes` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoDatetimesProperty {
    #[serde(with = "datetime_iso_format")]
    pub first: chrono::DateTime<chrono::Utc>,

    #[serde(with = "datetime_iso_format")]
    pub second: chrono::DateTime<chrono::Utc>,
}

// `read_write_duration` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteDurationProperty {
    #[serde(with = "duration_iso_format")]
    pub value: chrono::Duration,
}

// `read_write_optional_duration` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteOptionalDurationProperty {
    #[serde(with = "duration_iso_format")]
    pub value: chrono::Duration,
}

// `read_write_two_durations` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoDurationsProperty {
    #[serde(with = "duration_iso_format")]
    pub first: chrono::Duration,

    #[serde(with = "duration_iso_format")]
    pub second: chrono::Duration,
}

// `read_write_binary` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteBinaryProperty {
    #[serde(with = "base64_binary_format")]
    pub value: Vec<u8>,
}

// `read_write_optional_binary` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteOptionalBinaryProperty {
    #[serde(with = "base64_binary_format")]
    pub value: Vec<u8>,
}

// `read_write_two_binaries` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoBinariesProperty {
    #[serde(with = "base64_binary_format")]
    pub first: Vec<u8>,

    #[serde(with = "base64_binary_format")]
    pub second: Vec<u8>,
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::{DateTime, Utc};

    #[test]
    fn test_read_write_integer_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": 42 
        }"#;

        let parsed: ReadWriteIntegerProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_only_integer_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": 42 
        }"#;

        let parsed: ReadOnlyIntegerProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_optional_integer_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": 42 
        }"#;

        let parsed: ReadWriteOptionalIntegerProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_two_integers_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "first": 42 ,
        
            "second": 42 
        }"#;

        let parsed: ReadWriteTwoIntegersProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_only_string_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": "apples" 
        }"#;

        let parsed: ReadOnlyStringProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_string_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": "apples" 
        }"#;

        let parsed: ReadWriteStringProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_optional_string_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": "apples" 
        }"#;

        let parsed: ReadWriteOptionalStringProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_two_strings_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "first": "apples" ,
        
            "second": "apples" 
        }"#;

        let parsed: ReadWriteTwoStringsProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_struct_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": {"the_bool": true, "the_int": 42, "the_number": 3.14, "the_str": "apples", "the_enum": 1, "date_and_time": "1990-07-08T16:20:00Z", "time_duration": None, "data": None, "OptionalInteger": 42, "OptionalString": "apples", "OptionalEnum": 1, "OptionalDateTime": "1990-07-08T16:20:00Z", "OptionalDuration": None, "OptionalBinary": None} 
        }"#;

        let parsed: ReadWriteStructProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_optional_struct_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": {"the_bool": true, "the_int": 42, "the_number": 3.14, "the_str": "apples", "the_enum": 1, "date_and_time": "1990-07-08T16:20:00Z", "time_duration": None, "data": None, "OptionalInteger": 42, "OptionalString": "apples", "OptionalEnum": 1, "OptionalDateTime": "1990-07-08T16:20:00Z", "OptionalDuration": None, "OptionalBinary": None} 
        }"#;

        let parsed: ReadWriteOptionalStructProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_two_structs_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "first": {"the_bool": true, "the_int": 42, "the_number": 3.14, "the_str": "apples", "the_enum": 1, "date_and_time": "1990-07-08T16:20:00Z", "time_duration": None, "data": None, "OptionalInteger": 42, "OptionalString": "apples", "OptionalEnum": 1, "OptionalDateTime": "1990-07-08T16:20:00Z", "OptionalDuration": None, "OptionalBinary": None} ,
        
            "second": {"the_bool": true, "the_int": 42, "the_number": 3.14, "the_str": "apples", "the_enum": 1, "date_and_time": "1990-07-08T16:20:00Z", "time_duration": None, "data": None, "OptionalInteger": 42, "OptionalString": "apples", "OptionalEnum": 1, "OptionalDateTime": "1990-07-08T16:20:00Z", "OptionalDuration": None, "OptionalBinary": None} 
        }"#;

        let parsed: ReadWriteTwoStructsProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_only_enum_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": 1 
        }"#;

        let parsed: ReadOnlyEnumProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_enum_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": 1 
        }"#;

        let parsed: ReadWriteEnumProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_optional_enum_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": 1 
        }"#;

        let parsed: ReadWriteOptionalEnumProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_two_enums_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "first": 1 ,
        
            "second": 1 
        }"#;

        let parsed: ReadWriteTwoEnumsProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_datetime_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": "1990-07-08T16:20:00Z" 
        }"#;

        let parsed: ReadWriteDatetimeProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_optional_datetime_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": "1990-07-08T16:20:00Z" 
        }"#;

        let parsed: ReadWriteOptionalDatetimeProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_two_datetimes_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "first": "1990-07-08T16:20:00Z" ,
        
            "second": "1990-07-08T16:20:00Z" 
        }"#;

        let parsed: ReadWriteTwoDatetimesProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_duration_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": None 
        }"#;

        let parsed: ReadWriteDurationProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_optional_duration_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": None 
        }"#;

        let parsed: ReadWriteOptionalDurationProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_two_durations_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "first": None ,
        
            "second": None 
        }"#;

        let parsed: ReadWriteTwoDurationsProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_binary_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": None 
        }"#;

        let parsed: ReadWriteBinaryProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_optional_binary_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": None 
        }"#;

        let parsed: ReadWriteOptionalBinaryProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_two_binaries_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "first": None ,
        
            "second": None 
        }"#;

        let parsed: ReadWriteTwoBinariesProperty = serde_json::from_str(json_str).unwrap();
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
