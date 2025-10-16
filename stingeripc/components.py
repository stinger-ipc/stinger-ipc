from __future__ import annotations
from enum import Enum
import random
import stringcase
from abc import abstractmethod
from typing import Any, Optional
from .topic import (
    SignalTopicCreator,
    InterfaceTopicCreator,
    MethodTopicCreator,
    PropertyTopicCreator,
)
from .lang_symb import *
from .args import ArgType, ArgPrimitiveType
from .exceptions import InvalidStingerStructure
from jacobsjinjatoo import stringmanip

YamlArg = dict[str, str | bool]
YamlArgList = list[YamlArg]
YamlIfaceEnum = dict[str, str | YamlArgList]
YamlIfaceEnums = dict[str, YamlIfaceEnum]
YamlIfaceProperty = dict[str, str | bool | YamlArgList]

RESTRICTED_NAMES = ["type", "class", "struct", "enum", "list", "map", "set", "optional", "bool", "int", "float", "string", "datetime", "duration", "binary"]


class Arg:
    def __init__(self, name: str, description: Optional[str] = None):
        self._name = name
        self._description = description.strip()
        self._default_value = None
        self._type: ArgType = ArgType.UNKNOWN
        self._optional: bool = False

    def set_description(self, description: str) -> Arg:
        self._description = description.strip()
        return self

    def try_set_description_from_spec(self, spec: dict[str, Any]) -> Arg:
        if "description" in spec and isinstance(spec["description"], str):
            self.set_description(spec["description"])
        return self

    @property
    def name(self) -> str:
        return self._name

    @property
    def arg_type(self) -> ArgType:
        return self._type

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def optional(self) -> bool:
        return self._optional

    @optional.setter
    def optional(self, value: bool):
        self._optional = value

    @property
    def python_type(self) -> str:
        return self.name

    @property
    def python_class(self) -> str:
        return self.python_type

    @property
    def python_local_type(self) -> str:
        return self.python_type.split(".")[-1]

    @property
    def python_annotation(self) -> str:
        return self.python_class

    @property
    def rust_type(self) -> str:
        return self.name

    @property
    def rust_local_type(self) -> str:
        return self.rust_type

    @property
    def cpp_type(self) -> str:
        return stringmanip.upper_camel_case(self.name)
    
    @property
    def cpp_temp_type(self) -> str:
        if self.optional and "optional" not in self.cpp_type:
            return f"boost::optional<{self.cpp_type}>"
        return self.cpp_type

    @property
    def cpp_func_param_type(self) -> str:
        if self.optional and "optional" not in self.cpp_type:
            return f"boost::optional<{self.cpp_type}>"
        return self.cpp_type

    @classmethod
    def new_arg_from_stinger(
        cls, arg_spec: YamlArg, stinger_spec: Optional[StingerSpec] = None
    ) -> Arg:
        if "type" not in arg_spec:
            raise InvalidStingerStructure("No 'type' in arg structure")
        if "name" not in arg_spec:
            raise InvalidStingerStructure("No 'name' in arg structure")
        elif arg_spec["name"] in RESTRICTED_NAMES:
            arg_spec["name"] = f"{arg_spec['name']}_"
        if not isinstance(arg_spec["type"], str):
            raise InvalidStingerStructure("'type' in arg structure must be a string")
        if not isinstance(arg_spec["name"], str):
            raise InvalidStingerStructure("'name' in arg structure must be a string")

        if hasattr(ArgPrimitiveType, arg_spec["type"].upper()):
            arg = ArgPrimitive.new_arg_primitive_from_stinger(arg_spec)
            if opt := arg_spec.get("optional", False):
                assert isinstance(opt, bool), "Optional field must be a boolean"
                arg.optional = opt
            return arg
        else:
            if stinger_spec is None:
                raise RuntimeError(
                    "Need the root StingerSpec when creating an enum or struct Arg"
                )

        if arg_spec["type"] == "enum":
            if "enumName" not in arg_spec:
                raise InvalidStingerStructure(f"Enum args need a 'enumName'")
            if not isinstance(arg_spec["enumName"], str):
                raise InvalidStingerStructure("'enumName' in arg structure must be a string")
            if arg_spec["enumName"] not in stinger_spec.enums:
                raise InvalidStingerStructure(
                    f"Enum arg '{arg_spec['enumName']}' was not found in the list of stinger spec enums"
                )
            enum_arg = ArgEnum(
                arg_spec["name"], stinger_spec.get_interface_enum(arg_spec["enumName"])
            )
            if opt := arg_spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                enum_arg.optional = opt
            enum_arg.try_set_description_from_spec(arg_spec)
            return enum_arg

        if arg_spec["type"] == "struct":
            if "structName" not in arg_spec:
                raise InvalidStingerStructure("Struct args need a 'structName'")
            if not isinstance(arg_spec["structName"], str):
                raise InvalidStingerStructure("'structName' in arg structure must be a string")
            if arg_spec["structName"] not in stinger_spec.structs:
                raise InvalidStingerStructure(
                    f"Struct arg '{arg_spec["structName"]}' was not found in the list of stinger spec structs"
                )
            st_arg = ArgStruct(
                arg_spec["name"], stinger_spec.structs[arg_spec["structName"]]
            )
            if opt := arg_spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                st_arg.optional = opt
            st_arg.try_set_description_from_spec(arg_spec)
            return st_arg
        
        if arg_spec["type"] == "datetime":
            dt_arg = ArgDateTime(arg_spec["name"])
            if opt := arg_spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                dt_arg.optional = opt
            dt_arg.try_set_description_from_spec(arg_spec)
            return dt_arg

        if arg_spec["type"] == "duration":
            dur_arg = ArgDuration(arg_spec["name"])
            if opt := arg_spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                dur_arg.optional = opt
            dur_arg.try_set_description_from_spec(arg_spec)
            return dur_arg
        
        if arg_spec["type"] == "binary":
            bin_arg = ArgBinary(arg_spec["name"])
            if opt := arg_spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                bin_arg.optional = opt
            bin_arg.try_set_description_from_spec(arg_spec)
            return bin_arg

        raise RuntimeError(f"unknown arg type: {arg_spec['type']}")

    @abstractmethod
    def get_random_example_value(self, lang="python", seed: int = 0): ...


