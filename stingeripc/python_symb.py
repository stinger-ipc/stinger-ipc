from typing import Any

from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.config import StingerConfig
from stingeripc.lang_symb import ISymbolsProvider


class PythonSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "StingerSpec":
            return PythonInterfaceSymbols(model, self.config)
        elif model_class_name == "InterfaceStruct":
            return PythonStructSymbols(model, self.config)
        elif model_class_name == "InterfaceEnum":
            return PythonEnumSymbols(model)
        elif model_class_name == "IpcMethod":
            return PythonMethodSymbols(model, self.config)
        elif model_class_name == "IpcProperty":
            return PythonPropertySymbols(model, self.config)
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

    def __init__(self, config: StingerConfig | None = None):
        self.config = config

    @property
    def type_definition_module(self) -> str:
        return "interface_types"


class PythonInterfaceSymbols(PythonSymbols):

    def __init__(self, interface, config: StingerConfig | None = None):
        super().__init__(config)
        self._iface = interface

    @property
    def package_directory(self) -> str:
        s = f"{stringmanip.lower_only(self._iface.name).lower()}{stringmanip.lower_only(self.config.python.package_suffix) or 'ipc'}"  # type: ignore[union-attr]
        return s

    @property
    def package_name(self):
        s = f"{stringmanip.hyphen_case(self._iface.name).lower()}-{stringmanip.hyphen_case(self.config.python.package_suffix) or 'ipc'}"  # type: ignore[union-attr]
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

    def __init__(self, iface_struct, config: StingerConfig | None = None):
        super().__init__(config)
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

    def __init__(self, method, config: StingerConfig | None = None):
        super().__init__(config)
        self._method = method

    @property
    def return_value_annotation(self) -> str:
        if self._method.return_value is None:
            return "None"
        if isinstance(self._method.return_value, list):
            return self.response_class_name
        return self._method.return_value.python.annotation

    @property
    def response_class_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self._method.name)}MethodResponse"

    @property
    def request_class_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self._method.name)}MethodRequest"


class PythonPropertySymbols(PythonSymbols):

    def __init__(self, prop, config: StingerConfig | None = None):
        super().__init__(config)
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
    def setter_value_annotation(self) -> str:
        if len(self._prop._arg_list) == 1:
            return f"Union[{self._prop._arg_list[0].python.annotation}, {self.model_class_name}]"
        else:
            return self.model_class_name

    @property
    def model_class_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self._prop.name)}Property"
