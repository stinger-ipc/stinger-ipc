use derive_builder::Builder;

#[derive(Clone, Builder)]
pub struct SimpleInitialPropertyValues {
    pub school: String,
    pub school_version: u32,
}
