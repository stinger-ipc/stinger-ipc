use full_types::MethodReturnCode;

fn main() {
    println!("=== MethodReturnCode Conversion Examples ===\n");

    // Example 1: Create from numeric codes
    println!("1. Creating from numeric codes:");
    let success = MethodReturnCode::from_code(0, None);
    let client_error = MethodReturnCode::from_code(1, Some("Invalid parameter".to_string()));
    let server_error =
        MethodReturnCode::from_code(2, Some("Database connection failed".to_string()));
    let unknown_code = MethodReturnCode::from_code(999, Some("Unknown error code".to_string()));

    println!("  Code 0: {:?}", success);
    println!("  Code 1: {:?}", client_error);
    println!("  Code 2: {:?}", server_error);
    println!("  Code 999: {:?}", unknown_code);

    // Example 2: Create from string names
    println!("\n2. Creating from string names:");
    let success_str = MethodReturnCode::from_string("success", None);
    let client_str = MethodReturnCode::from_string("ClientError", Some("Bad input".to_string()));
    let server_str =
        MethodReturnCode::from_string("server_error", Some("Internal error".to_string()));
    let timeout_str =
        MethodReturnCode::from_string("timeout", Some("Operation timed out".to_string()));

    println!("  'success': {:?}", success_str);
    println!("  'ClientError': {:?}", client_str);
    println!("  'server_error': {:?}", server_str);
    println!("  'timeout': {:?}", timeout_str);

    // Example 3: Convert back to codes and names
    println!("\n3. Converting back to codes and names:");
    let examples = vec![
        MethodReturnCode::Success,
        MethodReturnCode::ClientError("Test error".to_string()),
        MethodReturnCode::ServerError("Server down".to_string()),
        MethodReturnCode::NotImplemented("Feature not ready".to_string()),
    ];

    for result in examples {
        println!("  {:?}", result);
        println!("    -> Code: {}", result.to_code());
        println!("    -> Name: {}", result.to_string_name());
        println!("    -> Message: '{}'", result.message());
        println!();
    }

    // Example 4: Practical usage in a function
    println!("4. Practical usage example:");
    let user_input_code = 2;
    let user_input_message = "Connection timeout";

    let result = create_result_from_user_input(user_input_code, user_input_message);
    println!(
        "  User provided code {} with message '{}': {:?}",
        user_input_code, user_input_message, result
    );
}

/// Example function showing how you might use this in practice
fn create_result_from_user_input(code: u32, message: &str) -> MethodReturnCode {
    let msg = if message.is_empty() {
        None
    } else {
        Some(message.to_string())
    };

    MethodReturnCode::from_code(code, msg)
}
