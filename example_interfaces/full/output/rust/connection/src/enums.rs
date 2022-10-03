/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Example interface.
*/

use std::fmt;
use num_derive::FromPrimitive;
use num_traits::FromPrimitive;



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

impl DayOfTheWeek {
    pub fn from_u32(value: u32) -> DayOfTheWeek {
        FromPrimitive::from_u32(value).unwrap()
    }
}

impl fmt::Display for DayOfTheWeek {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
       write!(f, "{:?}", self)
    }
}
