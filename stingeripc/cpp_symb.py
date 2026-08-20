from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.lang_symb import ISymbolsProvider


class CppSymbolsProvider(ISymbolsProvider):
    """Plugin that provides C++ symbols for model objects.

    Registers as the ``cpp`` language domain so templates can access C++ names
    and types via ``obj.cpp.<property>``.
    """

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "StingerSpec":
            return CppInterfaceSymbols(model)
        elif model_class_name == "IpcProperty":
            return CppPropertySymbols(model)
        elif model_class_name == "IpcMethod":
            return CppMethodSymbols(model)
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
    def property_struct_name(self) -> str:
        """C++ struct name generated for the property."""
        return f"{stringmanip.upper_camel_case(self._prop.name)}Property"


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
        return stringmanip.upper_camel_case(self._method.return_value_name)


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
