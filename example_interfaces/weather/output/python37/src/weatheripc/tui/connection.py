"""MQTT Connection screen for configuring broker connection."""

from textual.app import ComposeResult  # typing: ignore
from textual.screen import Screen  # typing: ignore
from textual.widgets import Header, Footer, Input, Button, Static, Checkbox  # typing: ignore
from textual.containers import Container, Vertical  # typing: ignore
from pyqttier.connection import Mqtt5Connection
from pyqttier.transport import MqttTransport, MqttTransportType


class ConnectionScreen(Screen):
    """Screen for configuring MQTT broker connection."""

    CSS = """
    ConnectionScreen {
        align: center middle;
    }
    
    #connection_form {
        width: 60;
        height: auto;
        border: solid $primary;
        padding: 1 2;
    }
    
    #title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    
    .input_group {
        height: auto;
        margin-bottom: 1;
    }
    
    .label {
        margin-bottom: 1;
    }
    
    Input {
        margin-bottom: 1;
    }
    
    Button {
        width: 100%;
        margin-top: 1;
    }
    """

    BINDINGS = [
        ("escape", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the connection screen widgets."""
        yield Header()
        with Container(id="connection_form"):
            yield Static("MQTT Broker Connection", id="title")
            with Vertical(classes="input_group"):
                yield Static("IP Address:", classes="label")
                yield Input(placeholder="localhost", value="localhost", id="ip_address")
            with Vertical(classes="input_group"):
                yield Static("Port:", classes="label")
                yield Input(placeholder="1883", value="1883", id="port")
            with Vertical(classes="input_group"):
                yield Static("Username (optional):", classes="label")
                yield Input(placeholder="", id="username")
            with Vertical(classes="input_group"):
                yield Static("Password (optional):", classes="label")
                yield Input(placeholder="", password=True, id="password")
            with Vertical(classes="input_group"):
                yield Checkbox("Use TLS", id="use_tls")
            yield Button("Connect", variant="primary", id="connect_button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle connect button press."""
        if event.button.id == "connect_button":
            ip_input = self.query_one("#ip_address", Input)
            port_input = self.query_one("#port", Input)
            username_input = self.query_one("#username", Input)
            password_input = self.query_one("#password", Input)
            tls_checkbox = self.query_one("#use_tls", Checkbox)

            ip_address = ip_input.value or "localhost"
            try:
                port = int(port_input.value or "1883")
            except ValueError:
                port = 1883

            username = username_input.value if username_input.value else None
            password = password_input.value if password_input.value else None
            credentials = (username, password) if (username and password) else None
            use_tls = tls_checkbox.value

            # Create the MQTT connection
            transport = MqttTransport(MqttTransportType.TCP, ip_address, port)
            if use_tls:
                transport.enable_tls()
            conn = Mqtt5Connection(transport, credentials=credentials)

            # Store connection in app for use by other screens
            self.app.mqtt_connection = conn

            # Navigate to discovery screen
            self.app.push_screen("discovery")
