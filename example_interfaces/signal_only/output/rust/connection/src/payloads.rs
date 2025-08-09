/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/


use serde::Serialize;



#[allow(dead_code)]
pub enum MethodResultCode {
    Success = 0,
    ClientError = 1,
    ServerError = 2,
    TransportError = 3,
    PayloadError = 4,
}



#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize)]
pub struct AnotherSignalSignalPayload {
    pub one: f32,
    
    pub two: bool,
    
    pub three: String,
    
}
