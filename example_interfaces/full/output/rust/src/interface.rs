use serde::{Deserialize, Serialize};

/// Interface information structure similar to Python's InterfaceInfo BaseModel
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InterfaceInfo {
    #[serde(default = "default_interface_name")]
    pub interface_name: String,

    #[serde(default = "default_title")]
    pub title: String,

    #[serde(default = "default_version")]
    pub version: String,

    pub instance: String,
    pub connection_topic: String,
    pub timestamp: String,
}

fn default_interface_name() -> String {
    "Full".to_string()
}

fn default_title() -> String {
    "Fully Featured Example Interface".to_string()
}

fn default_version() -> String {
    "0.0.1".to_string()
}

impl InterfaceInfo {
    /// Create a new InterfaceInfo with default values for interface_name, title, and version
    pub fn new(instance: String, connection_topic: String, timestamp: String) -> Self {
        Self {
            interface_name: default_interface_name(),
            title: default_title(),
            version: default_version(),
            instance,
            connection_topic,
            timestamp,
        }
    }

    /// Create a new InterfaceInfo with all fields specified
    pub fn with_all_fields(
        interface_name: String,
        title: String,
        version: String,
        instance: String,
        connection_topic: String,
        timestamp: String,
    ) -> Self {
        Self {
            interface_name,
            title,
            version,
            instance,
            connection_topic,
            timestamp,
        }
    }
}

impl Default for InterfaceInfo {
    fn default() -> Self {
        Self {
            interface_name: default_interface_name(),
            title: default_title(),
            version: default_version(),
            instance: String::new(),
            connection_topic: String::new(),
            timestamp: String::new(),
        }
    }
}
