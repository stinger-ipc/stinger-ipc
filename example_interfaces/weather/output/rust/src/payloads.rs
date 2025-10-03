//! Payloads module for weather IPC
//! 
//! Contains all the data structures, enums, and return codes used by the weather IPC system.

/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/

use num_derive::{FromPrimitive, ToPrimitive};
use num_traits::FromPrimitive;

use std::fmt;

use serde::{Deserialize, Serialize};

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
pub enum WeatherCondition {
    Rainy = 1,
    Sunny = 2,
    PartlyCloudy = 3,
    MostlyCloudy = 4,
    Overcast = 5,
    Windy = 6,
    Snowy = 7
}

#[allow(dead_code)]
impl WeatherCondition {
    pub fn from_u32(value: u32) -> Option<Self> {
        FromPrimitive::from_u32(value)
    }
}

impl From<WeatherCondition> for u32 {
    fn from(s: WeatherCondition) -> u32 {
        s as u32
    }
}

impl From<u32> for WeatherCondition {
    fn from(s: u32) -> WeatherCondition {
        WeatherCondition::from_u32(s).unwrap()
    }
}

impl fmt::Display for WeatherCondition {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
       write!(f, "{:?}", self)
    }
}



#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ForecastForHour {
    pub temperature: f32,
    pub starttime: String,
    pub condition: WeatherCondition,
    
}
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct ForecastForDay {
    pub high_temperature: f32,
    pub low_temperature: f32,
    pub condition: WeatherCondition,
    
    pub start_time: String,
    pub end_time: String,
}


// Structures for `refresh_daily_forecast` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `refresh_daily_forecast`
pub struct RefreshDailyForecastRequestObject {
}


#[derive(Debug, Clone, Serialize)]
/// Empty (no parameters) return structure for the `refresh_daily_forecast` method.
pub struct RefreshDailyForecastReturnValue {
}

// Structures for `refresh_hourly_forecast` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `refresh_hourly_forecast`
pub struct RefreshHourlyForecastRequestObject {
}


#[derive(Debug, Clone, Serialize)]
/// Empty (no parameters) return structure for the `refresh_hourly_forecast` method.
pub struct RefreshHourlyForecastReturnValue {
}

// Structures for `refresh_current_conditions` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
/// Request Object for `refresh_current_conditions`
pub struct RefreshCurrentConditionsRequestObject {
}


#[derive(Debug, Clone, Serialize)]
/// Empty (no parameters) return structure for the `refresh_current_conditions` method.
pub struct RefreshCurrentConditionsReturnValue {
}


// Structures for `current_time` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CurrentTimeSignalPayload {
    pub current_time: String,
    
}



// `location` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct LocationProperty {
    pub latitude: f32,
    pub longitude: f32,
    
}

// `current_temperature` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct CurrentTemperatureProperty {
    pub temperature_f: f32,
    
}

// `current_condition` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct CurrentConditionProperty {
    pub condition: WeatherCondition,
    pub description: String,
    
}

// `daily_forecast` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct DailyForecastProperty {
    pub monday: ForecastForDay,
    pub tuesday: ForecastForDay,
    pub wednesday: ForecastForDay,
    
}

// `hourly_forecast` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct HourlyForecastProperty {
    pub hour_0: ForecastForHour,
    pub hour_1: ForecastForHour,
    pub hour_2: ForecastForHour,
    pub hour_3: ForecastForHour,
    
}

// `current_condition_refresh_interval` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct CurrentConditionRefreshIntervalProperty {
    pub seconds: i32,
    
}

// `hourly_forecast_refresh_interval` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct HourlyForecastRefreshIntervalProperty {
    pub seconds: i32,
    
}

// `daily_forecast_refresh_interval` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct DailyForecastRefreshIntervalProperty {
    pub seconds: i32,
    
}
