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
pub struct Entry {
    /// An identifier.
    pub key: i32,
    /// A name.
    pub value: String,
}

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

    /// A struct type.
    pub an_entry_object: Entry,

    /// A date and time type.
    #[serde(with = "datetime_iso_format")]
    pub date_and_time: chrono::DateTime<chrono::Utc>,
    /// A duration type.
    #[serde(with = "duration_iso_format")]
    pub time_duration: chrono::Duration,
    /// A binary type.
    #[serde(with = "base64_binary_format")]
    pub data: Vec<u8>,
    /// An optional integer type.
    #[serde(rename = "OptionalInteger")]
    pub optional_integer: Option<i32>,
    /// An optional string type.
    #[serde(rename = "OptionalString")]
    pub optional_string: Option<String>,
    /// An optional enum type, one of the numbers.
    #[serde(rename = "OptionalEnum")]
    pub optional_enum: Option<Numbers>,

    /// An optional struct type.
    #[serde(rename = "optionalEntryObject")]
    pub optional_entry_object: Option<Entry>,

    /// An optional date and time type.
    #[serde(rename = "OptionalDateTime")]
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub optional_date_time: Option<chrono::DateTime<chrono::Utc>>,

    /// An optional duration type.
    #[serde(rename = "OptionalDuration")]
    #[serde(
        serialize_with = "duration_iso_format::serialize_option",
        deserialize_with = "duration_iso_format::deserialize_option"
    )]
    pub optional_duration: Option<chrono::Duration>,

    /// An optional binary type.
    #[serde(rename = "OptionalBinary")]
    #[serde(
        serialize_with = "base64_binary_format::serialize_option",
        deserialize_with = "base64_binary_format::deserialize_option"
    )]
    pub optional_binary: Option<Vec<u8>>,

    /// An array of integers.
    pub array_of_integers: Vec<i32>,

    /// An optional array of integers.
    pub optional_array_of_integers: Option<Vec<i32>>,

    /// An array of strings.
    pub array_of_strings: Vec<String>,

    /// An optional array of strings.
    pub optional_array_of_strings: Option<Vec<String>>,

    /// An array of enums.
    pub array_of_enums: Vec<Numbers>,

    /// An optional array of enums.
    pub optional_array_of_enums: Option<Vec<Numbers>>,

    /// An array of date and time values.
    #[serde(
        serialize_with = "datetime_iso_format::serialize_vec",
        deserialize_with = "datetime_iso_format::deserialize_vec"
    )]
    pub array_of_datetimes: Vec<chrono::DateTime<chrono::Utc>>,

    /// An optional array of date and time values.
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option_vec",
        deserialize_with = "datetime_iso_format::deserialize_option_vec"
    )]
    pub optional_array_of_datetimes: Option<Vec<chrono::DateTime<chrono::Utc>>>,

    /// An array of duration values.
    #[serde(
        serialize_with = "duration_iso_format::serialize_vec",
        deserialize_with = "duration_iso_format::deserialize_vec"
    )]
    pub array_of_durations: Vec<chrono::Duration>,

    /// An optional array of duration values.
    #[serde(
        serialize_with = "duration_iso_format::serialize_option_vec",
        deserialize_with = "duration_iso_format::deserialize_option_vec"
    )]
    pub optional_array_of_durations: Option<Vec<chrono::Duration>>,

    /// An array of binary values.
    #[serde(
        serialize_with = "base64_binary_format::serialize_vec",
        deserialize_with = "base64_binary_format::deserialize_vec"
    )]
    pub array_of_binaries: Vec<Vec<u8>>,

    /// An optional array of binary values.
    #[serde(
        serialize_with = "base64_binary_format::serialize_option_vec",
        deserialize_with = "base64_binary_format::deserialize_option_vec"
    )]
    pub optional_array_of_binaries: Option<Vec<Vec<u8>>>,

    /// An array of struct values.
    pub array_of_entry_objects: Vec<Entry>,

    /// An optional array of struct values.
    pub optional_array_of_entry_objects: Option<Vec<Entry>>,
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
    pub input1: Option<AllTypes>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalStruct` method.
pub struct CallOptionalStructReturnValues {
    pub output1: Option<AllTypes>,
}

// Structures for `callThreeStructs` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callThreeStructs` method.
pub struct CallThreeStructsRequestObject {
    /// The first struct input.  The other two don't have descriptions.
    pub input1: Option<AllTypes>,

    pub input2: AllTypes,

