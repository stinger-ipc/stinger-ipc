from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.lang_symb import ISymbolsProvider


class CppSymbolsProvider(ISymbolsProvider):
    """Plugin that provides C++ symbols for model objects.

    Registers as the ``cpp`` language domain so templates can access C++ names
    and types via ``obj.cpp.<property>``.
    """

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "ProtobufMessageRef":
            return CppProtobufRefSymbols(model)
        elif model_class_name == "ProtobufField":
            return CppProtobufFieldSymbols(model)
        elif model_class_name == "Payload":
            return CppPayloadSymbols(model)
        elif model_class_name == "StingerSpec":
            return CppInterfaceSymbols(model)
        elif model_class_name == "IpcProperty":
            return CppPropertySymbols(model)
        elif model_class_name == "IpcMethod":
            return CppMethodSymbols(model)
        elif model_class_name == "IpcCommand":
            return CppCommandSymbols(model)
        elif model_class_name == "InterfaceEnum":
            return CppEnumSymbols(model)
        elif model_class_name == "InterfaceStruct":
            return CppStructSymbols(model)
        elif model_class_name == "ArgEnum":
            return CppArgEnumSymbols(model)
        elif model_class_name == "ArgPrimitive":
            return CppArgPrimitiveSymbols(model)
        elif model_class_name == "ArgStruct":
            return CppArgStructSymbols(model)
        elif model_class_name == "ArgDateTime":
            return CppArgDateTimeSymbols(model)
        elif model_class_name == "ArgDuration":
            return CppArgDurationSymbols(model)
        elif model_class_name == "ArgBinary":
            return CppArgBinarySymbols(model)
        elif model_class_name == "ArgArray":
            return CppArgArraySymbols(model)
        elif model_class_name == "InterfaceConstant":
            return CppConstantSymbols(model)
        return None


class CppSymbols:
    """Base class for C++ symbol providers."""

    def __init__(self):
        pass


class CppInterfaceSymbols(CppSymbols):
    """C++ symbols for the top-level :class:`StingerSpec` (the interface)."""

    def __init__(self, interface):
        super().__init__()
        self._iface = interface

    @property
    def project_name(self) -> str:
        """Name of the generated C++ project (used by CMake)."""
        return f"{stringmanip.hyphen_case(self._iface.name)}-ipc"

    @property
    def cmake_name(self) -> str:
        """Camel-case name used as the CMake target for the project."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Ipc"

    @property
    def client_class_name(self) -> str:
        """C++ class name of the interface client."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Client"

    @property
    def server_class_name(self) -> str:
        """C++ class name of the interface server."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Server"

    @property
    def enum_header_file(self) -> str:
        """Filename of the generated enums header."""
        return "enums.hpp"

    @property
    def property_struct_header_file(self) -> str:
        """Filename of the generated property structs header."""
        return "property_structs.hpp"


class CppConstantSymbols(CppSymbols):
    """C++ symbols for an :class:`InterfaceConstant`."""

    def __init__(self, constant):
        super().__init__()
        self._constant = constant

    @property
    def type(self) -> str:
        """C++ type name for the constant's declared type."""
        type_map = {
            "integer": "int64_t",
            "float": "double",
            "boolean": "bool",
            "string": "std::string",
        }
        return type_map.get(self._constant.constant_type, "std::string")


class CppPropertySymbols(CppSymbols):
    """C++ symbols for an :class:`IpcProperty`."""

    def __init__(self, prop):
        super().__init__()
        self._prop = prop

    @property
    def is_protobuf(self) -> bool:
        """True when the property holds a protobuf message rather than a JSON value."""
        return self._prop.payload.is_protobuf

    @property
    def property_struct_name(self) -> str:
        """C++ struct name generated for the property."""
        return self._prop.payload.cpp.struct_name

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
    def temp_type(self) -> str:
        """C++ type used for a local holding the property's value."""
        if self.is_protobuf:
            return self._prop.payload.cpp.struct_name
        return self._prop.value.cpp.temp_type

    @property
    def value_type(self) -> str:
        """C++ type of the property's value.

        A protobuf property's value is the message itself: there is no wrapper
        struct with a single named field to unwrap.
        """
        if self.is_protobuf:
            return self._prop.payload.cpp.struct_name
        return self._prop.value.cpp.type


