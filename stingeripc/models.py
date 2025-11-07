from pydantic import BaseModel as PydanticBaseModel, Field
from typing import Optional, List, Dict, Literal
from enum import Enum
import importlib
from . import symbols
class BaseModel(PydanticBaseModel):
    @property
    def rust(self):
        # import symbols.rust module dynamically
        rust_mod = importlib.import_module("stingeripc.symbols.rust")
        symbols_class_name = f"{self.__class__.__name__}Symbols"
        symbols_class = getattr(rust_mod, symbols_class_name, None)
        if symbols_class is None:
            raise AttributeError(f"Symbols class '{symbols_class_name}' not found in symbols.rust")
        return symbols_class(self)

    @property
    def python(self):
        py_mod = importlib.import_module("stingeripc.symbols.python")
        symbols_class_name = f"{self.__class__.__name__}Symbols"
        symbols_class = getattr(py_mod, symbols_class_name, None)
        if symbols_class is None:
            raise AttributeError(f"Symbols class '{symbols_class_name}' not found in symbols.python")
        return symbols_class(self)
    
    @property
    def cpp(self):
        cpp_mod = importlib.import_module("stingeripc.symbols.cpp")
        symbols_class_name = f"{self.__class__.__name__}Symbols"
        symbols_class = getattr(cpp_mod, symbols_class_name, None)
        if symbols_class is None:
            raise AttributeError(f"Symbols class '{symbols_class_name}' not found in symbols.cpp")
        return symbols_class(self)

class SpecMetadata(BaseModel):
    version: str = Field(..., description="The version of the specification")

class InterfaceMetadata(BaseModel):
    name: str = Field(..., description="The name of the interface")
    version: str = Field(..., description="The version of the interface", pattern=r"^\d+\.\d+\.\d+$")
    title: Optional[str] = Field(None, description="A short title for the interface")
    summary: Optional[str] = Field(None, description="A brief summary of the interface")
    documentation: Optional[str] = Field(None, description="A brief description of the interface")

class ProtocolType(str, Enum):
    TCP = "tcp"
    WEBSOCKET = "websocket"

class InterfaceEnumValue(BaseModel):
    name: str = Field(..., description="The name of the enum value")
    description: Optional[str] = Field(None, description="A brief description of the enum value")

class InterfaceEnumSpec(BaseModel):
    values: List[InterfaceEnumValue] = Field(..., description="A list of enum values")
    documentation: Optional[str] = Field(None, description="A brief description of the enum")

class InterfaceEnum(BaseModel):
    name: str = Field(..., description="The name of the enum")
    spec: InterfaceEnumSpec = Field(..., description="The specification of the enum")

class GenericArg(BaseModel):
    name: str = Field(..., description="The name of the argument")
    documentation: Optional[str] = Field(None, description="A brief description of the argument")
    optional: Optional[bool] = Field(False, description="Whether the argument is optional")
    index: Optional[int] = Field(None, description="When exporting to a protocol buffer consumer, the index of each argument is required and must be unique")

class IntegerArg(GenericArg):
    type: Literal["integer"] = Field("integer", description="The type of the argument (integer)")

class NumberArg(GenericArg):
    type: Literal["float"] = Field("float", description="The type of the argument (number)")

class StringArg(GenericArg):
    type: Literal["string"] = Field("string", description="The type of the argument (string)")

class BooleanArg(GenericArg):
    type: Literal["boolean"] = Field("boolean", description="The type of the argument (boolean)")

class DateTimeArg(GenericArg):
    type: Literal["datetime"] = Field("datetime", description="The type of the argument (datetime)")

class DurationArg(GenericArg):
    type: Literal["duration"] = Field("duration", description="The type of the argument (duration)")

class BinaryArg(GenericArg):
    type: Literal["binary"] = Field("binary", description="The type of the argument (binary)")

class EnumArg(GenericArg):
    type: Literal["enum"] = Field("enum", description="The type of the argument (enum)")
    enumName: str = Field(..., description="The name of the enum type")

class StructArg(GenericArg):
    type: Literal["struct"] = Field("struct", description="The type of the argument (struct)")
    structName: str = Field(..., description="The name of the struct type")

class ListArg(GenericArg):
    type: Literal["list"] = Field("list", description="The type of the argument (list)")
    itemType: IntegerArg | NumberArg | StringArg | BooleanArg | DateTimeArg | DurationArg | BinaryArg | EnumArg | StructArg = Field(..., description="The type of items in the list")

AnyArg = IntegerArg | NumberArg | StringArg | BooleanArg | DateTimeArg | DurationArg | BinaryArg | EnumArg | StructArg | ListArg

class InterfaceStruct(BaseModel):
    name: str = Field(..., description="The name of the struct field")
    documentation: Optional[str] = Field(None, description="A brief description of the struct field")
    members: List[AnyArg] = Field(..., description="A list of members in the struct")

class ComponentExport(BaseModel):
    version: str = Field(..., description="The version of the component")
    consumers: List[str] = Field(..., description="A list of consumers for the component")

class InterfaceComponent(BaseModel):
    name: str = Field(..., description="The name of the component")
    documentation: Optional[str] = Field(None, description="A brief description of the component")

class InterfaceSignal(InterfaceComponent):
    payload: List[AnyArg] = Field([], description="A list of arguments for the signal")

class InterfaceMethod(InterfaceComponent):
    arguments: List[AnyArg] = Field([], description="A list of arguments for the method")
    returnValues: List[AnyArg] = Field([], description="A list of return values for the method")

class InterfaceProperty(InterfaceComponent):
    values: List[AnyArg] = Field(..., description="A list of values for the property")
    readOnly: Optional[bool] = Field(False, description="Whether the property is read-only")

class StingerSpec(BaseModel):
    stingeripc: SpecMetadata = Field(..., description="Metadata about the Stinger IPC specification")
    interface: InterfaceMetadata = Field(..., description="Metadata about the interface")
    enums: Optional[Dict[str, InterfaceEnum]] = Field(None, description="A dictionary of enums used in the interface")
    structs: Optional[Dict[str, InterfaceStruct]] = Field(None, description="A dictionary of structs used in the interface")
    signals: Optional[Dict[str, InterfaceSignal]] = Field(None, description="A dictionary of signals in the interface")
    methods: Optional[Dict[str, InterfaceMethod]] = Field(None, description="A dictionary of methods in the interface")
    properties: Optional[Dict[str, InterfaceProperty]] = Field(None, description="A dictionary of properties in the interface")
    