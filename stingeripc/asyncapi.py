"""
Provides the functionality needed to create an AsyncAPI service specification from a Stinger file.
"""

import sys
from jacobsjinjatoo import templator as jj2
from jacobsjinjatoo import stringmanip
import os.path
from enum import Enum
from typing import Any
from collections import OrderedDict
from .components import StingerSpec, Arg, ArgPrimitive, ArgEnum, ArgStruct
from .args import ArgType, ArgPrimitiveType


class Direction(Enum):
    SERVER_PUBLISHES = 1
    SERVER_SUBSCRIBES = 2


class SpecType(Enum):
    SERVER = 1
    CLIENT = 2
    LIB = 3


class ObjectSchema:

    def __init__(self):
        self._properties: dict[str, Any] = dict()
        self._required = set()
        self._dependent_schemas = {}

    def add_value_property(
        self, name: str, arg_primitive_type: ArgPrimitiveType, required=True
    ):
        schema = {"type": ArgPrimitiveType.to_json_type(arg_primitive_type)}
        self._properties[name] = schema
        if required:
            self._required.add(name)

    def add_value_dependency(self, name: str, required_on_name: str, required_on_value):
        self._dependent_schemas[name] = {
            "properties": {required_on_name: {"const": required_on_value}}
        }

    def add_const_value_property(
        self, name: str, arg_type: ArgPrimitiveType, const_value, required=True
    ):
        self.add_value_property(name, arg_type, required)
        self._properties[name]["const"] = const_value

    def add_enum_value_property(
        self, name: str, arg_type: ArgPrimitiveType, possible_values, required=True
    ):
        self.add_value_property(name, arg_type, required)
        self._properties[name]["enum"] = possible_values

    def add_reference_property(self, name: str, dollar_ref: str, required=True):
        schema = {"$ref": dollar_ref}
        self._properties[name] = schema
        if required:
            self._required.add(name)

    def to_schema(self) -> dict[str, str | dict[str, Any] | list[str]]:
        props: dict[str, Any] = dict()
        schema: dict[str, str | dict[str, Any] | list[str]] = {
            "type": "object",
            "properties": props,
            "required": sorted(list(self._required)),
        }
        for prop_name, prop_schema in self._properties.items():
            props[prop_name] = prop_schema
        return schema


class Message(object):
    """The information needed to create an AsyncAPI Message structure."""

    def __init__(self, message_name: str, schema: str | None = None):
        self.name = message_name
        self.schema = schema or {"type": "null"}
        self._traits: list[dict[str, Any]] = list()
        self._headers: dict[str, tuple[bool, Any]] = dict()

    def set_schema(self, schema: dict[str, Any]):
        self.schema = schema
        return self

    def set_reference(self, reference):
        return self.set_schema({"$ref": reference})

    def add_trait(self, trait):
        self._traits.append(trait)

    def add_header(self, name: str, schema: dict[str, Any], required: bool = False):
        self._headers[name] = (required, schema)

    def get_message(self) -> dict[str, Any]:
        msg: dict[str, Any] = {
            "name": self.name,
            "payload": self.schema,
        }
        if len(self._traits) > 0:
            msg["traits"] = self._traits
        if len(self._headers) > 0:
            msg["headers"] = OrderedDict(
                {
                    "properties": OrderedDict(),
                    "required": list(),
                }
            )
            for header_name, (required, schema) in self._headers.items():
                msg["headers"]["properties"][header_name] = schema
                if required:
                    msg["headers"]["required"].append(header_name)
        return msg