class ArgEnum(Arg):
    def __init__(self, name: str, enum: InterfaceEnum, description: Optional[str] = None):
        super().__init__(name, description)
        self._enum = enum
        self._type = ArgType.ENUM

    @property
    def enum(self) -> InterfaceEnum:
        return self._enum

    @property
    def python_type(self) -> str:
        return self._enum.python_type

    @property
    def python_local_type(self) -> str:
        return self._enum.python_local_type

    @property
    def python_class(self) -> str:
        return self._enum.python_type

    @property
    def python_annotation(self) -> str:
        if self.optional:
            return f"Optional[{self._enum.python_type}]"
        return self._enum.python_type

    @property
    def cpp_type(self) -> str:
        if self.optional:
            return f"boost::optional<{self._enum.cpp_type}>"
        return self._enum.cpp_type

    @property
    def rust_type(self) -> str:
        if self.optional:
            return f"Option<{self._enum.rust_type}>"
        return self._enum.rust_type

    @property
    def rust_local_type(self) -> str:
        if self.optional:
            return f"Option<{self._enum.rust_local_type}>"
        return self._enum.rust_local_type

    @property
    def cpp_temp_type(self) -> str:
        return self.cpp_type

    @property
    def cpp_data_type(self) -> str:
        return self._enum.cpp_type

    @property
    def cpp_rapidjson_type(self) -> str:
        return ArgPrimitiveType.to_cpp_rapidjson_type_str(ArgPrimitiveType.INTEGER)

    @property
    def markdown_type(self) -> str:
        return f"[Enum {self._enum.class_name}](#enum-{self._enum.class_name})"

    def get_random_example_value(self, lang="python", seed: int = 2) -> str:
        random_state = random.getstate()
        random.seed(seed)
        value = random.choice(self._enum.values)
        if lang == "python":
            retval = f"{self._enum.get_module_alias()}.{self._enum.class_name}.{stringcase.constcase(value) }"
        elif lang == "c++":
            retval = f"{self._enum.class_name}::{stringcase.constcase(value)}"
        elif lang == "rust":
            if self.optional:
                retval = f"Some({self._enum.class_name}::{stringmanip.upper_camel_case(value)})"
            else:
                retval = f"{self._enum.class_name}::{stringmanip.upper_camel_case(value)}"
        elif lang == "json":
            retval = str(random.randint(1, len(self._enum.values)))
        random.setstate(random_state)
        return retval

    def __repr__(self) -> str:
        return f"<ArgEnum name={self._name}>"


class ArgPrimitive(Arg):
    def __init__(
        self, name: str, arg_type: ArgPrimitiveType, description: Optional[str] = None
    ):
        super().__init__(name, description)
        self._arg_type = arg_type
        self._type = ArgType.PRIMITIVE

    @property
    def type(self) -> ArgPrimitiveType:
        return self._arg_type

    @property
    def python_type(self) -> str:
        return ArgPrimitiveType.to_python_type(self._arg_type)

    @property
    def python_annotation(self) -> str:
        return ArgPrimitiveType.to_python_type(self._arg_type, optional=self._optional)

    @property
    def rust_type(self) -> str:
        return ArgPrimitiveType.to_rust_type(self._arg_type, optional=self._optional)

    @property
    def cpp_type(self) -> str:
        return ArgPrimitiveType.to_cpp_type(self._arg_type, optional=self._optional)

    @property
    def protobuf_type(self) -> str:
        return ArgPrimitiveType.to_protobuf_type(self._arg_type)

    @property
    def cpp_temp_type(self) -> str:
        if self._arg_type == ArgPrimitiveType.STRING:
            if self.optional:
                return "boost::optional<std::string>"
            return "std::string"
        else:
            return self.cpp_type

    @property
    def json_type(self) -> str:
        return ArgPrimitiveType.to_json_type(self._arg_type)

    @property
    def cpp_rapidjson_type(self) -> str:
        return ArgPrimitiveType.to_cpp_rapidjson_type_str(self._arg_type)

    def get_random_example_value(
        self, lang="python", seed: int = 2
    ) -> str | float | int | bool | None:
        random_state = random.getstate()
        random.seed(seed)
        retval: str | float | int | bool | None = None
        if self._arg_type == ArgPrimitiveType.BOOLEAN:
            retval = random.choice([True, False])
            if lang != "python":
                retval = str(retval).lower()
        elif self._arg_type == ArgPrimitiveType.FLOAT:
            retval = random.choice([3.14, 1.0, 2.5, 97.9, 1.53])
        elif self._arg_type == ArgPrimitiveType.INTEGER:
            retval = random.choice([42, 1981, 2020, 2022, 1200, 5, 99, 123, 2025, 1955])
        elif self._arg_type == ArgPrimitiveType.STRING:
            retval = random.choice(
                ['"apples"', '"Joe"', '"example"', '"foo"', '"bar"', '"tiger"', '"bear"', '"root beer"']
            )
            if lang == "rust":
                retval = f"{retval}.to_string()"
            if self.optional and lang in ["cpp", "c++"]:
                retval = f'boost::make_optional(std::string({retval}))'
        if self.optional and lang == "rust":
            retval = f"Some({retval})"
        random.setstate(random_state)
        return retval

    def __repr__(self) -> str:
        return f"<ArgPrimitive name={self._name} type={ArgPrimitiveType.to_python_type(self.type)}>"

    @classmethod
    def new_arg_primitive_from_stinger(
        cls, arg_spec: dict[str, str | bool]
    ) -> ArgPrimitive:
        if "type" not in arg_spec:
            raise InvalidStingerStructure("No 'type' in arg structure")
        if "name" not in arg_spec:
            raise InvalidStingerStructure("No 'name' in arg structure")
        if not isinstance(arg_spec["type"], str):
            raise InvalidStingerStructure("'type' in arg structure must be a string")
        if not isinstance(arg_spec["name"], str):
            raise InvalidStingerStructure("'name' in arg structure must be a string")

        arg_primitive_type = ArgPrimitiveType.from_string(arg_spec["type"])
        arg: ArgPrimitive = cls(name=arg_spec["name"], arg_type=arg_primitive_type)

        arg.try_set_description_from_spec(arg_spec)
        return arg


