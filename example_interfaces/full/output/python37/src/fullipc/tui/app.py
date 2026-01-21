"""Main TUI application for FullIPC."""

import argparse
from typing import Optional, Dict, Any
from textual.app import App  # typing: ignore
from textual.screen import Screen  # typing: ignore
from pyqttier.connection import Mqtt5Connection
from fullipc.client import FullClient


class FullIPCApp(App):
    """A Textual app for FullIPC client interface."""

    # Store the MQTT connection and client globally
    mqtt_connection: Optional[Mqtt5Connection] = None
    full_client: Optional[FullClient] = None

    # Store TLS configuration
    tls_config: Dict[str, Any] = dict()

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

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="FullIPC TUI Application")
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

    app = FullIPCApp()

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
