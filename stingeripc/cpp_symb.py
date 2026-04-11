from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.lang_symb import ISymbolsProvider


class CppSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "StingerSpec":
            return CppInterfaceSymbols(model)
        elif model_class_name == "Property":
            return CppPropertySymbols(model)
        elif model_class_name == "Method":
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
        return None


class CppSymbols:
    def __init__(self):
        pass


class CppInterfaceSymbols(CppSymbols):

    def __init__(self, interface):
        super().__init__()
        self._iface = interface

    @property
    def project_name(self) -> str:
        return f"{stringmanip.hyphen_case(self._iface.name)}-ipc"

    @property
    def cmake_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self._iface.name)}Ipc"

    @property
    def client_class_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self._iface.name)}Client"

    @property
    def server_class_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self._iface.name)}Server"

    @property
    def enum_header_file(self) -> str:
        return "enums.hpp"

    @property
    def property_struct_header_file(self) -> str:
        return "property_structs.hpp"


class CppPropertySymbols(CppSymbols):

    def __init__(self, prop):
        super().__init__()
        self._prop = prop

    @property
    def property_struct_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self._prop.name)}Property"


class CppMethodSymbols(CppSymbols):

    def __init__(self, method):
        super().__init__()
        self._method = method

    @property
    def return_value_class(self) -> str:
        from stingeripc.components import Arg, ArgPrimitive, ArgStruct
        if self._method._return_value is None:
            return "void"
        elif isinstance(self._method._return_value, Arg):
            if isinstance(self._method._return_value, ArgPrimitive) and self._method._return_value.type == ArgPrimitiveType.STRING:
                if self._method._return_value.optional:
                    return "std::optional<std::string>"
                return "std::string"
            elif isinstance(self._method._return_value, ArgStruct) and self._method._return_value.optional:
                return f"std::optional<{self._method._return_value.cpp.type}>"
            return self._method._return_value.cpp.type
        elif isinstance(self._method._return_value, list):
            return stringmanip.upper_camel_case(self._method.return_value_name)


class CppEnumSymbols(CppSymbols):

    def __init__(self, enum):
        super().__init__()
        self._enum = enum

    @property
    def type(self) -> str:
        return stringmanip.upper_camel_case(self._enum.name)

    @property
    def rapidjson_type(self) -> str:
        return ArgPrimitiveType.to_cpp_rapidjson_type_str(ArgPrimitiveType.INTEGER)


class CppStructSymbols(CppSymbols):

    def __init__(self, struct):
        super().__init__()
        self._struct = struct

    @property
    def type(self) -> str:
        return stringmanip.upper_camel_case(self._struct.name)


class CppArgSymbols(CppSymbols):
    """Base C++ symbols for Arg objects."""

    def __init__(self, arg):
        super().__init__()
        self._arg = arg

    @property
    def type(self) -> str:
        return stringmanip.upper_camel_case(self._arg.name)

    @property
    def temp_type(self) -> str:
        if self._arg.optional and "optional" not in self.type:
            return f"std::optional<{self.type}>"
        return self.type

    @property
    def func_param_type(self) -> str:
        if self._arg.optional and "optional" not in self.type:
            return f"std::optional<{self.type}>"
        return self.type


class CppArgEnumSymbols(CppArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return f"std::optional<{self._arg.enum.cpp.type}>"
        return self._arg.enum.cpp.type

    @property
    def temp_type(self) -> str:
        return self.type

    @property
    def data_type(self) -> str:
        return self._arg.enum.cpp.type

    @property
    def rapidjson_type(self) -> str:
        return ArgPrimitiveType.to_cpp_rapidjson_type_str(ArgPrimitiveType.INTEGER)


class CppArgPrimitiveSymbols(CppArgSymbols):

    @property
    def type(self) -> str:
        return ArgPrimitiveType.to_cpp_type(self._arg.primitive_type, optional=self._arg.optional)

    @property
    def temp_type(self) -> str:
        if self._arg.primitive_type == ArgPrimitiveType.STRING:
            if self._arg.optional:
                return "std::optional<std::string>"
            return "std::string"
        return self.type

    @property
    def rapidjson_type(self) -> str:
        return ArgPrimitiveType.to_cpp_rapidjson_type_str(self._arg.primitive_type)


class CppArgStructSymbols(CppArgSymbols):

    @property
    def type(self) -> str:
        return self._arg.interface_struct.cpp.type

    @property
    def rapidjson_type(self) -> str:
        return "Object"


class CppArgDateTimeSymbols(CppArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return "std::optional<std::chrono::time_point<std::chrono::system_clock>>"
        return "std::chrono::time_point<std::chrono::system_clock>"

    @property
    def temp_type(self) -> str:
        return self.type

    @property
    def rapidjson_type(self) -> str:
        return "String"


class CppArgDurationSymbols(CppArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return "std::optional<std::chrono::duration<double>>"
        return "std::chrono::duration<double>"

    @property
    def temp_type(self) -> str:
        return self.type

    @property
    def rapidjson_type(self) -> str:
        return "String"


class CppArgBinarySymbols(CppArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return "std::optional<std::vector<uint8_t>>"
        return "std::vector<uint8_t>"

    @property
    def temp_type(self) -> str:
        return self.type

    @property
    def rapidjson_type(self) -> str:
        return "String"


class CppArgArraySymbols(CppArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return f"std::optional<std::vector<{self._arg.element.cpp.temp_type}>>"
        return f"std::vector<{self._arg.element.cpp.temp_type}>"

    @property
    def rapidjson_type(self) -> str:
        return "Array"
