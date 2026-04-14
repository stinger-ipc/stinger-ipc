from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, TYPE_CHECKING

from stingeripc.config import StingerConfig, TopicConfig

if TYPE_CHECKING:
    from stingeripc.ipc_signal import IpcSignal
    from stingeripc.ipc_method import IpcMethod
    from stingeripc.ipc_property import IpcProperty

from . import topic_util
from .lang_symb import *
from .exceptions import InvalidStingerStructure, InvalidConfiguration
from jacobsjinjatoo import stringmanip
from pydantic import BaseModel
from stingeripc.arg_models import (
    LanguageSymbolMixin,
    YamlArg,
    YamlArgList,
    YamlIfaceEnum,
    YamlIfaceEnums,
    YamlIfaceProperty,
    RESTRICTED_NAMES,
    Arg,
    ArgEnum,
    ArgPrimitive,
    ArgStruct,
    ArgDateTime,
    ArgDuration,
    ArgBinary,
    ArgArray,
)




class InterfaceComponent:

    def __init__(self, name: str, root: StingerSpec):
        self._name = name
        self._documentation: Optional[str] = None
        self._config = root._config
        self._root = root

    @property
    def name(self) -> str:
        return self._name

    @property
    def documentation(self) -> str | None:
        return self._documentation

    def set_documentation(self, documentation: str) -> InterfaceComponent:
        self._documentation = documentation
        return self

    def try_set_documentation_from_spec(
        self, spec: dict[str, Any]
    ) -> InterfaceComponent:
        if "documentation" in spec and isinstance(spec["documentation"], str):
            self._documentation = spec["documentation"]
        return self





class InterfaceEnum(LanguageSymbolMixin):

    @dataclass
    class EnumItem:
        name: str
        integer: int
        description: Optional[str] = None

    def __init__(self, name: str):
        LanguageSymbolMixin.__init__(self)
        self._name = name
        self._items: list[InterfaceEnum.EnumItem] = []
        self._documentation: Optional[str] = None

    def add_item(self, value: str, integer: Optional[int] = None, description: Optional[str] = None):
        integer_value = integer if integer is not None else ((max([i.integer for i in self._items]) + 1) if len(self._items) > 0 else 1)
        item = InterfaceEnum.EnumItem(name=value, integer=integer_value, description=description)
        self._items.append(item)

    def has_value(self, integer: int) -> bool:
        for item in self._items:
            if item.integer == integer:
                return True
        return False

    @property
    def name(self):
        return self._name

    @property
    def documentation(self) -> str | None:
        return self._documentation

    @property
    def class_name(self):
        return stringmanip.upper_camel_case(self.name)

    @property
    def items(self) -> list[EnumItem]:
        if self.has_value(0) and self._items[0].integer != 0:
            # Rearrange so that the item with integer value 0 is first. This is because .proto files require an initial 0-value.
            rearranged_items = [item for item in self._items if item.integer == 0]
            rearranged_items.extend([item for item in self._items if item.integer != 0])
            return rearranged_items
        else:
            return self._items

    @classmethod
    def new_enum_from_stinger(cls, name, enum_spec: YamlIfaceEnum) -> InterfaceEnum:
        ie = cls(name)
        for enum_obj in enum_spec.get("values", []):
            assert isinstance(enum_obj, dict), f"Enum values must be a dicts."
            if "name" in enum_obj and isinstance(enum_obj["name"], str):
                value_description = enum_obj.get("description", None)
                if value_description is not None and not isinstance(value_description, str):
                    raise InvalidStingerStructure(
                        f"InterfaceEnum '{name}' item descriptions must be strings."
                    )
                value_integer = enum_obj.get("value", None)
                if value_integer is not None and not isinstance(value_integer, int):
                    raise InvalidStingerStructure(
                        f"InterfaceEnum '{name}' item values must be integers."
                    )
                if value_integer is not None and ie.has_value(value_integer):
                    raise InvalidStingerStructure(
                        f"InterfaceEnum '{name}' already has an item with value {value_integer}."
                    )
                ie.add_item(enum_obj["name"], integer=value_integer, description=value_description)
            else:
                raise InvalidStingerStructure(
                    f"InterfaceEnum '{name}' items must have string names."
                )
        doc = enum_spec.get("documentation", None)
        if doc is not None and isinstance(doc, str):
            ie._documentation = doc
        return ie