class Channel(object):
    """The data needed to create an AsyncAPI Channel structure."""

    def __init__(
        self,
        topic: str,
        name: str,
        direction: Direction,
        message_name: str | None = None,
    ):
        self.topic = topic
        self.name = name
        self.direction = direction
        self.message_name = message_name or name
        self.mqtt = {"qos": 1, "retain": False}
        self.description: str | None = None
        self.parameters: dict[str, str] = dict()
        self._operation_traits: list[dict[str, Any]] = list()

    def set_mqtt(self, qos: int, retain: bool):
        self.mqtt = {"qos": qos, "retain": retain}
        return self

    def set_description(self, description: str):
        self.description = description
        return self

    def add_topic_parameters(self, name: str, json_schema_type: str):
        self.parameters[name] = json_schema_type
        return self

    def add_operation_trait(self, trait: dict[str, Any]):
        self._operation_traits.append(trait)
        return self

    def get_operation(
        self, client_type: SpecType, use_common=False
    ) -> dict[str, dict[str, Any]]:
        channel_item: dict[str, dict[str, Any]] = dict()
        op_item: OrderedDict[str, Any] = OrderedDict(
            {
                "operationId": self.name,
                "message": {
                    "$ref": f"{use_common or ''}#/components/messages/{self.message_name}"
                },
            }
        )
        if use_common is not False:
            op_item["traits"] = [
                {"$ref": f"{use_common}#/components/operationTraits/{self.name}"}
            ]
        elif len(self._operation_traits) > 0:
            op_item.update(
                OrderedDict(
                    {
                        "traits": self._operation_traits,
                    }
                )
            )
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
                params_obj[param_name] = {"schema": {"type": param_type}}
            channel_item.update({"parameters": params_obj})
        return channel_item


class Server(object):
    def __init__(self, name: str):
        self.name = name
        self._protocol = "mqtt"
        self._host: str | None = None
        self._port: int | None = None
        self._lwt_topic: str | None = None

    def set_host(self, host: str, port: int):
        self._host = host
        self._port = port
        return self

    def set_lwt_topic(self, topic: str):
        self._lwt_topic = topic
        return self

    @property
    def url(self) -> str:
        return "{}:{}".format(self._host or "{hostname}", self._port or "{port}")

    def get_server(self) -> dict[str, Any]:
        spec: dict[str, Any] = {
            "protocol": self._protocol,
            "protocolVersion": "5",
            "url": self.url,
        }
        if self._lwt_topic is not None:
            spec["bindings"] = OrderedDict(
                {
                    "mqtt": OrderedDict(
                        {
                            "lastWill": OrderedDict(
                                {
                                    "retain": False,
                                    "message": None,
                                    "qos": 1,
                                    "topic": self._lwt_topic,
                                }
                            )
                        }
                    )
                }
            )
        if self._host is None or self._port is None:
            spec["variables"] = {}
        if self._host is None:
            spec["variables"]["hostname"] = {
                "description": "The hosthame or IP address of the MQTT broker."
            }
        if self._port is None:
            spec["variables"]["port"] = {"description": "The port for the MQTT server"}
        return spec