class CppMethodSymbols(CppSymbols):
    """C++ symbols for an :class:`IpcMethod`."""

    def __init__(self, method):
        super().__init__()
        self._method = method

    @property
    def return_value_class(self) -> str:
        """C++ type that the method's handler returns, or ``void`` when it returns nothing.

        A protobuf response has no single ``Arg`` to unwrap: the handler builds the
        response message itself and the caller's future resolves to it, so the type
        is the message class.
        """
        from stingeripc.components import ArgPrimitive, ArgStruct

        if self._method.response_payload.is_protobuf:
            return self._method.response_payload.cpp.struct_name
        return_value = self._method.return_value
        if return_value is None:
            return "void"
        if isinstance(return_value, ArgPrimitive) and return_value.type == ArgPrimitiveType.STRING:
            if return_value.optional:
                return "std::optional<std::string>"
            return "std::string"
        if isinstance(return_value, ArgStruct) and return_value.optional:
            return f"std::optional<{return_value.cpp.type}>"  # type: ignore[attr-defined]
        return return_value.cpp.type

    @property
    def return_struct_name(self) -> str:
        """C++ struct name of the method's generated response payload."""
        return self._method.response_payload.cpp.struct_name


class CppCommandSymbols(CppSymbols):
    """C++ symbols for an :class:`IpcCommand`."""

    def __init__(self, command):
        super().__init__()
        self._command = command

    @property
    def payload_struct_name(self) -> str:
        """C++ struct name of the command's generated payload."""
        return self._command.payload.cpp.struct_name


class CppEnumSymbols(CppSymbols):
    """C++ symbols for an :class:`InterfaceEnum`."""

    def __init__(self, enum):
        super().__init__()
        self._enum = enum

    @property
    def type(self) -> str:
        """C++ type name for the enum."""
        return stringmanip.upper_camel_case(self._enum.name)

    @property
    def rapidjson_type(self) -> str:
        """RapidJSON type used when (de)serializing enum values (enums are integers)."""
        return ArgPrimitiveType.to_cpp_rapidjson_type_str(ArgPrimitiveType.INTEGER)


class CppStructSymbols(CppSymbols):
    """C++ symbols for an :class:`InterfaceStruct`."""

    def __init__(self, struct):
        super().__init__()
        self._struct = struct

    @property
    def type(self) -> str:
        """C++ type name for the struct."""
        return stringmanip.upper_camel_case(self._struct.name)


class CppArgSymbols(CppSymbols):
    """Base C++ symbols for Arg objects."""

    def __init__(self, arg):
        super().__init__()
        self._arg = arg

    @property
    def type(self) -> str:
        """C++ type name for this argument."""
        return stringmanip.upper_camel_case(self._arg.name)

    @property
    def temp_type(self) -> str:
        """C++ type used for temporary values, wrapped in ``std::optional`` when the arg is optional."""
        if self._arg.optional and "optional" not in self.type:
            return f"std::optional<{self.type}>"
        return self.type

    @property
    def func_param_type(self) -> str:
        """C++ type used for function parameters, wrapped in ``std::optional`` when the arg is optional."""
        if self._arg.optional and "optional" not in self.type:
            return f"std::optional<{self.type}>"
        return self.type


class CppArgEnumSymbols(CppArgSymbols):
    """C++ symbols for an :class:`ArgEnum`."""

    @property
    def type(self) -> str:
        """C++ type name of the referenced enum, wrapped in ``std::optional`` when optional."""
        if self._arg.optional:
            return f"std::optional<{self._arg.enum.cpp.type}>"
        return self._arg.enum.cpp.type

    @property
    def temp_type(self) -> str:
        """C++ temporary type for the enum (same as ``type``)."""
        return self.type

    @property
    def data_type(self) -> str:
        """C++ data type of the referenced enum."""
        return self._arg.enum.cpp.type

    @property
    def rapidjson_type(self) -> str:
        """RapidJSON type used when (de)serializing enum values."""
        return ArgPrimitiveType.to_cpp_rapidjson_type_str(ArgPrimitiveType.INTEGER)


