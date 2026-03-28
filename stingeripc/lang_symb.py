
from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.exceptions import InvalidStingerStructure

class ISymbolsProvider:

    def for_model(self, model_class_name:str, model) -> object|None:
        return None

class ModelSymbols:
    
    def __init__(self, model):
        self._model = model
    
class RustSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name:str, model) -> object|None:
        if model_class_name == "StingerSpec":
            return RustInterfaceSymbols(model)
        elif model_class_name == "InterfaceEnum":
            return RustEnumSymbols(model)
        elif model_class_name == "InterfaceStruct":
            return RustStructSymbols(model)
        elif model_class_name == "Property":
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
        return None


class PythonSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name:str, model) -> object|None:
        if model_class_name == "StingerSpec":
            return PythonInterfaceSymbols(model)
        elif model_class_name == "InterfaceStruct":
            return PythonStructSymbols(model)
        elif model_class_name == "InterfaceEnum":
            return PythonEnumSymbols(model)
        elif model_class_name == "Method":
            return PythonMethodSymbols(model)
        elif model_class_name == "Property":
            return PythonPropertySymbols(model)
        elif model_class_name == "ArgEnum":
            return PythonArgEnumSymbols(model)
        elif model_class_name == "ArgPrimitive":
            return PythonArgPrimitiveSymbols(model)
        elif model_class_name == "ArgStruct":
            return PythonArgStructSymbols(model)
        elif model_class_name == "ArgDateTime":
            return PythonArgDateTimeSymbols(model)
        elif model_class_name == "ArgDuration":
            return PythonArgDurationSymbols(model)
        elif model_class_name == "ArgBinary":
            return PythonArgBinarySymbols(model)
        elif model_class_name == "ArgArray":
            return PythonArgArraySymbols(model)
        return None

class PythonSymbols:

    def __init__(self):
        ...

    @property
    def type_definition_module(self) -> str:
        return "interface_types"


class PythonInterfaceSymbols(PythonSymbols):

    def __init__(self, interface):
        super().__init__()
        self._iface = interface

    @property
    def package_name(self):
        s = f"{stringmanip.lower_camel_case(self._iface.name).lower()}ipc"
        return s.replace('__', '_')

    @property
    def client_class_name(self) -> str:
        """ Name of the python class for the interface client."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Client"

    @property
    def server_class_name(self) -> str:
        """ Name of the python class for the interface server."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Server"


class PythonStructSymbols(PythonSymbols):

    def __init__(self, iface_struct):
        super().__init__()
        self._iface_struct = iface_struct

    @property
    def type(self) -> str:
        return stringmanip.upper_camel_case(self._iface_struct.name)

    @property
    def local_type(self) -> str:
        return stringmanip.upper_camel_case(self._iface_struct.name)


class PythonEnumSymbols(PythonSymbols):

    def __init__(self, enum):
        super().__init__()
        self._enum = enum

    @property
    def type(self) -> str:
        return stringmanip.upper_camel_case(self._enum.name)

    @property
    def local_type(self) -> str:
        return stringmanip.upper_camel_case(self._enum.name)


class PythonArgSymbols(PythonSymbols):
    """Base Python symbols for Arg objects."""

    def __init__(self, arg):
        super().__init__()
        self._arg = arg

    @property
    def type(self) -> str:
        return self._arg.name

    @property
    def class_name(self) -> str:
        return self.type

    @property
    def local_type(self) -> str:
        return self.type.split(".")[-1]

    @property
    def annotation(self) -> str:
        return self.class_name


class PythonArgEnumSymbols(PythonArgSymbols):

    @property
    def type(self) -> str:
        return self._arg.enum.python.type

    @property
    def local_type(self) -> str:
        return self._arg.enum.python.local_type

    @property
    def class_name(self) -> str:
        return self._arg.enum.python.type

    @property
    def annotation(self) -> str:
        if self._arg.optional:
            return f"Optional[{self._arg.enum.python.type}]"
        return self._arg.enum.python.type


class PythonArgPrimitiveSymbols(PythonArgSymbols):

    @property
    def type(self) -> str:
        return ArgPrimitiveType.to_python_type(self._arg.primitive_type)

    @property
    def annotation(self) -> str:
        return ArgPrimitiveType.to_python_type(self._arg.primitive_type, optional=self._arg.optional)


class PythonArgStructSymbols(PythonArgSymbols):

    @property
    def type(self) -> str:
        return self._arg.interface_struct.python.local_type

    @property
    def local_type(self) -> str:
        return self._arg.interface_struct.python.local_type

    @property
    def annotation(self) -> str:
        if self._arg.optional:
            return f"Optional[{self.type}]"
        return self.type


class PythonArgDateTimeSymbols(PythonArgSymbols):

    @property
    def type(self) -> str:
        return "datetime"

    @property
    def local_type(self) -> str:
        return "datetime"

    @property
    def annotation(self) -> str:
        if self._arg.optional:
            return "Optional[datetime]"
        return "datetime"


class PythonArgDurationSymbols(PythonArgSymbols):

    @property
    def type(self) -> str:
        return "timedelta"

    @property
    def annotation(self) -> str:
        if self._arg.optional:
            return "Optional[timedelta]"
        return "timedelta"


class PythonArgBinarySymbols(PythonArgSymbols):

    @property
    def type(self) -> str:
        return "bytes"

    @property
    def annotation(self) -> str:
        if self._arg.optional:
            return f"Optional[{self.type}]"
        return self.type


