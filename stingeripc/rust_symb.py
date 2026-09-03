from typing import Any

from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.config import StingerConfig
from stingeripc.lang_symb import ISymbolsProvider


class RustSymbolsProvider(ISymbolsProvider):
    """Plugin that provides Rust symbols for model objects.

    Registers as the ``rust`` language domain so templates can access Rust
    names and types via ``obj.rust.<property>``.
    """

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "ProtobufMessageRef":
            return RustProtobufRefSymbols(model)
        elif model_class_name == "Payload":
            return RustPayloadSymbols(model)
        elif model_class_name == "StingerSpec":
            return RustInterfaceSymbols(model, self.config)
        elif model_class_name == "InterfaceEnum":
            return RustEnumSymbols(model)
        elif model_class_name == "InterfaceStruct":
            return RustStructSymbols(model)
        elif model_class_name == "IpcMethod":
            return RustMethodSymbols(model)
        elif model_class_name == "IpcCommand":
            return RustCommandSymbols(model)
        elif model_class_name == "IpcProperty":
            return RustPropertySymbols(model)
        elif model_class_name == "ArgEnum":
            return RustArgEnumSymbols(model)
        elif model_class_name == "ArgPrimitive":
            return RustArgPrimitiveSymbols(model)
        elif model_class_name == "ArgStruct":
            return RustArgStructSymbols(model)
        elif model_class_name == "ArgDateTime":
            return RustArgDateTimeSymbols(model)
        elif model_class_name == "ArgDuration":
            return RustArgDurationSymbols(model)
        elif model_class_name == "ArgBinary":
            return RustArgBinarySymbols(model)
        elif model_class_name == "ArgArray":
            return RustArgArraySymbols(model)
        elif model_class_name == "InterfaceConstant":
            return RustConstantSymbols(model)
        return None


class RustSymbols:
    """Base class for Rust symbol providers.

    Holds the generation ``config`` (used to derive package names and
    suffixes) shared by Rust symbol classes.
    """

    def __init__(self, config: StingerConfig | None = None):
        self.config = config


class RustInterfaceSymbols(RustSymbols):
    """Rust symbols for the top-level :class:`StingerSpec` (the interface)."""

    def __init__(self, interface, config: StingerConfig | None = None):
        super().__init__(config)
        self._iface = interface

    @property
    def package_name(self) -> str:
        """Name of the rust package for the interface client."""
        s = f"{stringmanip.snake_case(self._iface.name)}_{stringmanip.snake_case(self.config.rust.package_suffix) or 'ipc'}"  # type: ignore[union-attr]
        return s

    @property
    def client_struct_name(self) -> str:
        """Name of the rust struct for the interface client."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Client"

    @property
    def server_struct_name(self) -> str:
        """Name of the struct for the interface server."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Server"


class RustEnumSymbols(RustSymbols):
    """Rust symbols for an :class:`InterfaceEnum`."""

    def __init__(self, enum):
        super().__init__()
        self._enum = enum

    @property
    def local_type(self) -> str:
        """Unqualified Rust type name for the enum."""
        return stringmanip.upper_camel_case(self._enum.name)

    @property
    def type(self) -> str:
        """Fully-qualified Rust type name for the enum."""
        return self.local_type


class RustStructSymbols(RustSymbols):
    """Rust symbols for an :class:`InterfaceStruct`."""

    def __init__(self, struct):
        super().__init__()
        self._struct = struct

    @property
    def local_type(self) -> str:
        """Unqualified Rust type name for the struct."""
        return stringmanip.upper_camel_case(self._struct.name)

    @property
    def type(self) -> str:
        """Fully-qualified Rust type name for the struct."""
        return self.local_type


class RustMethodSymbols(RustSymbols):
    """Rust symbols for an :class:`IpcMethod`."""

    def __init__(self, method):
        super().__init__()
        self._method = method

    @property
    def return_value_type(self) -> str:
        """Rust return type for the method's return value."""
        if self._method.response_payload.is_protobuf:
            return self._method.response_payload.rust.struct_name
        if self._method.return_value is None:
            return "()"
        return self._method.return_value.rust.type

    @property
    def return_struct_name(self) -> str:
        """Rust struct name of the method's generated response payload."""
        return self._method.response_payload.rust.struct_name


class RustCommandSymbols(RustSymbols):
    """Rust symbols for an :class:`IpcCommand`."""

    def __init__(self, command):
        super().__init__()
        self._command = command

    @property
    def payload_struct_name(self) -> str:
        """Rust struct name of the command's generated payload."""
        return self._command.payload.rust.struct_name