class CppArgPrimitiveSymbols(CppArgSymbols):
    """C++ symbols for an :class:`ArgPrimitive`."""

    @property
    def type(self) -> str:
        """C++ type name for the primitive, wrapped in ``std::optional`` when optional."""
        return ArgPrimitiveType.to_cpp_type(self._arg.primitive_type, optional=self._arg.optional)

    @property
    def temp_type(self) -> str:
        """C++ temporary type for the primitive (strings are handled specially)."""
        if self._arg.primitive_type == ArgPrimitiveType.STRING:
            if self._arg.optional:
                return "std::optional<std::string>"
            return "std::string"
        return self.type

    @property
    def rapidjson_type(self) -> str:
        """RapidJSON type used when (de)serializing this primitive."""
        return ArgPrimitiveType.to_cpp_rapidjson_type_str(self._arg.primitive_type)


class CppArgStructSymbols(CppArgSymbols):
    """C++ symbols for an :class:`ArgStruct`."""

    @property
    def type(self) -> str:
        """C++ type name of the referenced struct."""
        return self._arg.interface_struct.cpp.type

    @property
    def rapidjson_type(self) -> str:
        """RapidJSON type used when (de)serializing structs (always ``Object``)."""
        return "Object"


class CppArgDateTimeSymbols(CppArgSymbols):
    """C++ symbols for an :class:`ArgDateTime`."""

    @property
    def type(self) -> str:
        """C++ type name for datetimes, wrapped in ``std::optional`` when optional."""
        if self._arg.optional:
            return "std::optional<std::chrono::time_point<std::chrono::system_clock>>"
        return "std::chrono::time_point<std::chrono::system_clock>"

    @property
    def temp_type(self) -> str:
        """C++ temporary type for datetimes (same as ``type``)."""
        return self.type

    @property
    def rapidjson_type(self) -> str:
        """RapidJSON type used when (de)serializing datetimes (ISO strings)."""
        return "String"


class CppArgDurationSymbols(CppArgSymbols):
    """C++ symbols for an :class:`ArgDuration`."""

    @property
    def type(self) -> str:
        """C++ type name for durations, wrapped in ``std::optional`` when optional."""
        if self._arg.optional:
            return "std::optional<std::chrono::duration<double>>"
        return "std::chrono::duration<double>"

    @property
    def temp_type(self) -> str:
        """C++ temporary type for durations (same as ``type``)."""
        return self.type

    @property
    def rapidjson_type(self) -> str:
        """RapidJSON type used when (de)serializing durations (ISO strings)."""
        return "String"


class CppArgBinarySymbols(CppArgSymbols):
    """C++ symbols for an :class:`ArgBinary`."""

    @property
    def type(self) -> str:
        """C++ type name for binary data, wrapped in ``std::optional`` when optional."""
        if self._arg.optional:
            return "std::optional<std::vector<uint8_t>>"
        return "std::vector<uint8_t>"

    @property
    def temp_type(self) -> str:
        """C++ temporary type for binary data (same as ``type``)."""
        return self.type

    @property
    def rapidjson_type(self) -> str:
        """RapidJSON type used when (de)serializing binary data (base64 strings)."""
        return "String"


class CppArgArraySymbols(CppArgSymbols):
    """C++ symbols for an :class:`ArgArray`."""

    @property
    def type(self) -> str:
        """C++ type name for the array, wrapped in ``std::optional`` when optional."""
        if self._arg.optional:
            return f"std::optional<std::vector<{self._arg.element.cpp.temp_type}>>"
        return f"std::vector<{self._arg.element.cpp.temp_type}>"

    @property
    def rapidjson_type(self) -> str:
        """RapidJSON type used when (de)serializing arrays (always ``Array``)."""
        return "Array"


