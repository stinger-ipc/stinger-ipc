from typing import Any

from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.config import StingerConfig
from stingeripc.lang_symb import ISymbolsProvider


class PythonSymbolsProvider(ISymbolsProvider):
    """Plugin that provides Python symbols for model objects.

    Registers as the ``python`` language domain so templates can access Python
    names and types via ``obj.python.<property>``.
    """

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
        elif model_class_name == "InterfaceConstant":
            return PythonConstantSymbols(model)
        return None


class PythonSymbols:
    """Base class for Python symbol providers.

    Holds the generation ``config`` (used to derive package names and
    suffixes) and exposes shared properties such as the type-definition module
    name.
    """

    def __init__(self, config: StingerConfig | None = None):
        self.config = config

    @property
    def type_definition_module(self) -> str:
        """Name of the module that defines the interface's data types."""
        return "interface_types"


class PythonInterfaceSymbols(PythonSymbols):
    """Python symbols for the top-level :class:`StingerSpec` (the interface)."""

    def __init__(self, interface, config: StingerConfig | None = None):
        super().__init__(config)
        self._iface = interface

    @property
    def package_directory(self) -> str:
        """Name of the generated Python package directory."""
        s = f"{stringmanip.lower_only(self._iface.name).lower()}{stringmanip.lower_only(self.config.python.package_suffix) or 'ipc'}"  # type: ignore[union-attr]
        return s

    @property
    def package_name(self):
        """Distribution name of the generated Python package."""
        s = f"{stringmanip.hyphen_case(self._iface.name).lower()}-{stringmanip.hyphen_case(self.config.python.package_suffix) or 'ipc'}"  # type: ignore[union-attr]
        return s

    @property
    def module_name(self) -> str:
        """Importable module name of the generated package (same as ``package_directory``)."""
        return self.package_directory

    @property
    def client_class_name(self) -> str:
        """Name of the python class for the interface client."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Client"

    @property
    def server_class_name(self) -> str:
        """Name of the python class for the interface server."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Server"


class PythonStructSymbols(PythonSymbols):
    """Python symbols for an :class:`InterfaceStruct`."""

    def __init__(self, iface_struct, config: StingerConfig | None = None):
        super().__init__(config)
        self._iface_struct = iface_struct

    @property
    def type(self) -> str:
        """Fully-qualified Python type name for the struct."""
        return stringmanip.upper_camel_case(self._iface_struct.name)

    @property
    def local_type(self) -> str:
        """Unqualified Python class name for the struct."""
        return stringmanip.upper_camel_case(self._iface_struct.name)


class PythonEnumSymbols(PythonSymbols):
    """Python symbols for an :class:`InterfaceEnum`."""

    def __init__(self, enum):
        super().__init__()
        self._enum = enum

    @property
    def type(self) -> str:
        """Fully-qualified Python type name for the enum."""
        return stringmanip.upper_camel_case(self._enum.name)

    @property
    def local_type(self) -> str:
        """Unqualified Python class name for the enum."""
        return stringmanip.upper_camel_case(self._enum.name)


class PythonArgSymbols(PythonSymbols):
    """Base Python symbols for Arg objects."""

    def __init__(self, arg):
        super().__init__()
        self._arg = arg

    @property
    def type(self) -> str:
        """Python type name for this argument."""
        return self._arg.name

    @property
    def class_name(self) -> str:
        """Python class name for this argument's type."""
        return self.type

    @property
    def local_type(self) -> str:
        """Unqualified Python type name for this argument."""
        return self.type.split(".")[-1]

    @property
    def annotation(self) -> str:
        """Python type annotation for this argument."""
        return self.class_name


class PythonArgEnumSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgEnum`."""

    @property
    def type(self) -> str:
        """Python type name of the referenced enum."""
        return self._arg.enum.python.type

    @property
    def local_type(self) -> str:
        """Unqualified Python type name of the referenced enum."""
        return self._arg.enum.python.local_type

    @property
    def class_name(self) -> str:
        """Python class name of the referenced enum."""
        return self._arg.enum.python.type

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return f"Optional[{self._arg.enum.python.type}]"
        return self._arg.enum.python.type


class PythonArgPrimitiveSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgPrimitive`."""

    @property
    def type(self) -> str:
        """Python type name for the primitive (e.g. ``int``)."""
        return ArgPrimitiveType.to_python_type(self._arg.primitive_type)

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        return ArgPrimitiveType.to_python_type(self._arg.primitive_type, optional=self._arg.optional)


class PythonArgStructSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgStruct`."""

    @property
    def type(self) -> str:
        """Python type name of the referenced struct."""
        return self._arg.interface_struct.python.local_type

    @property
    def local_type(self) -> str:
        """Unqualified Python type name of the referenced struct."""
        return self._arg.interface_struct.python.local_type

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return f"Optional[{self.type}]"
        return self.type


class PythonArgDateTimeSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgDateTime`."""

    @property
    def type(self) -> str:
        """Python type name for datetimes (``datetime``)."""
        return "datetime"

    @property
    def local_type(self) -> str:
        """Unqualified Python type name for datetimes (``datetime``)."""
        return "datetime"

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return "Optional[datetime]"
        return "datetime"


class PythonArgDurationSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgDuration`."""

    @property
    def type(self) -> str:
        """Python type name for durations (``timedelta``)."""
        return "timedelta"

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return "Optional[timedelta]"
        return "timedelta"


class PythonArgBinarySymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgBinary`."""

    @property
    def type(self) -> str:
        """Python type name for binary data (``bytes``)."""
        return "bytes"

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return f"Optional[{self.type}]"
        return self.type


class PythonArgArraySymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgArray`."""

    @property
    def type(self) -> str:
        """Python type name for arrays (``list``)."""
        return "list"

    @property
    def annotation(self) -> str:
        """Python type annotation of the element list, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return f"Optional[List[{self._arg.element.python.annotation}]]"
        return f"List[{self._arg.element.python.annotation}]"


class PythonConstantSymbols(PythonSymbols):
    """Python symbols for an :class:`InterfaceConstant`."""

    def __init__(self, constant):
        super().__init__()
        self._constant = constant

    @property
    def type(self) -> str:
        """Python type name for the constant's declared type."""
        type_map = {
            "integer": "int",
            "float": "float",
            "boolean": "bool",
            "string": "str",
        }
        return type_map.get(self._constant.constant_type, "str")

    @property
    def local_type(self) -> str:
        """Unqualified Python type name for the constant."""
        return self.type


class PythonMethodSymbols(PythonSymbols):
    """Python symbols for an :class:`IpcMethod`."""

    def __init__(self, method, config: StingerConfig | None = None):
        super().__init__(config)
        self._method = method

    @property
    def return_value_annotation(self) -> str:
        """Python return type annotation for the method's return value(s)."""
        if self._method.return_value is None:
            return "None"
        if isinstance(self._method.return_value, list):
            return self.response_class_name
        return self._method.return_value.python.annotation

    @property
    def response_class_name(self) -> str:
        """Python class name of the generated method response payload."""
        return f"{stringmanip.upper_camel_case(self._method.name)}MethodResponse"

    @property
    def request_class_name(self) -> str:
        """Python class name of the generated method request payload."""
        return f"{stringmanip.upper_camel_case(self._method.name)}MethodRequest"


class PythonPropertySymbols(PythonSymbols):
    """Python symbols for an :class:`IpcProperty`."""

    def __init__(self, prop, config: StingerConfig | None = None):
        super().__init__(config)
        self._prop = prop

    @property
    def class_name(self) -> str:
        """Python class name for the property's value type."""
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].python.class_name
        else:
            return f"{stringmanip.upper_camel_case(self._prop.name)}Property"

    @property
    def type(self) -> str:
        """Python type name for the property's value."""
        return self.class_name

    @property
    def local_type(self) -> str:
        """Unqualified Python type name for the property's value."""
        return self.class_name.split(".")[-1]

    @property
    def annotation(self) -> str:
        """Python type annotation for the property's value."""
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].python.annotation
        else:
            return f"{stringmanip.upper_camel_case(self._prop.name)}Property"

    @property
    def getter_value_annotation(self) -> str:
        """Python type annotation used by the property getter."""
        if len(self._prop._arg_list) == 1:
            return self._prop._arg_list[0].python.annotation
        return self.model_class_name

    @property
    def setter_value_annotation(self) -> str:
        """Python type annotation used by the property setter."""
        if len(self._prop._arg_list) == 1:
            return f"Union[{self._prop._arg_list[0].python.annotation}, {self.model_class_name}]"
        else:
            return self.model_class_name

    @property
    def model_class_name(self) -> str:
        """Python class name of the generated property model."""
        return f"{stringmanip.upper_camel_case(self._prop.name)}Property"
