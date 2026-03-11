"""Discovery screen for finding WeatherIPC servers."""

from typing import Set
from textual.app import ComposeResult # typing: ignore
from textual.screen import Screen # typing: ignore
from textual.widgets import Header, Footer, Static, Button # typing: ignore
from textual.containers import Grid, Container # typing: ignore
from textual.reactive import reactive # typing: ignore
from weatheripc.client import WeatherClientDiscoverer, DiscoveredInstance, WeatherClient
from weatheripc.tui.helpers import get_package_version
import logging

logger = logging.getLogger(__name__)

class DiscoveryScreen(Screen):
    """Screen for discovering available WeatherIPC servers."""
    
    CSS = """
    DiscoveryScreen {
        align: center top;
    }
    
    #title {
        width: 100%;
        text-align: center;
        text-style: bold;
        padding: 1;
        background: $primary;
    }
    
    #instances_container {
        width: 100%;
        height: auto;
        padding: 2;
    }
    
    #instances_grid {
        grid-size: 3;
        grid-gutter: 1;
        width: 100%;
        height: auto;
    }
    
    .instance_box {
        height: 5;
        border: solid $accent;
        text-align: center;
        content-align: center middle;
    }
    
    .instance_box:hover {
        background: $accent 20%;
    }
    
    .incomplete_instance {
        height: 5;
        border: dashed $warning;
        text-align: center;
        content-align: center middle;
        color: $text-muted;
        text-style: italic;
    }

    Static.no_servers {
        height: 5;
        text-align: center;
        content-align: center middle;
        color: $text-muted;
    }
    """
    
    BINDINGS = [
        ("escape", "app.quit", "Quit"),
    ]
    
    # Reactive variable to track discovered instances
    discovered_instances: reactive[Set[str]] = reactive(set())
    incomplete_interfaces: reactive[Set[str]] = reactive(set())
    
    def __init__(self):
        """Initialize the discovery screen."""
        super().__init__()
        self.discoverer = None
        self.instance_extra_params: dict[str, dict] = {}  # Store extra_params for each instance
    
    def compose(self) -> ComposeResult:
        """Compose the discovery screen widgets."""
        yield Header()
        pkg_name, pkg_ver = get_package_version()
        title_text = f"Discovered Servers \\[{pkg_name}=={pkg_ver}]"
        yield Static(title_text, id="title")
        with Container(id="instances_container"):
            yield Grid(id="instances_grid")
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize discovery when screen mounts."""
        # Get the MQTT connection from the app
        conn = self.app.mqtt_connection
        
        if conn is None:
            self.notify("No MQTT connection available!", severity="error")
            return
        
        # Create the discoverer
        self.discoverer = WeatherClientDiscoverer(conn)
        
        # Subscribe to newly discovered services
        self.discoverer.add_discovered_service_callback(self._on_service_discovered)
        self.discoverer.set_discovered_interface_info_callback(self._on_interface_info_received)
        
        # Initialize the list with currently known instances
        initial_instances = self.discoverer.get_service_instance_ids()
        self.discovered_instances = set(initial_instances)
        
        # Populate the grid
        self._update_grid()
    
    def _on_interface_info_received(self, interface_info) -> None:
        """Callback when new interface info is received."""
        logger.debug("Discovered interface info for instance %s", interface_info)
        # Extract instance_id from interface_info (assuming it has an instance_id attribute)
        if hasattr(interface_info, 'instance_id'):
            instance_id = interface_info.instance_id
            # Use call_from_thread to safely update from MQTT callback thread
            self.app.call_from_thread(self._add_incomplete_interface, instance_id)

    def _on_service_discovered(self, instance: DiscoveredInstance) -> None:
        """Callback when a new service is discovered."""
        logger.debug("Discovered new instance: %s", instance.instance_id)
        # Use call_from_thread to safely update from MQTT callback thread
        extra_params = {
            "prefix": instance.info.prefix,
        }
        self.app.call_from_thread(self._add_instance, instance.instance_id, extra_params)
    
    def _add_incomplete_interface(self, instance_id: str) -> None:
        """Add an incomplete interface (called on main thread)."""
        # Only add if not already fully discovered
        if instance_id not in self.discovered_instances:
            new_incomplete = self.incomplete_interfaces.copy()
            new_incomplete.add(instance_id)
            self.incomplete_interfaces = new_incomplete

    def _add_instance(self, instance_id: str, extra_params: dict) -> None:
        """Add an instance to the discovered set (called on main thread)."""
        # Remove from incomplete if present
        if instance_id in self.incomplete_interfaces:
            new_incomplete = self.incomplete_interfaces.copy()
            new_incomplete.discard(instance_id)
            self.incomplete_interfaces = new_incomplete
        
        # Add to fully discovered
        new_instances = self.discovered_instances.copy()
        new_instances.add(instance_id)
        self.instance_extra_params[instance_id] = extra_params
        self.discovered_instances = new_instances
    
    def watch_discovered_instances(self, old_instances: Set[str], new_instances: Set[str]) -> None:
        """React to changes in discovered instances."""
        self._update_grid()
    
    def watch_incomplete_interfaces(
        self, old_interfaces: Set[str], new_interfaces: Set[str]
    ) -> None:
        """React to changes in incomplete interfaces."""
        self._update_grid()

    def _update_grid(self) -> None:
        """Update the grid display with current instances."""
        grid = self.query_one("#instances_grid", Grid)
        grid.remove_children()
        
        if not self.discovered_instances:
            grid.mount(Static("No weather instances discovered yet...", classes="no_servers"))
        else:
            # Show fully discovered instances first (clickable)
            for instance_id in sorted(self.discovered_instances):
                # Build button label with instance_id and extra_params
                label_parts = [instance_id]
                if instance_id in self.instance_extra_params:
                    extra = self.instance_extra_params[instance_id]
                    for key, value in extra.items():
                        label_parts.append(f"{key}: {value}")
                
                label = "\n".join(label_parts)
                btn = Button(label, classes="instance_box")
                btn.instance_id = instance_id  # Store instance_id on the button
                grid.mount(btn)

            # Show incomplete interfaces (non-clickable)
            for instance_id in sorted(self.incomplete_interfaces):
                static = Static(f"{instance_id}\n(discovering...)", classes="incomplete_instance")
                grid.mount(static)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle instance box click."""
        if hasattr(event.button, 'instance_id'):
            instance_id = event.button.instance_id
            
            # Get the DiscoveredInstance object
            assert self.discoverer is not None, "Discoverer not initialized"
            discovered_instance = self.discoverer.get_discovery_info(instance_id)
            
            if discovered_instance is None:
                self.notify(f"Could not find instance {instance_id}", severity="error")
                return
            
            # Create the WeatherClient
            conn = self.app.mqtt_connection
            client = WeatherClient(conn, discovered_instance)
            
            # Store the client in the app for the Client screen to use
            self.app.weather_client = client
            
            # Create a fresh ClientScreen instance and navigate to it
            from weatheripc.tui.client import ClientScreen
            self.app.push_screen(ClientScreen())