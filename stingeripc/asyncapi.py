"""
Provides the functionality needed to create an AsyncAPI service specification from a Stinger file.
"""


import sys
from collections import OrderedDict
from jacobsjinjatoo import templator as jj2
from jacobsjinjatoo import stringmanip
import os.path
from enum import Enum
from typing import Optional, Dict, Any, Union, List

from .components import StingerSpec
from .args import ArgType, ArgValueType

class Direction(Enum):
    SERVER_PUBLISHES = 1
    SERVER_SUBSCRIBES = 2


class SpecType(Enum):
    SERVER = 1
    CLIENT = 2
    LIB = 3


class ObjectSchema:
    def __init__(self):
        self._properties = OrderedDict()
    
    def add_value_property(self, name: str, arg_type: ArgValueType):
        schema = {
            "type": ArgValueType.to_json_type(arg_type)
        }
        self._properties[name] = schema

    def add_const_value_property(self, name: str, arg_type: ArgValueType, const_value):
        self.add_value_property(name, arg_type)
        self._properties[name]['const'] = const_value

    def add_reference_property(self, name: str, dollar_ref: str):
        schema = {
            "$ref": dollar_ref
        }
        self._properties[name] = schema

    def to_schema(self) -> Dict[str, Union[Dict[str,Any], List[str]]]:
        schema = {
            "type": "object",
            "properties": {},
            "required": [],
        }
        for prop_name, prop_schema in self._properties.items():
            schema['properties'][prop_name] = prop_schema
            schema['required'].append(prop_name)
        return schema


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
        self.description = None # type: Optional[str]
        self.parameters = dict() # type: Dict[str, str]

    def set_mqtt(self, qos: int, retain: bool):
        self.mqtt = {"qos": qos, "retain": retain}
        return self

    def set_description(self, description: str):
        self.description = description
        return self

    def add_topic_parameters(self, name: str, json_schema_type: str):
        self.parameters[name] = json_schema_type
        return self

    def get_operation_trait(self) -> dict:
        return {
            "operationId": self.name,
            "bindings": {
                "mqtt": self.mqtt,
            },
        }

    def get_operation(self, client_type: SpecType, use_common=False) -> OrderedDict:
        channel_item = dict()
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
            channel_item.update({"publish": op_item})
        else:
            channel_item.update({"subscribe": op_item})
        if len(self.parameters) > 0:
            params_obj = dict()
            for param_name, param_type in self.parameters.items():
                params_obj[param_name] = {
                    "schema": {
                        "type": param_type
                    }
                }
            channel_item.update({"parameters": params_obj})
        return channel_item


class Server(object):
    def __init__(self, name: str):
        self.name = name
        self._protocol = "mqtt"
        self._host = None
        self._port = None
        self._lwt_topic = None

    def set_host(self, host: str, port: int):
        self._host = host
        self._port = port
        return self

    def set_lwt_topic(self, topic: str):
        self._lwt_topic = topic
        return self

    @property
    def url(self) -> str:
        return "{}:{}".format(
            self._host or "{hostname}",
            self._port or "{port}"
        )

    def get_server(self) -> Dict[str, Any]:
        spec = {
            "protocol": self._protocol,
            "protocolVersion": "3.1.1",
            "url": self.url,
        }
        if self._lwt_topic is not None:
            spec['bindings'] = {
                "mqtt": {
                    "lastWill": {
                        "retain": False,
                        "message": None,
                        "qos": 1,
                        "topic": self._lwt_topic,
                    }
                }
            }
        if self._host is None or self._port is None:
            spec['variables'] = {}
        if self._host is None:
            spec['variables']['hostname'] = {
                "description": "The hosthame or IP address of the MQTT broker."
            }
        if self._port is None:
            spec['variables']['port'] = {
                "description": "The port for the MQTT server"
            }
        return spec

class AsyncApiCreator(object):
    """A class to create a AsyncAPI specification from several AsyncAPI structures.

    It also accepts a Stinger spec for creating all the structures.
    """

    def __init__(self):
        self.asyncapi = OrderedDict(
            {
                "asyncapi": "2.4.0",
                "id": "",
                "info": OrderedDict(),
                "channels": OrderedDict(),
                "components": OrderedDict(
                    {
                        "operationTraits": OrderedDict(),
                        "messages": OrderedDict(),
                        "schemas": OrderedDict()
                    }
                ),
            }
        )
        self.channels = []
        self.messages = []
        self.servers = []
        self.name = "interface"

    def add_schema(self, schema_name, schema_spec: Dict[str, Any]):
        self.asyncapi['components']['schemas'][schema_name] = schema_spec

    def add_channel(self, channel: Channel):
        self.channels.append(channel)

    def add_message(self, message: Message):
        self.messages.append(message)

    def add_server(self, server: Server):
        self.servers.append(server)

    def set_interface_name(self, name):
        self.name = name
        self.asyncapi["id"] = f"urn:stingeripc:{name}"

    def add_to_info(self, key, value):
        self.asyncapi["info"][key] = value

    def get_asyncapi(self, client_type: SpecType, use_common=None):
        spec = self.asyncapi.copy()
        if len(self.servers) > 0:
            spec['servers'] = {}
        for svr in self.servers:
            spec['servers'][svr.name] = svr.get_server()
        for ch in self.channels:
            spec["channels"][ch.topic] = ch.get_operation(
                client_type, use_common or False
            )
        if use_common is None:
            for msg in self.messages:
                spec["components"]["messages"][msg.name] = msg.get_message()
        return spec


