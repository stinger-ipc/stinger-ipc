/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the weather interface.
*/


use std::fmt;
use num_derive::{FromPrimitive, ToPrimitive};
use num_traits::{FromPrimitive, ToPrimitive};

use serde::{Serialize, Deserialize};


#[repr(u32)]
#[derive(Debug, FromPrimitive, ToPrimitive, Clone, Serialize, Deserialize)]
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
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ForecastForHour {
    pub temperature: f32,
    pub starttime: String,
    pub condition: WeatherCondition,
    
}
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct ForecastForDay {
    pub high_temperature: f32,
    pub low_temperature: f32,
    pub condition: WeatherCondition,
    
    pub start_time: String,
    pub end_time: String,
}

#[allow(dead_code)]
#[derive(Debug)]
pub enum MethodResultCode {
    Success = 0,
    ClientError = 1,
    ServerError = 2,
    TransportError = 3,
    PayloadError = 4,
    Timeout = 5,
    UnknownError = 6,
    NotImplemented = 7,
}


// Structures for `refresh_daily_forecast` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RefreshDailyForecastRequestObject {
}

// Structures for `refresh_hourly_forecast` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RefreshHourlyForecastRequestObject {
}

// Structures for `refresh_current_conditions` method

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RefreshCurrentConditionsRequestObject {
}


// Structures for `current_time` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CurrentTimeSignalPayload {
    pub current_time: String,
    
}



// `location` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct LocationProperty {
    pub latitude: f32,
    pub longitude: f32,
    
}

// `current_temperature` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CurrentTemperatureProperty {
    pub temperature_f: f32,
    
}

// `current_condition` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CurrentConditionProperty {
    pub condition: WeatherCondition,
    pub description: String,
    
}

// `daily_forecast` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct DailyForecastProperty {
    pub monday: ForecastForDay,
    pub tuesday: ForecastForDay,
    pub wednesday: ForecastForDay,
    
}

// `hourly_forecast` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct HourlyForecastProperty {
    pub hour_0: ForecastForHour,
    pub hour_1: ForecastForHour,
    pub hour_2: ForecastForHour,
    pub hour_3: ForecastForHour,
    
}

// `current_condition_refresh_interval` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct CurrentConditionRefreshIntervalProperty {
    pub seconds: i32,
    
}

// `hourly_forecast_refresh_interval` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct HourlyForecastRefreshIntervalProperty {
    pub seconds: i32,
    
}

// `daily_forecast_refresh_interval` property structure.
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct DailyForecastRefreshIntervalProperty {
    pub seconds: i32,
    
}