class ArgStruct(Arg):
    def __init__(self, name: str, iface_struct: InterfaceStruct):
        super().__init__(name)
        assert isinstance(
            iface_struct, InterfaceStruct
        ), f"Passed {iface_struct=} is type {type(iface_struct)} which is not InterfaceStruct"
        self._interface_struct: InterfaceStruct = iface_struct
        self._type = ArgType.STRUCT

    @property
    def members(self) -> list[Arg]:
        return self._interface_struct.members

    @property
    def cpp_type(self) -> str:
        return self._interface_struct.cpp_type

    @property
    def python_type(self) -> str:
        return f"interface_types.{self._interface_struct.python_local_type}"

    @property
    def python_local_type(self) -> str:
        return self._interface_struct.python_local_type

    @property
    def rust_type(self) -> str:
        return self._interface_struct.rust_type

    @property
    def rust_local_type(self) -> str:
        return self._interface_struct.rust_local_type

    @property
    def markdown_type(self) -> str:
        return f"[Struct {self._interface_struct.class_name}](#enum-{self._interface_struct.class_name})"

    @property
    def cpp_rapidjson_type(self) -> str:
        return "Object"

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        if lang in ["rust", "python"]:
            example_list: dict[str, str] = {
                stringcase.snakecase(a.name): str(a.get_random_example_value(lang, seed=seed))
                for a in self.members
            }
        else:
            example_list: dict[str, str] = {
                a.name: str(a.get_random_example_value(lang, seed=seed))
                for a in self.members
            }
        if lang == "c++":
            return self.cpp_type + "{" + ", ".join(example_list.values()) + "}"
        elif lang == "python":
            init_list = ", ".join([f"{k}={v}" for k, v in example_list.items()])
            return f"{self.python_type}({init_list})"
        elif lang == "rust":
            return "%s {%s}" % (
                self.rust_type,
                ", ".join([f"{k}: {v}" for k, v in example_list.items()]),
            )
        elif lang == "json":
            return "{" + ", ".join([f'"{k}": {v}' for k, v in example_list.items()]) + "}"
        return None

    def __str__(self) -> str:
        return f"<ArgStruct name={self.name}>"

    def __repr__(self):
        return f"ArgStruct(name={self.name}, iface_struct={self._interface_struct})"

class ArgDateTime(Arg):
    def __init__(self, name: str):
        super().__init__(name)
        self._type = ArgType.DATETIME

    @property
    def cpp_type(self) -> str:
        if self.optional:
            return "boost::optional<std::chrono::time_point<std::chrono::system_clock>>"
        return "std::chrono::time_point<std::chrono::system_clock>"

    @property
    def cpp_temp_type(self) -> str:
        return self.cpp_type

    @property
    def cpp_rapidjson_type(self) -> str:
        return "String"

    @property
    def python_type(self) -> str:
        return "datetime.datetime"

    @property
    def python_local_type(self) -> str:
        return "datetime"
    
    @property
    def python_annotation(self) -> str:
        if self.optional:
            return "Optional[datetime]"
        return "datetime"

    @property
    def rust_type(self) -> str:
        return "chrono::DateTime<chrono::Utc>"

    @property
    def markdown_type(self) -> str:
        return "[DateTime](#datetime)"

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        if lang == "python":
            if self.optional and random.choice([True, False, False, False]):
                return "None"
            return f"datetime.now()"
        elif lang == "rust":
            return "chrono::Utc::now()"
        elif lang in ["c++", "cpp"]:
            return "std::chrono::system_clock::now()"
        elif lang == "json":
            return '"1990-07-08T16:20:00Z"'
        return None

    def __str__(self) -> str:
        return f"<ArgDateTime name={self.name}>"

    def __repr__(self):
        return f"ArgDateTime(name={self.name})"

