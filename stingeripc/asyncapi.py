"""
Provides the functionality needed to create an AsyncAPI service specification from a Stinger file.
"""

import json
import re
import warnings

warnings.filterwarnings("ignore", module="asyncapi3")
from typing import Any
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

from stinger_python_utils.return_codes import (
    MethodReturnCode,
)

from stingeripc.arg_datatypes import InterfaceEnum, InterfaceStruct
from stingeripc.arg_models import Arg, ArgArray, ArgEnum, ArgStruct, ArgPrimitive
from stingeripc.ipc_method import IpcMethod
from stingeripc.ipc_property import IpcProperty
from stingeripc.ipc_signal import IpcSignal
from stingeripc.components import StingerSpec
from stingeripc.args import ArgType
from stingeripc.config import StingerConfig
from jacobsjinjatoo.stringmanip import lower_camel_case, upper_camel_case


def _primitive_type_to_schema(arg: ArgPrimitive) -> dict:
    schema_dict: dict[str, Any] = {}
    type_map = {
        "string": "string",
        "integer": "integer",
        "float": "number",
        "boolean": "boolean",
    }
    json_type: str | list[str] = type_map.get(arg.primitive_type.name.lower(), "string")
    if arg.optional:
        assert isinstance(json_type, str)
        schema_dict["type"] = [json_type, "null"]
    else:
        schema_dict["type"] = json_type
    if arg.description:
        schema_dict["description"] = arg.description
    return schema_dict


def _other_arg_to_schema(arg: Arg) -> dict:
    schema_dict: dict[str, Any] = {"type": "string"}
    if arg.arg_type.name.lower() == "datetime":
        schema_dict["format"] = "date-time"
    elif arg.arg_type.name.lower() == "duration":
        schema_dict["format"] = "duration"
        if arg.description:
            schema_dict["description"] = (arg.description + " The value should be an ISO 8601 duration string, e.g. 'PT1H30M' for 1 hour and 30 minutes.").strip()
        else:
            schema_dict["description"] = "The value should be an ISO 8601 duration string, e.g. 'PT1H30M' for 1 hour and 30 minutes."
    elif arg.arg_type.name.lower() == "binary":
        schema_dict["format"] = "byte"
        if arg.description:
            schema_dict["description"] = (arg.description + " The value should be a base64-encoded string.").strip()
        else:
            schema_dict["description"] = "The value should be a base64-encoded string."
    if arg.optional:
        schema_dict["type"] = [schema_dict["type"], "null"]
    return schema_dict


def _enum_to_schema(ie: InterfaceEnum) -> Schema:
    kwargs: dict = {"type": "integer", "enum": [item.integer for item in ie.enum_items]}
    item_descriptions: list[str] = [f"JSON Value `{item.integer}` is `{item.name}` - {item.description or ''}" for item in ie.enum_items]
    if ie.documentation:
        item_descriptions.insert(0, ie.documentation)
    kwargs["description"] = "\n".join(item_descriptions)
    return Schema(**kwargs)


def _array_to_schema(arg: ArgArray) -> dict:
    if arg.element.arg_type == ArgType.ENUM:
        assert isinstance(arg.element, ArgEnum)
        item_schema: dict[str, Any] = {"$ref": f"#/components/schemas/{arg.element.enum.name}"}
    elif arg.element.arg_type == ArgType.STRUCT:
        assert isinstance(arg.element, ArgStruct)
        item_schema = {"$ref": f"#/components/schemas/{arg.element.interface_struct.name}"}
    elif arg.element.arg_type == ArgType.PRIMITIVE:
        assert isinstance(arg.element, ArgPrimitive)
        item_schema = _primitive_type_to_schema(arg.element)
    else:
        item_schema = _other_arg_to_schema(arg.element)
    array_schema: dict[str, Any] = {"type": "array", "items": item_schema}
    if arg.optional:
        array_schema["type"] = [array_schema["type"], "null"]
    if arg.description:
        array_schema["description"] = arg.description
    return array_schema