    pub input3: AllTypes,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeStructs` method.
pub struct CallThreeStructsReturnValues {
    /// The first struct output.  The other two don't have descriptions.
    pub output1: Option<AllTypes>,

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
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub input1: Option<chrono::DateTime<chrono::Utc>>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalDateTime` method.
pub struct CallOptionalDateTimeReturnValues {
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub output1: Option<chrono::DateTime<chrono::Utc>>,
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
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub input3: Option<chrono::DateTime<chrono::Utc>>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeDateTimes` method.
pub struct CallThreeDateTimesReturnValues {
    /// The first date and time output.  The other two don't have descriptions.
    #[serde(with = "datetime_iso_format")]
    pub output1: chrono::DateTime<chrono::Utc>,
    #[serde(with = "datetime_iso_format")]
    pub output2: chrono::DateTime<chrono::Utc>,
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub output3: Option<chrono::DateTime<chrono::Utc>>,
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
    #[serde(
        serialize_with = "duration_iso_format::serialize_option",
        deserialize_with = "duration_iso_format::deserialize_option"
    )]
    pub input1: Option<chrono::Duration>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalDuration` method.
pub struct CallOptionalDurationReturnValues {
    #[serde(
        serialize_with = "duration_iso_format::serialize_option",
        deserialize_with = "duration_iso_format::deserialize_option"
    )]
    pub output1: Option<chrono::Duration>,
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
    #[serde(
        serialize_with = "duration_iso_format::serialize_option",
        deserialize_with = "duration_iso_format::deserialize_option"
    )]
    pub input3: Option<chrono::Duration>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeDurations` method.
pub struct CallThreeDurationsReturnValues {
    /// The first duration output.  The other two don't have descriptions.
    #[serde(with = "duration_iso_format")]
    pub output1: chrono::Duration,
    #[serde(with = "duration_iso_format")]
    pub output2: chrono::Duration,
    #[serde(
        serialize_with = "duration_iso_format::serialize_option",
        deserialize_with = "duration_iso_format::deserialize_option"
    )]
    pub output3: Option<chrono::Duration>,
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
    #[serde(
        serialize_with = "base64_binary_format::serialize_option",
        deserialize_with = "base64_binary_format::deserialize_option"
    )]
    pub input1: Option<Vec<u8>>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalBinary` method.
