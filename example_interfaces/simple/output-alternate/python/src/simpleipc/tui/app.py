"""Main TUI application for SimpleIPC."""

from typing import Optional
from textual.app import App # typing: ignore
from textual.screen import Screen # typing: ignore
from pyqttier.connection import Mqtt5Connection
from simpleipc.client import SimpleClient


class SimpleIPCApp(App):
    """A Textual app for SimpleIPC client interface."""
    
    # Store the MQTT connection and client globally
    mqtt_connection: Optional[Mqtt5Connection] = None
    simple_client: Optional[SimpleClient] = None
    
    CSS = """
    Screen {
        align: center middle;
    }
    """
    
    def on_mount(self) -> None:
        """Start with the connection screen."""
        # Import screens here to avoid circular imports
        from simpleipc.tui.connection import ConnectionScreen
        from simpleipc.tui.discovery import DiscoveryScreen
        from simpleipc.tui.client import ClientScreen
        
        # Install screens
        self.install_screen(ConnectionScreen(), name="connection")
        self.install_screen(DiscoveryScreen(), name="discovery")
        self.install_screen(ClientScreen(), name="client")
        
        # Start with connection screen
        self.push_screen("connection")


def main() -> None:
    """Run the TUI application."""
    app = SimpleIPCApp()
    app.run()


if __name__ == "__main__":
    main()