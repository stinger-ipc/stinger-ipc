"""Main TUI application for TestableIPC."""

from typing import Optional
from textual.app import App  # typing: ignore
from textual.screen import Screen  # typing: ignore
from pyqttier.connection import Mqtt5Connection
from testableipc.client import TestableClient


class TestableIPCApp(App):
    """A Textual app for TestableIPC client interface."""

    # Store the MQTT connection and client globally
    mqtt_connection: Optional[Mqtt5Connection] = None
    testable_client: Optional[TestableClient] = None

    CSS = """
    Screen {
        align: center middle;
    }
    """

    def on_mount(self) -> None:
        """Start with the connection screen."""
        # Import screens here to avoid circular imports
        from testableipc.tui.connection import ConnectionScreen
        from testableipc.tui.discovery import DiscoveryScreen
        from testableipc.tui.client import ClientScreen

        # Install screens
        self.install_screen(ConnectionScreen(), name="connection")
        self.install_screen(DiscoveryScreen(), name="discovery")
        self.install_screen(ClientScreen(), name="client")

        # Start with connection screen
        self.push_screen("connection")


def main() -> None:
    """Run the TUI application."""
    app = TestableIPCApp()
    app.run()


if __name__ == "__main__":
    main()