class ArgDuration(Arg):
    def __init__(self, name: str):
        super().__init__(name)
        self._type = ArgType.DURATION

    @property
    def cpp_type(self) -> str:
        if self.optional:
            return "boost::optional<std::chrono::duration<double>>"
        return "std::chrono::duration<double>"

    @property
    def cpp_temp_type(self) -> str:
        return self.cpp_type

    @property
    def python_type(self) -> str:
        return "datetime.timedelta"

    @property
    def python_annotation(self) -> str:
        if self.optional:
            return "Optional[timedelta]"
        return "timedelta"

    @property
    def rust_type(self) -> str:
        return "chrono::Duration"

    @property
    def markdown_type(self) -> str:
        return "[Duration](#duration)"

    @property
    def cpp_rapidjson_type(self) -> str:
        return "String"

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        random_state = random.getstate()
        random.seed(seed)
        retval = None
        if lang == "python":
            if self.optional and random.choice([True, False, False, False]):
                retval = "None"
            else:
                retval = f"timedelta(seconds={random.randint(1, 3600)})"
        elif lang == "rust":
            retval = f"chrono::Duration::seconds({random.randint(1, 3600)})"
        elif lang in ["c++", "cpp"]:
            retval = f"std::chrono::duration<double>({random.randint(1, 3600)})"
        random.setstate(random_state)
        return retval

    def __str__(self) -> str:
        return f"<ArgDuration name={self.name}>"

    def __repr__(self):
        return f"ArgDuration(name={self.name})"
    

class ArgBinary(Arg):
    def __init__(self, name: str):
        super().__init__(name)
        self._type = ArgType.BINARY

    @property
    def python_type(self) -> str:
        return "bytes"

    @property
    def rust_type(self) -> str:
        return "Vec<u8>"

    @property
    def markdown_type(self) -> str:
        return "[Binary](#binary)"

    @property
    def cpp_rapidjson_type(self) -> str:
        return "String"
    
    @property
    def cpp_type(self) -> str:
        if self.optional:
            return "boost::optional<std::vector<uint8_t>>"
        return "std::vector<uint8_t>"
    
    @property
    def cpp_temp_type(self) -> str:
        return self.cpp_type

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        if lang == "python":
            return f'b"example binary data"'
        elif lang == "rust":
            return 'vec![101, 120, 97, 109, 112, 108, 101]'  # "example" in ASCII bytes
        elif lang in ["c++", "cpp"]:
            return 'std::vector<uint8_t>{101, 120, 97, 109, 112, 108, 101}'  # "example" in ASCII bytes
        return None

    def __str__(self) -> str:
        return f"<ArgBinary name={self.name}>"

    def __repr__(self):
        return f"ArgBinary(name={self.name})"
    

class ArgList(Arg):
    def __init__(self, name: str, element_type: Arg):
        super().__init__(name)
        self._element_type = element_type
        self._type = ArgType.LIST

    @property
    def element_type(self) -> Arg:
        return self._element_type

    @property
    def cpp_type(self) -> str:
        return f"std::vector<{self._element_type.cpp_type}>"

    @property
    def python_type(self) -> str:
        return f"list[{self._element_type.python_type}]"

    @property
    def rust_type(self) -> str:
        return f"Vec<{self._element_type.rust_type}>"

    @property
    def markdown_type(self) -> str:
        return f"List of {self._element_type.markdown_type}"

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        example_value = self._element_type.get_random_example_value(lang, seed=seed)
        if lang == "python":
            return f"[{example_value}, {example_value}]"
        elif lang == "rust":
            return f"vec![{example_value}, {example_value}]"
        elif lang in ["c++", "cpp"]:
            return f"std::vector<{self._element_type.cpp_type}>{{{example_value}, {example_value}}}"
        return None

    def __str__(self) -> str:
        return f"<ArgList name={self.name} element_type={self._element_type}>"

    def __repr__(self):
        return f"ArgList(name={self.name}, element_type={self._element_type})"


class InterfaceComponent:

    def __init__(self, name: str):
        self._name = name
        self._documentation: Optional[str] = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def documentation(self) -> str | None:
        return self._documentation

    def set_documentation(self, documentation: str) -> InterfaceComponent:
        self._documentation = documentation
        return self

    def try_set_documentation_from_spec(
        self, spec: dict[str, Any]
    ) -> InterfaceComponent:
        if "documentation" in spec and isinstance(spec["documentation"], str):
            self._documentation = spec["documentation"]
        return self


class Signal(InterfaceComponent):
    def __init__(self, topic_creator: SignalTopicCreator, name: str):
        super().__init__(name)
        self._topic_creator = topic_creator
        self._arg_list: list[Arg] = []

    def add_arg(self, arg: Arg) -> Signal:
        if arg.name in [a.name for a in self._arg_list]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._arg_list.append(arg)
        return self

    @property
    def arg_list(self) -> list[Arg]:
        return self._arg_list

    @property
    def topic(self) -> str:
        return self._topic_creator.signal_topic(self.name)

    @classmethod
    def new_signal_from_stinger(
        cls,
        topic_creator: SignalTopicCreator,
        name: str,
        signal_spec: dict[str, str],
        stinger_spec: Optional[StingerSpec] = None,
    ) -> "Signal":
        """Alternative constructor from a Stinger signal structure."""
        signal = cls(topic_creator, name)
        if "payload" not in signal_spec:
            raise InvalidStingerStructure("Signal specification must have 'payload'")
        if not isinstance(signal_spec["payload"], list):
            raise InvalidStingerStructure(
                f"Payload must be a list.  It is '{type(signal_spec['payload'])}' "
            )

        for arg_spec in signal_spec["payload"]:
            if "name" not in arg_spec or "type" not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            signal.add_arg(new_arg)

        signal.try_set_documentation_from_spec(signal_spec)

        return signal


