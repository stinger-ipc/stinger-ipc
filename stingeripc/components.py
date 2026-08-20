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
from .args import ArgPrimitiveType, ArgType
from .exceptions import InvalidConfiguration, InvalidStingerStructure
from .lang_symb import *
from .exceptions import InvalidStingerStructure, InvalidConfiguration
from jacobsjinjatoo import stringmanip
from pydantic import BaseModel, ConfigDict, PrivateAttr
from stingeripc.arg_models import (
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
from stingeripc.arg_datatypes import InterfaceConstant, InterfaceEnum, InterfaceStruct


class InterfaceComponent(BaseModel):
    """Base class for the elements of an interface: signals, methods, and properties.

    Every interface component has a unique ``name`` within the interface and an
    optional human-readable ``documentation`` string.  Instances also hold a
    reference to the owning :class:`StingerSpec` (``_root``) and its
    :class:`StingerConfig` (``_config``) so that derived classes can compute
    topics and other configurable values lazily.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    name: str
    documentation: Optional[str] = None
    _config: Any = PrivateAttr()
    _root: Any = PrivateAttr()

    def __init__(self, name: str, root: "StingerSpec"):
        super().__init__(name=name)
        self._config = root._config
        self._root = root

    def set_documentation(self, documentation: str) -> "InterfaceComponent":
        """Set the documentation string for this component and return self.

        Assigning documentation in a fluent style lets callers chain the call
        without a separate assignment step.
        """
        self.documentation = documentation
        return self

    def try_set_documentation_from_spec(self, spec: dict[str, Any]) -> "InterfaceComponent":
        """Set ``documentation`` from a parsed interface spec dict if present.

        If ``spec`` contains a string ``documentation`` key it is stored on the
        component; otherwise the existing value is left unchanged.
        """
        if "documentation" in spec and isinstance(spec["documentation"], str):
            self.documentation = spec["documentation"]
        return self


class StingerSpec:
    """Root model of a parsed Stinger IPC interface.

    Holds the interface metadata (name, version, title, summary, documentation,
    license) and the collections of signals, methods, properties, enums,
    structs, and constants defined by the interface.  It also exposes the
    helpers used by the templates to compute topics and answer feature
    questions (e.g. whether the interface uses enums, binary payloads, or JSON
    schema constraints).
    """

    def __init__(self, interface: dict[str, Any], config: StingerConfig):
        LanguageSymbolMixin.enhance(self, config)
        self._config = config
        try:
            self._name: str = interface["name"]
            self._version: str = interface["version"]
        except KeyError as e:
            raise InvalidStingerStructure(f"Missing interface property in {interface}: {e}")
        except TypeError:
            raise InvalidStingerStructure(f"Interface didn't appear to have a correct type")

        assert isinstance(config, StingerConfig), f"Config must be a StingerConfig object. Got {type(config)}"
        assert isinstance(config.topics, TopicConfig), f"Config must have a TopicConfig object in its 'topics' property. Got {type(config.topics)}"

        if not topic_util.is_valid_topic_template(self._config.topics.interface_discovery, self._config.topics.params):
            raise InvalidConfiguration(f"Interface discovery topic template '{self._config.topics.interface_discovery}' is not valid. ")

        self._summary = interface.get("summary")
        self._title = interface.get("title")
        self._documentation = interface.get("documentation")
        self._license = interface.get("license")

        self.signals: dict[str, IpcSignal] = {}
        self.properties: dict[str, IpcProperty] = {}
        self.methods: dict[str, IpcMethod] = {}
        self.enums: dict[str, InterfaceEnum] = {}
        self.structs: dict[str, InterfaceStruct] = {}
        self.constants: dict[str, InterfaceConstant] = {}
        self._spec_version: Optional[str] = None

    @property
    def method_return_codes(self) -> dict[int, str]:
        """Mapping of method return code integers to their human-readable names.

        Used by the generated code to render the method return code enum and to
        document what each code means.
        """
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
        """Return the topic used by servers to advertise the interface.

        The topic is derived from the configured ``interface_discovery`` topic
        template, with the interface name filled in.
        """
        topic_template = self._config.topics.interface_discovery
        topic_template = topic_util.topic_template_fill_in(topic_template, interface_name=self.name)
        return topic_template

    @property
    def summary(self) -> str:
        """One-line summary of the interface, or an empty string if not set."""
        return self._summary or ""

    @property
    def title(self) -> str:
        """Title of the interface, falling back to its name if not set."""
        return self._title or self._name or ""

    @property
    def documentation(self) -> str:
        """Full documentation string for the interface, or an empty string if not set."""
        return self._documentation or ""

    @property
    def license(self) -> str:
        """License text declared for the interface, or an empty string if not set."""
        return self._license or ""

    def add_signal(self, signal: IpcSignal):
        """Register a signal on the interface, keyed by its name."""
        from stingeripc.ipc_signal import IpcSignal

        assert isinstance(signal, IpcSignal)
        self.signals[signal.name] = signal

    def add_method(self, method: IpcMethod):
        """Register a method on the interface, keyed by its name."""
        from stingeripc.ipc_method import IpcMethod

        assert isinstance(method, IpcMethod)
        self.methods[method.name] = method

    def add_property(self, prop: IpcProperty):
        """Register a property on the interface, keyed by its name."""
        from stingeripc.ipc_property import IpcProperty

        assert isinstance(prop, IpcProperty)
        self.properties[prop.name] = prop

    @property
    def properties_rw(self) -> dict[str, IpcProperty]:
        """The subset of properties that are read/write (not read-only)."""
        return {k: v for k, v in self.properties.items() if not v.read_only}

    def add_enum(self, interface_enum: InterfaceEnum):
        """Register an enum on the interface, keyed by its name."""
        assert interface_enum is not None
        self.enums[interface_enum.name] = interface_enum

    def add_struct(self, interface_struct: InterfaceStruct):
        """Register a struct on the interface, keyed by its name."""
        assert interface_struct is not None
        self.structs[interface_struct.name] = interface_struct

    def add_constant(self, interface_constant: InterfaceConstant):
        """Register a constant on the interface, keyed by its name."""
        assert interface_constant is not None
        self.constants[interface_constant.name] = interface_constant

    def uses_enums(self) -> bool:
        """Return True if the interface declares any enums."""
        return bool(self.enums)

    def uses_schemas(self) -> bool:
        """True if any argument anywhere in the interface declares a JSON schema constraint."""
        return any(arg.value_schema for arg in self._all_args())

    def _all_args(self) -> list["Arg"]:
        """Flat list of every argument that appears anywhere in the interface.

        Struct values and array element types are included recursively so that
        callers can reason about the full set of data types actually used.
        """
        top_level: list["Arg"] = []
        for signal in self.signals.values():
            top_level += signal.arg_list
        for prop in self.properties.values():
            top_level += prop.arg_list
        for method in self.methods.values():
            top_level += method.arg_list + method.return_arg_list
        for struct in self.structs.values():
            top_level += struct.values

        collected: list["Arg"] = []
        stack = list(top_level)
        while stack:
            arg = stack.pop()
            collected.append(arg)
            element = getattr(arg, "element", None)
            if element is not None:
                stack.append(element)
            values = getattr(arg, "values", None)
            if values is not None:
                stack.extend(values)
        return collected

    def _uses_arg_type(self, arg_type: ArgType) -> bool:
        """Return True if any argument anywhere in the interface uses the given arg type."""
        return any(arg.arg_type == arg_type for arg in self._all_args())

    def uses_binary(self) -> bool:
        """True if any argument anywhere in the interface is a binary field."""
        return self._uses_arg_type(ArgType.BINARY)

    def uses_datetime(self) -> bool:
        """True if any argument anywhere in the interface is a datetime field."""
        return self._uses_arg_type(ArgType.DATETIME)

    def uses_duration(self) -> bool:
        """True if any argument anywhere in the interface is a duration field."""
        return self._uses_arg_type(ArgType.DURATION)

    def get_interface_enum(self, name: str) -> InterfaceEnum:
        """Return the enum registered under `name`, or raise if it is unknown."""
        if name in self.enums:
            return self.enums[name]
        raise InvalidStingerStructure(f"Enum '{name}' not found in stinger spec")

    @property
    def name(self):
        """Name of the interface."""
        return self._name

    @property
    def version(self):
        """Version of the interface as a dotted string (e.g. '1.2.3')."""
        return self._version

    @property
    def spec_version(self) -> Optional[str]:
        """The stingeripc schema/format version this spec was loaded from (e.g. '0.2.0')."""
        return self._spec_version

    @property
    def signal_qos(self) -> int:
        """QoS level used when publishing/subscribing to signal topics."""
        return 2

    @property
    def method_request_qos(self) -> int:
        """QoS level used when publishing method request messages."""
        return 2

    def all_methods_response_topic(self) -> str:
        """Return the topic template that matches responses for every method.

        The `method_name` placeholder is replaced with the MQTT wildcard `+`
        so a single subscription receives responses for all methods.
        """
        topic_template = self._config.topics.method_responses
        topic_template = topic_util.topic_template_fill_in(topic_template, interface_name=self.name, method_name="+")
        return topic_template

    @property
    def method_response_qos(self) -> int:
        """QoS level used when publishing method response messages."""
        return 1

    @property
    def property_value_qos(self) -> int:
        """QoS level used when publishing property value messages."""
        return 1

    @property
    def property_update_qos(self) -> int:
        """QoS level used when publishing property update messages."""
        return 1

    def all_properties_response_topic(self) -> str:
        """Return the topic template that matches update responses for every property.

        The `property_name` placeholder is replaced with the MQTT wildcard
        `+` so a single subscription receives responses for all properties.
        """
        topic_template = self._config.topics.property_update_responses
        topic_template = topic_util.topic_template_fill_in(topic_template, interface_name=self.name, property_name="+")
        return topic_template

    @property
    def property_response_qos(self) -> int:
        """QoS level used when publishing property update response messages."""
        return 1

    def all_properties_value_topic(self) -> str:
        """Return the topic template that matches value messages for every property.

        The ``property_name`` placeholder is replaced with the MQTT wildcard
        ``+`` so a single subscription receives values for all properties.
        """
        topic_template = self._config.topics.property_values
        topic_template = topic_util.topic_template_fill_in(topic_template, interface_name=self.name, property_name="+")
        return topic_template

    def all_signals_topic(self) -> str:
        """Return the topic template that matches messages for every signal.

        The ``signal_name`` placeholder is replaced with the MQTT wildcard ``+``
        so a single subscription receives all signals.
        """
        topic_template = self._config.topics.signals
        topic_template = topic_util.topic_template_fill_in(topic_template, interface_name=self.name, signal_name="+")
        return topic_template

    @classmethod
    def new_spec_from_stinger(cls, stinger: dict[str, Any], config: StingerConfig) -> StingerSpec:
        """Construct a fully populated StingerSpec from a parsed Stinger YAML dict.

        Validates the declared format version, then builds the enums, structs,
        constants, signals, methods, and properties in dependency order (enums
        and structs first because other elements may reference them).
        """
        if "stingeripc" not in stinger:
            raise InvalidStingerStructure("Missing 'stingeripc' format version")
        if "version" not in stinger["stingeripc"]:
            raise InvalidStingerStructure("Stinger spec version not present")
        if stinger["stingeripc"]["version"] not in ["0.3.0"]:
            raise InvalidStingerStructure(f"Unsupported stinger spec version {stinger['stingeripc']['version']}")

        stinger_spec = StingerSpec(stinger["interface"], config)
        stinger_spec._spec_version = stinger["stingeripc"]["version"]

        from stingeripc.ipc_signal import IpcSignal
        from stingeripc.ipc_method import IpcMethod
        from stingeripc.ipc_property import IpcProperty

        # Enums must come before other components because other components may use enum values.
        try:
            if "enums" in stinger:
                for enum_name, enum_spec in stinger["enums"].items():
                    ie = InterfaceEnum.new_enum_from_stinger(enum_name, enum_spec)
                    assert ie is not None, f"Did not create enum from {enum_name} and {enum_spec}"
                    stinger_spec.add_enum(ie)
        except TypeError as e:
            raise InvalidStingerStructure(f"Signal specification appears to be invalid: {e}")

        try:
            if "structures" in stinger:
                for struct_name, struct_spec in stinger["structures"].items():
                    istruct = InterfaceStruct.new_struct_from_stinger(struct_name, struct_spec, stinger_spec)
                    assert istruct is not None, f"Did not create struct from {struct_name} and {struct_spec}"
                    stinger_spec.add_struct(istruct)
        except TypeError as e:
            raise InvalidStingerStructure(f"Struct specification appears to be invalid: {e}")

        try:
            if "constants" in stinger:
                for const_name, const_spec in stinger["constants"].items():
                    ic = InterfaceConstant.new_constant_from_stinger(const_name, const_spec)
                    assert ic is not None, f"Did not create constant from {const_name} and {const_spec}"
                    stinger_spec.add_constant(ic)
        except TypeError as e:
            raise InvalidStingerStructure(f"Constant specification appears to be invalid: {e}")

        try:
            if "signals" in stinger:
                for signal_name, signal_spec in stinger["signals"].items():
                    signal = IpcSignal.new_signal_from_stinger(
                        signal_name,
                        signal_spec,
                        stinger_spec,
                    )
                    assert signal is not None, f"Did not create signal from {signal_name} and {signal_spec}"
                    stinger_spec.add_signal(signal)
        except TypeError as e:
            raise InvalidStingerStructure(f"Signal specification appears to be invalid: {e}")

        try:
            if "methods" in stinger:
                for method_name, method_spec in stinger["methods"].items():
                    method = IpcMethod.new_method_from_stinger(
                        method_name,
                        method_spec,
                        stinger_spec,
                    )
                    assert method is not None, f"Did not create method from {method_name} and {method_spec}"
                    stinger_spec.add_method(method)
        except TypeError as e:
            raise InvalidStingerStructure(f"Method specification appears to be invalid: {e}")

        try:
            if "properties" in stinger:
                for prop_name, prop_spec in stinger["properties"].items():
                    prop = IpcProperty.new_property_from_stinger(
                        prop_name,
                        prop_spec,
                        stinger_spec,
                    )
                    assert prop is not None, f"Did not create property from {prop_name} and {prop_spec}"
                    stinger_spec.add_property(prop)
        except TypeError as e:
            raise InvalidStingerStructure(f"Property specification appears to be invalid: {e}")

        return stinger_spec
