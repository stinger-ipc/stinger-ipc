/*
DO NOT MODIFY THIS FILE .  It is automatically generated and changes will be over-written
on the next generation.

It contains enumerations used by the SignalOnly interface.
*/

use serde::{Deserialize, Serialize};

// Structures for `anotherSignal` signal
#[allow(dead_code, non_snake_case)]
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct AnotherSignalSignalPayload {
    pub one: f32,

    pub two: bool,

    pub three: String,
}
