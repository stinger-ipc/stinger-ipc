"""
Provides the functionality needed to create an AsyncAPI service specification from a Stinger file.
"""


import sys
from collections import OrderedDict
from jacobsjinjatoo import templator as jj2
from jacobsjinjatoo import stringmanip
import os.path
from enum import Enum
from typing import Optional


class Direction(Enum):
    SERVER_PUBLISHES = 1
    SERVER_SUBSCRIBES = 2


class SpecType(Enum):
    SERVER = 1
    CLIENT = 2
    LIB = 3


class Message(object):
    """The information needed to create an AsyncAPI Message structure."""

    def __init__(self, message_name: str, schema: Optional[str] = None):
        self.name = message_name
        self.schema = schema or {"type": "null"}

    def set_schema(self, schema: dict):
        self.schema = schema
        return self

    def set_reference(self, reference):
        return self.set_schema({"$ref": reference})

    def get_message(self):
        return {
            "name": self.name,
            "payload": self.schema,
        }


class Channel(object):
    """The data needed to create an AsyncAPI Channel structure."""

    def __init__(
        self,
        topic: str,
        name: str,
        direction: Direction,
        message_name: Optional[str] = None,
    ):
        self.topic = topic
        self.name = name
        self.direction = direction
        self.message_name = message_name or name
        self.mqtt = {"qos": 1, "retain": False}

    def set_mqtt(self, qos: int, retain: bool):
        self.mqtt = {"qos": qos, "retain": retain}
        return self

    def get_operation_trait(self) -> dict:
        return {
            "operationId": self.name,
            "bindings": {
                "mqtt": self.mqtt,
            },
        }

    def get_operation(self, client_type: SpecType, use_common=False) -> OrderedDict:
        op_item = OrderedDict(
            {
                "message": {
                    "$ref": f"{use_common or ''}#/components/messages/{self.message_name}"
                }
            }
        )
        if use_common is not False:
            op_item["traits"] = [
                {"$ref": f"{use_common}#/components/operationTraits/{self.name}"}
            ]
        else:
            op_item.update(self.get_operation_trait())
        if (
            client_type == SpecType.SERVER
            and self.direction == Direction.SERVER_PUBLISHES
        ) or (
            client_type == SpecType.CLIENT
            and self.direction == Direction.SERVER_SUBSCRIBES
        ):
            return {"publish": op_item}
        else:
            return {"subscribe": op_item}


class AsyncApiCreator(object):
    """A class to create a AsyncAPI specification from several AsyncAPI structures.

    It also accepts a Stinger spec for creating all the structures.
    """

    def __init__(self):
        self.asyncapi = OrderedDict(
            {
                "asyncapi": "2.0.0",
                "id": "",
                "info": OrderedDict(),
                "channels": OrderedDict(),
                "components": OrderedDict(
                    {
                        "operationTraits": OrderedDict(),
                        "messages": OrderedDict(),
                    }
                ),
            }
        )
        self.channels = []
        self.messages = []
        self.name = "interface"

    def _add_channel(self, channel: Channel):
        self.channels.append(channel)

    def _add_message(self, message: Message):
        self.messages.append(message)

    def _set_interface_name(self, name):
        self.name = name
        self.asyncapi["id"] = f"urn:stingeripc:{name}"

    def _set_interface_version(self, version_str):
        self.asyncapi["info"]["version"] = version_str
        message = Message("stinger_version", {"type": "string"})
        channel = Channel(
            topic=f"{self.name}/stingerVersion",
            name="stinger_version",
            direction=Direction.SERVER_PUBLISHES,
            message_name=message.name,
        )
        channel.set_mqtt(1, True)
        self._add_channel(channel)
        self._add_message(message)

    def _add_signal(self, signal_name, signal_def):
        msg_name = f"{signal_name}Signal"
        msg = Message(msg_name).set_reference(signal_def["payload"])
        self._add_message(msg)
        channel = Channel(
            f"{self.name}/{signal_name}",
            signal_name,
            Direction.SERVER_PUBLISHES,
            msg.name,
        )
        channel.set_mqtt(2, False)
        self._add_channel(channel)

    def _add_param(self, param_name, param_def):
        msg_name = "{}Param".format(stringmanip.upper_camel_case(param_name))
        msg = Message(msg_name).set_reference(param_def["type"])
        self._add_message(msg)

        value_channel_topic = f"{self.name}/{param_name}/value"
        value_channel_name = f"{param_name}Value"
        value_channel = Channel(
            value_channel_topic,
            value_channel_name,
            Direction.SERVER_PUBLISHES,
            msg.name,
        )
        value_channel.set_mqtt(1, True)
        self._add_channel(value_channel)

        update_channel_topic = f"{self.name}/{param_name}/update"
        update_channel_name = f"Update{param_name}"
        update_channel = Channel(
            update_channel_topic,
            update_channel_name,
            Direction.SERVER_SUBSCRIBES,
            msg.name,
        )
        update_channel.set_mqtt(1, True)
        self._add_channel(update_channel)

    def add_stinger(self, stinger):
        assert stinger["stingeripc"] == "0.0.1"
        try:
            self._set_interface_name(stinger["interface"]["name"])
        except KeyError:
            raise Exception("The Stinger File does not have a name")
        self._set_interface_version(stinger["interface"]["version"])
        if "signals" in stinger:
            for sig_name, sig_def in stinger["signals"].items():
                self._add_signal(sig_name, sig_def)
        if "params" in stinger:
            for param_name, param_def in stinger["params"].items():
                self._add_param(param_name, param_def)

    def get_asyncapi(self, client_type: SpecType, use_common=None):
        spec = self.asyncapi.copy()
        for ch in self.channels:
            spec["channels"][ch.topic] = ch.get_operation(
                client_type, use_common or False
            )
        if use_common is None:
            for msg in self.messages:
                spec["components"]["messages"][msg.name] = msg.get_message()
        return spec
