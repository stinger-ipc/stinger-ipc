use std::any::Any;
use signal_only_server::SignalOnlyServer;

trait Initializable {

    fn initialize(&self, &server: SignalOnlyServer);

    fn as_any(&self) -> &dyn Any;
}