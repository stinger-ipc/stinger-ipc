"""Client screen for interacting with WeatherIPC server."""

import concurrent.futures as futures
from datetime import datetime, timedelta
import isodate
from typing import List, Optional, Any, Dict
from textual.app import ComposeResult  # typing: ignore
from textual.screen import Screen, ModalScreen  # typing: ignore
from textual.widgets import Header, Footer, Static, RichLog, Button, Input, Label, Select  # typing: ignore
from textual.containers import Horizontal, VerticalScroll, Vertical  # typing: ignore
from weatheripc.interface_types import *
from weatheripc.client import WeatherClient


class PropertyEditModal(ModalScreen[bool]):
    """Modal screen for editing a property value."""

    CSS = """
    PropertyEditModal {
        align: center middle;
    }
    
    #property_modal_container {
        width: 60%;
        height: auto;
        background: $surface;
        border: thick $primary;
        padding: 1;
    }
    
    #property_modal_title {
        text-style: bold;
        text-align: center;
        background: $primary;
        padding: 1;
        margin-bottom: 1;
    }
    
    .property_input_label {
        margin-top: 1;
        margin-bottom: 1;
    }

    .property_input_value_label {
        margin-top: 1;
        margin-bottom: 1;
        color: $primary;
    }
    
    #property_input {
        margin-bottom: 1;
    }

    .property_input_value {
        margin-bottom: 1;
    }
    
    #property_button_container {
        layout: horizontal;
        height: auto;
        margin-top: 1;
    }
    
    #property_button_container Button {
        width: 1fr;
        margin: 0 1;
    }
    """

    def __init__(self, property_name: str, current_value: Any, client: WeatherClient):
        super().__init__()
        self.property_name = property_name
        self.current_value = current_value
        self.client = client

    def compose(self) -> ComposeResult:
        """Compose the modal screen."""
        with Vertical(id="property_modal_container"):
            yield Static(f"Edit: {self.property_name}", id="property_modal_title")
            yield Label(f"Current value: {self.current_value}", classes="property_input_label")
            if self.property_name == "location":
                yield Label(f"latitude", classes="property_input_value_label")
                yield Input(placeholder=f"latitude value", value=str(self.current_value.latitude), classes="property_input_value", id="property_input_latitude")

                yield Label(f"longitude", classes="property_input_value_label")
                yield Input(placeholder=f"longitude value", value=str(self.current_value.longitude), classes="property_input_value", id="property_input_longitude")

            if self.property_name == "current_temperature":

                yield Input(placeholder=f"Enter new value", value=str(self.current_value) if self.current_value is not None else "", id="property_input")

            if self.property_name == "current_condition":
                yield Label(f"condition", classes="property_input_value_label")
                yield Input(placeholder=f"condition value", value=str(self.current_value.condition), classes="property_input_value", id="property_input_condition")

                yield Label(f"description", classes="property_input_value_label")
                yield Input(placeholder=f"description value", value=str(self.current_value.description), classes="property_input_value", id="property_input_description")

            if self.property_name == "daily_forecast":
                yield Label(f"monday (JSON)", classes="property_input_value_label")
                yield Input(placeholder=f"monday value", value=self.current_value.monday.model_dump_json(), classes="property_input_value", id="property_input_monday")

                yield Label(f"tuesday (JSON)", classes="property_input_value_label")
                yield Input(placeholder=f"tuesday value", value=self.current_value.tuesday.model_dump_json(), classes="property_input_value", id="property_input_tuesday")

                yield Label(f"wednesday (JSON)", classes="property_input_value_label")
                yield Input(placeholder=f"wednesday value", value=self.current_value.wednesday.model_dump_json(), classes="property_input_value", id="property_input_wednesday")

            if self.property_name == "hourly_forecast":
                yield Label(f"hour_0 (JSON)", classes="property_input_value_label")
                yield Input(placeholder=f"hour_0 value", value=self.current_value.hour_0.model_dump_json(), classes="property_input_value", id="property_input_hour_0")

                yield Label(f"hour_1 (JSON)", classes="property_input_value_label")
                yield Input(placeholder=f"hour_1 value", value=self.current_value.hour_1.model_dump_json(), classes="property_input_value", id="property_input_hour_1")

                yield Label(f"hour_2 (JSON)", classes="property_input_value_label")
                yield Input(placeholder=f"hour_2 value", value=self.current_value.hour_2.model_dump_json(), classes="property_input_value", id="property_input_hour_2")

                yield Label(f"hour_3 (JSON)", classes="property_input_value_label")
                yield Input(placeholder=f"hour_3 value", value=self.current_value.hour_3.model_dump_json(), classes="property_input_value", id="property_input_hour_3")

            if self.property_name == "current_condition_refresh_interval":

                yield Input(placeholder=f"Enter new value", value=str(self.current_value) if self.current_value is not None else "", id="property_input")

            if self.property_name == "hourly_forecast_refresh_interval":

                yield Input(placeholder=f"Enter new value", value=str(self.current_value) if self.current_value is not None else "", id="property_input")

            if self.property_name == "daily_forecast_refresh_interval":

                yield Input(placeholder=f"Enter new value", value=str(self.current_value) if self.current_value is not None else "", id="property_input")

            with Horizontal(id="property_button_container"):
                yield Button("Update", variant="primary", id="update_button")
                yield Button("Cancel", variant="error", id="cancel_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "update_button":
            try:
                if self.property_name == "location":
                    input_widget_latitude = self.query_one("#property_input_latitude", Input)
                    # latitude should be ArgPrimitiveType.FLOAT
                    new_location_value_latitude = float(input_widget_latitude.value)

                    input_widget_longitude = self.query_one("#property_input_longitude", Input)
                    # longitude should be ArgPrimitiveType.FLOAT
                    new_location_value_longitude = float(input_widget_longitude.value)

                    new_location_value = LocationProperty(
                        latitude=new_location_value_latitude,
                        longitude=new_location_value_longitude,
                    )

                    self.client.location = new_location_value
                elif self.property_name == "current_condition_refresh_interval":
                    input_widget = self.query_one("#property_input", Input)
                    new_current_condition_refresh_interval_value = int(input_widget.value)

                    self.client.current_condition_refresh_interval = new_current_condition_refresh_interval_value
                elif self.property_name == "hourly_forecast_refresh_interval":
                    input_widget = self.query_one("#property_input", Input)
                    new_hourly_forecast_refresh_interval_value = int(input_widget.value)

                    self.client.hourly_forecast_refresh_interval = new_hourly_forecast_refresh_interval_value
                elif self.property_name == "daily_forecast_refresh_interval":
                    input_widget = self.query_one("#property_input", Input)
                    new_daily_forecast_refresh_interval_value = int(input_widget.value)

                    self.client.daily_forecast_refresh_interval = new_daily_forecast_refresh_interval_value

                self.dismiss(True)
            except Exception as e:
                self.app.notify(f"Error updating property: {e}", severity="error")
        else:
            self.dismiss(False)


class MethodCallModal(ModalScreen[Optional[str]]):
    """Modal screen for calling a method with inputs."""

    CSS = """
    MethodCallModal {
        align: center middle;
    }
    
    #modal_container {
        width: 80;
        height: auto;
        max-height: 90%;
        background: $surface;
        border: thick $primary;
        padding: 1;
    }
    
    #modal_title {
        text-style: bold;
        text-align: center;
        background: $primary;
        padding: 1;
        margin-bottom: 1;
    }
    
    #inputs_container {
        height: auto;
        max-height: 60%;
        overflow-y: auto;
    }
    
    .input_label {
        margin-top: 1;
        margin-bottom: 1;
    }
    
    Input {
        margin-bottom: 1;
    }
    
    #button_container {
        layout: horizontal;
        height: auto;
        margin-top: 1;
    }
    
    #button_container Button {
        width: 1fr;
        margin: 0 1;
    }
    
    #result_text {
        margin-top: 1;
        padding: 1;
        background: $panel;
        border: solid $accent;
        max-height: 20;
        overflow-y: auto;
    }
    """

    def __init__(self, method_name: str, params: Dict[str, type], client: Any):
        super().__init__()
        self.method_name = method_name
        self.params = params
        self.client = client
        self.result_widget: Optional[Static] = None

    def compose(self) -> ComposeResult:
        """Compose the modal screen."""
        with Vertical(id="modal_container"):
            yield Static(f"Call: {self.method_name}", id="modal_title")

            with VerticalScroll(id="inputs_container"):
                if self.params:
                    for param_name, param_type in self.params.items():
                        yield Label(f"{param_name} ({param_type.__name__ if hasattr(param_type, '__name__') else str(param_type)}):", classes="input_label")
                        yield Input(placeholder=f"Enter {param_name}", id=f"input_{param_name}")
                else:
                    yield Static("No parameters required")

            with Horizontal(id="button_container"):
                yield Button("Call Method", variant="primary", id="call_button")
                yield Button("Close", variant="error", id="cancel_button")

            self.result_widget = Static("", id="result_text")
            yield self.result_widget

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel_button":
            self.dismiss(None)
        elif event.button.id == "call_button":
            self._call_method()

    def _call_method(self) -> None:
        """Call the method with collected inputs."""
        assert self.result_widget is not None, "result_widget must be initialized"
        try:
            # Collect inputs
            kwargs = {}
            for param_name, param_type in self.params.items():
                input_widget = self.query_one(f"#input_{param_name}", Input)
                value_str = input_widget.value

                # Simple parsing - for demo, handle basic types
                if value_str:
                    kwargs[param_name] = self._parse_value(value_str, param_type)
                elif "Optional" not in str(param_type):
                    self.result_widget.update("[red]Error: Missing required parameter[/red]")
                    return
                else:
                    kwargs[param_name] = None

            # Call the method
            self.result_widget.update("[yellow]Calling method...[/yellow]")
            method = getattr(self.client, self.method_name)
            future_result = method(**kwargs)

            # Wait for result (with timeout)
            try:
                result = future_result.result(timeout=5.0)
                self.result_widget.update(f"[green]Success![/green]\n\nResult: {result}")
            except futures.TimeoutError:
                self.result_widget.update("[red]Timeout waiting for response[/red]")
            except Exception as e:
                self.result_widget.update(f"[red]Error: {e}[/red]")

        except Exception as e:
            self.result_widget.update(f"[red]Error preparing call: {e}[/red]")

    def _parse_value(self, value_str: str, param_type: type) -> Any:
        """Parse a string value to the appropriate type."""
        type_str = str(param_type)

        if "int" in type_str.lower():
            return int(value_str)
        elif "float" in type_str.lower() or "number" in type_str.lower():
            return float(value_str)
        elif "str" in type_str.lower():
            return value_str
        elif "bool" in type_str.lower():
            return value_str.lower() in ("true", "1", "yes")
        else:
            # For complex types, return the string for now
            return value_str


class ClientScreen(Screen):
    """Screen for interacting with a connected WeatherIPC server."""

    CSS = """
    ClientScreen {
        layout: vertical;
    }
    
    #main_container {
        width: 100%;
        height: 1fr;
    }
    
    #left_pane {
        width: 20%;
        border-right: solid $primary;
        padding: 1;
    }
    
    #middle_pane {
        width: 30%;
        border-right: solid $primary;
        padding: 1;
    }
    
    #right_pane {
        width: 50%;
        padding: 1;
    }
    
    .pane_title {
        text-style: bold;
        background: $primary;
        padding: 1;
        text-align: center;
        margin-bottom: 1;
    }
    
    RichLog {
        height: 1fr;
        border: solid $accent;
    }
    
    .property_item {
        margin: 0;
        padding: 1;
        background: $surface;
        border: solid $accent;
    }
    
    .property_item.writable {
        background: $surface;
    }
    
    .property_item.writable:hover {
        background: $accent 20%;
    }
    
    .property_item.readonly {
        background: $surface-darken-1;
        color: $text-muted;
    }
    
    .property_name {
        text-style: bold;
        color: $accent;
    }
    
    .property_value {
        margin-top: 1;
        color: $text;
    }
    """

    BINDINGS = [
        ("escape", "back_to_discovery", "Back to Discovery"),
    ]

    def __init__(self):
        """Initialize the client screen."""
        super().__init__()
        self.client = None

    def compose(self) -> ComposeResult:
        """Compose the client screen widgets."""
        yield Header()
        with Horizontal(id="main_container"):
            with VerticalScroll(id="left_pane"):
                yield Static("Methods", classes="pane_title")
                # Method buttons will be added dynamically
            with VerticalScroll(id="middle_pane"):
                yield Static("Properties", classes="pane_title")
                # Properties will be added dynamically
            with VerticalScroll(id="right_pane"):
                yield Static("Signals", classes="pane_title")
                yield RichLog(id="signals_log", highlight=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        """Set up signal handlers when screen mounts."""
        # Get the client from the app
        self.client = self.app.weather_client

        if self.client is None:
            self.notify("No client available!", severity="error")
            return

        # Add method buttons
        self._add_method_buttons()

        # Register all signal handlers
        self._register_signal_handlers()

        # Register all property handlers
        self._register_property_handlers()

    def _add_method_buttons(self) -> None:
        """Add buttons for all call_* methods."""
        pane = self.query_one("#left_pane", VerticalScroll)

        # Define all methods with their parameters
        methods = {
            "refresh_daily_forecast": {},
            "refresh_hourly_forecast": {},
            "refresh_current_conditions": {},
        }  # type: Dict[str, Dict[str, Any]]

        for method_name, params in methods.items():
            btn = Button(method_name, classes="method_button")
            btn.method_name = method_name  # Store for retrieval
            btn.method_params = params
            pane.mount(btn)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle method button presses."""
        if hasattr(event.button, "method_name"):
            method_name = event.button.method_name
            method_params = event.button.method_params

            # Show modal for method call
            modal = MethodCallModal(method_name, method_params, self.client)
            self.app.push_screen(modal)

    def _register_signal_handlers(self) -> None:
        """Register callbacks for all receive_* methods."""
        log = self.query_one("#signals_log", RichLog)

        # Define a generic handler factory
        def make_handler(signal_name: str):
            def handler(*args, **kwargs):
                # Format the received data
                if args:
                    data = ", ".join([f"{arg}" for arg in args])
                elif kwargs:
                    data = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
                else:
                    data = "(no data)"

                # Log to the RichLog widget
                timestamp = datetime.now().strftime("%H:%M:%S")
                log.write(f"[gray]{timestamp}[/gray] [bold cyan]{signal_name}[/bold cyan]: {data}")

            return handler

        # Register all signal handlers
        assert self.client is not None, "Client must be initialized"
        self.client.receive_current_time(make_handler("current_time"))

    def _register_property_handlers(self) -> None:
        """Register callbacks for all *_changed methods and create property displays."""
        pane = self.query_one("#middle_pane", VerticalScroll)

        # Define property registration helper
        def register_property(prop_name: str, changed_method_name: str, is_writable: bool = False):
            # Create a Static widget for this property
            prop_widget = Static(id=f"prop_{prop_name}")
            prop_widget.add_class("property_item")

            # Add writable or readonly class
            if is_writable:
                prop_widget.add_class("writable")
                prop_widget.can_focus = True
                prop_widget.property_name = prop_name  # Store for click handling
            else:
                prop_widget.add_class("readonly")

            pane.mount(prop_widget)

            if prop_name == "location":

                def on_location_updated(value: LocationProperty):
                    prop_widget.current_value = value

                    values = []

                    # Multiple values

                    line = f"[bold]latitude[/bold]: { value.latitude }"  # Other - PRIMITIVE
                    values.append(line)

                    line = f"[bold]longitude[/bold]: { value.longitude }"  # Other - PRIMITIVE
                    values.append(line)

                    value_str = "\n".join(values)

                    # Update the widget
                    prop_widget.update(f"[bold cyan]{prop_name}[/bold cyan]\n{value_str}")

                # Register the handler with call_immediately=True
                assert self.client is not None, "Client must be initialized"
                self.client.location_changed(on_location_updated, call_immediately=True)

            elif prop_name == "current_temperature":

                def on_current_temperature_updated(value: float):
                    prop_widget.current_value = value

                    values = []

                    # Single value
                    if value is None:
                        values.append("None")
                    else:

                        values.append(f"{value}")  # other - PRIMITIVE

                    value_str = "\n".join(values)

                    # Update the widget
                    prop_widget.update(f"[bold cyan]{prop_name}[/bold cyan]\n{value_str}")

                # Register the handler with call_immediately=True
                assert self.client is not None, "Client must be initialized"
                self.client.current_temperature_changed(on_current_temperature_updated, call_immediately=True)

            elif prop_name == "current_condition":

                def on_current_condition_updated(value: CurrentConditionProperty):
                    prop_widget.current_value = value

                    values = []

                    # Multiple values

                    line = f"[bold]condition[/bold]: { value.condition.name if value.condition else 'None' } ({ value.condition.value if value.condition else 'None' })"  # Enum
                    values.append(line)

                    line = f"[bold]description[/bold]: { value.description }"  # Other - PRIMITIVE
                    values.append(line)

                    value_str = "\n".join(values)

                    # Update the widget
                    prop_widget.update(f"[bold cyan]{prop_name}[/bold cyan]\n{value_str}")

                # Register the handler with call_immediately=True
                assert self.client is not None, "Client must be initialized"
                self.client.current_condition_changed(on_current_condition_updated, call_immediately=True)

            elif prop_name == "daily_forecast":

                def on_daily_forecast_updated(value: DailyForecastProperty):
                    prop_widget.current_value = value

                    values = []

                    # Multiple values

                    if value.monday is None:
                        values.append(f"[bold]monday[/bold]: None")
                    else:
                        values.append(f"[bold]monday.high_temperature[/bold]: { value.monday.high_temperature }")  # Struct Member
                        values.append(f"[bold]monday.low_temperature[/bold]: { value.monday.low_temperature }")  # Struct Member
                        values.append(f"[bold]monday.condition[/bold]: { value.monday.condition }")  # Struct Member
                        values.append(f"[bold]monday.start_time[/bold]: { value.monday.start_time }")  # Struct Member
                        values.append(f"[bold]monday.end_time[/bold]: { value.monday.end_time }")  # Struct Member

                    if value.tuesday is None:
                        values.append(f"[bold]tuesday[/bold]: None")
                    else:
                        values.append(f"[bold]tuesday.high_temperature[/bold]: { value.tuesday.high_temperature }")  # Struct Member
                        values.append(f"[bold]tuesday.low_temperature[/bold]: { value.tuesday.low_temperature }")  # Struct Member
                        values.append(f"[bold]tuesday.condition[/bold]: { value.tuesday.condition }")  # Struct Member
                        values.append(f"[bold]tuesday.start_time[/bold]: { value.tuesday.start_time }")  # Struct Member
                        values.append(f"[bold]tuesday.end_time[/bold]: { value.tuesday.end_time }")  # Struct Member

                    if value.wednesday is None:
                        values.append(f"[bold]wednesday[/bold]: None")
                    else:
                        values.append(f"[bold]wednesday.high_temperature[/bold]: { value.wednesday.high_temperature }")  # Struct Member
                        values.append(f"[bold]wednesday.low_temperature[/bold]: { value.wednesday.low_temperature }")  # Struct Member
                        values.append(f"[bold]wednesday.condition[/bold]: { value.wednesday.condition }")  # Struct Member
                        values.append(f"[bold]wednesday.start_time[/bold]: { value.wednesday.start_time }")  # Struct Member
                        values.append(f"[bold]wednesday.end_time[/bold]: { value.wednesday.end_time }")  # Struct Member

                    value_str = "\n".join(values)

                    # Update the widget
                    prop_widget.update(f"[bold cyan]{prop_name}[/bold cyan]\n{value_str}")

                # Register the handler with call_immediately=True
                assert self.client is not None, "Client must be initialized"
                self.client.daily_forecast_changed(on_daily_forecast_updated, call_immediately=True)

            elif prop_name == "hourly_forecast":

                def on_hourly_forecast_updated(value: HourlyForecastProperty):
                    prop_widget.current_value = value

                    values = []

                    # Multiple values

                    if value.hour_0 is None:
                        values.append(f"[bold]hour_0[/bold]: None")
                    else:
                        values.append(f"[bold]hour_0.temperature[/bold]: { value.hour_0.temperature }")  # Struct Member
                        values.append(f"[bold]hour_0.starttime[/bold]: { value.hour_0.starttime }")  # Struct Member
                        values.append(f"[bold]hour_0.condition[/bold]: { value.hour_0.condition }")  # Struct Member

                    if value.hour_1 is None:
                        values.append(f"[bold]hour_1[/bold]: None")
                    else:
                        values.append(f"[bold]hour_1.temperature[/bold]: { value.hour_1.temperature }")  # Struct Member
                        values.append(f"[bold]hour_1.starttime[/bold]: { value.hour_1.starttime }")  # Struct Member
                        values.append(f"[bold]hour_1.condition[/bold]: { value.hour_1.condition }")  # Struct Member

                    if value.hour_2 is None:
                        values.append(f"[bold]hour_2[/bold]: None")
                    else:
                        values.append(f"[bold]hour_2.temperature[/bold]: { value.hour_2.temperature }")  # Struct Member
                        values.append(f"[bold]hour_2.starttime[/bold]: { value.hour_2.starttime }")  # Struct Member
                        values.append(f"[bold]hour_2.condition[/bold]: { value.hour_2.condition }")  # Struct Member

                    if value.hour_3 is None:
                        values.append(f"[bold]hour_3[/bold]: None")
                    else:
                        values.append(f"[bold]hour_3.temperature[/bold]: { value.hour_3.temperature }")  # Struct Member
                        values.append(f"[bold]hour_3.starttime[/bold]: { value.hour_3.starttime }")  # Struct Member
                        values.append(f"[bold]hour_3.condition[/bold]: { value.hour_3.condition }")  # Struct Member

                    value_str = "\n".join(values)

                    # Update the widget
                    prop_widget.update(f"[bold cyan]{prop_name}[/bold cyan]\n{value_str}")

                # Register the handler with call_immediately=True
                assert self.client is not None, "Client must be initialized"
                self.client.hourly_forecast_changed(on_hourly_forecast_updated, call_immediately=True)

            elif prop_name == "current_condition_refresh_interval":

                def on_current_condition_refresh_interval_updated(value: int):
                    prop_widget.current_value = value

                    values = []

                    # Single value
                    if value is None:
                        values.append("None")
                    else:

                        values.append(f"{value}")  # other - PRIMITIVE

                    value_str = "\n".join(values)

                    # Update the widget
                    prop_widget.update(f"[bold cyan]{prop_name}[/bold cyan]\n{value_str}")

                # Register the handler with call_immediately=True
                assert self.client is not None, "Client must be initialized"
                self.client.current_condition_refresh_interval_changed(on_current_condition_refresh_interval_updated, call_immediately=True)

            elif prop_name == "hourly_forecast_refresh_interval":

                def on_hourly_forecast_refresh_interval_updated(value: int):
                    prop_widget.current_value = value

                    values = []

                    # Single value
                    if value is None:
                        values.append("None")
                    else:

                        values.append(f"{value}")  # other - PRIMITIVE

                    value_str = "\n".join(values)

                    # Update the widget
                    prop_widget.update(f"[bold cyan]{prop_name}[/bold cyan]\n{value_str}")

                # Register the handler with call_immediately=True
                assert self.client is not None, "Client must be initialized"
                self.client.hourly_forecast_refresh_interval_changed(on_hourly_forecast_refresh_interval_updated, call_immediately=True)

            elif prop_name == "daily_forecast_refresh_interval":

                def on_daily_forecast_refresh_interval_updated(value: int):
                    prop_widget.current_value = value

                    values = []

                    # Single value
                    if value is None:
                        values.append("None")
                    else:

                        values.append(f"{value}")  # other - PRIMITIVE

                    value_str = "\n".join(values)

                    # Update the widget
                    prop_widget.update(f"[bold cyan]{prop_name}[/bold cyan]\n{value_str}")

                # Register the handler with call_immediately=True
                assert self.client is not None, "Client must be initialized"
                self.client.daily_forecast_refresh_interval_changed(on_daily_forecast_refresh_interval_updated, call_immediately=True)

        # Register all properties
        register_property("location", "location_changed", is_writable=True)
        register_property("current_temperature", "current_temperature_changed", is_writable=False)
        register_property("current_condition", "current_condition_changed", is_writable=False)
        register_property("daily_forecast", "daily_forecast_changed", is_writable=False)
        register_property("hourly_forecast", "hourly_forecast_changed", is_writable=False)
        register_property("current_condition_refresh_interval", "current_condition_refresh_interval_changed", is_writable=True)
        register_property("hourly_forecast_refresh_interval", "hourly_forecast_refresh_interval_changed", is_writable=True)
        register_property("daily_forecast_refresh_interval", "daily_forecast_refresh_interval_changed", is_writable=True)

    def on_click(self, event) -> None:
        """Handle clicks on property widgets."""
        assert self.client is not None, "Client must be initialized"

        # Check if the clicked widget is a writable property
        widget = event.widget
        if hasattr(widget, "property_name") and hasattr(widget, "current_value"):
            property_name = widget.property_name
            current_value = widget.current_value

            # Open the edit modal
            modal = PropertyEditModal(property_name, current_value, self.client)
            self.app.push_screen(modal)

    def action_back_to_discovery(self) -> None:
        """Navigate back to the discovery screen."""
        self.app.pop_screen()
