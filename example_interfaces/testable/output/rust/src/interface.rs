use serde::{Deserialize, Serialize};
use chrono::{Utc, SecondsFormat};
use builder_pattern::Builder;

/// Interface information structure similar to Python's InterfaceInfo BaseModel
#[derive(Debug, Clone, Serialize, Deserialize, Builder)]
pub struct InterfaceInfo {
    pub interface_name: String,
    pub title: String,
    pub version: String,
    pub instance: String,
    pub connection_topic: String,
    #[default_lazy(||Utc::now().to_rfc3339_opts(SecondsFormat::Secs, true))]
    pub timestamp: String,
}
