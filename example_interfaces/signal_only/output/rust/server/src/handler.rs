use std::any::Any;
use signal_only_types::payloads::MethodReturnCode;


/// Method handlers for the SignalOnlyServer server.
/// This trait must be implemented by the user of the server to handle incoming method requests.
pub trait SignalOnlyMethodHandlers: Send + Sync {

    

    fn as_any(&self) -> &dyn Any;
}