class Method(InterfaceComponent):

    def __init__(self, topic_creator: MethodTopicCreator, name: str):
        super().__init__(name)
        self._python = PythonMethodSymbols(self)
        self._topic_creator = topic_creator
        self._arg_list: list[Arg] = []
        self._return_value: Arg | list[Arg] | None = None
        self._return_arg_list: list[Arg] = []

    @property
    def python(self) -> PythonMethodSymbols:
        return self._python

    def add_arg(self, arg: Arg) -> Method:
        if arg.name in [a.name for a in self._arg_list]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._arg_list.append(arg)
        return self

    def add_return_value(self, value: Arg) -> Method:
        self._return_arg_list.append(value)
        if self._return_value is None:
            self._return_value = value
        elif isinstance(self._return_value, list):
            if value.name in [a.name for a in self._return_value]:
                raise InvalidStingerStructure(
                    f"A return value named '{value.name}' has been already added."
                )
            self._return_value.append(value)
        elif isinstance(self._return_value, Arg):
            if value.name == self._return_value.name:
                raise InvalidStingerStructure(
                    f"Attempt to add '{value.name}' to return value when it is already been added."
                )
            self._return_value = [self._return_value, value]
        return self

    @property
    def arg_list(self) -> list[Arg]:
        return self._arg_list

    @property
    def return_arg_list(self) -> list[Arg]:
        return self._return_arg_list

    @property
    def return_value(self) -> Arg | list[Arg] | None:
        return self._return_value

    @property
    def return_value_name(self) -> str:
        return f"{self.name} return values"

    @property
    def return_value_cpp_class(self) -> str:
        if self._return_value is None:
            return "void"
        elif isinstance(self._return_value, Arg):
            if isinstance(self._return_value, ArgPrimitive) and self._return_value.type == ArgPrimitiveType.STRING:
                if self._return_value.optional:
                    return "boost::optional<std::string>"
                return "std::string"
            elif isinstance(self._return_value, ArgStruct) and self._return_value.optional:
                return f"boost::optional<{self._return_value.cpp_type}>"
            return self._return_value.cpp_type
        elif isinstance(self._return_value, list):
            return stringmanip.upper_camel_case(self.return_value_name)

    @property
    def return_value_rust_type(self) -> str:
        if self._return_value is None:
            return "()"
        elif isinstance(self._return_value, Arg):
            return self._return_value.rust_type
        elif isinstance(self._return_value, list):
            return stringmanip.upper_camel_case(self.return_value_name)

    @property
    def return_value_python_type(self):
        if self._return_value is None:
            return "None"
        elif isinstance(self._return_value, Arg):
            return self._return_value.python_type
        elif isinstance(self._return_value, list):
            return (
                f"interface_types.{stringmanip.upper_camel_case(self.name)}MethodResponse"
            )
        else:
            raise RuntimeError(f"Did not handle return value type for: {self._return_value}")

    @property
    def return_value_python_annotation(self):
        if self._return_value is None:
            return "None"
        elif isinstance(self._return_value, Arg):
            return self._return_value.python_annotation
        elif isinstance(self._return_value, list):
            return (
                f"interface_types.{stringmanip.upper_camel_case(self.name)}MethodResponse"
            )
        else:
            raise RuntimeError(f"Did not handle return value type for: {self._return_value}")

    @property
    def return_value_python_local_type(self):
        if self._return_value is None:
            return "None"
        elif isinstance(self._return_value, Arg):
            return self._return_value.python_local_type
        elif isinstance(self._return_value, list):
            return stringmanip.upper_camel_case(self.return_value_name)

    @property
    def return_value_property_name(self) -> str:
        if isinstance(self._return_value, Arg):
            return self._return_value.name
        else:
            return self.name

    @property
    def return_value_type(self) -> str | bool:
        if self._return_value is None:
            return False
        elif isinstance(self._return_value, Arg):
            return self._return_value.arg_type.name.lower()
        elif isinstance(self._return_value, list):
            return "multiple"
        raise RuntimeError("Method return value type was not recognized")

    def get_return_value_random_example_value(
        self, lang: str = "python", seed: int = 2
    ):
        if lang == "python":
            if self._return_value is None:
                return "None"
            elif isinstance(self._return_value, Arg):
                return self._return_value.get_random_example_value(lang, seed)
            elif isinstance(self._return_value, list):
                s = ", ".join([f"{a.name}={a.get_random_example_value(lang,seed)}" for a in self._return_value])
                return f"{self.return_value_python_type}({s})"
            else:
                raise RuntimeError(f"Did not handle return value type for: {self._return_value}")
        if lang == "c++" or lang == "cpp":
            if self._return_value is None:
                return "null"
            elif isinstance(self._return_value, Arg):
                return self._return_value.get_random_example_value(lang, seed)
            elif isinstance(self._return_value, list):
                return ", ".join(
                    [
                        str(a.get_random_example_value(lang, seed))
                        for a in self._return_value
                    ]
                )
        raise RuntimeError(f"No random example for return value for {lang}")

    @property
    def topic(self) -> str:
        return self._topic_creator.method_topic(self.name)

    def response_topic(self, client_id) -> str:
        return self._topic_creator.method_response_topic(self.name, client_id)

    @classmethod
    def new_method_from_stinger(
        cls,
        topic_creator: MethodTopicCreator,
        name: str,
        method_spec: dict[str, str],
        stinger_spec: Optional[StingerSpec] = None,
    ) -> "Method":
        """Alternative constructor from a Stinger method structure."""
        method = cls(topic_creator, name)
        if "arguments" not in method_spec:
            raise InvalidStingerStructure(
                f"Method '{name}' specification must have 'arguments'"
            )
        if not isinstance(method_spec["arguments"], list):
            raise InvalidStingerStructure(
                f"Arguments for '{name}' method must be a list.  It is '{type(method_spec['arguments'])}' "
            )

        for arg_spec in method_spec["arguments"]:
            if "name" not in arg_spec or "type" not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            method.add_arg(new_arg)

        if "returnValues" in method_spec:
            if not isinstance(method_spec["returnValues"], list):
                raise InvalidStingerStructure(f"ReturnValues must be a list.")

            for arg_spec in method_spec["returnValues"]:
                if "name" not in arg_spec or "type" not in arg_spec:
                    raise InvalidStingerStructure(
                        "Return value must have name and type."
                    )
                new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
                method.add_return_value(new_arg)

        method.try_set_documentation_from_spec(method_spec)

        return method


