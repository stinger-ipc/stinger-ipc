"""
Provides the functionality needed to create an AsyncAPI service specification from a Stinger file.
"""

import json
import warnings

warnings.filterwarnings("ignore", module="asyncapi3")

from asyncapi3 import AsyncAPI3
from asyncapi3 import models
from asyncapi3.models import Schema
from asyncapi3.models.components import Schemas

from asyncapi3.models.bindings import (
    MQTTChannelBindings,
    MQTTOperationBindings,
    MQTTMessageBindings,
    ChannelBindingsObject,
    OperationBindingsObject,
    MessageBindingsObject,
)

from stingeripc.arg_datatypes import InterfaceEnum, InterfaceStruct
from stingeripc.arg_models import Arg, ArgEnum, ArgStruct, ArgPrimitive
from stingeripc.ipc_method import IpcMethod
from stingeripc.ipc_property import IpcProperty
from stingeripc.ipc_signal import IpcSignal
from stingeripc.components import StingerSpec
from stingeripc.args import ArgType

def _primitive_type_to_schema(type_str: str) -> dict:
    type_map = {
        "string": "string",
        "integer": "integer",
        "float": "number",
        "boolean": "boolean",
        "datetime": "string",
        "duration": "string",
        "binary": "string",
    }
    return {"type": type_map.get(type_str, "string")}


def _enum_to_schema(ie: InterfaceEnum) -> Schema:
    kwargs: dict = {"type": "integer", "enum": [item.integer for item in ie.enum_items]}
    item_descriptions: list[str] = [f"JSON Value `{item.integer}` is `{item.name}` - {item.description or ''}" for item in ie.enum_items]
    if ie.documentation:
        item_descriptions.insert(0, ie.documentation)
    kwargs["description"] = "\n".join(item_descriptions)
    return Schema(**kwargs)


def _struct_to_schema(ist: InterfaceStruct) -> Schema:
    from stingeripc.arg_models import ArgEnum, ArgStruct, ArgPrimitive
    from stingeripc.args import ArgType
    properties: dict[str, dict] = {}
    required: list[str] = []
    for member in ist.members:
        if member.arg_type == ArgType.ENUM:
            assert isinstance(member, ArgEnum)
            prop: dict = {"$ref": f"#/components/schemas/{member.enum.name}"}
        elif member.arg_type == ArgType.STRUCT:
            assert isinstance(member, ArgStruct)
            prop = {"$ref": f"#/components/schemas/{member.interface_struct.name}"}
        elif member.arg_type == ArgType.PRIMITIVE:
            assert isinstance(member, ArgPrimitive)
            prop = _primitive_type_to_schema(member.primitive_type.name.lower())
        else:
            prop = {"type": "string"}
        if member.description:
            prop["description"] = member.description
        properties[member.name] = prop
        if not member.optional:
            required.append(member.name)
    kwargs: dict = {"type": "object", "properties": properties}
    if required:
        kwargs["required"] = required
    if ist.documentation:
        kwargs["description"] = ist.documentation
    return Schema(**kwargs)

def _arg_schema(arg: Arg) -> dict:
    if arg.arg_type == ArgType.ENUM:
        assert isinstance(arg, ArgEnum)
        return {"$ref": f"#/components/schemas/{arg.enum.name}"}
    elif arg.arg_type == ArgType.STRUCT:
        assert isinstance(arg, ArgStruct)
        return {"$ref": f"#/components/schemas/{arg.interface_struct.name}"}
    elif arg.arg_type == ArgType.PRIMITIVE:
        assert isinstance(arg, ArgPrimitive)
        return _primitive_type_to_schema(arg.primitive_type.name.lower())
    return {"type": "string"}

def _parameters_for_address(address: str) -> models.channel.Parameters:
    params: dict = {}
    if '{service_id}' in address:
        params["service_id"] = {'$ref': '#/components/parameters/service_id'}
    if '{client_id}' in address:
        params["client_id"] = {'$ref': '#/components/parameters/client_id'}
    return models.channel.Parameters(root=params)

def arg_list_to_schema(arg_list: list[Arg]) -> Schema:
    properties: dict[str, dict] = {}
    required: list[str] = []
    for arg in arg_list:
        properties[arg.name] = _arg_schema(arg)
        if not arg.optional:
            required.append(arg.name)
    kwargs: dict = {"type": "object", "properties": properties}
    if required:
        kwargs["required"] = required
    return Schema(**kwargs)