class RustArgSymbols(RustSymbols):
    """Base Rust symbols for Arg objects."""

    def __init__(self, arg):
        super().__init__()
        self._arg = arg

    @property
    def type(self) -> str:
        """Rust type name for this argument."""
        return self._arg.name

    @property
    def local_type(self) -> str:
        """Unqualified Rust type name for this argument."""
        return self.type


class RustArgEnumSymbols(RustArgSymbols):
    """Rust symbols for an :class:`ArgEnum`."""

    @property
    def type(self) -> str:
        """Rust type name of the referenced enum, wrapped in ``Option`` when optional."""
        if self._arg.optional:
            return f"Option<{self._arg.enum.rust.type}>"
        return self._arg.enum.rust.type

    @property
    def local_type(self) -> str:
        """Unqualified Rust type name of the referenced enum, wrapped in ``Option`` when optional."""
        if self._arg.optional:
            return f"Option<{self._arg.enum.rust.local_type}>"
        return self._arg.enum.rust.local_type


class RustArgPrimitiveSymbols(RustArgSymbols):
    """Rust symbols for an :class:`ArgPrimitive`."""

    @property
    def type(self) -> str:
        """Rust type name for the primitive (e.g. ``i32``), wrapped in ``Option`` when optional."""
        return ArgPrimitiveType.to_rust_type(self._arg.primitive_type, optional=self._arg.optional)


class RustArgStructSymbols(RustArgSymbols):
    """Rust symbols for an :class:`ArgStruct`."""

    @property
    def type(self) -> str:
        """Rust type name of the referenced struct, wrapped in ``Option`` when optional."""
        if self._arg.optional:
            return f"Option<{self._arg.interface_struct.rust.type}>"
        return self._arg.interface_struct.rust.type

    @property
    def local_type(self) -> str:
        """Unqualified Rust type name of the referenced struct, wrapped in ``Option`` when optional."""
        if self._arg.optional:
            return f"Option<{self._arg.interface_struct.rust.local_type}>"
        return self._arg.interface_struct.rust.local_type

    @property
    def temp_type(self) -> str:
        """Unqualified Rust type name of the referenced struct (never wrapped)."""
        return self._arg.interface_struct.rust.local_type


class RustArgDateTimeSymbols(RustArgSymbols):
    """Rust symbols for an :class:`ArgDateTime`."""

    @property
    def type(self) -> str:
        """Rust type name for datetimes, wrapped in ``Option`` when optional."""
        if self._arg.optional:
            return "Option<chrono::DateTime<chrono::Utc>>"
        return "chrono::DateTime<chrono::Utc>"


class RustArgDurationSymbols(RustArgSymbols):
    """Rust symbols for an :class:`ArgDuration`."""

    @property
    def type(self) -> str:
        """Rust type name for durations, wrapped in ``Option`` when optional."""
        if self._arg.optional:
            return "Option<chrono::Duration>"
        return "chrono::Duration"


class RustArgBinarySymbols(RustArgSymbols):
    """Rust symbols for an :class:`ArgBinary`."""

    @property
    def type(self) -> str:
        """Rust type name for binary data, wrapped in ``Option`` when optional."""
        if self._arg.optional:
            return "Option<Vec<u8>>"
        return "Vec<u8>"


class RustArgArraySymbols(RustArgSymbols):
    """Rust symbols for an :class:`ArgArray`."""

    @property
    def type(self) -> str:
        """Rust type name for the array, wrapped in ``Option`` when optional."""
        if self._arg.optional:
            return f"Option<Vec<{self._arg.element.rust.type}>>"
        return f"Vec<{self._arg.element.rust.type}>"


class RustConstantSymbols(RustSymbols):
    """Rust symbols for an :class:`InterfaceConstant`."""

    def __init__(self, constant):
        super().__init__()
        self._constant = constant

    @property
    def type(self) -> str:
        """Rust type name for the constant's declared type."""
        type_map = {
            "integer": "i64",
            "float": "f64",
            "boolean": "bool",
            "string": "&str",
        }
        return type_map.get(self._constant.constant_type, "&str")

    @property
    def local_type(self) -> str:
        """Unqualified Rust type name for the constant."""
        return self.type


