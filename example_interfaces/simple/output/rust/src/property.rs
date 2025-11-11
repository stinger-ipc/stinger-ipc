
use derive_builder::Builder;
#[allow(unused_imports)]
use crate::payloads::{*};

#[derive(Clone, Builder, Debug)]
pub struct SimpleInitialPropertyValues {
    
    pub school: String,
    pub school_version: u32,
    
}
