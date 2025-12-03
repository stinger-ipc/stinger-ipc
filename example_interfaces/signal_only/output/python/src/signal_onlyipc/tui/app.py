"""Main TUI application for SignalOnlyIPC."""

from typing import Optional
from textual.app import App
from textual.screen import Screen
from signal_onlyipc.connection import MqttBrokerConnection
from signal_onlyipc.client import SignalOnlyClient


class SignalOnlyIPCApp(App):
    """A Textual app for SignalOnlyIPC client interface."""

    # Store the MQTT connection and client globally
    mqtt_connection: Optional[MqttBrokerConnection] = None
    signal_only_client: Optional[SignalOnlyClient] = None

    CSS = """
    Screen {
        align: center middle;
    }
    """

    def on_mount(self) -> None:
        """Start with the connection screen."""
        # Import screens here to avoid circular imports
        from signal_onlyipc.tui.connection import ConnectionScreen
        from signal_onlyipc.tui.discovery import DiscoveryScreen
        from signal_onlyipc.tui.client import ClientScreen

        # Install screens
        self.install_screen(ConnectionScreen(), name="connection")
        self.install_screen(DiscoveryScreen(), name="discovery")
        self.install_screen(ClientScreen(), name="client")

        # Start with connection screen
        self.push_screen("connection")


def main() -> None:
    """Run the TUI application."""
    app = SignalOnlyIPCApp()
    app.run()


if __name__ == "__main__":
    main()