class RustPropertySymbols(RustSymbols):
    """Rust symbols for an :class:`IpcProperty`."""

    def __init__(self, prop):
        super().__init__()
        self._prop = prop

    @property
    def is_protobuf(self) -> bool:
        """True when the property holds a protobuf message rather than a JSON value."""
        return self._prop.payload.is_protobuf

    @property
    def is_optional(self) -> bool:
        """True when the property's value may be absent.

        A protobuf message is never optional in this sense: an unset message is
        still a message, with its fields at their defaults.
        """
        if self.is_protobuf:
            return False
        return bool(self._prop.value.optional)

    @property
    def has_value_schema(self) -> bool:
        """True when the property's value declares a JSON schema constraint.

        Never for a protobuf message, which carries no JSON schema.
        """
        if self.is_protobuf:
            return False
        return bool(self._prop.value.value_schema)

    @property
    def local_type(self) -> str:
        """Unqualified Rust type name for the property's value."""
        if self.is_protobuf:
            return self._prop.payload.protobuf.message_name
        return self._prop.value.rust.local_type

    @property
    def type(self) -> str:
        """Rust type name for the property's value.

        A protobuf property's value is the message itself: there is no wrapper
        struct with a single named field, so the value type and the payload type
        are the same thing.
        """
        if self.is_protobuf:
            return self._prop.payload.rust.struct_name
        return self._prop.value.rust.type


# The name of the generated struct for each kind of payload.  These reproduce
# exactly the names the templates used to spell inline, so that routing them through
# the payload changes no generated output.
_RUST_PAYLOAD_NAMES = {
    "SIGNAL": lambda name: f"{stringmanip.upper_camel_case(name)}SignalPayload",
    "COMMAND": lambda name: f"{stringmanip.upper_camel_case(name)}CommandPayload",
    "METHOD_REQUEST": lambda name: f"{stringmanip.upper_camel_case(name)}RequestObject",
    "METHOD_RESPONSE": lambda name: stringmanip.upper_camel_case(f"{name} return value"),
    "PROPERTY": lambda name: f"{stringmanip.upper_camel_case(name)}Property",
}


class RustPayloadSymbols(RustSymbols):
    """Rust symbols for a :class:`Payload`."""

    def __init__(self, payload):
        super().__init__()
        self._payload = payload

    @property
    def struct_name(self) -> str:
        """Rust name of the type that carries this payload."""
        if self._payload.is_protobuf:
            return self._payload.protobuf.rust.qualified_name
        return _RUST_PAYLOAD_NAMES[self._payload.role.name](self._payload.owner_name)

    @property
    def class_name(self) -> str:
        """Alias for :attr:`struct_name`, so templates can use one spelling across languages."""
        return self.struct_name

    @property
    def channel_type(self) -> str:
        """The type a broadcast channel carrying this payload hands to receivers.

        Always the payload struct, including for a payload with no arguments or
        exactly one.  A channel has a single item type, so unlike Python and C++
        there is no way to offer the unpacked form alongside the object; making it
        uniform is what lets the client and server dispatch code drop the
        zero/one/many special cases it used to repeat at every channel site.
        """
        return self.struct_name


# How prost names protobuf's well-known types.  prost never generates code for
# them: it substitutes a ready-made type, which for most is the `prost-types`
# struct of the same name, but for `Empty` and the wrapper messages is a plain
# Rust type instead.  Mirrored here because generated code has to spell the
# message the same way prost does, and these exceptions are not derivable from
# the name.  Kept in step with prost-build's `ExternPaths::new`.
_RUST_WELL_KNOWN_EXCEPTIONS = {
    "Empty": "()",
    "BoolValue": "bool",
    "BytesValue": "::prost::alloc::vec::Vec<u8>",
    "DoubleValue": "f64",
    "FloatValue": "f32",
    "Int32Value": "i32",
    "Int64Value": "i64",
    "StringValue": "::prost::alloc::string::String",
    "UInt32Value": "u32",
    "UInt64Value": "u64",
}


class RustProtobufRefSymbols(RustSymbols):
    """Rust symbols for a :class:`ProtobufMessageRef`."""

    def __init__(self, ref):
        super().__init__()
        self._ref = ref

    @property
    def module_path(self) -> str:
        """Path of the generated module holding this message.

        prost writes one file per protobuf package with the messages at its top
        level, and those files are included into a single ``proto`` module, so the
        package does not reappear in the Rust path.

        A well-known type is the exception: prost generates nothing for one,
        substituting the ready-made definition in ``prost-types``.
        """
        if self._ref.is_well_known:
            return "::prost_types"
        return "crate::proto"

    @property
    def qualified_name(self) -> str:
        """How generated Rust code names this message, fully qualified from the crate root."""
        if self._ref.is_well_known:
            substitute = _RUST_WELL_KNOWN_EXCEPTIONS.get(self._ref.message_name)
            if substitute is not None:
                return substitute
        return f"{self.module_path}::{self._ref.message_name}"

    @property
    def external_name(self) -> str:
        """How code outside the library names this message.

        Examples and integration tests are separate crates, so they import the
        library's ``proto`` module rather than reaching through ``crate::``.  A
        well-known type is spelled the same way everywhere, since it comes from
        neither.
        """
        if self._ref.is_well_known:
            return self.qualified_name
        return f"proto::{self._ref.message_name}"
