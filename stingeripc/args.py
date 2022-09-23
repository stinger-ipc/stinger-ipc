"""
An `Arg` one of the following:
 * An argument to a method
 * A component of the return type of a method
 * A component of a signal

An `Arg` can be defined in several different ways:
 * `Value` means that the type of the Arg is simply provided.
 * `Enum` means that the type of the Arg is an integer and the value of the integer is controlled by an enumerated list.
 * `JSON Schema` means that the value of the arg is controlled by a JSON schema.

When the `Arg` type is `Value` then it has an `ArgValueType` which controlls which type the arg is.
"""

from __future__ import annotations
from enum import Enum
from .exceptions import InvalidStingerStructure

class ArgType(Enum):
    UNKNOWN = 0
    VALUE = 1
    ENUM = 2
    JSON_SCHEMA = 3
    STRUCT = 4


class ArgValueType(Enum):
    BOOLEAN = 0
    INTEGER = 1
    FLOAT = 2
    STRING = 3

    @classmethod
    def from_string(cls, arg_type: str) -> ArgValueType:
        if hasattr(cls, arg_type.upper()):
            return getattr(cls, arg_type.upper())
        else:
            raise InvalidStingerStructure(f"No ArgType called '{arg_type}'")

    @classmethod
    def to_python_type(cls, arg_type: ArgValueType) -> str:
        if arg_type == cls.BOOLEAN:
            return "bool"
        elif arg_type == cls.INTEGER:
            return "int"
        elif arg_type == cls.FLOAT:
            return "float"
        elif arg_type == cls.STRING:
            return "str"
        raise InvalidStingerStructure("Unhandled arg type")

    @classmethod
    def to_rust_type(cls, arg_type: ArgValueType) -> str:
        if arg_type == cls.BOOLEAN:
            return "bool"
        elif arg_type == cls.INTEGER:
            return "i32"
        elif arg_type == cls.FLOAT:
            return "f32"
        elif arg_type == cls.STRING:
            return "String"
        raise InvalidStingerStructure("Unhandled arg type")

    @classmethod
    def to_json_type(cls, arg_type: ArgValueType) -> str:
        if arg_type == cls.BOOLEAN:
            return "boolean"
        elif arg_type == cls.INTEGER:
            return "integer"
        elif arg_type == cls.FLOAT:
            return "number"
        elif arg_type == cls.STRING:
            return "string"
        raise InvalidStingerStructure("Unhandled arg type")

    @classmethod
    def to_cpp_type(cls, arg_type: ArgValueType, ) -> str:
        if arg_type == cls.BOOLEAN:
            return "bool"
        elif arg_type == cls.INTEGER:
            return "int"
        elif arg_type == cls.FLOAT:
            return "double"
        elif arg_type == cls.STRING:
            return "const std::string&"
        raise InvalidStingerStructure("Unhandled arg type")

    @classmethod
    def to_cpp_rapidjson_type_str(cls, arg_type: ArgValueType) -> str:
        if arg_type == cls.BOOLEAN:
            return "Bool"
        elif arg_type == cls.INTEGER:
            return "Int"
        elif arg_type == cls.FLOAT:
            return "Double"
        elif arg_type == cls.STRING:
            return "String"
        raise InvalidStingerStructure("Unhandled arg type")