class StingerToAsyncApi:

    def __init__(self, stinger: StingerSpec):
        self._asyncapi: AsyncApiCreator = AsyncApiCreator()
        self._stinger: StingerSpec = stinger
        self._convert()

    def _convert(self):
        self._asyncapi.set_interface_name(self._stinger.name)
        self._add_interface_info()
        self._add_servers()
        self._add_enums()
        self._add_signals()
        self._add_methods()
        return self

    def _add_interface_info(self):
        topic, info = self._stinger.interface_info
        self._asyncapi.add_to_info("version", info['version'])
        self._asyncapi.add_to_info("title", info['title'])
        ch = Channel(topic, "interfaceInfo", Direction.SERVER_PUBLISHES)
        ch.set_mqtt(qos=1, retain=True)
        self._asyncapi.add_channel(ch)
        msg = Message("interfaceInfo")
        schema = ObjectSchema()
        for k,v in info.items():
            schema.add_const_value_property(k, ArgValueType.STRING, v)
        msg.set_schema(schema.to_schema())
        self._asyncapi.add_message(msg)

    def _add_servers(self):
        info_topic, _ = self._stinger.interface_info
        for broker_name, broker_spec in self._stinger.brokers.items():
            svr = Server(broker_name)
            if broker_spec.hostname is not None and broker_spec.port is not None:
                svr.set_host(broker_spec.hostname, broker_spec.port)
            svr.set_lwt_topic(info_topic)
            self._asyncapi.add_server(svr)

    def _add_enums(self):
        for enum_name, enum_spec in self._stinger.enums.items():
            schema_name = f"enum_{enum_name}"
            description = [
                f"The {enum_name} enum has the following values:"
            ]
            accepted_values = []
            for i, enum_value in enumerate(enum_spec.values):
                description.append(f"{i} - {enum_value}")
                accepted_values.append(i)
            json_schema = {
                "type":  "integer",
                "description": "\n ".join(description),
                "enum": accepted_values
            }
            self._asyncapi.add_schema(schema_name, json_schema)

    def _add_signals(self):
        for sig_name, sig_spec in self._stinger.signals.items():
            ch = Channel(sig_spec.topic, sig_name, Direction.SERVER_PUBLISHES)
            self._asyncapi.add_channel(ch)
            msg = Message(sig_name)
            schema = ObjectSchema()
            for arg_spec in sig_spec.arg_list:
                if arg_spec.arg_type == ArgType.VALUE:
                    schema.add_value_property(arg_spec.name, arg_spec.type)
                elif arg_spec.arg_type == ArgType.ENUM:
                    schema.add_reference_property(arg_spec.name, f"#/components/schemas/enum_{arg_spec.enum.name}")
            msg.set_schema(schema.to_schema())
            self._asyncapi.add_message(msg)

    def _add_methods(self):
        for method_name, method_spec in self._stinger.methods.items():
            call_ch = Channel(method_spec.topic, method_name, Direction.SERVER_SUBSCRIBES)
            call_ch.set_mqtt(2, False)
            self._asyncapi.add_channel(call_ch)
            call_msg = Message(method_name)
            call_msg_schema = ObjectSchema()
            for arg_spec in method_spec.arg_list:
                if arg_spec.arg_type == ArgType.VALUE:
                    call_msg_schema.add_value_property(arg_spec.name, arg_spec.type)
                elif arg_spec.arg_type == ArgType.ENUM:
                    call_msg_schema.add_reference_property(arg_spec.name, f"#/components/schemas/enum_{arg_spec.enum.name}")
            call_msg.set_schema(call_msg_schema.to_schema())
            self._asyncapi.add_message(call_msg)

            resp_ch = Channel(method_spec.response_topic("{client_id}"), f"{method_name}Response", Direction.SERVER_PUBLISHES)
            resp_ch.add_topic_parameters("client_id", "string").set_mqtt(1, False)
            self._asyncapi.add_channel(resp_ch)

    def get_asyncapi(self):
        return self._asyncapi.get_asyncapi(SpecType.CLIENT)