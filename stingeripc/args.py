"""
An `Arg` is used in one of the following contexts:
 * An argument to a method
 * A component of the return type of a method
 * A component of a signal
 * A component of a property

An `Arg` can be defined in several different ways:
 * `Primitive` means that the type of the Arg is a primitive type that is directly provided.
 * `Enum` means that the type of the Arg is an integer and the value of the integer is controlled by an enumerated list.
 * `Struct` means that the type of the Arg is a structure make up of additional args.

When the `Arg` type is `Primitive` then it has an `ArgPrimitiveType` which controlls which type the arg is.
"""

from __future__ import annotations
from enum import Enum
from .exceptions import InvalidStingerStructure


class ArgType(Enum):
    UNKNOWN = 0
    PRIMITIVE = 1
    ENUM = 2
    STRUCT = 3
    DATETIME = 4
    DURATION = 5
    BINARY = 6
    ARRAY = 7


class ArgPrimitiveType(Enum):
    """This is not an Arg, rather it is an enumeration of different primitives that an ArgPrimitive can represent."""

    BOOLEAN = 0
    INTEGER = 1
    FLOAT = 2
    STRING = 3

    @classmethod
    def from_string(cls, arg_type: str) -> ArgPrimitiveType:
        if hasattr(cls, arg_type.upper()):
            return getattr(cls, arg_type.upper())
        else:
            raise InvalidStingerStructure(f"No ArgType called '{arg_type}'")

    @classmethod
    def to_python_type(cls, arg_type: ArgPrimitiveType, optional: bool = False) -> str:
        if optional:
            return f"Optional[{cls.to_python_type(arg_type, optional=False)}]"
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
    def to_rust_type(cls, arg_type: ArgPrimitiveType, optional: bool = False) -> str:
        if optional:
            return f"Option<{cls.to_rust_type(arg_type, optional=False)}>"
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
    def to_json_type(cls, arg_type: ArgPrimitiveType) -> str:
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
    def to_cpp_type(cls, arg_type: ArgPrimitiveType, optional: bool = False) -> str:
        if arg_type == cls.BOOLEAN:
            if optional:
                return "boost::optional<bool>"
            else:
                return "bool"
        elif arg_type == cls.INTEGER:
            if optional:
                return "boost::optional<int>"
            else:
                return "int"
        elif arg_type == cls.FLOAT:
            if optional:
                return "boost::optional<double>"
            else:
                return "double"
        elif arg_type == cls.STRING:
            if optional:
                return "boost::optional<std::string>"
            else:
                return "const std::string&"
        raise InvalidStingerStructure("Unhandled arg type")

    @classmethod
    def to_cpp_rapidjson_type_str(cls, arg_type: ArgPrimitiveType) -> str:
        if arg_type == cls.BOOLEAN:
            return "Bool"
        elif arg_type == cls.INTEGER:
            return "Int"
        elif arg_type == cls.FLOAT:
            return "Double"
        elif arg_type == cls.STRING:
            return "String"
        raise InvalidStingerStructure("Unhandled arg type")

    @classmethod
    def to_protobuf_type(cls, arg_type: ArgPrimitiveType) -> str:
        if arg_type == cls.BOOLEAN:
            return "bool"
        elif arg_type == cls.INTEGER:
            return "int32"
        elif arg_type == cls.FLOAT:
            return "float"
        elif arg_type == cls.STRING:
            return "string"
        raise InvalidStingerStructure("Unhandled arg type")