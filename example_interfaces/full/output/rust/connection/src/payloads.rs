/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Example interface.
*/


use std::fmt;
use num_derive::FromPrimitive;
use num_traits::FromPrimitive;

use serde::{Serialize, Deserialize};


#[derive(Debug, FromPrimitive)]
pub enum DayOfTheWeek {
    Sunday = 1,
    Monday = 2,
    Tuesday = 3,
    Wednesday = 4,
    Thursday = 5,
    Friday = 6,
    Saturday = 7
}

#[allow(dead_code)]
impl DayOfTheWeek {
    pub fn from_u32(value: u32) -> Option<Self> {
        FromPrimitive::from_u32(value)
    }
}

impl fmt::Display for DayOfTheWeek {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
       write!(f, "{:?}", self)
    }
}


#[allow(dead_code)]
#[derive(Debug)]
pub enum MethodResultCode {
    Success = 0,
    ClientError = 1,
    ServerError = 2,
    TransportError = 3,
    PayloadError = 4,
}


#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize)]
pub struct AddNumbersRequestObject {
    pub first: i32,
    pub second: i32,
}

#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize)]
pub struct DoSomethingRequestObject {
    pub aString: String,
}

#[allow(dead_code)]
pub struct DoSomethingReturnValue {
    pub label: String,
    pub identifier: i32,
    pub day: DayOfTheWeek,
}


#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct TodayIsSignalPayload {
    pub dayOfMonth: i32,
    pub dayOfWeek: u32,
    
}