def _struct_to_schema(ist: InterfaceStruct) -> Schema:
    from stingeripc.arg_models import ArgEnum, ArgStruct, ArgPrimitive
    from stingeripc.args import ArgType

    properties: dict[str, dict] = {}
    required: list[str] = []
    for member in ist.members:
        if member.arg_type == ArgType.ENUM:
            assert isinstance(member, ArgEnum)
            if member.optional:
                prop: dict[str, Any] = {"anyOf": [{"$ref": f"#/components/schemas/{member.enum.name}"}, {"type": "null"}]}
            else:
                prop: dict[str, Any] = {"$ref": f"#/components/schemas/{member.enum.name}"}
        elif member.arg_type == ArgType.STRUCT:
            assert isinstance(member, ArgStruct)
            if member.optional:
                prop: dict[str, Any] = {"anyOf": [{"$ref": f"#/components/schemas/{member.interface_struct.name}"}, {"type": "null"}]}
            else:
                prop: dict[str, Any] = {"$ref": f"#/components/schemas/{member.interface_struct.name}"}
        elif member.arg_type == ArgType.PRIMITIVE:
            assert isinstance(member, ArgPrimitive)
            prop: dict[str, Any] = _primitive_type_to_schema(member)
        elif member.arg_type == ArgType.ARRAY:
            assert isinstance(member, ArgArray)
            prop: dict[str, Any] = _array_to_schema(member)
        else:
            prop: dict[str, Any] = _other_arg_to_schema(member)
        if member.description and "description" not in prop:
            prop["description"] = member.description
        properties[member.name] = prop
        if not member.optional:
            required.append(member.name)
    kwargs: dict[str, Any] = {"type": "object", "properties": properties}
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
        return _primitive_type_to_schema(arg)
    return {"type": "string"}


def _parameters_for_address(address: str, config: StingerConfig) -> models.channel.Parameters:
    params: dict = {}
    if "{service_id}" in address:
        params["service_id"] = {"$ref": "#/components/parameters/service_id"}
    if "{client_id}" in address:
        params["client_id"] = {"$ref": "#/components/parameters/client_id"}
    for topic_param in config.topics.params:
        if f"{{{topic_param}}}" in address:
            params[topic_param] = {"$ref": f"#/components/parameters/{topic_param}"}
    return models.channel.Parameters(root=params)


def _topic_template_to_regex(topic_template: str) -> str:
    """Convert a topic template into a regex where placeholders map to [^\}]+."""
    return re.sub(r"\{[^{}]+\}", r"[^\\}]+", topic_template)


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
    def __init__(self, signal: IpcSignal, config: StingerConfig):
        self.signal = signal
        self.config = config

    def get_payload_schema(self) -> Schema:
        return arg_list_to_schema(self.signal.arg_list)

    def get_message(self) -> models.Message:
        payload_schema = self.get_payload_schema()
        return models.Message(
            name=self.signal.name,
            summary=f"The message for the '{self.signal.name}' signal.",
            description=f"The payload represents the data for the signal.  It is encoded as a JSON object.",
            payload=payload_schema,
            contentType="application/json",
            bindings=MessageBindingsObject(mqtt=MQTTMessageBindings(contentType="application/json")),
        )

    def to_channel(self) -> models.Channel:
        message = self.get_message()
        address = self.signal.topic()
        return models.Channel(
            address=address,
            description=self.signal.documentation,
            messages=models.message.Messages(root={self.signal.name: message}),
            parameters=_parameters_for_address(address, self.config),
        )

    def to_operation(self) -> models.Operation:
        name = self.signal.name
        return models.Operation(
            summary=f"Receive the '{self.signal.name}' signal.",
            description=f"""
            The server publishes a message to the signal topic whenever the signal is emitted.
            Clients can subscribe to the signal topic to receive messages whenever the signal is emitted.

            ```plantuml
            Client -> MQTT Broker: Subscribe
            Server -> MQTT Broker: '{self.signal.name}' Signal
            MQTT Broker -> Client: '{self.signal.name}' Signal
            ```

            The message is not retained, so clients will only receive the signal message when the signal is emitted while they are subscribed.
            """,
            action="receive",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
            tags=[models.base.Tag(name="signal")],
        )