pub struct CallOptionalBinaryReturnValues {
    #[serde(
        serialize_with = "base64_binary_format::serialize_option",
        deserialize_with = "base64_binary_format::deserialize_option"
    )]
    pub output1: Option<Vec<u8>>,
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
    #[serde(
        serialize_with = "base64_binary_format::serialize_option",
        deserialize_with = "base64_binary_format::deserialize_option"
    )]
    pub input3: Option<Vec<u8>>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callThreeBinaries` method.
pub struct CallThreeBinariesReturnValues {
    /// The first binary output.  The other two don't have descriptions.
    #[serde(with = "base64_binary_format")]
    pub output1: Vec<u8>,
    #[serde(with = "base64_binary_format")]
    pub output2: Vec<u8>,
    #[serde(
        serialize_with = "base64_binary_format::serialize_option",
        deserialize_with = "base64_binary_format::deserialize_option"
    )]
    pub output3: Option<Vec<u8>>,
}

// Structures for `callOneListOfIntegers` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOneListOfIntegers` method.
pub struct CallOneListOfIntegersRequestObject {
    pub input1: Vec<i32>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOneListOfIntegers` method.
pub struct CallOneListOfIntegersReturnValues {
    pub output1: Vec<i32>,
}

// Structures for `callOptionalListOfFloats` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callOptionalListOfFloats` method.
pub struct CallOptionalListOfFloatsRequestObject {
    pub input1: Option<Vec<f32>>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callOptionalListOfFloats` method.
pub struct CallOptionalListOfFloatsReturnValues {
    pub output1: Option<Vec<f32>>,
}

// Structures for `callTwoLists` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `callTwoLists` method.
pub struct CallTwoListsRequestObject {
    /// The first list of enums.
    pub input1: Vec<Numbers>,

    pub input2: Option<Vec<String>>,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `callTwoLists` method.
pub struct CallTwoListsReturnValues {
    /// The first list of enums.
    pub output1: Vec<Numbers>,

    pub output2: Option<Vec<String>>,
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
    pub value: Option<AllTypes>,
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
    pub third: Option<AllTypes>,
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
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub value: Option<chrono::DateTime<chrono::Utc>>,
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
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub third: Option<chrono::DateTime<chrono::Utc>>,
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
    #[serde(
        serialize_with = "duration_iso_format::serialize_option",
        deserialize_with = "duration_iso_format::deserialize_option"
    )]
    pub value: Option<chrono::Duration>,
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
    #[serde(
        serialize_with = "duration_iso_format::serialize_option",
        deserialize_with = "duration_iso_format::deserialize_option"
    )]
    pub third: Option<chrono::Duration>,
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
    #[serde(
        serialize_with = "base64_binary_format::serialize_option",
        deserialize_with = "base64_binary_format::deserialize_option"
    )]
    pub value: Option<Vec<u8>>,
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
    #[serde(
        serialize_with = "base64_binary_format::serialize_option",
        deserialize_with = "base64_binary_format::deserialize_option"
    )]
    pub third: Option<Vec<u8>>,
}

// Structures for `singleArrayOfIntegers` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleArrayOfIntegersSignalPayload {
    /// The array of integers.
    pub values: Vec<i32>,
}

// Structures for `singleOptionalArrayOfStrings` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct SingleOptionalArrayOfStringsSignalPayload {
    /// The array of strings.
    pub values: Option<Vec<String>>,
}

// Structures for `arrayOfEveryType` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ArrayOfEveryTypeSignalPayload {
    /// The first array of integers.
    pub first_of_integers: Vec<i32>,

    /// The second array of floats.
    pub second_of_floats: Vec<f32>,

    /// The third array of strings.
    pub third_of_strings: Vec<String>,

    /// The fourth array of enums.
    pub fourth_of_enums: Vec<Numbers>,

    /// The fifth array of structs.
    pub fifth_of_structs: Vec<Entry>,

    /// The sixth array of date and time values.
    #[serde(
        serialize_with = "datetime_iso_format::serialize_vec",
        deserialize_with = "datetime_iso_format::deserialize_vec"
    )]
    pub sixth_of_datetimes: Vec<chrono::DateTime<chrono::Utc>>,

    /// The seventh array of duration values.
    #[serde(
        serialize_with = "duration_iso_format::serialize_vec",
        deserialize_with = "duration_iso_format::deserialize_vec"
    )]
    pub seventh_of_durations: Vec<chrono::Duration>,

    /// The eighth array of binary values.
    #[serde(
        serialize_with = "base64_binary_format::serialize_vec",
        deserialize_with = "base64_binary_format::deserialize_vec"
    )]
    pub eighth_of_binaries: Vec<Vec<u8>>,
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
    /// An integer value.
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
    /// A string value.
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
    pub value: Option<AllTypes>,
}

// `read_write_two_structs` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoStructsProperty {
    /// A struct value.
    pub first: AllTypes,

    pub second: Option<AllTypes>,
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
    /// An enum value.
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
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub value: Option<chrono::DateTime<chrono::Utc>>,
}

// `read_write_two_datetimes` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoDatetimesProperty {
    /// A date and time value.
    #[serde(with = "datetime_iso_format")]
    pub first: chrono::DateTime<chrono::Utc>,
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option",
        deserialize_with = "datetime_iso_format::deserialize_option"
    )]
    pub second: Option<chrono::DateTime<chrono::Utc>>,
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
    #[serde(
        serialize_with = "duration_iso_format::serialize_option",
        deserialize_with = "duration_iso_format::deserialize_option"
    )]
    pub value: Option<chrono::Duration>,
}

// `read_write_two_durations` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoDurationsProperty {
    /// A duration of time.
    #[serde(with = "duration_iso_format")]
    pub first: chrono::Duration,
    #[serde(
        serialize_with = "duration_iso_format::serialize_option",
        deserialize_with = "duration_iso_format::deserialize_option"
    )]
    pub second: Option<chrono::Duration>,
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
    #[serde(
        serialize_with = "base64_binary_format::serialize_option",
        deserialize_with = "base64_binary_format::deserialize_option"
    )]
    pub value: Option<Vec<u8>>,
}

// `read_write_two_binaries` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteTwoBinariesProperty {
    /// A binary blob of data.
    #[serde(with = "base64_binary_format")]
    pub first: Vec<u8>,
    #[serde(
        serialize_with = "base64_binary_format::serialize_option",
        deserialize_with = "base64_binary_format::deserialize_option"
    )]
    pub second: Option<Vec<u8>>,
}

// `read_write_list_of_strings` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteListOfStringsProperty {
    pub value: Vec<String>,
}

// `read_write_lists` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ReadWriteListsProperty {
    pub the_list: Vec<Numbers>,

    #[serde(rename = "optionalList")]
    #[serde(
        serialize_with = "datetime_iso_format::serialize_option_vec",
        deserialize_with = "datetime_iso_format::deserialize_option_vec"
    )]
    pub optional_list: Option<Vec<chrono::DateTime<chrono::Utc>>>,
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
            "value": {"the_bool": true, "the_int": 42, "the_number": 3.14, "the_str": "apples", "the_enum": 1, "an_entry_object": {"key": 42, "value": "apples"}, "date_and_time": "1990-07-08T16:20:00Z", "time_duration": None, "data": None, "OptionalInteger": 42, "OptionalString": "apples", "OptionalEnum": 1, "optionalEntryObject": {"key": 42, "value": "apples"}, "OptionalDateTime": "1990-07-08T16:20:00Z", "OptionalDuration": None, "OptionalBinary": None, "array_of_integers": None, "optional_array_of_integers": None, "array_of_strings": None, "optional_array_of_strings": None, "array_of_enums": None, "optional_array_of_enums": None, "array_of_datetimes": None, "optional_array_of_datetimes": None, "array_of_durations": None, "optional_array_of_durations": None, "array_of_binaries": None, "optional_array_of_binaries": None, "array_of_entry_objects": None, "optional_array_of_entry_objects": None} 
        }"#;

        let parsed: ReadWriteStructProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_optional_struct_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": {"the_bool": true, "the_int": 42, "the_number": 3.14, "the_str": "apples", "the_enum": 1, "an_entry_object": {"key": 42, "value": "apples"}, "date_and_time": "1990-07-08T16:20:00Z", "time_duration": None, "data": None, "OptionalInteger": 42, "OptionalString": "apples", "OptionalEnum": 1, "optionalEntryObject": {"key": 42, "value": "apples"}, "OptionalDateTime": "1990-07-08T16:20:00Z", "OptionalDuration": None, "OptionalBinary": None, "array_of_integers": None, "optional_array_of_integers": None, "array_of_strings": None, "optional_array_of_strings": None, "array_of_enums": None, "optional_array_of_enums": None, "array_of_datetimes": None, "optional_array_of_datetimes": None, "array_of_durations": None, "optional_array_of_durations": None, "array_of_binaries": None, "optional_array_of_binaries": None, "array_of_entry_objects": None, "optional_array_of_entry_objects": None} 
        }"#;

        let parsed: ReadWriteOptionalStructProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_two_structs_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "first": {"the_bool": true, "the_int": 42, "the_number": 3.14, "the_str": "apples", "the_enum": 1, "an_entry_object": {"key": 42, "value": "apples"}, "date_and_time": "1990-07-08T16:20:00Z", "time_duration": None, "data": None, "OptionalInteger": 42, "OptionalString": "apples", "OptionalEnum": 1, "optionalEntryObject": {"key": 42, "value": "apples"}, "OptionalDateTime": "1990-07-08T16:20:00Z", "OptionalDuration": None, "OptionalBinary": None, "array_of_integers": None, "optional_array_of_integers": None, "array_of_strings": None, "optional_array_of_strings": None, "array_of_enums": None, "optional_array_of_enums": None, "array_of_datetimes": None, "optional_array_of_datetimes": None, "array_of_durations": None, "optional_array_of_durations": None, "array_of_binaries": None, "optional_array_of_binaries": None, "array_of_entry_objects": None, "optional_array_of_entry_objects": None} ,
        
            "second": {"the_bool": true, "the_int": 42, "the_number": 3.14, "the_str": "apples", "the_enum": 1, "an_entry_object": {"key": 42, "value": "apples"}, "date_and_time": "1990-07-08T16:20:00Z", "time_duration": None, "data": None, "OptionalInteger": 42, "OptionalString": "apples", "OptionalEnum": 1, "optionalEntryObject": {"key": 42, "value": "apples"}, "OptionalDateTime": "1990-07-08T16:20:00Z", "OptionalDuration": None, "OptionalBinary": None, "array_of_integers": None, "optional_array_of_integers": None, "array_of_strings": None, "optional_array_of_strings": None, "array_of_enums": None, "optional_array_of_enums": None, "array_of_datetimes": None, "optional_array_of_datetimes": None, "array_of_durations": None, "optional_array_of_durations": None, "array_of_binaries": None, "optional_array_of_binaries": None, "array_of_entry_objects": None, "optional_array_of_entry_objects": None} 
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
    fn test_read_write_list_of_strings_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "value": None 
        }"#;

        let parsed: ReadWriteListOfStringsProperty = serde_json::from_str(json_str).unwrap();
    }

    #[test]
    fn test_read_write_lists_property_json_format() {
        // Test deserializing from a known JSON string
        let json_str = r#"{
            "the_list": None ,
        
            "optionalList": None 
        }"#;

        let parsed: ReadWriteListsProperty = serde_json::from_str(json_str).unwrap();
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