# The name of the generated struct for each kind of payload.  These reproduce
# exactly the names the templates used to spell inline, so that routing them through
# the payload changes no generated output.
_CPP_PAYLOAD_NAMES = {
    "SIGNAL": lambda name: f"{stringmanip.upper_camel_case(name)}Payload",
    "COMMAND": lambda name: f"{stringmanip.upper_camel_case(name)}CommandPayload",
    "METHOD_REQUEST": lambda name: f"{stringmanip.upper_camel_case(name)}RequestArguments",
    "METHOD_RESPONSE": lambda name: stringmanip.upper_camel_case(f"{name} return value"),
    "PROPERTY": lambda name: f"{stringmanip.upper_camel_case(name)}Property",
}


class CppPayloadSymbols(CppSymbols):
    """C++ symbols for a :class:`Payload`."""

    def __init__(self, payload):
        super().__init__()
        self._payload = payload

    @property
    def struct_name(self) -> str:
        """C++ name of the type that carries this payload."""
        if self._payload.is_protobuf:
            return self._payload.protobuf.cpp.qualified_name
        return _CPP_PAYLOAD_NAMES[self._payload.role.name](self._payload.owner_name)

    @property
    def class_name(self) -> str:
        """Alias for :attr:`struct_name`, so templates can use one spelling across languages."""
        return self.struct_name


class CppProtobufRefSymbols(CppSymbols):
    """C++ symbols for a :class:`ProtobufMessageRef`."""

    def __init__(self, ref):
        super().__init__()
        self._ref = ref

    @property
    def namespace(self) -> str:
        """The C++ namespace protoc puts this message in, from its protobuf package."""
        return "::".join(p for p in self._ref.package.split(".") if p)

    @property
    def include(self) -> str:
        """The ``#include`` argument, brackets and all, for this message's header.

        A well-known type's header ships with libprotobuf and is found on the
        include path; the interface's own headers protoc wrote into the generated
        library are quoted and relative to it.
        """
        header = self._ref.proto_file.replace(".proto", ".pb.h")
        return f"<{header}>" if self._ref.is_well_known else f'"proto/{header}"'

    @property
    def scoped_name(self) -> str:
        """The message's name below its namespace, e.g. ``Analytics::DetectionEvent``.

        protoc declares a nested message as a class inside its parent, so the
        enclosing messages spell out the same way the namespace does.
        """
        return "::".join(self._ref.scoped_name.split("."))

    @property
    def qualified_name(self) -> str:
        """How generated C++ code names this message, e.g. ``::weather::v1::CurrentConditions``."""
        ns = self.namespace
        return f"::{ns}::{self.scoped_name}" if ns else f"::{self.scoped_name}"


# What protoc's C++ backend spells each scalar field kind as.  A message or enum
# field's type is the generated class, which only its resolved reference knows.
_CPP_SCALAR_TYPES = {
    "double": "double",
    "float": "float",
    "int32": "int32_t",
    "sint32": "int32_t",
    "sfixed32": "int32_t",
    "int64": "int64_t",
    "sint64": "int64_t",
    "sfixed64": "int64_t",
    "uint32": "uint32_t",
    "fixed32": "uint32_t",
    "uint64": "uint64_t",
    "fixed64": "uint64_t",
    "bool": "bool",
    "string": "std::string",
    # protoc gives a `bytes` field a std::string too; the bytes are simply not text.
    "bytes": "std::string",
}

# The field kinds that fit in a register, and so are taken by value rather than by
# const reference.  An enum is one of them; its generated type is an `enum` proper.
_CPP_TRIVIAL_KINDS = frozenset(_CPP_SCALAR_TYPES) - {"string", "bytes"}