class AsyncApiMethodHelper:
    def __init__(self, method: IpcMethod, config: StingerConfig):
        self.method = method
        self.config = config

    def request_channel_name(self) -> str:
        return f"{self.method.name}_request"

    def response_channel_name(self) -> str:
        return f"{self.method.name}_response"

    def request_message_key(self) -> str:
        return f"{self.method.name}_request"

    def response_message_key(self) -> str:
        return self.method.return_value_name.replace(" ", "_")

    def get_request_message(self) -> models.Message:
        payload_schema = arg_list_to_schema(self.method.arg_list)
        response_topic_schema = _topic_template_to_regex(self.method.response_topic())
        return models.Message(
            name=self.request_message_key(),
            description="""The payload represents the arguments for the method call.  It is encoded as a JSON object.
            
            Correlation data must be provided as an MQTT property.  The data can be any binary data, but must be unique to this method.  Typically, using a UUID is sufficient to ensure uniqueness.  The server will include the same correlation data in the response message, so the client can match responses to requests when multiple requests are in-flight.
            
            A response topic must be provided as an MQTT property.  The server will publish the response message to the provided response topic.  The method-calling client must have a valid subscription to the MQTT response topic.
            """,
            payload=payload_schema,
            contentType="application/json",
            bindings=MessageBindingsObject(
                mqtt=MQTTMessageBindings(
                    contentType="application/json",
                    correlationData={"type": "string", "format": "uuid"},
                    responseTopic={"type": "string", "pattern": response_topic_schema},
                )
            ),
            tags=[models.base.Tag(name="method"), models.base.Tag(name="request")],
        )

    def request_to_channel(self) -> models.Channel:
        message = self.get_request_message()
        address = self.method.request_topic()
        return models.Channel(
            address=address,
            description=self.method.documentation,
            messages=models.message.Messages(root={self.request_message_key(): message}),
            parameters=_parameters_for_address(address, self.config),
        )

    def request_to_operation(self) -> models.Operation:
        name = self.request_channel_name()
        return models.Operation(
            action="send",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description="""
            A method may call one of the server's methods by publishing a message to the method's request topic.

            ```plantuml
            Client -> MQTT Broker: Method Request
            MQTT Broker -> Server: Method Request
            Server -> Server: Process method call
            Server -> MQTT Broker: Method Response
            MQTT Broker -> Client: Method Response
            ```
            """,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
            tags=[models.base.Tag(name="method"), models.base.Tag(name="request")],
            reply=models.OperationReply(channel=models.base.Reference(ref=f"#/channels/{self.response_channel_name()}")),
        )

    def get_response_message(self) -> models.Message:
        payload_schema = arg_list_to_schema(self.method.return_arg_list)
        return models.Message(
            name=self.method.return_value_name,
            description="""
            This payload represents the {% if self.method.return_arg_list | length > 1 %}return values{%elif self.method.return_arg_list | length == 1 %}return value{% else %}completion{% endif %} of the method call response.  It is encoded as a JSON object.
            
            A "correlation data" MQTT property will be included in the response message, and will match the correlation data provided in the request message, so the client can match responses to requests when multiple requests are in-flight.  Whatever binary data was provided as correlation data in the request will be provided as correlation data in the response.
            (Hint: any blob of data works, so you could include extra tracking information like a timestamp if you needed it).
            """,
            payload=payload_schema,
            contentType="application/json",
            bindings=MessageBindingsObject(mqtt=MQTTMessageBindings(contentType="application/json")),
            tags=[models.base.Tag(name="method"), models.base.Tag(name="response")],
        )

    def response_to_channel(self) -> models.Channel:
        response_key = self.response_message_key()
        message = self.get_response_message()
        address = self.method.response_topic()
        return models.Channel(
            address=address,
            description=self.method.documentation,
            messages=models.message.Messages(root={response_key: message}),
            parameters=_parameters_for_address(address, self.config),
        )

    def response_to_operation(self) -> models.Operation:
        name = self.response_channel_name()
        return models.Operation(
            action="receive",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description="""
            The server will publish a response message to the response topic provided in the request message.  The response message will contain the return value(s) of the method call.

            ```plantuml
            Client -> MQTT Broker: Method Request
            MQTT Broker -> Server: Method Request
            Server -> Server: Process method call
            Server -> MQTT Broker: Method Response
            MQTT Broker -> Client: Method Response
            ```
            """,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{self.response_message_key()}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
            tags=[models.base.Tag(name="method"), models.base.Tag(name="response")],
        )