class AsyncApiCreator(object):
    """A class to create a AsyncAPI specification from several AsyncAPI structures.

    It also accepts a Stinger spec for creating all the structures.
    """

    def __init__(self):
        self.info = dict()
        self.asyncapi: OrderedDict[str, Any] = OrderedDict(
            {
                "asyncapi": "2.4.0",
                "id": "",
                "info": OrderedDict(),
                "channels": OrderedDict(),
                "components": OrderedDict(
                    {
                        "operationTraits": OrderedDict(
                            {
                                "methodCall": OrderedDict(
                                    {
                                        "bindings": OrderedDict(
                                            {
                                                "mqtt": OrderedDict(
                                                    {
                                                        "bindingVersion": "0.2.0",
                                                        "qos": 2,
                                                        "retain": False,
                                                    }
                                                ),
                                            }
                                        ),
                                    }
                                ),
                                "methodCallback": OrderedDict(
                                    {
                                        "bindings": OrderedDict(
                                            {
                                                "mqtt": OrderedDict(
                                                    {
                                                        "bindingVersion": "0.2.0",
                                                        "qos": 1,
                                                        "retain": False,
                                                    }
                                                ),
                                            }
                                        ),
                                    }
                                ),
                                "signal": OrderedDict(
                                    {
                                        "bindings": OrderedDict(
                                            {
                                                "mqtt": OrderedDict(
                                                    {
                                                        "bindingVersion": "0.2.0",
                                                        "qos": 2,
                                                        "retain": False,
                                                    }
                                                ),
                                            }
                                        ),
                                    }
                                ),
                            }
                        ),
                        "messageTraits": OrderedDict(
                            {
                                "methodJsonArguments": OrderedDict(
                                    {
                                        "bindings": OrderedDict(
                                            {
                                                "mqtt": OrderedDict(
                                                    {
                                                        "bindingVersion": "0.2.0",
                                                        "contentType": "application/json",
                                                        "correlationData": OrderedDict(
                                                            {
                                                                "type": "string",
                                                                "format": "uuid",
                                                            }
                                                        ),
                                                    }
                                                ),
                                            }
                                        ),
                                    }
                                ),
                                "methodJsonResponse": OrderedDict(
                                    {
                                        "bindings": OrderedDict(
                                            {
                                                "mqtt": OrderedDict(
                                                    {
                                                        "bindingVersion": "0.2.0",
                                                        "contentType": "application/json",
                                                        "correlationData": OrderedDict(
                                                            {
                                                                "type": "string",
                                                                "format": "uuid",
                                                            }
                                                        ),
                                                        "responseTopic": {
                                                            "type": "string",
                                                        },
                                                    }
                                                ),
                                            }
                                        ),
                                    }
                                ),
                                "signalJson": OrderedDict(
                                    {
                                        "bindings": OrderedDict(
                                            {
                                                "mqtt": OrderedDict(
                                                    {
                                                        "bindingVersion": "0.2.0",
                                                        "contentType": "application/json",
                                                    }
                                                ),
                                            }
                                        ),
                                    }
                                ),
                            }
                        ),
                        "messages": OrderedDict(),
                        "schemas": OrderedDict(),
                    }
                ),
            }
        )
        self.channels = []
        self.messages = []
        self.servers = []
        self.name = "interface"

    def add_schema(self, schema_name: str, schema_spec: dict[str, Any]):
        schema_dict: dict[str, Any] = self.asyncapi["components"]["schemas"]
        schema_dict[schema_name] = schema_spec

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
            spec["servers"] = {}
        for svr in self.servers:
            spec["servers"][svr.name] = svr.get_server()
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
        if len(self._stinger.methods) > 0:
            schema_name = f"stinger_method_return_codes"
            description = [
                f"The stinger_method_return_codes enum has the following values:"
            ]
            accepted_values = []
            for i, enum_value in self._stinger.method_return_codes.items():
                description.append(f"{i} - {enum_value}")
                accepted_values.append(i)
            json_schema = {
                "type": "integer",
                "description": "\n ".join(description),
                "enum": accepted_values,
            }
            self._asyncapi.add_schema(schema_name, json_schema)
        return self

    def _add_interface_info(self):
        topic, info = self._stinger.interface_info
        self._asyncapi.add_to_info("version", info["version"])
        self._asyncapi.add_to_info("title", info["title"])
        ch = Channel(topic, "interfaceInfo", Direction.SERVER_PUBLISHES)
        ch.set_mqtt(qos=1, retain=True)
        self._asyncapi.add_channel(ch)
        msg = Message("interfaceInfo")
        schema = ObjectSchema()
        for k, v in info.items():
            schema.add_const_value_property(k, ArgPrimitiveType.STRING, v)
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
            description = [f"The {enum_name} enum has the following values:"]
            accepted_values = []
            for i, enum_value in enumerate(enum_spec.values):
                description.append(f"{i} - {enum_value}")
                accepted_values.append(i)
            json_schema = {
                "type": "integer",
                "description": "\n ".join(description),
                "enum": accepted_values,
            }
            self._asyncapi.add_schema(schema_name, json_schema)

    def _add_signals(self):
        for sig_name, sig_spec in self._stinger.signals.items():
            ch = Channel(sig_spec.topic, sig_name, Direction.SERVER_PUBLISHES)
            ch.add_operation_trait({"$ref": "#/components/operationTraits/signal"})
            self._asyncapi.add_channel(ch)
            msg = Message(sig_name)
            msg.add_trait({"$ref": "#/components/messageTraits/signalJson"})
            schema = ObjectSchema()
            for arg_spec in sig_spec.arg_list:
                if isinstance(arg_spec, ArgPrimitive):
                    schema.add_value_property(arg_spec.name, arg_spec.type)
                elif isinstance(arg_spec, ArgEnum):
                    schema.add_reference_property(
                        arg_spec.name, f"#/components/schemas/enum_{arg_spec.enum.name}"
                    )
            msg.set_schema(schema.to_schema())
            self._asyncapi.add_message(msg)

    def _add_methods(self):
        for method_name, method_spec in self._stinger.methods.items():
            call_ch = Channel(
                method_spec.topic, method_name, Direction.SERVER_SUBSCRIBES
            )
            call_ch.add_operation_trait(
                {"$ref": "#/components/operationTraits/methodCall"}
            )
            self._asyncapi.add_channel(call_ch)
            call_msg = Message(method_name)
            call_msg.add_trait(
                {"$ref": "#/components/messageTraits/methodJsonArguments"}
            )
            call_msg_schema = ObjectSchema()
            for arg_spec in method_spec.arg_list:
                if isinstance(arg_spec, ArgPrimitive):
                    call_msg_schema.add_value_property(arg_spec.name, arg_spec.type)
                elif isinstance(arg_spec, ArgEnum):
                    call_msg_schema.add_reference_property(
                        arg_spec.name, f"#/components/schemas/enum_{arg_spec.name}"
                    )
            call_msg.set_schema(call_msg_schema.to_schema())
            self._asyncapi.add_message(call_msg)

            resp_ch = Channel(
                method_spec.response_topic("{client_id}"),
                f"{method_name}Response",
                Direction.SERVER_PUBLISHES,
            )
            resp_ch.add_operation_trait(
                {"$ref": "#/components/operationTraits/methodCall"}
            )
            self._asyncapi.add_channel(resp_ch)
            resp_msg = Message(f"{method_name}Response")
            resp_msg.add_trait(
                {"$ref": "#/components/messageTraits/methodJsonArguments"}
            )
            resp_msg.add_header(
                "result",
                {"$ref": "#/components/schemas/stinger_method_return_codes"},
                required=True,
            )
            resp_msg.add_header("debug", {"type": "string"}, required=False)
            resp_msg_schema = ObjectSchema()

            def add_arg(arg: Arg):
                if isinstance(arg, ArgPrimitive):
                    resp_msg_schema.add_value_property(
                        arg.name, arg.type, required=True
                    )
                elif isinstance(arg, ArgEnum):
                    resp_msg_schema.add_reference_property(
                        arg.name,
                        f"#/components/schemas/enum_{arg.enum.name}",
                        required=True,
                    )

            if isinstance(method_spec.return_value, ArgStruct):
                for arg_spec in method_spec.return_value.members:
                    add_arg(arg_spec)
                    resp_msg_schema.add_value_dependency(arg_spec.name, "result", 0)
            elif method_spec.return_value is not None:
                assert isinstance(
                    method_spec.return_value, Arg
                ), "Method return value must be a primitive or enum"
                add_arg(method_spec.return_value)
                resp_msg_schema.add_value_dependency(
                    method_spec.return_value_name, "result", 0
                )

            resp_msg.set_schema(resp_msg_schema.to_schema())
            self._asyncapi.add_message(resp_msg)

    def get_asyncapi(self):
        return self._asyncapi.get_asyncapi(SpecType.CLIENT)