class AsyncApiSignalHelper:
    def __init__(self, signal: IpcSignal):
        self.signal = signal

    def get_payload_schema(self) -> Schema:
        return arg_list_to_schema(self.signal.arg_list)

    def get_message(self) -> models.Message:
        payload_schema = self.get_payload_schema()
        return models.Message(
            name=self.signal.name,
            description=f"This is the message for the '{self.signal.name}' signal.  It is encoded as a JSON object.",
            payload=payload_schema,
            bindings=MessageBindingsObject(mqtt=MQTTMessageBindings(contentType="application/json")),
        )

    def to_channel(self) -> models.Channel:
        message = self.get_message()
        address = self.signal.topic()
        return models.Channel(
            address=address,
            description=self.signal.documentation,
            messages=models.message.Messages(root={self.signal.name: message}),
            parameters=_parameters_for_address(address),
        )

    def to_operation(self) -> models.Operation:
        name = self.signal.name
        return models.Operation(
            action="receive",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description=self.signal.documentation,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
        )


class AsyncApiMethodHelper:
    def __init__(self, method: IpcMethod):
        self.method = method

    def request_channel_name(self) -> str:
        return f"{self.method.name}_request"

    def response_channel_name(self) -> str:
        return f"{self.method.name}_response"

    def request_message_key(self) -> str:
        return f"{self.method.name}_request"

    def response_message_key(self) -> str:
        return self.method.return_value_name.replace(" ", "_")

    def request_to_channel(self) -> models.Channel:
        payload_schema = Schema(
            **{
                "type": "object",
                "properties": {arg.name: _arg_schema(arg) for arg in self.method.arg_list},
                "required": [arg.name for arg in self.method.arg_list if not arg.optional] or None,
            }
        )
        message = models.Message(
            name=self.request_message_key(),
            description=self.method.documentation,
            payload=payload_schema,
            bindings=MessageBindingsObject(mqtt=MQTTMessageBindings(contentType="application/json")),
        )
        address = self.method.request_topic()
        return models.Channel(
            address=address,
            description=self.method.documentation,
            messages=models.message.Messages(root={self.request_message_key(): message}),
            parameters=_parameters_for_address(address),
        )

    def request_to_operation(self) -> models.Operation:
        name = self.request_channel_name()
        return models.Operation(
            action="send",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description=self.method.documentation,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
        )

    def response_to_channel(self) -> models.Channel:
        payload_schema = Schema(
            **{
                "type": "object",
                "properties": {arg.name: _arg_schema(arg) for arg in self.method.return_arg_list},
                "required": [arg.name for arg in self.method.return_arg_list if not arg.optional] or None,
            }
        )
        response_key = self.response_message_key()
        message = models.Message(
            name=self.method.return_value_name,
            description=self.method.documentation,
            payload=payload_schema,
            bindings=MessageBindingsObject(mqtt=MQTTMessageBindings(contentType="application/json")),
        )
        address = self.method.response_topic()
        return models.Channel(
            address=address,
            description=self.method.documentation,
            messages=models.message.Messages(root={response_key: message}),
            parameters=_parameters_for_address(address),
        )

    def response_to_operation(self) -> models.Operation:
        name = self.response_channel_name()
        return models.Operation(
            action="receive",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description=self.method.documentation,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{self.response_message_key()}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
        )


