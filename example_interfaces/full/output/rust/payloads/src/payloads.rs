/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Full interface.
*/

use num_derive::{FromPrimitive, ToPrimitive};
use num_traits::FromPrimitive;
use std::fmt;

use serde::{Deserialize, Serialize};

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
