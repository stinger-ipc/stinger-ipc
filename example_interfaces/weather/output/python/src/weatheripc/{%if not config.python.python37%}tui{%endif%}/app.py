"""Main TUI application for WeatherIPC."""

from typing import Optional
from textual.app import App
from textual.screen import Screen
from weatheripc.connection import MqttBrokerConnection
from weatheripc.client import WeatherClient


class WeatherIPCApp(App):
    """A Textual app for WeatherIPC client interface."""

    # Store the MQTT connection and client globally
    mqtt_connection: Optional[MqttBrokerConnection] = None
    weather_client: Optional[WeatherClient] = None

    CSS = """
    Screen {
        align: center middle;
    }
    """

    def on_mount(self) -> None:
        """Start with the connection screen."""
        # Import screens here to avoid circular imports
        from weatheripc.tui.connection import ConnectionScreen
        from weatheripc.tui.discovery import DiscoveryScreen
        from weatheripc.tui.client import ClientScreen

        # Install screens
        self.install_screen(ConnectionScreen(), name="connection")
        self.install_screen(DiscoveryScreen(), name="discovery")
        self.install_screen(ClientScreen(), name="client")

        # Start with connection screen
        self.push_screen("connection")


def main() -> None:
    """Run the TUI application."""
    app = WeatherIPCApp()
    app.run()


if __name__ == "__main__":
    main()