class InterfaceStruct(LanguageSymbolMixin):

    def __init__(self, name: str):
        LanguageSymbolMixin.__init__(self)
        self._name = name
        self._members: list[Arg] = []
        self._documentation: Optional[str] = None

    def add_member(self, arg: Arg):
        self._members.append(arg)

    @property
    def name(self):
        return self._name

    @property
    def documentation(self) -> str | None:
        return self._documentation

    @property
    def class_name(self):
        return stringmanip.upper_camel_case(self.name)

    @property
    def values(self) -> list[Arg]:
        return self._members

    @property
    def members(self) -> list[Arg]:
        return self._members

    @classmethod
    def new_struct_from_stinger(
        cls,
        name,
        spec: dict[str, str | list[dict[str, str]]],
        stinger_spec: StingerSpec,
    ) -> InterfaceStruct:
        istruct = cls(name)
        for memb in spec.get("members", []):
            if not isinstance(memb, dict):
                raise InvalidStingerStructure("Struct members must be dicts")
            arg = Arg.new_arg_from_stinger(memb, stinger_spec=stinger_spec)
            istruct.add_member(arg)
        documentation = spec.get("documentation", None)
        if documentation is not None and not isinstance(documentation, str):
            raise InvalidStingerStructure("Struct documentation must be a string")
        istruct._documentation = documentation
        return istruct

    def __str__(self) -> str:
        return f"<InterfaceStruct members={[m.name for m in self.members]}>"

    def __repr__(self):
        return f"InterfaceStruct(name={self.name})"


