# Test Able IPC Library

A Rust library providing client, server, and payload functionality for the Test Able IPC system: This tries to capture most variants of features.

## Features

This library uses feature flags to control which modules are included in your build:

### Available Features

- **`payloads`**: Includes only the payload types, enums, and structures.
- **`client`**: Includes client functionality and payloads.
- **`server`**: Includes server functionality and payloads.

## Usage

Add this to your `Cargo.toml`:

```toml
[dependencies]
full_ipc = { path = ".", features = ["client"] }  # For client functionality
# OR
full_ipc = { path = ".", features = ["server"] }  # For server functionality
# OR  
full_ipc = { path = ".", features = ["payloads"] } # For just payload types
```

## Examples

### Running Examples

Each example requires the corresponding feature to be enabled:

```bash
# Client example
cargo run --example test__able_client_demo --features client

# Server example
cargo run --example test__able_server_demo --features server

# Payloads example
cargo run --example test__able_connection_demo --features payloads
```

### Building with Specific Features

```bash
# Build with client feature
cargo build --features client

# Build with server feature
cargo build --features server

# Build with just payloads
cargo build --features payloads

```

## Library Structure

```
src/
├── lib.rs          # Main library file with feature gates
├── client.rs       # Client module (enabled with 'client' feature)
├── server.rs       # Server module (enabled with 'server' feature)  
└── payloads.rs     # Payload types and structures

examples/
├── client.rs       # Client usage example
├── server.rs       # Server usage example
└── pub_and_recv.rs # Payloads usage example
```

## Generated Code

**⚠️ Important:** The source files in this library are automatically generated. Do not modify them directly as changes will be overwritten on the next generation.

## Dependencies

The library automatically includes the necessary dependencies based on the features you enable:

- **Core dependencies** (always included): futures, mqttier, serde, serde_json, tokio, num-derive, num-traits, uuid
- **Client dependencies** (with `client` feature): paho-mqtt, json, log, env_logger  
- **Server dependencies** (with `server` feature): async-trait, tracing, env_logger

This modular approach allows you to include only the functionality you need, reducing compile times and binary size.