from stinger_python_utils.mcp import (
    MethodDefinition,
    PropertyDefinition,
    SignalDefinition,
    StingerMCPPlugin,
)

from fullipc.client import FullClient, FullClientDiscoverer
from fullipc.interface_types import *


class FullMCPPlugin(StingerMCPPlugin):
    """MCP plugin for the Full interface."""

    def get_plugin_name(self) -> str:
        return "full"

    def get_discovery_class(self) -> type:
        return FullClientDiscoverer

    def get_client_class(self) -> type:
        return FullClient

    def get_signals(self) -> list[SignalDefinition]:
        return [
            SignalDefinition(
                name="today_is",
                description="",
            ),
            SignalDefinition(
                name="random_word",
                description="",
            ),
        ]

    def get_methods(self) -> list[MethodDefinition]:
        return [
            MethodDefinition(
                name="add_numbers",
                description="",
                arguments_model=AddNumbersMethodRequest,
            ),
            MethodDefinition(
                name="do_something",
                description="",
                arguments_model=DoSomethingMethodRequest,
            ),
            MethodDefinition(
                name="what_time_is_it",
                description="Get the current date and time.",
                arguments_model=WhatTimeIsItMethodRequest,
            ),
            MethodDefinition(
                name="hold_temperature",
                description="Hold a temperature for a specified duration.",
                arguments_model=HoldTemperatureMethodRequest,
            ),
        ]

    def get_properties(self) -> list[PropertyDefinition]:
        return [
            PropertyDefinition(
                name="favorite_number",
                description="My favorite number ",
                readonly=False,
                schema=FavoriteNumberProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="favorite_foods",
                description="",
                readonly=False,
                schema=FavoriteFoodsProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="lunch_menu",
                description="",
                readonly=True,
                schema=LunchMenuProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="family_name",
                description="This is to test a property with a single string value.",
                readonly=False,
                schema=FamilyNameProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="last_breakfast_time",
                description="This is to test a property with a single datetime value.",
                readonly=False,
                schema=LastBreakfastTimeProperty.model_json_schema(),
            ),
            PropertyDefinition(
                name="last_birthdays",
                description="This is to test a property with multiple datetime values.",
                readonly=False,
                schema=LastBirthdaysProperty.model_json_schema(),
            ),
        ]
