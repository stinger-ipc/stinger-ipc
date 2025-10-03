use chrono::{DateTime, Utc};
use signal_only_ipc::NowSignalPayload;

fn main() {
    // Create a payload with current timestamp
    let now = Utc::now();
    let payload = NowSignalPayload { timestamp: now };

    // Serialize to JSON
    let json = serde_json::to_string_pretty(&payload).expect("Failed to serialize");
    println!("Serialized NowSignalPayload:");
    println!("{}", json);

    // Deserialize back
    let deserialized: NowSignalPayload =
        serde_json::from_str(&json).expect("Failed to deserialize");

    println!("\nDeserialized timestamp: {}", deserialized.timestamp);
    println!("Original timestamp: {}", now);
    println!("Timestamps match: {}", deserialized.timestamp == now);

    // Show manual serialization with custom timestamp
    let custom_time = DateTime::parse_from_rfc3339("2023-12-25T12:30:45.123456789Z")
        .unwrap()
        .with_timezone(&Utc);

    let custom_payload = NowSignalPayload {
        timestamp: custom_time,
    };
    let custom_json = serde_json::to_string_pretty(&custom_payload).expect("Failed to serialize");

    println!("\nCustom timestamp payload:");
    println!("{}", custom_json);
}
