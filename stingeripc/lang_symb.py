
from jacobsjinjatoo import stringmanip
import stringcase

class PythonSymbols:
    def __init__(self):
        ...

    @property
    def type_definition_module(self) -> str:
        return "stinger_types"


class PythonInterfaceSymbols(PythonSymbols):

    def __init__(self, interface):
        super().__init__()
        self._iface = interface

    @property
    def package_name(self):
        return f"{stringmanip.lower_camel_case(self._iface.name).lower()}ipc"

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
    def client_package_name(self) -> str:
        """ Name of the rust package for the interface client."""
        return f"{stringcase.snakecase(self._iface.name)}_client"

    @property
    def server_package_name(self) -> str:
        """ Name of the rust package for the interface server."""
        return f"{stringcase.snakecase(self._iface.name)}_server"
    
    @property
    def common_package_name(self) -> str:
        """ Name of the rust package for the interface common types."""
        return f"{stringcase.snakecase(self._iface.name)}_types"

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