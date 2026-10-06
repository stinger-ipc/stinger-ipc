from typing import Any

from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.config import ExternalProtobufConfig, StingerConfig
from stingeripc.exceptions import InvalidStingerStructure
from stingeripc.lang_symb import ISymbolsProvider

# The keywords prost escapes by turning the identifier into a raw one.  A protobuf
# field is free to be called `type` or `match`; Rust's is not, and generated code has
# to spell the member exactly the way prost named it.  Kept in step with
# prost-build's `ident::to_snake`.
_RUST_RAW_KEYWORDS = frozenset(
    {
        # 2015 strict keywords.
        "as",
        "break",
        "const",
        "continue",
        "else",
        "enum",
        "false",
        "fn",
        "for",
        "if",
        "impl",
        "in",
        "let",
        "loop",
        "match",
        "mod",
        "move",
        "mut",
        "pub",
        "ref",
        "return",
        "static",
        "struct",
        "trait",
        "true",
        "type",
        "unsafe",
        "use",
        "where",
        "while",
        # 2018 strict keywords.
        "dyn",
        # 2015 reserved keywords.
        "abstract",
        "become",
        "box",
        "do",
        "final",
        "macro",
        "override",
        "priv",
        "typeof",
        "unsized",
        "virtual",
        "yield",
        # 2018 reserved keywords.
        "async",
        "await",
        "try",
    }
)

# The keywords that cannot be raw identifiers, which prost suffixes instead.
_RUST_SUFFIXED_KEYWORDS = frozenset({"self", "super", "extern", "crate"})


def _rust_sanitize(ident: str) -> str:
    """Make an already snake-cased identifier safe to use as a Rust name."""
    if ident in _RUST_RAW_KEYWORDS:
        return f"r#{ident}"
    if ident in _RUST_SUFFIXED_KEYWORDS:
        return f"{ident}_"
    return ident


def _rust_ident(name: str) -> str:
    """Spell a protobuf name the way prost spells it as a Rust identifier."""
    return _rust_sanitize(stringmanip.snake_case(name))


