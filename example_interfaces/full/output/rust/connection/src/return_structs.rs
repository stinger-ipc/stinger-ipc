/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the Example interface.
*/


use crate::enums::{ DayOfTheWeek };


pub enum MethodResultCode {
    Success = 0,
    ClientError = 1,
    ServerError = 2,
    TransportError = 3,
    PayloadError = 4,
}


#[allow(dead_code)]
pub struct DoSomethingReturnValue {

    pub label: String,

    pub identifier: i32,

    pub day: DayOfTheWeek,

}
