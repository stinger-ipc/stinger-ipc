
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum  

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

class InterfacEnumValue(BaseModel):
    name: str = Field(..., description="The name of the enum value")
    description: Optional[str] = Field(None, description="A brief description of the enum value")

class InterfaceEnum(BaseModel):
    values: List[InterfacEnumValue] = Field(..., description="A list of enum values")
    documentation: Optional[str] = Field(None, description="A brief description of the enum")

class GenericArg(BaseModel):
    name: str = Field(..., description="The name of the argument")
    documentation: Optional[str] = Field(None, description="A brief description of the argument")
    optional: Optional[bool] = Field(False, description="Whether the argument is optional")
    index: Optional[int] = Field(None, description="When exporting to a protocol buffer consumer, the index of each argument is required and must be unique")

class IntegerArg(GenericArg):
    type: str = Field("integer", const=True, description="The type of the argument (integer)")

class NumberArg(GenericArg):
    type: str = Field("float", const=True, description="The type of the argument (number)")

class StringArg(GenericArg):
    type: str = Field("string", const=True, description="The type of the argument (string)")

class BooleanArg(GenericArg):
    type: str = Field("boolean", const=True, description="The type of the argument (boolean)")

class DateTimeArg(GenericArg):
    type: str = Field("datetime", const=True, description="The type of the argument (datetime)")

class DurationArg(GenericArg):
    type: str = Field("duration", const=True, description="The type of the argument (duration)")

class BinaryArg(GenericArg):
    type: str = Field("binary", const=True, description="The type of the argument (binary)")

class EnumArg(GenericArg):
    type: str = Field("enum", const=True, description="The type of the argument (enum)")
    enumName: str = Field(..., description="The name of the enum type")

class StructArg(GenericArg):
    type: str = Field("struct", const=True, description="The type of the argument (struct)")
    structName: str = Field(..., description="The name of the struct type")

class ListArg(GenericArg):
    type: str = Field("list", const=True, description="The type of the argument (list)")
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
    brokers: Optional[List[Broker]] = Field(None, description="A list of brokers for the interface")
    enums: Optional[Dict[str, InterfaceEnum]] = Field(None, description="A dictionary of enums used in the interface")
    structs: Optional[Dict[str, InterfaceStruct]] = Field(None, description="A dictionary of structs used in the interface")