class RustSymbolsProvider(ISymbolsProvider):
    """Plugin that provides Rust symbols for model objects.

    Registers as the ``rust`` language domain so templates can access Rust
    names and types via ``obj.rust.<property>``.
    """

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "ProtobufMessageRef":
            return RustProtobufRefSymbols(model, self.config)
        elif model_class_name == "ProtobufField":
            return RustProtobufFieldSymbols(model)
        elif model_class_name == "ProtobufOneof":
            return RustProtobufOneofSymbols(model)
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
    def external_return_value_type(self) -> str:
        """The same type as :attr:`return_value_type`, spelled for code outside the library.

        The documentation and the example crates are not the library, so a protobuf
        message reaches them through ``proto::`` rather than through ``crate::``.
        """
        if self._method.response_payload.is_protobuf:
            return self._method.response_payload.protobuf.rust.external_name
        return self.return_value_type

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
            return self._prop.payload.protobuf.rust.scoped_name
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
    def is_unit(self) -> bool:
        """True when this payload's Rust type is ``()``.

        Only ``google.protobuf.Empty`` is: prost substitutes the unit type for it
        rather than generating an empty struct.  Binding a local of unit type is
        something clippy objects to, and the generated code binds one anyway so that
        the publish and decode paths stay the same shape for every payload.
        """
        return self.struct_name == "()"

    @property
    def params(self) -> list:
        """The things a generated function takes one parameter for, in order.

        A JSON payload contributes its arguments; a protobuf payload contributes the
        members of the prost struct, which is its fields with each real ``oneof``
        collapsed into the single ``Option<Enum>`` member prost gives it.
        """
        if self._payload.is_protobuf:
            return self._payload.protobuf.rust.struct_fields
        return self._payload.args

    @property
    def has_params(self) -> bool:
        """True when a function carrying this payload takes any parameters at all.

        ``google.protobuf.Empty`` and a JSON payload with no arguments both answer
        False, which is what lets a call site leave out the comma after ``&mut self``
        and skip binding a local nothing would read.
        """
        return bool(self.params)

    @property
    def param_count(self) -> int:
        """How many parameters a function carrying this payload takes."""
        return len(self.params)

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

    def __init__(self, ref, config: StingerConfig | None = None):
        super().__init__(config)
        self._ref = ref

    @property
    def _external(self) -> ExternalProtobufConfig | None:
        """Where the host's bindings live, or None when this crate bundles this message's."""
        if self.config is None or self.config.protobuf.mode != "external" or self._ref.is_well_known:
            return None
        return self.config.protobuf.external

    @property
    def is_external(self) -> bool:
        """True when the host supplies this message's bindings rather than the crate bundling them."""
        return self._external is not None

    @property
    def module_path(self) -> str:
        """Path of the generated module holding this message.

        prost writes one file per protobuf package with the messages at its top
        level, and those files are included into a single ``proto`` module, so the
        package does not reappear in the Rust path.

        A well-known type is the exception: prost generates nothing for one,
        substituting the ready-made definition in ``prost-types``.

        When the host supplies the bindings the path starts at the configured
        ``rust_module`` instead, and a protobuf package nests below it one module
        per segment, which is how prost-build lays out its output.
        """
        if self._ref.is_well_known:
            return "::prost_types"
        external = self._external
        if external is not None:
            base = external.rust_module
            if not base:
                raise InvalidStingerStructure(f"[protobuf] mode is 'external' but [protobuf.external] rust_module is not set, so the Rust path of '{self._ref.full_name}' is unknown.")
            return "::".join([base, *(_rust_ident(segment) for segment in self._ref.package.split(".") if segment)])
        return "crate::proto"

    @property
    def scoped_name(self) -> str:
        """The message's path below its module, e.g. ``analytics::DetectionEvent``.

        prost has no nested structs: a message declared inside another becomes a
        struct in a module named after the parent, in snake case.
        """
        parents = [stringmanip.snake_case(name) for name in self._ref.scope]
        return "::".join([*parents, self._ref.message_name])

    @property
    def qualified_name(self) -> str:
        """How generated Rust code names this message, fully qualified from the crate root."""
        if self._ref.is_well_known:
            substitute = _RUST_WELL_KNOWN_EXCEPTIONS.get(self._ref.message_name)
            if substitute is not None:
                return substitute
        return f"{self.module_path}::{self.scoped_name}"

    @property
    def external_name(self) -> str:
        """How code outside the library names this message.

        Examples and integration tests are separate crates, so they import the
        library's ``proto`` module rather than reaching through ``crate::``.  A
        well-known type is spelled the same way everywhere, since it comes from
        neither, and so is a message whose bindings the host supplies, since the
        configured ``rust_module`` is reachable from the crate and from outside it.
        """
        if self._ref.is_well_known or self.is_external:
            return self.qualified_name
        return f"proto::{self.scoped_name}"

    @property
    def own_module(self) -> str:
        """The module prost puts this message's own nested declarations in.

        prost has no nested items: a message's nested messages, enums and ``oneof``
        enums all become siblings in a module named after the message in snake case,
        below the module its parents made.  ``traps.v1.Reading`` therefore owns
        ``reading``, and its ``source`` oneof is ``reading::Source``.
        """
        return "::".join(stringmanip.snake_case(name) for name in [*self._ref.scope, self._ref.message_name])

    @property
    def struct_fields(self) -> list:
        """The members of the prost struct, in the order a generated function takes them.

        Not quite the message's fields: prost gives a real ``oneof`` a single
        ``Option<Enum>`` member rather than one member per alternative, so the whole
        group is one parameter.  Members a caller must supply come first and those it
        may leave out come after -- the same split :attr:`ProtobufMessageRef.param_fields`
        makes, so a message's parameters line up with the other languages'.
        """
        by_oneof = {oneof.name: oneof for oneof in self._ref.oneofs}
        members: list = []
        claimed: set = set()
        for field in self._ref.fields:
            if field.oneof_name is None:
                members.append(field)
                continue
            if field.oneof_name in claimed:
                continue
            claimed.add(field.oneof_name)
            members.append(by_oneof[field.oneof_name])
        # A oneof has no `is_optional_param`: it is always optional, since prost can
        # only offer "one of these, or none".
        return [m for m in members if not getattr(m, "is_optional_param", True)] + [m for m in members if getattr(m, "is_optional_param", True)]

    @property
    def comparable_fields(self) -> list:
        """The struct members a generated test can check an exact value of.

        Floating point does not survive a round trip predictably enough to compare,
        and a repeated, map or message member has no example value to compare against.
        """
        return [member for member in self.struct_fields if member.rust.is_comparable]


# How a protobuf scalar is spelled in the Rust prost generates.  Confirmed against
# `partials/protoc.toml`, which asks protoc for `--prost_out` with no type overrides,
# so these are prost's defaults rather than a configured mapping.
_RUST_SCALAR_TYPES = {
    "double": "f64",
    "float": "f32",
    "int32": "i32",
    "sint32": "i32",
    "sfixed32": "i32",
    "int64": "i64",
    "sint64": "i64",
    "sfixed64": "i64",
    "uint32": "u32",
    "fixed32": "u32",
    "uint64": "u64",
    "fixed64": "u64",
    "bool": "bool",
    "string": "String",
    "bytes": "Vec<u8>",
}