class Property(InterfaceComponent):

    def __init__(self, topic_creator: PropertyTopicCreator, name: str):
        super().__init__(name)
        self._topic_creator = topic_creator
        self._arg_list: list[Arg] = []
        self._read_only = False

    def add_arg(self, arg: Arg) -> Property:
        if arg.name in [a.name for a in self._arg_list]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._arg_list.append(arg)
        return self

    @property
    def python_local_type(self) -> str:
        return self.python_class.split(".")[-1]

    @property
    def python_class(self) -> str:
        if len(self._arg_list) == 1:
            return self._arg_list[0].python_class
        else:
            return f"interface_types.{stringmanip.upper_camel_case(self.name)}Property"

    @property
    def python_annotation(self) -> str:
        if len(self._arg_list) == 1:
            return self._arg_list[0].python_annotation
        else:
            return f"interface_types.{stringmanip.upper_camel_case(self.name)}Property"

    @property
    def rust_local_type(self) -> str:
        if len(self._arg_list) == 1:
            return self._arg_list[0].rust_local_type
        else:
            return f"{stringmanip.upper_camel_case(self.name)}Property"

    @property
    def rust_type(self) -> str:
        if len(self._arg_list) == 1:
            return self._arg_list[0].rust_type
        else:
            return f"{self.rust_local_type}"

    @property
    def arg_list(self) -> list[Arg]:
        return self._arg_list

    @property
    def value_topic(self) -> str:
        return self._topic_creator.property_value_topic(self.name)

    @property
    def update_topic(self) -> str:
        return self._topic_creator.property_update_topic(self.name)

    @property
    def read_only(self) -> bool:
        return self._read_only

    @classmethod
    def new_method_from_stinger(
        cls,
        topic_creator: PropertyTopicCreator,
        name: str,
        prop_spec: YamlIfaceProperty,
        stinger_spec: Optional[StingerSpec] = None,
    ) -> "Property":
        """Alternative constructor from a Stinger method structure."""
        prop_obj = cls(topic_creator, name)
        if "values" not in prop_spec:
            raise InvalidStingerStructure("Property specification must have 'values'")
        if not isinstance(prop_spec["values"], list):
            raise InvalidStingerStructure(
                f"Values must be a list.  It is '{type(prop_spec['values'])}' "
            )

        for arg_spec in prop_spec["values"]:
            if "name" not in arg_spec or "type" not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            prop_obj.add_arg(new_arg)

        if r_o := prop_spec.get("readOnly", False):
            if not isinstance(r_o, bool):
                raise InvalidStingerStructure("'readOnly' in property structure must be a boolean")
            prop_obj._read_only = r_o

        prop_obj.try_set_documentation_from_spec(prop_spec)

        return prop_obj

    def __str__(self) -> str:
        return f"Property<name={self.name} values=[{', '.join([a.name for a in self.arg_list])}]>"


