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
    kwargs: dict = {"type": "string", "enum": [item.name for item in ie.items]}
    if ie.documentation:
        kwargs["description"] = ie.documentation
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
    return models.channel.Parameters(root=params)

def _signal_to_channel(signal: IpcSignal) -> models.Channel:

    payload_schema = Schema(
        **{
            "type": "object",
            "properties": {arg.name: _arg_schema(arg) for arg in signal.arg_list},
            "required": [arg.name for arg in signal.arg_list if not arg.optional] or None,
        }
    )
    message = models.Message(
        name=signal.name,
        description=signal.documentation,
        payload=payload_schema,
        bindings=MessageBindingsObject(mqtt=MQTTMessageBindings(contentType="application/json")),
    )
    address = signal.topic()
    channel = models.Channel(
        address=address,
        description=signal.documentation,
        messages=models.message.Messages(root={signal.name: message}),
        parameters=_parameters_for_address(address),
    )
    return channel


def _signal_to_operation(name: str, signal: IpcSignal) -> models.Operation:
    return models.Operation(
        action="receive",
        channel=models.base.Reference(ref=f"#/channels/{name}"),
        description=signal.documentation,
        messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{name}")],
        bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
    )


def _method_request_to_operation(name: str, method: IpcMethod) -> models.Operation:
    return models.Operation(
        action="send",
        channel=models.base.Reference(ref=f"#/channels/{name}"),
        description=method.documentation,
        messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{name}")],
        bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
    )


def _method_request_to_channel(method: IpcMethod) -> models.Channel:
    payload_schema = Schema(
        **{
            "type": "object",
            "properties": {arg.name: _arg_schema(arg) for arg in method.arg_list},
            "required": [arg.name for arg in method.arg_list if not arg.optional] or None,
        }
    )
    message = models.Message(
        name=method.name,
        description=method.documentation,
        payload=payload_schema,
        bindings=MessageBindingsObject(mqtt=MQTTMessageBindings(contentType="application/json")),
    )
    address = method.request_topic()
    channel = models.Channel(
        address=address,
        description=method.documentation,
        messages=models.message.Messages(root={method.name: message}),
        parameters=_parameters_for_address(address),
    )
    return channel



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
        channels[name] = _signal_to_channel(signal)
        operations[name] = _signal_to_operation(name, signal)
    for method_name, method in spec.methods.items():
        channels[method_name] = _method_request_to_channel(method)
        operations[method_name] = _method_request_to_operation(method_name, method)


    aa = AsyncAPI3(
        info=models.Info(
            title=spec.name,
            version=spec._version,
            description=spec.summary or None,
        ),
        components=models.Components(schemas=Schemas(root=schemas) if schemas else None),
        channels=models.Channels(root=channels) if channels else None,
        operations=models.operation.Operations(root=operations) if operations else None,
    )

    aa.components.parameters = models.channel.Parameters(root={
        "service_id": models.Parameter(description="The ID of the service/instance")
    })

    return json.loads(aa.model_dump_json(exclude_none=True))
