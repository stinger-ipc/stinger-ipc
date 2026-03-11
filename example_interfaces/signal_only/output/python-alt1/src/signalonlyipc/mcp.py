from stinger_python_utils.mcp import (
    MethodDefinition,
    PropertyDefinition,
    SignalDefinition,
    StingerMCPPlugin,
)

from signalonlyipc.client import SignalOnlyClient, SignalOnlyClientDiscoverer
from signalonlyipc.interface_types import *


class SignalOnlyMCPPlugin(StingerMCPPlugin):
    """MCP plugin for the SignalOnly interface."""

    def get_plugin_name(self) -> str:
        return "signalonly"

    def get_discovery_class(self) -> type:
        return SignalOnlyClientDiscoverer

    def get_client_class(self) -> type:
        return SignalOnlyClient

    def get_signals(self) -> list[SignalDefinition]:
        return [
            SignalDefinition(
                name="another_signal",
                description="",
            ),
            SignalDefinition(
                name="bark",
                description="Emitted when a dog barks.",
            ),
            SignalDefinition(
                name="maybe_number",
                description="A signal with optionally no payload.",
            ),
            SignalDefinition(
                name="maybe_name",
                description="A signal with optionally no payload.",
            ),
            SignalDefinition(
                name="now",
                description="The current date and time.",
            ),
        ]

    def get_methods(self) -> list[MethodDefinition]:
        return []

    def get_properties(self) -> list[PropertyDefinition]:
        return []