class AsyncApiPropertyHelper:
    def __init__(self, prop: IpcProperty, config: StingerConfig):
        self.prop = prop
        self.config = config

    def value_channel_name(self) -> str:
        return f"{self.prop.name}_value"

    def update_request_channel_name(self) -> str:
        return f"{self.prop.name}_update_request"

    def update_response_channel_name(self) -> str:
        return f"{self.prop.name}_update_response"

    def payload_schema(self) -> Schema:
        return arg_list_to_schema(self.prop.arg_list)

    def _payload_ref(self) -> Schema:
        return Schema(**{"$ref": f"#/components/schemas/{self.prop.name}_property"})

    def get_value_message(self) -> models.Message:
        return models.Message(
            name=f"{upper_camel_case(self.prop.name)}PropertyValue",
            title=f"{self.prop.name} value",
            summary=f"The current value of the '{self.prop.name}' property.",
            description=f"""The payload represents the current value of the property.  It is encoded as a JSON object.

            The `PropertyValue` user property value (an integer provided as an MQTT string) is a version number that increments with each new value of the property.
            A client typically stores this value in order to provide it in update requests.
            """,
            payload=self._payload_ref(),
            contentType="application/json",
            bindings=MessageBindingsObject(mqtt=MQTTMessageBindings(contentType="application/json")),
            headers=Schema(
                type="object",
                properties={
                    "PropertyValue": {"type": "integer", "description": "An integer that increments with each new value of the property."},
                    "DebugInfo": {
                        "type": "string",
                        "description": "A optional (not likely to be provided) string that the client should log or print for debugging purposes.",
                    },
                },
                required=["PropertyValue"],
            ),
            tags=[models.base.Tag(name="property"), models.base.Tag(name="value")],
        )

    def get_request_message(self) -> models.Message:
        return models.Message(
            name=f"{upper_camel_case(self.prop.name)}UpdateRequest",
            summary=f"A request to update the '{self.prop.name}' property.",
            description="""The payload represents the new property value that the client wants to set.
            
                The entirety of the JSON object must be provided, and will completely replace the
                current value of the property if the update is accepted.
                
                The `PropertyVersion` user property value (a number provided as an MQTT string)
                should be the same `PropertyVersion` value that was most recently received.""",
            payload=self._payload_ref(),
            contentType="application/json",
            bindings=MessageBindingsObject(
                mqtt=MQTTMessageBindings(
                    contentType="application/json",
                    correlationData={"type": "string", "format": "uuid"},
                    responseTopic={"type": "string", "pattern": _topic_template_to_regex(self.prop.response_topic())},
                )
            ),
            headers=Schema(
                type="object",
                properties={
                    "PropertyValue": {
                        "type": "integer",
                        "description": "This is the current version of the property.  The version in the request must match the version of the property value for the update to be accepted.  This prevents lost updates when multiple clients are updating the same property.",
                    },
                },
                required=["PropertyValue"],
            ),
            tags=[models.base.Tag(name="property"), models.base.Tag(name="update"), models.base.Tag(name="request")],
        )

    def get_response_message(self) -> models.Message:
        return models.Message(
            name=f"{upper_camel_case(self.prop.name)}UpdateResponse",
            summary=f"The response after updating the '{self.prop.name}' property.",
            description="""The payload represents the latest value of the property after the update attempt.
            
            If the property update was successful, then there should be a `ReturnCode` user property with value `0`, and the payload should match the value that was sent in the update request.
            The `PropertyValue` user property will be the newest version of the property value after the update.
            The `DebugInfo` user property is usually empty or unset on success, but is not required to be empty.  If provided, the
            client should log or print the provided `DebugInfo` string for debugging purposes.

            If the property update was unsuccessful, then there should be a `ReturnCode` user property with a non-zero value, and the payload will contain the server's current value for the property.
            The `PropertyValue` user property will be the version of the current property value (which may or may not be what it was before).
            The `DebugInfo` user property should contain a string describing why the update was unsuccessful, and the client should log or print it for debugging purposes, but the client is not to specifically parse the `DebugInfo` for programatic meaning.
            """,
            payload=self._payload_ref(),
            contentType="application/json",
            bindings=MessageBindingsObject(
                mqtt=MQTTMessageBindings(
                    contentType="application/json",
                    correlationData={"type": "string", "format": "uuid"},
                )
            ),
            headers=Schema(
                type="object",
                properties={
                    "PropertyValue": {
                        "type": "integer",
                        "description": "This is the current version of the property.  The version in the request must match the version of the property value for the update to be accepted.  This prevents lost updates when multiple clients are updating the same property.",
                        "minimum": -1,
                    },
                    "ReturnCode": {
                        "type": "integer",
                        "description": " | ".join([f"{code.name}: {code.value}" for code in MethodReturnCode]),
                        "enum": [code.value for code in MethodReturnCode],
                    },
                    "DebugInfo": {
                        "type": "string",
                        "description": "A string describing why the update was unsuccessful, if applicable.",
                    },
                },
                required=["PropertyValue", "ReturnCode", "DebugInfo"],
            ),
            tags=[models.base.Tag(name="property"), models.base.Tag(name="update"), models.base.Tag(name="response")],
        )

    def value_to_channel(self) -> models.Channel:
        address = self.prop.value_topic()
        return models.Channel(
            title=f"{upper_camel_case(self.prop.name)}PropertyValue",
            summary=f"The current value of the '{self.prop.name}' property.",
            address=address,
            description=self.prop.documentation,
            messages=models.message.Messages(root={self.prop.name: self.get_value_message()}),
            parameters=_parameters_for_address(address, self.config),
            tags=[models.base.Tag(name="property"), models.base.Tag(name="value")],
        )

    def value_to_operation(self) -> models.Operation:
        name = self.value_channel_name()
        return models.Operation(
            title=f"Receive{upper_camel_case(self.prop.name)}PropertyValue",
            summary=f"Receive the current value of the '{self.prop.name}' property.",
            description=f"""
            Every time the property value changes, the server will publish the current property value to MQTT.
            It publishes with a retain=true flag, so that clients can receive the current property value immediately upon subscribing.
            Clients can subscribe to the value topic to receive the current property value and be notified of changes to the property value.

            ```plantuml
            Server -> MQTT Broker: '{self.prop.name}' Value (retain=true)
            Client -> MQTT Broker: Subscribe
            MQTT Broker -> Client: '{self.prop.name}' Value
            ```
            """,
            action="receive",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{self.prop.name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
            tags=[models.base.Tag(name="property"), models.base.Tag(name="value")],
        )

    def update_request_to_channel(self) -> models.Channel:
        address = self.prop.update_topic()
        return models.Channel(
            title=f"{upper_camel_case(self.prop.name)}UpdateRequest",
            summary=f"A request to update the '{self.prop.name}' property.",
            description=self.prop.documentation,
            address=address,
            messages=models.message.Messages(root={self.prop.name: self.get_request_message()}),
            parameters=_parameters_for_address(address, self.config),
        )

    def update_request_to_operation(self) -> models.Operation:
        name = self.update_request_channel_name()
        address = self.prop.update_topic()
        return models.Operation(
            action="send",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description=f"""
            A client publishes to this topic in order to request that the server updates the property value to provided value.

            The server will respond with a message on the response topic indicating whether the update was successful, and what the new property value is after the update attempt.

            ```plantuml
            Server -> MQTT Broker: Subscribe to {address}
            Client -> MQTT Broker: Update Request
            MQTT Broker -> Server:  Update Request
            Server -> Server: Update property value
            Server -> MQTT Broker: New Property Value
            MQTT Broker -> Client: New Property Value
            Server -> MQTT Broker: Property Update Response
            MQTT Broker -> Client: Property Update Response
            ```
            """,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{self.prop.name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
            tags=[models.base.Tag(name="property")],
            reply=models.OperationReply(channel=models.base.Reference(ref=f"#/channels/{self.update_response_channel_name()}")),
        )

    def update_response_to_channel(self) -> models.Channel:
        address = self.prop.response_topic()
        return models.Channel(
            title=f"{upper_camel_case(self.prop.name)}UpdateResponse",
            summary=f"A response to the update request for the '{self.prop.name}' property.",
            address=address,
            description=self.prop.documentation,
            messages=models.message.Messages(root={self.prop.name: self.get_response_message()}),
            parameters=_parameters_for_address(address, self.config),
        )

    def update_response_to_operation(self) -> models.Operation:
        name = self.update_response_channel_name()
        address = self.prop.update_topic()
        return models.Operation(
            action="receive",
            channel=models.base.Reference(ref=f"#/channels/{name}"),
            description=f"""
            A server publishes to this topic in order to provide the response to an update request.

            The server will respond with a message on the response topic indicating whether the update was successful, and what the new property value is after the update attempt.

            ```plantuml
            Server -> MQTT Broker: Subscribe to {address}
            Client -> MQTT Broker: Update Request
            MQTT Broker -> Server:  Update Request
            Server -> Server: Update property value
            Server -> MQTT Broker: New Property Value
            MQTT Broker -> Client: New Property Value
            Server -> MQTT Broker: Property Update Response
            MQTT Broker -> Client: Property Update Response
            ```

            If the update failed, the most recent property value will be included in the response payload, 
            and the client should update its local cached property value to match the value in the response, 
            as that is the current value of the property on the server.
            """,
            messages=[models.base.Reference(ref=f"#/channels/{name}/messages/{self.prop.name}")],
            bindings=OperationBindingsObject(mqtt=MQTTOperationBindings(qos=2, retain=False)),
            tags=[models.base.Tag(name="property")],
        )


def stinger_to_asyncapi(spec: StingerSpec, config: StingerConfig | None = None) -> dict:
    """Convert a StingerSpec to an AsyncAPI 3.0 specification dict."""
    config_obj = config or StingerConfig()

    schemas: dict[str, Schema] = {}
    for enum_name, ie in spec.enums.items():
        schemas[enum_name] = _enum_to_schema(ie)
    for struct_name, ist in spec.structs.items():
        schemas[struct_name] = _struct_to_schema(ist)

    channels: dict[str, models.Channel] = {}
    operations: dict[str, models.Operation] = {}
    for name, signal in spec.signals.items():
        signal_helper = AsyncApiSignalHelper(signal, config_obj)
        channels[name] = signal_helper.to_channel()
        operations[name] = signal_helper.to_operation()
    for method_name, method in spec.methods.items():
        method_helper = AsyncApiMethodHelper(method, config_obj)
        channels[method_helper.request_channel_name()] = method_helper.request_to_channel()
        operations[method_helper.request_channel_name()] = method_helper.request_to_operation()
        channels[method_helper.response_channel_name()] = method_helper.response_to_channel()
        operations[method_helper.response_channel_name()] = method_helper.response_to_operation()
    for prop_name, prop in spec.properties.items():
        prop_helper = AsyncApiPropertyHelper(prop, config_obj)
        schemas[f"{prop.name}_property"] = prop_helper.payload_schema()
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
            tags=[
                models.base.Tag(name="signal"),
                models.base.Tag(name="method"),
                models.base.Tag(name="property"),
            ],
        ),
        components=models.Components(
            schemas=Schemas(root=schemas) if schemas else None,
        ),
        channels=models.Channels(root=channels) if channels else None,
        operations=models.operation.Operations(root=operations) if operations else None,
    )

    component_parameters: dict[str, models.Parameter] = {
        "service_id": models.Parameter(description="The ID of the service/instance"),
        "client_id": models.Parameter(description="The MQTT Client ID"),
    }
    for topic_param in config_obj.topics.params:
        if topic_param not in component_parameters:
            component_parameters[topic_param] = models.Parameter(description=f"Topic parameter '{topic_param}'")

    aa.components.parameters = models.channel.Parameters(root=component_parameters)

    return json.loads(aa.model_dump_json(exclude_none=True))