class StingerSpec(LanguageSymbolMixin):

    def __init__(self, interface: dict[str, Any], config: StingerConfig):
        LanguageSymbolMixin.__init__(self, config)
        self._config = config
        try:
            self._name: str = interface["name"]
            self._version: str = interface["version"]
        except KeyError as e:
            raise InvalidStingerStructure(
                f"Missing interface property in {interface}: {e}"
            )
        except TypeError:
            raise InvalidStingerStructure(
                f"Interface didn't appear to have a correct type"
            )

        assert isinstance(config, StingerConfig), f"Config must be a StingerConfig object. Got {type(config)}"
        assert isinstance(config.topics, TopicConfig), f"Config must have a TopicConfig object in its 'topics' property. Got {type(config.topics)}"

        if not topic_util.is_valid_topic_template(self._config.topics.interface_discovery, self._config.topics.params):
            raise InvalidConfiguration(
                f"Interface discovery topic template '{self._config.topics.interface_discovery}' is not valid. "
            )

        self._summary = interface.get("summary")
        self._title = interface.get("title")
        self._documentation = interface.get("documentation")

        self.signals: dict[str, IpcSignal] = {}
        self.properties: dict[str, IpcProperty] = {}
        self.methods: dict[str, IpcMethod] = {}
        self.enums: dict[str, InterfaceEnum] = {}
        self.structs: dict[str, InterfaceStruct] = {}

    @property
    def method_return_codes(self) -> dict[int, str]:
        return {
            0: "Success",
            1: "Client Error",
            2: "Server Error",
            3: "Transport Error",
            4: "Payload Error",
            5: "Client Serialization Error",
            6: "Client Deserialization Error",
            7: "Server Serialization Error",
            8: "Server Deserialization Error",
            9: "Method Not Found",
            10: "Unauthorized",
            11: "Timeout",
            12: "OutOfSync",
            13: "Unknown Error",
            14: "Not Implemented",
            15: "Service Unavailable",
        }

    def interface_info_topic(self) -> str:
        topic_template = self._config.topics.interface_discovery
        topic_template = topic_util.topic_template_fill_in(topic_template, interface_name=self.name)
        return topic_template

    @property
    def summary(self) -> str:
        return self._summary or ""
    
    @property
    def title(self) -> str:
        return self._title or self._name or ""
    
    @property
    def documentation(self) -> str:
        return self._documentation or ""

    def add_signal(self, signal: IpcSignal):
        from stingeripc.ipc_signal import IpcSignal
        assert isinstance(signal, IpcSignal)
        self.signals[signal.name] = signal

    def add_method(self, method: IpcMethod):
        from stingeripc.ipc_method import IpcMethod
        assert isinstance(method, IpcMethod)
        self.methods[method.name] = method

    def add_property(self, prop: IpcProperty):
        from stingeripc.ipc_property import IpcProperty
        assert isinstance(prop, IpcProperty)
        self.properties[prop.name] = prop

    @property
    def properties_rw(self) -> dict[str, IpcProperty]:
        return {k: v for k, v in self.properties.items() if not v.read_only}

    def add_enum(self, interface_enum: InterfaceEnum):
        assert interface_enum is not None
        self.enums[interface_enum.name] = interface_enum

    def add_struct(self, interface_struct: InterfaceStruct):
        assert interface_struct is not None
        self.structs[interface_struct.name] = interface_struct

    def uses_enums(self) -> bool:
        return bool(self.enums)

    def get_interface_enum(self, name: str) -> InterfaceEnum:
        if name in self.enums:
            return self.enums[name]
        raise InvalidStingerStructure(f"Enum '{name}' not found in stinger spec")

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def signal_qos(self) -> int:
        return 2

    @property
    def method_request_qos(self) -> int:
        return 2

    def all_methods_response_topic(self) -> str:
        topic_template = self._config.topics.method_responses
        topic_template = topic_util.topic_template_fill_in(topic_template, interface_name=self.name, method_name="+")
        return topic_template

    @property
    def method_response_qos(self) -> int:
        return 1

    @property
    def property_value_qos(self) -> int:
        return 1
    
    @property
    def property_update_qos(self) -> int:
        return 1

    def all_properties_response_topic(self) -> str:
        topic_template = self._config.topics.property_update_responses
        topic_template = topic_util.topic_template_fill_in(topic_template, interface_name=self.name, property_name="+")
        return topic_template

    @property
    def property_response_qos(self) -> int:
        return 1

    def all_properties_value_topic(self) -> str:
        topic_template = self._config.topics.property_values
        topic_template = topic_util.topic_template_fill_in(topic_template, interface_name=self.name, property_name="+")
        return topic_template

    @classmethod
    def new_spec_from_stinger(
        cls, stinger: dict[str, Any], config: StingerConfig
    ) -> StingerSpec:
        if "stingeripc" not in stinger:
            raise InvalidStingerStructure("Missing 'stingeripc' format version")
        if "version" not in stinger["stingeripc"]:
            raise InvalidStingerStructure("Stinger spec version not present")
        if stinger["stingeripc"]["version"] not in ["0.0.7", "0.1.0"]:
            raise InvalidStingerStructure(
                f"Unsupported stinger spec version {stinger['stingeripc']['version']}"
            )

        stinger_spec = StingerSpec(stinger["interface"], config)

        from stingeripc.ipc_signal import IpcSignal
        from stingeripc.ipc_method import IpcMethod
        from stingeripc.ipc_property import IpcProperty

        # Enums must come before other components because other components may use enum values.
        try:
            if "enums" in stinger:
                for enum_name, enum_spec in stinger["enums"].items():
                    ie = InterfaceEnum.new_enum_from_stinger(enum_name, enum_spec)
                    assert (
                        ie is not None
                    ), f"Did not create enum from {enum_name} and {enum_spec}"
                    stinger_spec.add_enum(ie)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Signal specification appears to be invalid: {e}"
            )

        try:
            if "structures" in stinger:
                for struct_name, struct_spec in stinger["structures"].items():
                    istruct = InterfaceStruct.new_struct_from_stinger(
                        struct_name, struct_spec, stinger_spec
                    )
                    assert (
                        istruct is not None
                    ), f"Did not create struct from {struct_name} and {struct_spec}"
                    stinger_spec.add_struct(istruct)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Struct specification appears to be invalid: {e}"
            )

        try:
            if "signals" in stinger:
                for signal_name, signal_spec in stinger["signals"].items():
                    signal = IpcSignal.new_signal_from_stinger(
                        signal_name,
                        signal_spec,
                        stinger_spec,
                    )
                    assert (
                        signal is not None
                    ), f"Did not create signal from {signal_name} and {signal_spec}"
                    stinger_spec.add_signal(signal)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Signal specification appears to be invalid: {e}"
            )

        try:
            if "methods" in stinger:
                for method_name, method_spec in stinger["methods"].items():
                    method = IpcMethod.new_method_from_stinger(
                        method_name,
                        method_spec,
                        stinger_spec,
                    )
                    assert (
                        method is not None
                    ), f"Did not create method from {method_name} and {method_spec}"
                    stinger_spec.add_method(method)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Method specification appears to be invalid: {e}"
            )

        try:
            if "properties" in stinger:
                for prop_name, prop_spec in stinger["properties"].items():
                    prop = IpcProperty.new_property_from_stinger(
                        prop_name,
                        prop_spec,
                        stinger_spec,
                    )
                    assert (
                        prop is not None
                    ), f"Did not create property from {prop_name} and {prop_spec}"
                    stinger_spec.add_property(prop)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Property specification appears to be invalid: {e}"
            )

        return stinger_spec