# Reserved words of C++ itself.  protoc appends an underscore to an accessor whose
# field name is one of these, and a generated parameter has to dodge them too.
_CPP_KEYWORDS = frozenset(
    """alignas alignof and and_eq asm auto bitand bitor bool break case catch char char8_t char16_t char32_t class
    compl concept const consteval constexpr constinit const_cast continue co_await co_return co_yield decltype default
    delete do double dynamic_cast else enum explicit export extern false float for friend goto if inline int long
    mutable namespace new noexcept not not_eq nullptr operator or or_eq private protected public register
    reinterpret_cast requires return short signed sizeof static static_assert static_cast struct switch template this
    thread_local throw true try typedef typeid typename union unsigned using virtual void volatile wchar_t while xor
    xor_eq""".split()
)

# Locals the generated client and server declare around a per-field parameter list.
# A parameter that shadowed one of these would compile but would not mean what the
# surrounding statement says, so it gets the same trailing underscore a keyword does.
_CPP_TEMPLATE_LOCALS = frozenset(
    """msg errMsg topic topicArgs topicParams payload payloadStr payloadHandler payloadHandlers signalPayload
    commandPayload commandProperties requestArgs returnPayload returnValue correlationData responseTopic responseFuture
    promise lock cb handler handlers value doc e out kv item itr ok future server client conn broker instanceId
    instanceInfo subscriptionId noSubId optContentType optCorrelationData optResponseTopic""".split()
)