# The scalars an exact equality check is meaningful for.  A float that has been
# through the wire is not reliably the literal a test wrote down.
_RUST_INCOMPARABLE_SCALARS = frozenset({"float", "double"})


class RustProtobufFieldSymbols(RustSymbols):
    """Rust symbols for one field of a protobuf message, as prost generates it."""

    def __init__(self, field):
        super().__init__()
        self._field = field

    def _element_type(self, field, external: bool) -> str:
        """The type of one element of ``field``, before any container or ``Option``."""
        if field.is_enum:
            # prost keeps an enum field as its raw i32: an unknown value on the wire
            # still has to survive a decode, which a Rust enum could not hold.
            return "i32"
        if field.is_message:
            if field.kind == "group":
                raise InvalidStingerStructure(f"The protobuf field '{field.name}' is a proto2 group, which is not supported.")
            return field.type_ref.rust.external_name if external else field.type_ref.rust.qualified_name
        try:
            return _RUST_SCALAR_TYPES[field.kind]
        except KeyError:
            raise InvalidStingerStructure(f"The protobuf field '{field.name}' has type '{field.kind}', which has no Rust equivalent.")

    def _type(self, external: bool) -> str:
        field = self._field
        if field.is_map:
            key = self._element_type(field.map_key, external)
            value = self._element_type(field.map_value, external)
            return f"::std::collections::HashMap<{key}, {value}>"
        element = self._element_type(field, external)
        if field.repeated:
            return f"Vec<{element}>"
        # prost wraps a singular message in `Option` whatever the syntax says: a
        # message field is absent until something sets it.
        if field.is_message or field.is_optional_param:
            return f"Option<{element}>"
        return element

    @property
    def field_name(self) -> str:
        """The name prost gives this field as a struct member."""
        return _rust_ident(self._field.name)

    def param_name(self, prefix: str = "") -> str:
        """The name a generated function gives this field as a parameter.

        ``prefix`` is how a stub marks a parameter it does not read (``_days``).  It
        is applied before the keyword check, so a prefixed keyword is an ordinary
        identifier again: ``_type``, not ``_r#type``.
        """
        return _rust_sanitize(f"{prefix}{stringmanip.snake_case(self._field.name)}")

    @property
    def type(self) -> str:
        """The Rust type of this field inside the library, reaching messages through ``crate``."""
        return self._type(external=False)

    @property
    def external_type(self) -> str:
        """The Rust type of this field outside the library, reaching messages through ``proto``."""
        return self._type(external=True)

    def example_value(self, seed: int = 2) -> str:
        """An example value for this field, for demos and generated tests.

        A container's example is empty and a message's is absent: filling either in
        would need the shape of another declaration, which this field's descriptor
        does not carry.
        """
        field = self._field
        if field.is_map:
            return "Default::default()"
        if field.repeated:
            return "Vec::new()"
        if field.is_message:
            return "None"
        value = "0" if field.is_enum else field.get_random_example_value(lang="rust", seed=seed)
        return f"Some({value})" if field.is_optional_param else value

    @property
    def is_comparable(self) -> bool:
        """True when a generated test can assert this field came back exactly as sent."""
        field = self._field
        return field.is_scalar and not field.repeated and not field.is_map and field.kind not in _RUST_INCOMPARABLE_SCALARS


class RustProtobufOneofSymbols(RustSymbols):
    """Rust symbols for a real ``oneof``, which prost gives one struct member.

    Unlike the other languages, Rust never sees the alternatives as separate
    parameters: prost declares an enum with one variant per member and the struct
    holds an ``Option`` of it, so the whole group is a single value.
    """

    def __init__(self, oneof):
        super().__init__()
        self._oneof = oneof

    def _type(self, module: str) -> str:
        return f"Option<{module}::{self._oneof.parent.rust.own_module}::{stringmanip.upper_camel_case(self._oneof.name)}>"

    @property
    def field_name(self) -> str:
        """The name prost gives this oneof as a struct member."""
        return _rust_ident(self._oneof.name)

    def param_name(self, prefix: str = "") -> str:
        """The name a generated function gives this oneof as a parameter."""
        return _rust_sanitize(f"{prefix}{stringmanip.snake_case(self._oneof.name)}")

    @property
    def type(self) -> str:
        """The Rust type of this oneof inside the library."""
        return self._type(self._oneof.parent.rust.module_path)

    @property
    def external_type(self) -> str:
        """The Rust type of this oneof outside the library."""
        return self._type("proto")

    def example_value(self, seed: int = 2) -> str:
        """An example value for this oneof: none of its alternatives.

        Picking one would mean naming a variant of a generated enum, and leaving the
        group unset is always valid.
        """
        return "None"

    @property
    def is_comparable(self) -> bool:
        """False: the example value is `None`, which proves nothing about the wire."""
        return False
