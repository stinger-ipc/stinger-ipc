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
use serde::{Deserialize, Serialize};
use std::fmt;

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

impl From<u32> for DayOfTheWeek {
    fn from(s: u32) -> DayOfTheWeek {
        DayOfTheWeek::from_u32(s).unwrap()
    }
}

impl fmt::Display for DayOfTheWeek {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct Lunch {
    pub drink: bool,
    pub sandwich: String,
    pub crackers: f32,
    pub day: DayOfTheWeek,

    pub order_number: Option<i32>,
}

// Structures for `addNumbers` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `addNumbers`
pub struct AddNumbersRequestObject {
    pub first: i32,
    pub second: i32,
    pub third: Option<i32>,
}

#[derive(Debug, Clone, Serialize)]
pub struct AddNumbersReturnValue {
    pub sum: i32,
}

// Structures for `doSomething` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `doSomething`
pub struct DoSomethingRequestObject {
    pub aString: String,
}

#[allow(dead_code)]
#[derive(Debug, Clone, Serialize, Deserialize)]
/// Return Object for `doSomething`
pub struct DoSomethingReturnValue {
    pub label: String,
    pub identifier: i32,
    pub day: DayOfTheWeek,
}

// Structures for `echo` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `echo`
pub struct EchoRequestObject {
    pub message: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct EchoReturnValue {
    pub message: String,
}

// Structures for `todayIs` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct TodayIsSignalPayload {
    pub dayOfMonth: i32,
    pub dayOfWeek: Option<DayOfTheWeek>,
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
    pub tuesday: Lunch,
}

// `family_name` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct FamilyNameProperty {
    pub family_name: String,
}
