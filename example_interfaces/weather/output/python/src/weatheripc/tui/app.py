"""Main TUI application for WeatherIPC."""

import argparse
from typing import Optional, Dict, Any
from textual.app import App # typing: ignore
from textual.screen import Screen # typing: ignore
from textual.command import Provider, Hit  # typing: ignore
from pyqttier.connection import Mqtt5Connection
from weatheripc.client import WeatherClient


class LogsCommandProvider(Provider):
    """Command provider for showing logs."""

    async def search(self, query: str):
        """Search for log-related commands."""
        matcher = self.matcher(query)
        
        if matcher.match("logs") or matcher.match("show logs") or matcher.match("view logs"):
            yield Hit(
                score=matcher.match("show logs"),
                match_display="Show Logs",
                command=lambda: self.app.push_screen("logs"),
                help="View application logs for debugging"
            )


class WeatherIPCApp(App):
    """A Textual app for WeatherIPC client interface."""
    
    # Store the MQTT connection and client globally
    mqtt_connection: Optional[Mqtt5Connection] = None
    weather_client: Optional[WeatherClient] = None
    
    # Store TLS configuration
    tls_config: Dict[str, Any] = dict()
    
    COMMANDS = {LogsCommandProvider}

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
        from weatheripc.tui.logs import LogsScreen, install_log_handler
        
        # Install log capture handler
        install_log_handler()

        # Install screens
        self.install_screen(ConnectionScreen(), name="connection")
        self.install_screen(DiscoveryScreen(), name="discovery")
        self.install_screen(LogsScreen(), name="logs")
        
        # Start with connection screen
        self.push_screen("connection")


def main() -> None:
    """Run the TUI application."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="WeatherIPC TUI Application")
    parser.add_argument(
        "--cafile",
        help="Path to CA certificate file for TLS certificate validation",
    )
    parser.add_argument(
        "--capath",
        help="Path to directory containing CA certificates for TLS",
    )
    parser.add_argument(
        "--cert",
        help="Path to client certificate file for TLS client authentication",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification (not recommended for production)",
    )
    args = parser.parse_args()

    app = WeatherIPCApp()

    # Store TLS configuration in the app
    app.tls_config = {
        "cafile": args.cafile,
        "capath": args.capath,
        "cert": args.cert,
        "insecure": args.insecure,
    }
    
    app.run()


if __name__ == "__main__":
    main()