

use payloads.DoSomethingReturnValue;



/// Method handlers for the FullServer server.
/// This trait must be implemented by the user of the server to handle incoming method requests.
pub trait FullServerMethodHandler: Send + Sync {
    /// Pointer to a function to handle the addNumbers method request.
    handle_add_numbers(&self, first: i32, second: i32, third: Option<i32>) -> Result<i32, MethodResultCode>;
    
    /// Pointer to a function to handle the doSomething method request.
    handle_do_something(&self, a_string: String) -> Result<DoSomethingReturnValue, MethodResultCode>;
    
    
}