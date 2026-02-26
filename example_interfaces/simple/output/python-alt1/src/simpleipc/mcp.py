from stinger_python_utils.mcp import (
    MethodDefinition,
    PropertyDefinition,
    SignalDefinition,
    StingerMCPPlugin,
)

from simpleipc.client import SimpleClient, SimpleClientDiscoverer
from simpleipc.interface_types import *


class SimpleMCPPlugin(StingerMCPPlugin):
    """MCP plugin for the Simple interface."""

    def get_plugin_name(self) -> str:
        return "simple"

    def get_discovery_class(self) -> type:
        return SimpleClientDiscoverer

    def get_client_class(self) -> type:
        return SimpleClient

    def get_signals(self) -> list[SignalDefinition]:
        return [
            SignalDefinition(
                name="person_entered",
                description="",
            ),
        ]

    def get_methods(self) -> list[MethodDefinition]:
        return [
            MethodDefinition(
                name="trade_numbers",
                description="A simple method which trades favorite numbers.",
                arguments_model=TradeNumbersMethodRequest,
            ),
        ]

    def get_properties(self) -> list[PropertyDefinition]:
        return [
            PropertyDefinition(
                name="school",
                description="",
                readonly=False,
                schema=SchoolProperty.model_json_schema(),
            ),
        ]
