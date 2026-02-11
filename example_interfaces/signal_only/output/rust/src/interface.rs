use chrono::{SecondsFormat, Utc};
use derive_builder::Builder;
use serde::{Deserialize, Serialize};

/// Interface information structure similar to Python's InterfaceInfo BaseModel
#[derive(Debug, Clone, Serialize, Deserialize, Builder)]
pub struct InterfaceInfo {
    pub interface_name: String,
    pub title: String,
    pub version: String,
    pub instance: String,
    pub connection_topic: String,
    #[builder(default = "Utc::now().to_rfc3339_opts(SecondsFormat::Secs, true)")]
    pub timestamp: String,
    pub prefix: String,
}
