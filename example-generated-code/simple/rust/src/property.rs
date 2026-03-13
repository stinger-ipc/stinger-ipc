#[allow(unused_imports)]
use crate::payloads::*;
use derive_builder::Builder;

#[derive(Clone, Builder, Debug)]
pub struct SimpleInitialPropertyValues {
    pub school: String,
    pub school_version: u32,
}
