/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/


use serde::{Serialize, Deserialize};





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



// Structures for `anotherSignal` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct AnotherSignalSignalPayload {
    pub one: f32,
    
    pub two: bool,
    
    pub three: String,
    
}


