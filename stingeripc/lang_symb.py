
from jacobsjinjatoo import stringmanip
from typing import Any
from stingeripc.args import ArgPrimitiveType
from stingeripc.exceptions import InvalidStingerStructure

class ISymbolsProvider:
    """ An ISymbolsProvider is an interface for classes providing symbols and names for a specific plugin or language.
    The plugin system will check for plugins implementing ISymbolsProvider to know how to use them.

    The plugin uses the `project.entry-points."stinger_symbols"` entry point to find classes that implement this interface.  
    """

    def __init__(self, config: dict[str, Any]|None = None):
        """ The constructor takes stinger generation configuration as an argument."""
        self.config = config

    def for_model(self, model_class_name:str, model) -> object|None:
        """ This should return an object containing symbols for the given model, or None if this provider does not handle that model class. """
        return None

class ModelSymbols:
    
    def __init__(self, model):
        self._model = model
    
class RustSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name:str, model) -> object|None:
        if model_class_name == "StingerSpec":
            return RustInterfaceSymbols(model, self.config)
        return None

class PythonSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name:str, model) -> object|None:
        if model_class_name == "StingerSpec":
            return PythonInterfaceSymbols(model, self.config)
        elif model_class_name == "InterfaceStruct":
            return PythonStructSymbols(model, self.config)
        elif model_class_name == "Method":
            return PythonMethodSymbols(model, self.config)
        elif model_class_name == "Property":
            return PythonPropertySymbols(model, self.config)
        return None

class PythonSymbols:

    def __init__(self, config: dict[str, Any]|None = None):
        self.config = config

    @property
    def type_definition_module(self) -> str:
        return "interface_types"


class PythonInterfaceSymbols(PythonSymbols):

    def __init__(self, interface, config: dict[str, Any]|None = None):
        super().__init__(config)
        self._iface = interface

    @property
    def package_directory(self) -> str:
        s = f"{stringmanip.lower_only(self._iface.name).lower()}{stringmanip.lower_only(self.config.python.package_suffix or 'ipc')}"
        return s

    @property
    def package_name(self):
        s = f"{stringmanip.hyphen_case(self._iface.name).lower()}-{stringmanip.hyphen_case(self.config.python.package_suffix or 'ipc')}"
        return s

    @property
    def module_name(self) -> str:
        return self.package_directory

    @property
    def client_class_name(self) -> str:
        """ Name of the python class for the interface client."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Client"

    @property
    def server_class_name(self) -> str:
        """ Name of the python class for the interface server."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Server"


class PythonStructSymbols(PythonSymbols):

    def __init__(self, iface_struct, config: dict[str, Any]|None = None):
        super().__init__(config)
        self._iface_struct = iface_struct


class PythonMethodSymbols(PythonSymbols):

    def __init__(self, method, config: dict[str, Any]|None = None):
        super().__init__(config)
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

    def __init__(self, prop, config: dict[str, Any]|None = None):
        super().__init__(config)
        self._prop = prop

    @property
    def getter_value_annotation(self) -> str:
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].python_annotation
        else:
            return self.model_class_name

    @property
    def setter_value_annotation(self) -> str:
        if len(self._prop._arg_list) == 1:
            return f"Union[{self._prop._arg_list[0].python_annotation}, {self.model_class_name}]"
        else:
            return self.model_class_name

    @property
    def model_class_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self._prop.name)}Property"

class RustSymbols:

    def __init__(self, config: dict[str, Any]|None = None):
        self.config = config
        

class RustInterfaceSymbols(RustSymbols):

    def __init__(self, interface, config: dict[str, Any]|None = None):
        super().__init__(config)
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

class CppSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name:str, model) -> object|None:
        if model_class_name == "StingerSpec":
            return CppInterfaceSymbols(model)
        elif model_class_name == "Property":
            return CppPropertySymbols(model)
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