class InterfaceEnum:

    def __init__(self, name: str):
        self._name = name
        self._values: list[str] = []
        self._value_descriptions: list[str | None] = []
        self._documentation: Optional[str] = None

    def add_value(self, value: str, description: Optional[str] = None):
        self._values.append(value)
        self._value_descriptions.append(description.strip())

    @property
    def name(self):
        return self._name

    @property
    def documentation(self) -> str | None:
        return self._documentation

    @property
    def class_name(self):
        return stringmanip.upper_camel_case(self.name)

    @staticmethod
    def get_module_name(lang="python") -> str:
        return "interface_types"

    @staticmethod
    def get_module_alias(lang="python") -> str:
        return "interface_types"

    @property
    def python_type(self) -> str:
        return f"{self.get_module_alias()}.{stringmanip.upper_camel_case(self.name)}"

    @property
    def python_local_type(self) -> str:
        return f"{stringmanip.upper_camel_case(self.name)}"

    @property
    def rust_local_type(self) -> str:
        return stringmanip.upper_camel_case(self.name)

    @property
    def rust_type(self) -> str:
        return f"{self.rust_local_type}"

    @property
    def cpp_type(self) -> str:
        return stringmanip.upper_camel_case(self.name)

    @property
    def values(self):
        return self._values
    
    def value_description(self, index: int) -> str | None:
        if index < 0 or index >= len(self._value_descriptions):
            return None
        return self._value_descriptions[index]

    @classmethod
    def new_enum_from_stinger(cls, name, enum_spec: YamlIfaceEnum) -> InterfaceEnum:
        ie = cls(name)
        for enum_obj in enum_spec.get("values", []):
            assert isinstance(enum_obj, dict), f"Enum values must be a dicts."
            if "name" in enum_obj and isinstance(enum_obj["name"], str):
                value_description = enum_obj.get("description", None)
                if value_description is not None and not isinstance(value_description, str):
                    raise InvalidStingerStructure(
                        f"InterfaceEnum '{name}' item descriptions must be strings."
                    )
                ie.add_value(enum_obj["name"], description=value_description)
            else:
                raise InvalidStingerStructure(
                    f"InterfaceEnum '{name}' items must have string names."
                )
        doc = enum_spec.get("documentation", None)
        if doc is not None and isinstance(doc, str):
            ie.documentation = doc
        return ie


class InterfaceStruct:

    def __init__(self, name: str):
        self._name = name
        self._members: list[Arg] = []
        self._documentation: Optional[str] = None

    def add_member(self, arg: Arg):
        self._members.append(arg)

    @property
    def name(self):
        return self._name

    @property
    def documentation(self) -> str | None:
        return self._documentation

    @property
    def class_name(self):
        return stringmanip.upper_camel_case(self.name)

    @staticmethod
    def get_module_name(lang="python") -> str:
        return "interface_types"

    @staticmethod
    def get_module_alias(lang="python") -> str:
        return "interface_types"

    @property
    def python_type(self) -> str:
        return f"{self.get_module_alias()}.{stringmanip.upper_camel_case(self.name)}"

    @property
    def python_local_type(self) -> str:
        return stringmanip.upper_camel_case(self.name)

    @property
    def rust_local_type(self) -> str:
        return stringmanip.upper_camel_case(self.name)

    @property
    def rust_type(self) -> str:
        return f"{self.rust_local_type}"

    @property
    def cpp_type(self) -> str:
        return stringmanip.upper_camel_case(self.name)

    @property
    def values(self) -> list[Arg]:
        return self._members

    @property
    def members(self) -> list[Arg]:
        return self._members

    @classmethod
    def new_struct_from_stinger(
        cls,
        name,
        spec: dict[str, str | list[dict[str, str]]],
        stinger_spec: StingerSpec,
    ) -> InterfaceStruct:
        istruct = cls(name)
        for memb in spec.get("members", []):
            if not isinstance(memb, dict):
                raise InvalidStingerStructure("Struct members must be dicts")
            arg = Arg.new_arg_from_stinger(memb, stinger_spec=stinger_spec)
            istruct.add_member(arg)
        documentation = spec.get("documentation", None)
        if documentation is not None and not isinstance(documentation, str):
            raise InvalidStingerStructure("Struct documentation must be a string")
        istruct._documentation = documentation
        return istruct

    def __str__(self) -> str:
        return f"<InterfaceStruct members={[m.name for m in self.members]}>"

    def __repr__(self):
        return f"InterfaceStruct(name={self.name})"


class MqttTransportProtocol(Enum):
    TCP = 0
    WEBSOCKETS = 1


class Broker:
    def __init__(self, name: str = "Default"):
        self._name: str = name
        self._host: Optional[str] = None
        self._port: Optional[int] = None
        self._auth = None
        self._transport_protocol: MqttTransportProtocol = MqttTransportProtocol.TCP

    @property
    def name(self) -> str:
        return self._name

    @property
    def class_name(self) -> str:
        return f"{stringmanip.upper_camel_case(self.name)}Connection"

    @property
    def hostname(self) -> str | None:
        return self._host

    @hostname.setter
    def hostname(self, value: str):
        self._host = value

    @property
    def port(self) -> int | None:
        return self._port

    @port.setter
    def port(self, port: int):
        self._port = port

    @classmethod
    def new_broker_from_stinger(cls, name: str, spec: dict[str, Any]) -> Broker:
        new_broker = cls(name=name)
        if "host" in spec:
            new_broker.hostname = spec["host"]
        if "port" in spec:
            new_broker.port = int(spec["port"])
        return new_broker

    def __repr__(self) -> str:
        return f"<Broker name={self.name} host={self.hostname}:{self.port}>"


