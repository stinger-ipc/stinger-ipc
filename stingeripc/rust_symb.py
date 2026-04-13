from typing import Any

from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.config import StingerConfig
from stingeripc.lang_symb import ISymbolsProvider


class RustSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "StingerSpec":
            return RustInterfaceSymbols(model, self.config)
        elif model_class_name == "InterfaceEnum":
            return RustEnumSymbols(model)
        elif model_class_name == "InterfaceStruct":
            return RustStructSymbols(model)
        elif model_class_name == "Method":
            return RustMethodSymbols(model)
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


class RustSymbols:

    def __init__(self, config: StingerConfig | None = None):
        self.config = config


class RustInterfaceSymbols(RustSymbols):

    def __init__(self, interface, config: StingerConfig | None = None):
        super().__init__(config)
        self._iface = interface

    @property
    def package_name(self) -> str:
        """ Name of the rust package for the interface client."""
        s = f"{stringmanip.snake_case(self._iface.name)}_{stringmanip.snake_case(self.config.rust.package_suffix) or 'ipc'}"  # type: ignore[union-attr]
        return s

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


class RustMethodSymbols(RustSymbols):

    def __init__(self, method):
        super().__init__()
        self._method = method

    @property
    def return_value_type(self) -> str:
        if self._method.return_value is None:
            return "()"
        elif isinstance(self._method.return_value, list):
            return stringmanip.upper_camel_case(self._method.return_value_name)
        return self._method.return_value.rust.type


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