class AsyncApiPropertyHelper:
    def __init__(self, prop: IpcProperty):
        self.prop = prop

    def value_channel_name(self) -> str:
        return f"{self.prop.name}_value"

    def update_request_channel_name(self) -> str:
        return f"{self.prop.name}_update_request"

    def update_response_channel_name(self) -> str:
        return f"{self.prop.name}_update_response"

    def payload_schema(self) -> Schema:
        return Schema(
            **{
                "type": "object",
                "properties": {arg.name: _arg_schema(arg) for arg in self.prop.arg_list},
                "required": [arg.name for arg in self.prop.arg_list if not arg.optional] or None,
            }
        )

    def get_message(self) -> models.Message:
        return models.Message(
            name=self.prop.name,
            description=f"This is the message for the value of the '{self.prop.name}' property.  It is encoded as a JSON object.",
            payload=self.payload_schema(),
            bindings=MessageBindingsObject(mqtt=MQTTMessageBindings(contentType="application/json")),
        )

    def value_to_channel(self) -> models.Channel:
        address = self.prop.value_topic()
        return models.Channel(
            address=address,
            description=self.prop.documentation,
            messages=models.message.Messages(root={self.prop.name: self.get_message()}),
            parameters=_parameters_for_address(address),
        )

    def value_to_operation(self) -> models.Operation:
        name = self.value_channel_name()
        return models.Operation(
            action="receive",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description=self.prop.documentation,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{self.prop.name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
        )

    def update_request_to_channel(self) -> models.Channel:
        address = self.prop.update_topic()
        return models.Channel(
            address=address,
            description=self.prop.documentation,
            messages=models.message.Messages(root={self.prop.name: self.get_message()}),
            parameters=_parameters_for_address(address),
        )

    def update_request_to_operation(self) -> models.Operation:
        name = self.update_request_channel_name()
        return models.Operation(
            action="send",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description=self.prop.documentation,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{self.prop.name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
        )

    def update_response_to_channel(self) -> models.Channel:
        address = self.prop.response_topic()
        return models.Channel(
            address=address,
            description=self.prop.documentation,
            messages=models.message.Messages(root={self.prop.name: self.get_message()}),
            parameters=_parameters_for_address(address),
        )

    def update_response_to_operation(self) -> models.Operation:
        name = self.update_response_channel_name()
        return models.Operation(
            action="receive",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description=self.prop.documentation,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{self.prop.name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
        )


def stinger_to_asyncapi(spec: StingerSpec) -> dict:
    """Convert a StingerSpec to an AsyncAPI 3.0 specification dict."""
    schemas: dict[str, Schema] = {}
    for enum_name, ie in spec.enums.items():
        schemas[enum_name] = _enum_to_schema(ie)
    for struct_name, ist in spec.structs.items():
        schemas[struct_name] = _struct_to_schema(ist)

    channels: dict[str, models.Channel] = {}
    operations: dict[str, models.Operation] = {}
    for name, signal in spec.signals.items():
        signal_helper = AsyncApiSignalHelper(signal)
        channels[name] = signal_helper.to_channel()
        operations[name] = signal_helper.to_operation()
    for method_name, method in spec.methods.items():
        method_helper = AsyncApiMethodHelper(method)
        channels[method_helper.request_channel_name()] = method_helper.request_to_channel()
        operations[method_helper.request_channel_name()] = method_helper.request_to_operation()
        channels[method_helper.response_channel_name()] = method_helper.response_to_channel()
        operations[method_helper.response_channel_name()] = method_helper.response_to_operation()
    for prop_name, prop in spec.properties.items():
        prop_helper = AsyncApiPropertyHelper(prop)
        channels[prop_helper.value_channel_name()] = prop_helper.value_to_channel()
        operations[prop_helper.value_channel_name()] = prop_helper.value_to_operation()
        if not prop.read_only:
            channels[prop_helper.update_request_channel_name()] = prop_helper.update_request_to_channel()
            operations[prop_helper.update_request_channel_name()] = prop_helper.update_request_to_operation()
            channels[prop_helper.update_response_channel_name()] = prop_helper.update_response_to_channel()
            operations[prop_helper.update_response_channel_name()] = prop_helper.update_response_to_operation()


    aa = AsyncAPI3(
        info=models.Info(
            title=spec.name,
            version=spec._version,
            description=spec.summary or None,
        ),
        components=models.Components(
            schemas=Schemas(root=schemas) if schemas else None,
            messages=models.message.Messages(root={
                msg_key: msg
                for channel in channels.values()
                if channel.messages
                for msg_key, msg in channel.messages.root.items()
            }) or None,
        ),
        channels=models.Channels(root=channels) if channels else None,
        operations=models.operation.Operations(root=operations) if operations else None,
    )

    aa.components.parameters = models.channel.Parameters(root={
        "service_id": models.Parameter(description="The ID of the service/instance"),
        "client_id": models.Parameter(description="The MQTT Client ID"),
    })

    return json.loads(aa.model_dump_json(exclude_none=True))