class StingerSpec:
    def __init__(self, topic_creator: InterfaceTopicCreator, interface: dict[str, Any]):
        self._topic_creator = topic_creator
        try:
            self._name: str = interface["name"]
            self._version: str = interface["version"]
            self._python = PythonInterfaceSymbols(self)
            self._rust = RustInterfaceSymbols(self)
            self._cpp = CppInterfaceSymbols(self)
        except KeyError as e:
            raise InvalidStingerStructure(
                f"Missing interface property in {interface}: {e}"
            )
        except TypeError:
            raise InvalidStingerStructure(
                f"Interface didn't appear to have a correct type"
            )

        self._summary = interface.get("summary")
        self._title = interface.get("title")
        self._documentation = interface.get("documentation")

        self.signals: dict[str, Signal] = {}
        self.properties: dict[str, Property] = {}
        self.methods: dict[str, Method] = {}
        self.enums: dict[str, InterfaceEnum] = {}
        self.structs: dict[str, InterfaceStruct] = {}

    @property
    def method_return_codes(self) -> dict[int, str]:
        return {
            0: "Success",
            1: "Client Error",
            2: "Server Error",
            3: "Transport Error",
            4: "Payload Error",
            5: "Client Serialization Error",
            6: "Client Deserialization Error",
            7: "Server Serialization Error",
            8: "Server Deserialization Error",
            9: "Method Not Found",
            10: "Unauthorized",
            11: "Timeout",
            12: "OutOfSync",
            13: "Unknown Error",
            14: "Not Implemented",
            15: "Service Unavailable",
        }

    @property
    def interface_info_topic(self) -> str:
        return self._topic_creator.interface_info_topic()

    @property
    def summary(self) -> str:
        return self._summary or ""
    
    @property
    def title(self) -> str:
        return self._title or self._name or ""
    
    @property
    def documentation(self) -> str:
        return self._documentation or ""

    def add_signal(self, signal: Signal):
        assert isinstance(signal, Signal)
        self.signals[signal.name] = signal

    def add_method(self, method: Method):
        assert isinstance(method, Method)
        self.methods[method.name] = method

    def add_property(self, prop: Property):
        assert isinstance(prop, Property)
        self.properties[prop.name] = prop

    @property
    def properties_rw(self) -> dict[str, Property]:
        return {k: v for k, v in self.properties.items() if not v.read_only}

    def add_enum(self, interface_enum: InterfaceEnum):
        assert interface_enum is not None
        self.enums[interface_enum.name] = interface_enum

    def add_struct(self, interface_struct: InterfaceStruct):
        assert interface_struct is not None
        self.structs[interface_struct.name] = interface_struct

    def uses_enums(self) -> bool:
        return bool(self.enums)

    def get_interface_enum(self, name: str) -> InterfaceEnum:
        if name in self.enums:
            return self.enums[name]
        raise InvalidStingerStructure(f"Enum '{name}' not found in stinger spec")

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def python(self) -> PythonInterfaceSymbols:
        return self._python

    @property
    def rust(self) -> RustInterfaceSymbols:
        return self._rust

    @property
    def cpp(self) -> CppInterfaceSymbols:
        return self._cpp

    @staticmethod
    def get_enum_module_name() -> str:
        return InterfaceEnum.get_module_name()

    @staticmethod
    def get_enum_module_alias() -> str:
        return InterfaceEnum.get_module_alias()

    @classmethod
    def new_spec_from_stinger(
        cls, topic_creator, stinger: dict[str, Any]
    ) -> StingerSpec:
        if "stingeripc" not in stinger:
            raise InvalidStingerStructure("Missing 'stingeripc' format version")
        if "version" not in stinger["stingeripc"]:
            raise InvalidStingerStructure("Stinger spec version not present")
        if stinger["stingeripc"]["version"] not in ["0.0.7"]:
            raise InvalidStingerStructure(
                f"Unsupported stinger spec version {stinger['stingeripc']['version']}"
            )

        stinger_spec = StingerSpec(topic_creator, stinger["interface"])

        # Enums must come before other components because other components may use enum values.
        try:
            if "enums" in stinger:
                for enum_name, enum_spec in stinger["enums"].items():
                    ie = InterfaceEnum.new_enum_from_stinger(enum_name, enum_spec)
                    assert (
                        ie is not None
                    ), f"Did not create enum from {enum_name} and {enum_spec}"
                    stinger_spec.add_enum(ie)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Signal specification appears to be invalid: {e}"
            )

        try:
            if "structures" in stinger:
                for struct_name, struct_spec in stinger["structures"].items():
                    istruct = InterfaceStruct.new_struct_from_stinger(
                        struct_name, struct_spec, stinger_spec
                    )
                    assert (
                        istruct is not None
                    ), f"Did not create struct from {struct_name} and {struct_spec}"
                    stinger_spec.add_struct(istruct)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Struct specification appears to be invalid: {e}"
            )

        try:
            if "signals" in stinger:
                for signal_name, signal_spec in stinger["signals"].items():
                    signal = Signal.new_signal_from_stinger(
                        topic_creator.signal_topic_creator(),
                        signal_name,
                        signal_spec,
                        stinger_spec,
                    )
                    assert (
                        signal is not None
                    ), f"Did not create signal from {signal_name} and {signal_spec}"
                    stinger_spec.add_signal(signal)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Signal specification appears to be invalid: {e}"
            )

        try:
            if "methods" in stinger:
                for method_name, method_spec in stinger["methods"].items():
                    method = Method.new_method_from_stinger(
                        topic_creator.method_topic_creator(),
                        method_name,
                        method_spec,
                        stinger_spec,
                    )
                    assert (
                        method is not None
                    ), f"Did not create method from {method_name} and {method_spec}"
                    stinger_spec.add_method(method)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Method specification appears to be invalid: {e}"
            )

        try:
            if "properties" in stinger:
                for prop_name, prop_spec in stinger["properties"].items():
                    prop = Property.new_method_from_stinger(
                        topic_creator.property_topic_creator(),
                        prop_name,
                        prop_spec,
                        stinger_spec,
                    )
                    assert (
                        prop is not None
                    ), f"Did not create property from {prop_name} and {prop_spec}"
                    stinger_spec.add_property(prop)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Property specification appears to be invalid: {e}"
            )

        return stinger_spec
