"""Main TUI application for FullIPC."""

from typing import Optional
from textual.app import App # typing: ignore
from textual.screen import Screen # typing: ignore
from pyqttier.connection import Mqtt5Connection
from fullipc.client import FullClient


class FullIPCApp(App):
    """A Textual app for FullIPC client interface."""
    
    # Store the MQTT connection and client globally
    mqtt_connection: Optional[Mqtt5Connection] = None
    full_client: Optional[FullClient] = None
    
    CSS = """
    Screen {
        align: center middle;
    }
    """
    
    def on_mount(self) -> None:
        """Start with the connection screen."""
        # Import screens here to avoid circular imports
        from fullipc.tui.connection import ConnectionScreen
        from fullipc.tui.discovery import DiscoveryScreen
        from fullipc.tui.client import ClientScreen
        
        # Install screens
        self.install_screen(ConnectionScreen(), name="connection")
        self.install_screen(DiscoveryScreen(), name="discovery")
        self.install_screen(ClientScreen(), name="client")
        
        # Start with connection screen
        self.push_screen("connection")


def main() -> None:
    """Run the TUI application."""
    app = FullIPCApp()
    app.run()


if __name__ == "__main__":
    main()