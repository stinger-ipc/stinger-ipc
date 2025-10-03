//! Full IPC Library
//!
//! This library provides client, server, and payload functionality for the Full IPC system.
//! Use features to control which modules are included:
//!
//! - `client`: Includes client and payloads modules
//! - `server`: Includes server and payloads modules  
//! - `payloads`: Includes only payloads module

pub mod interface;

#[cfg(feature = "payloads")]
pub mod payloads;

#[cfg(feature = "client")]
pub mod client;

#[cfg(feature = "server")]
pub mod server;

// Re-export commonly used types from payloads when available
#[cfg(feature = "payloads")]
pub use payloads::*;