class PythonArgArraySymbols(PythonArgSymbols):

    @property
    def type(self) -> str:
        return "list"

    @property
    def annotation(self) -> str:
        if self._arg.optional:
            return f"Optional[List[{self._arg.element.python.annotation}]]"
        return f"List[{self._arg.element.python.annotation}]"


class PythonMethodSymbols(PythonSymbols):

    def __init__(self, method):
        super().__init__()
        self._method = method
    
    @property
    def return_value_annotation(self) -> str:
        return self._method.return_value_python_type
    
    @property
    def return_value_local_class(self) -> str:
        return f"{stringmanip.upper_camel_case(self._method.name)}ReturnValue"

    @property
    def return_value_class(self):
        return f"{self.type_definition_module}.{self.return_value_local_class}"

class PythonPropertySymbols(PythonSymbols):

    def __init__(self, prop):
        super().__init__()
        self._prop = prop

    @property
    def class_name(self) -> str:
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].python.class_name
        else:
            return f"{stringmanip.upper_camel_case(self._prop.name)}Property"

    @property
    def type(self) -> str:
        return self.class_name

    @property
    def local_type(self) -> str:
        return self.class_name.split(".")[-1]

    @property
    def annotation(self) -> str:
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].python.annotation
        else:
            return f"{stringmanip.upper_camel_case(self._prop.name)}Property"

    @property
    def getter_value_annotation(self) -> str:
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].python.annotation
        return self.model_class_name

    @property
    def getter_value_annotation(self) -> str:
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].python.annotation
        else:
            return self.model_class_name

    @property
    def setter_value_annotation(self) -> str:
        if len(self._prop._arg_list) == 1:
            return f"Union[{self._prop._arg_list[0].python.annotation}, {self.model_class_name}]"
        else:
            return self.model_class_name

    @property
    def model_class_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self._prop.name)}Property"

class RustSymbols:
    def __init__(self):
        pass

class RustInterfaceSymbols(RustSymbols):

    def __init__(self, interface):
        super().__init__()
        self._iface = interface

    @property
    def package_name(self) -> str:
        """ Name of the rust package for the interface client."""
        s = f"{stringmanip.snake_case(self._iface.name)}_ipc"
        return s.replace('__', '_')

    @property
    def client_struct_name(self) -> str:
        """ Name of the rust struct for the interface client."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Client"

    @property
    def server_struct_name(self) -> str:
        """ Name of the struct for the interface server."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Server"

class RustEnumSymbols(RustSymbols):

    def __init__(self, enum):
        super().__init__()
        self._enum = enum

    @property
    def local_type(self) -> str:
        return stringmanip.upper_camel_case(self._enum.name)

    @property
    def type(self) -> str:
        return self.local_type


class RustStructSymbols(RustSymbols):

    def __init__(self, struct):
        super().__init__()
        self._struct = struct

    @property
    def local_type(self) -> str:
        return stringmanip.upper_camel_case(self._struct.name)

    @property
    def type(self) -> str:
        return self.local_type


class RustArgSymbols(RustSymbols):
    """Base Rust symbols for Arg objects."""

    def __init__(self, arg):
        super().__init__()
        self._arg = arg

    @property
    def type(self) -> str:
        return self._arg.name

    @property
    def local_type(self) -> str:
        return self.type


class RustArgEnumSymbols(RustArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return f"Option<{self._arg.enum.rust.type}>"
        return self._arg.enum.rust.type

    @property
    def local_type(self) -> str:
        if self._arg.optional:
            return f"Option<{self._arg.enum.rust.local_type}>"
        return self._arg.enum.rust.local_type


class RustArgPrimitiveSymbols(RustArgSymbols):

    @property
    def type(self) -> str:
        return ArgPrimitiveType.to_rust_type(self._arg.primitive_type, optional=self._arg.optional)


class RustArgStructSymbols(RustArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return f"Option<{self._arg.interface_struct.rust.type}>"
        return self._arg.interface_struct.rust.type

    @property
    def local_type(self) -> str:
        if self._arg.optional:
            return f"Option<{self._arg.interface_struct.rust.local_type}>"
        return self._arg.interface_struct.rust.local_type

    @property
    def temp_type(self) -> str:
        return self._arg.interface_struct.rust.local_type


class RustArgDateTimeSymbols(RustArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return "Option<chrono::DateTime<chrono::Utc>>"
        return "chrono::DateTime<chrono::Utc>"


class RustArgDurationSymbols(RustArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return "Option<chrono::Duration>"
        return "chrono::Duration"


class RustArgBinarySymbols(RustArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return "Option<Vec<u8>>"
        return "Vec<u8>"


class RustArgArraySymbols(RustArgSymbols):

    @property
    def type(self) -> str:
        if self._arg.optional:
            return f"Option<Vec<{self._arg.element.rust.type}>>"
        return f"Vec<{self._arg.element.rust.type}>"


class RustPropertySymbols(RustSymbols):

    def __init__(self, prop):
        super().__init__()
        self._prop = prop

    @property
    def local_type(self) -> str:
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].rust.local_type
        return f"{stringmanip.upper_camel_case(self._prop.name)}Property"

    @property
    def type(self) -> str:
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].rust.type
        return self.local_type


class CppSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name:str, model) -> object|None:
        if model_class_name == "StingerSpec":
            return CppInterfaceSymbols(model)
        elif model_class_name == "Property":
            return CppPropertySymbols(model)
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


class CppEnumSymbols(CppSymbols):

    def __init__(self, enum):
        super().__init__()
        self._enum = enum

    @property
    def type(self) -> str:
        return stringmanip.upper_camel_case(self._enum.name)


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