class CppProtobufFieldSymbols(CppSymbols):
    """C++ symbols for one :class:`ProtobufField`.

    These say how protoc's generated class names the field -- what type it holds,
    what its accessors are called -- so that a generated per-field API can take the
    field as a parameter and put it on the message without the template knowing
    anything about protobuf's C++ backend.
    """

    def __init__(self, field):
        super().__init__()
        self._field = field

    @property
    def base_type(self) -> str:
        """The C++ type of one value of this field, before repetition or presence.

        A repeated field's element type, a map's value type, and the type inside the
        ``std::optional`` of a field with presence are all this.
        """
        from stingeripc.exceptions import InvalidStingerStructure

        field = self._field
        if field.kind == "group":
            raise InvalidStingerStructure(f"protobuf field '{field.name}' is a proto2 group, which the generated C++ API does not support.")
        if field.is_message or field.is_enum:
            if field.type_ref is None:
                raise InvalidStingerStructure(f"protobuf field '{field.name}' names the type '{field.type_name}', which was never resolved.")
            return field.type_ref.cpp.qualified_name
        scalar = _CPP_SCALAR_TYPES.get(field.kind)
        if scalar is None:
            raise InvalidStingerStructure(f"protobuf field '{field.name}' has the unsupported type '{field.kind}'.")
        return scalar

    @property
    def value_type(self) -> str:
        """The C++ type a caller holds this field's whole value in.

        A map is a ``std::map`` rather than protobuf's own ``Map``, and a repeated
        field a ``std::vector`` rather than a ``RepeatedField``: the generated API
        is the one the application writes against, so it speaks the standard library
        and the generated code converts at the boundary.
        """
        field = self._field
        if field.is_map:
            return f"std::map<{field.map_key.cpp.base_type}, {field.map_value.cpp.base_type}>"
        if field.repeated:
            return f"std::vector<{self.base_type}>"
        if field.is_optional_param:
            return f"std::optional<{self.base_type}>"
        return self.base_type

    @property
    def is_trivial(self) -> bool:
        """True for a singular value small enough to pass in a register."""
        field = self._field
        if field.repeated or field.is_map or field.is_optional_param:
            return False
        return field.is_enum or field.kind in _CPP_TRIVIAL_KINDS

    @property
    def param_type(self) -> str:
        """The C++ type this field is taken as by a generated function."""
        if self.is_trivial:
            return self.value_type
        return f"const {self.value_type}&"

    @property
    def param_name(self) -> str:
        """The name a generated function gives this field's parameter.

        lowerCamelCase like a JSON argument's, with a trailing underscore when that
        would collide with a C++ keyword or with a local the generated code declares
        around the parameter list.
        """
        name = stringmanip.lower_camel_case(self._field.name)
        if name in _CPP_KEYWORDS or name in _CPP_TEMPLATE_LOCALS:
            return f"{name}_"
        return name

    @property
    def accessor(self) -> str:
        """The stem protoc builds this field's accessors from.

        protoc lower-cases the field name and, when the result is a C++ keyword,
        appends an underscore -- so a field named ``class`` is read with ``class_()``
        and written with ``set_class_()``.
        """
        name = self._field.name.lower()
        if name in _CPP_KEYWORDS:
            return f"{name}_"
        return name

    @property
    def getter(self) -> str:
        """protoc's getter for this field."""
        return self.accessor

    @property
    def setter(self) -> str:
        """protoc's setter for this field."""
        return f"set_{self.accessor}"

    @property
    def adder(self) -> str:
        """protoc's appender for this repeated field."""
        return f"add_{self.accessor}"

    @property
    def mutable(self) -> str:
        """protoc's mutable accessor for this field."""
        return f"mutable_{self.accessor}"

    @property
    def has(self) -> str:
        """protoc's presence test for this field."""
        return f"has_{self.accessor}"

    @property
    def is_comparable(self) -> bool:
        """True when a generated test can compare this field with ``==``.

        Singular scalars only, and not the floating-point ones: an example value
        that survives a serialize/parse round trip exactly is what a check like that
        needs, and the aggregate kinds have no natural spelling for a literal.
        """
        field = self._field
        if field.repeated or field.is_map or field.is_optional_param or not field.is_scalar:
            return False
        return field.kind not in ("float", "double")

    def set_statement(self, msg: str, param: str) -> str:
        """C++ that puts the value of ``param`` onto the message named ``msg``.

        Each shape of field is written a different way -- a scalar through its
        setter, a message by assigning through ``mutable_``, a repeated field or a
        map an element at a time -- and a field with presence only when the caller
        supplied one.
        """
        field = self._field
        if field.is_map:
            return f"for (const auto& kv : {param}) {{ (*{msg}.{self.mutable}())[kv.first] = kv.second; }}"
        if field.repeated:
            if field.is_message:
                return f"for (const auto& item : {param}) {{ *{msg}.{self.adder}() = item; }}"
            return f"for (const auto& item : {param}) {{ {msg}.{self.adder}(item); }}"
        if field.is_optional_param:
            return f"if ({param}) {{ {self._singular_set(msg, f'*{param}')} }}"
        return self._singular_set(msg, param)

    def _singular_set(self, msg: str, value: str) -> str:
        if self._field.is_message:
            return f"*{msg}.{self.mutable}() = {value};"
        return f"{msg}.{self.setter}({value});"

    def extract_expr(self, msg: str) -> str:
        """A C++ expression reading this field's :attr:`value_type` off ``msg``.

        The aggregate kinds are copied out of protobuf's own containers, since a
        ``RepeatedField`` is not a ``std::vector`` and a map entry is not a
        ``std::pair``; a field with presence reads as an empty optional when unset.
        """
        field = self._field
        if field.is_map:
            return f"[&] {{ {self.value_type} out; for (const auto& kv : {msg}.{self.getter}()) {{ out.emplace(kv.first, kv.second); }} return out; }}()"
        if field.repeated:
            return f"{self.value_type}({msg}.{self.getter}().begin(), {msg}.{self.getter}().end())"
        if field.is_optional_param:
            return f"{msg}.{self.has}() ? {self.value_type}({msg}.{self.getter}()) : std::nullopt"
        return f"{msg}.{self.getter}()"

    def example_value(self, seed: int = 2) -> str:
        """A C++ literal a demo or a test can pass for this field.

        Only a singular scalar has one worth making up; anything else is left at the
        value an application would get from a default-constructed container, which
        for a field with presence means no value at all.
        """
        field = self._field
        if field.is_optional_param:
            return "std::nullopt"
        if field.repeated or field.is_map or field.is_message or field.is_enum:
            return f"{self.value_type}{{}}"
        return field.get_random_example_value(lang="cpp", seed=seed)
