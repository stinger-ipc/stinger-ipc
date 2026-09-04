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
        """C++ type that the method's handler returns, or ``void`` when it returns nothing."""
        from stingeripc.components import ArgPrimitive, ArgStruct

        return_value = self._method.return_value
        if return_value is None:
            return "void"
        if isinstance(return_value, ArgPrimitive) and return_value.type == ArgPrimitiveType.STRING:
            if return_value.optional:
                return "std::optional<std::string>"
            return "std::string"
        if isinstance(return_value, ArgStruct) and return_value.optional:
            return f"std::optional<{return_value.cpp.type}>"  # type: ignore[attr-defined]
        return return_value.cpp.type  # type: ignore[attr-defined]

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
