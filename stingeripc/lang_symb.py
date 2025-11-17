
from jacobsjinjatoo import stringmanip
import stringcase

class ISymbolsProvider:

    def get_domain(self) -> str:
        return "example"

    def for_model(self, model_class_name:str, model) -> object|None:
        return None

class RustSymbolsProvider(ISymbolsProvider):

    def get_domain(self) -> str:
        return "rust"

    def for_model(self, model_class_name:str, model) -> object|None:
        if model_class_name == "StingerSpec":
            return RustInterfaceSymbols(model)
        return None

class PythonSymbolsProvider(ISymbolsProvider):

    def get_domain(self) -> str:
        return "python"

    def for_model(self, model_class_name:str, model) -> object|None:
        if model_class_name == "StingerSpec":
            return PythonInterfaceSymbols(model)
        elif model_class_name == "InterfaceStruct":
            return PythonStructSymbols(model)
        elif model_class_name == "Method":
            return PythonMethodSymbols(model)
        return None

class CppSymbolsProvider(ISymbolsProvider):

    def get_domain(self) -> str:
        return "cpp"

    def for_model(self, model_class_name:str, model) -> object|None:
        if model_class_name == "StingerSpec":
            return CppInterfaceSymbols(model)
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
        s = f"{stringcase.snakecase(self._iface.name)}_ipc"
        return s.replace('__', '_')

    @property
    def client_struct_name(self) -> str:
        """ Name of the rust struct for the interface client."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Client"

    @property
    def server_struct_name(self) -> str:
        """ Name of the struct for the interface server."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Server"

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

