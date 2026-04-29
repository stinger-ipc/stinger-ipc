from __future__ import annotations

import random
from abc import abstractmethod
from copy import copy
from typing import Any, Optional, Mapping, TYPE_CHECKING

from jacobsjinjatoo import stringmanip
from pydantic import BaseModel, Field, ConfigDict

from stingeripc.config import StingerConfig
from .args import ArgType, ArgPrimitiveType
from .exceptions import InvalidStingerStructure
from .lang_symb import LanguageSymbolMixin

if TYPE_CHECKING:
    from stingeripc.arg_datatypes import InterfaceEnum, InterfaceStruct
    from stingeripc.components import StingerSpec

YamlArg = Mapping[str, str | bool]
YamlArgList = list[YamlArg]
YamlIfaceEnum = dict[str, str | YamlArgList]
YamlIfaceEnums = dict[str, YamlIfaceEnum]
YamlIfaceProperty = dict[str, str | bool | YamlArgList]

# These names cannot be used for method/property/signal names because they are reserved keywords.
RESTRICTED_NAMES = ["type", "class", "struct", "enum", "list", "map", "set", "optional", "bool", "int", "float", "string", "datetime", "duration", "binary"]


class Arg(BaseModel):
    """Represents an argument to a method, signal, or property.  This is the base class for all argument types."""
    model_config = ConfigDict(extra="allow")
    name:str  = Field(..., description="The name of the argument")
    description: str|None = Field(default=None, description="A description of the argument")
    optional: bool = Field(default=False, description="Whether the argument is optional")
    arg_type: ArgType = Field(default=ArgType.UNKNOWN, description="The type of the argument")

    def try_set_description_from_spec(self, spec: Mapping[str, Any]) -> "Arg":
        if "description" in spec and isinstance(spec["description"], str):
            self.description = spec["description"].strip()
        return self

    def __str__(self) -> str:
        return repr(self)

    @classmethod
    def new_arg_from_stinger(
        cls, arg_spec: YamlArg, stinger_spec: Optional[StingerSpec] = None
    ) -> Arg:
        # arg_spec may be an immutable Mapping; copy to mutable dict for validation/mutation
        spec: dict[str, Any]
        if isinstance(arg_spec, dict):
            spec = arg_spec
        else:
            spec = dict(arg_spec)

        if "type" not in spec:
            raise InvalidStingerStructure("No 'type' in arg structure")
        if "name" not in spec:
            raise InvalidStingerStructure("No 'name' in arg structure")
        elif spec["name"] in RESTRICTED_NAMES:
            spec["name"] = f"{spec['name']}_"
        if not isinstance(arg_spec["type"], str):
            raise InvalidStingerStructure("'type' in arg structure must be a string")
        if not isinstance(arg_spec["name"], str):
            raise InvalidStingerStructure("'name' in arg structure must be a string")

        if hasattr(ArgPrimitiveType, spec["type"].upper()):
            arg = ArgPrimitive.new_arg_primitive_from_stinger(spec)
            if opt := spec.get("optional", False):
                assert isinstance(opt, bool), "Optional field must be a boolean"
                arg.optional = opt
            return arg
        else:
            if stinger_spec is None:
                raise RuntimeError(
                    "Need the root StingerSpec when creating an enum or struct Arg"
                )

        if spec["type"] == "enum":
            if "enumName" not in arg_spec:
                raise InvalidStingerStructure(f"Enum args need a 'enumName'")
            if not isinstance(arg_spec["enumName"], str):
                raise InvalidStingerStructure("'enumName' in arg structure must be a string")
            if arg_spec["enumName"] not in stinger_spec.enums:
                raise InvalidStingerStructure(
                    f"Enum arg '{arg_spec['enumName']}' was not found in the list of stinger spec enums"
                )
            enum_arg = ArgEnum(
                name=spec["name"], enum=stinger_spec.get_interface_enum(spec["enumName"])
            )
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                enum_arg.optional = opt
            enum_arg.try_set_description_from_spec(spec)
            return enum_arg

        if spec["type"] == "struct":
            if "structName" not in spec:
                raise InvalidStingerStructure("Struct args need a 'structName'")
            if not isinstance(spec["structName"], str):
                raise InvalidStingerStructure("'structName' in arg structure must be a string")
            if spec["structName"] not in stinger_spec.structs:
                raise InvalidStingerStructure(
                    f"Struct arg '{spec["structName"]}' was not found in the list of stinger spec structs"
                )
            st_arg = ArgStruct(
                name=spec["name"], interface_struct=stinger_spec.structs[spec["structName"]]
            )
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                st_arg.optional = opt
            st_arg.try_set_description_from_spec(spec)
            return st_arg
        
        if spec["type"] == "datetime":
            dt_arg = ArgDateTime(name=spec["name"])
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                dt_arg.optional = opt
            dt_arg.try_set_description_from_spec(spec)
            return dt_arg

        if spec["type"] == "duration":
            dur_arg = ArgDuration(name=spec["name"])
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                dur_arg.optional = opt
            dur_arg.try_set_description_from_spec(spec)
            return dur_arg
        
        if spec["type"] == "binary":
            bin_arg = ArgBinary(name=spec["name"])
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                bin_arg.optional = opt
            bin_arg.try_set_description_from_spec(spec)
            return bin_arg
        
        if spec["type"] == "array":
            if "itemType" not in spec:
                raise InvalidStingerStructure("Array args need an 'itemType'")
            element_arg_spec = copy(spec["itemType"])
            if not isinstance(element_arg_spec, dict):
                raise InvalidStingerStructure("'itemType' in arg structure must be a dict")
            element_arg_spec["name"] = "name_not_used_in_array_element"
            element_arg = Arg.new_arg_from_stinger(element_arg_spec, stinger_spec)
            array_arg = ArgArray(name=spec["name"], element=element_arg)
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                array_arg.optional = opt
            array_arg.try_set_description_from_spec(spec)
            return array_arg

        raise RuntimeError(f"unknown arg type: {arg_spec['type']}")

    @abstractmethod
    def get_random_example_value(self, lang="python", seed: int = 0):
        pass


class ArgEnum(Arg):
    
    enum: InterfaceEnum = Field(..., description="The InterfaceEnum that restricts the values this ArgEnum represents.")
    arg_type: ArgType = Field(default=ArgType.ENUM, description="The type of the argument, which is 'enum' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)
    def get_random_example_value(self, lang="python", seed: int = 2) -> str:
        random_state = random.getstate()
        random.seed(seed)
        random_enum_item = random.choice(self.enum.items)
        if lang == "python":
            retval = f"{self.enum.class_name}.{stringmanip.const_case(random_enum_item.name) }"
        elif lang == "c++":
            retval = f"{self.enum.class_name}::{stringmanip.const_case(random_enum_item.name)}"
        elif lang == "rust":
            if self.optional:
                retval = f"Some({self.enum.class_name}::{stringmanip.upper_camel_case(random_enum_item.name)})"
            else:
                retval = f"{self.enum.class_name}::{stringmanip.upper_camel_case(random_enum_item.name)}"
        elif lang == "json":
            retval = str(random_enum_item.integer)
        elif hasattr(self, lang) and hasattr(getattr(self, lang), "get_random_example_value"):
            retval = getattr(self, lang).get_random_example_value(seed=seed)
        else:
            raise RuntimeError(f"Unknown language for enum random example value: {lang}")
        random.setstate(random_state)
        return retval

    def __repr__(self) -> str:
        return f"<ArgEnum name={self.name}>"


class ArgPrimitive(Arg):
    
    arg_type: ArgType = Field(default=ArgType.PRIMITIVE, description="The type of the argument, which is 'primitive' for this class")
    primitive_type: ArgPrimitiveType = Field(..., description="The specific primitive type that this argument represents (e.g. boolean, integer, float, string)")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)


    @property
    def type(self) -> ArgPrimitiveType:
        return self.primitive_type

    @property
    def protobuf_type(self) -> str:
        return ArgPrimitiveType.to_protobuf_type(self.primitive_type)

    @property
    def json_type(self) -> str:
        return ArgPrimitiveType.to_json_type(self.primitive_type)

    def get_random_example_value(
        self, lang="python", seed: int = 2
    ) -> str | float | int | bool | None:
        random_state = random.getstate()
        random.seed(seed)
        retval: str | float | int | bool | None = None
        if self.primitive_type == ArgPrimitiveType.BOOLEAN:
            retval = random.choice([True, False])
            if lang != "python":
                retval = str(retval).lower()
        elif self.primitive_type == ArgPrimitiveType.FLOAT:
            retval = random.choice([3.14, 1.0, 2.5, 97.9, 1.53])
        elif self.primitive_type == ArgPrimitiveType.INTEGER:
            retval = random.choice([42, 1981, 2020, 2022, 1200, 5, 99, 123, 2025, 1955])
        elif self.primitive_type == ArgPrimitiveType.STRING:
            retval = random.choice(
                ['"apples"', '"Joe"', '"example"', '"foo"', '"bar"', '"tiger"', '"bear"', '"root beer"']
            )
            if lang == "rust":
                retval = f"{retval}.to_string()"
            if self.optional and lang in ["cpp", "c++"]:
                retval = f'std::make_optional(std::string({retval}))'
        if self.optional and lang == "rust":
            retval = f"Some({retval})"
        random.setstate(random_state)
        return retval

    def __repr__(self) -> str:
        return f"<ArgPrimitive name={self.name} type={ArgPrimitiveType.to_python_type(self.primitive_type)}>"

    @classmethod
    def new_arg_primitive_from_stinger(
        cls, arg_spec: Mapping[str, Any]
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
        arg: ArgPrimitive = cls(name=arg_spec["name"], primitive_type=arg_primitive_type)

        arg.try_set_description_from_spec(arg_spec)
        return arg


class ArgStruct(Arg):

    interface_struct: InterfaceStruct = Field(..., description="The InterfaceStruct that defines the structure used for this argument.")
    arg_type: ArgType = Field(default=ArgType.STRUCT, description="The type of the argument, which is 'struct' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)
    @property
    def struct(self) -> InterfaceStruct:
        return self.interface_struct

    @property
    def members(self) -> list[Arg]:
        return self.interface_struct.members

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        # Build a dict of example values keyed appropriately depending on language.
        example_list: dict[str, str]
        if lang in ["rust", "python"]:
            example_list = {
                stringmanip.snake_case(a.name): str(a.get_random_example_value(lang, seed=seed))
                for a in self.members
            }
        else:
            example_list = {
                a.name: str(a.get_random_example_value(lang, seed=seed))
                for a in self.members
            }
        if lang == "c++":
            return self.cpp.type + "{" + ", ".join(example_list.values()) + "}"  # type: ignore[attr-defined]
        elif lang == "python":
            init_list = ", ".join([f"{k}={v}" for k, v in example_list.items()])
            return f"{self.interface_struct.python.type}({init_list})"  # type: ignore[attr-defined]
        elif lang == "rust":
            return "%s%s {%s}%s" % (
                "Some(" if self.optional else "",
                self.interface_struct.rust.type,  # type: ignore[attr-defined]
                ", ".join([f"{k}: {v}" for k, v in example_list.items()]),
                ")" if self.optional else "",
            )
        elif lang == "json":
            return "{" + ", ".join([f'"{k}": {v}' for k, v in example_list.items()]) + "}"
        elif hasattr(self, lang) and hasattr(getattr(self, lang), "get_random_example_value"):
            return getattr(self, lang).get_random_example_value(seed=seed)
        return None

    def __str__(self) -> str:
        return f"<ArgStruct name={self.name}>"

    def __repr__(self):
        return f"ArgStruct(name={self.name}, iface_struct={self.interface_struct})"

class ArgDateTime(Arg):
    
    arg_type: ArgType = Field(default=ArgType.DATETIME, description="The type of the argument, which is 'datetime' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)


    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        if lang == "python":
            if self.optional and random.choice([True, False, False, False]):
                return "None"
            return f"datetime.now(UTC)"
        elif lang == "rust":
            if self.optional:
                return "Some(chrono::Utc::now())"
            return "chrono::Utc::now()"
        elif lang in ["c++", "cpp"]:
            return "std::chrono::system_clock::now()"
        elif lang == "json":
            return '"1990-07-08T16:20:00Z"'
        elif hasattr(self, lang) and hasattr(getattr(self, lang), "get_random_example_value"):
            return getattr(self, lang).get_random_example_value(seed=seed)
        return None

    def __str__(self) -> str:
        return f"<ArgDateTime name={self.name}>"

    def __repr__(self):
        return f"ArgDateTime(name={self.name})"

class ArgDuration(Arg):
    arg_type: ArgType = Field(default=ArgType.DURATION, description="The type of the argument, which is 'duration' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)


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
            if self.optional:
                retval = f"Some(chrono::Duration::seconds({random.randint(1, 3600)}))"
            else:
                retval = f"chrono::Duration::seconds({random.randint(1, 3600)})"
        elif lang in ["c++", "cpp"]:
            retval = f"std::chrono::duration<double>({random.randint(1, 3600)})"
        elif lang == "json":
            if self.optional and random.choice([True, False, False, False]):
                retval = "null"
            else:
                retval = f'"PT{random.randint(1, 3600)}S"'  # ISO 8601 duration format
        elif hasattr(self, lang) and hasattr(getattr(self, lang), "get_random_example_value"):
            retval = getattr(self, lang).get_random_example_value(seed=seed)
        random.setstate(random_state)
        return retval

    def __str__(self) -> str:
        return f"<ArgDuration name={self.name}>"

    def __repr__(self):
        return f"ArgDuration(name={self.name})"
    

class ArgBinary(Arg):
    
    arg_type: ArgType = Field(default=ArgType.BINARY, description="The type of the argument, which is 'binary' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)



    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        if lang == "python":
            return f'b"example binary data"'
        elif lang == "rust":
            if self.optional:
                return 'Some(vec![101, 120, 97, 109, 112, 108, 101])'  # "example" in ASCII bytes
            return 'vec![101, 120, 97, 109, 112, 108, 101]'  # "example" in ASCII bytes
        elif lang in ["c++", "cpp"]:
            return 'std::vector<uint8_t>{101, 120, 97, 109, 112, 108, 101}'  # "example" in ASCII bytes
        if lang == "json":
            if self.optional and random.choice([True, False, False, False]):
                retval = "null"
            else:
                retval = '"ZXhhbXBsZSBiaW5hcnkgZGF0YQ=="'  # "example binary data" base64-encoded
            return retval
        elif hasattr(self, lang) and hasattr(getattr(self, lang), "get_random_example_value"):
            return getattr(self, lang).get_random_example_value(seed=seed)
        return None

    def __str__(self) -> str:
        return f"<ArgBinary name={self.name}>"

    def __repr__(self):
        return f"ArgBinary(name={self.name})"
    

class ArgArray(Arg):
    
    element: Arg = Field(..., description="The type of the elements in the array")
    arg_type: ArgType = Field(default=ArgType.ARRAY, description="The type of the argument, which is 'array' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)


    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        example_value = self.element.get_random_example_value(lang, seed=seed)
        example_value2 = self.element.get_random_example_value(lang, seed=seed+1)
        example_value3 = self.element.get_random_example_value(lang, seed=seed+2)
        if lang == "python":
            return f"[{example_value}, {example_value2}]"
        elif lang == "rust":
            if self.optional:
                return f"Some(vec![{example_value}, {example_value2}, {example_value3}])"
            return f"vec![{example_value}, {example_value2}]"
        elif lang in ["c++", "cpp"]:
            return f"std::vector<{self.element.cpp.temp_type}>{{{example_value}, {example_value2}, {example_value3}}}"  # type: ignore[attr-defined]
        elif lang == "json":
            if self.optional and random.choice([True, False, False, False, False]):
                retval = "null"
            elif random.choice([True, False, False, True, False]):
                retval = "[]"
            else:
                retval = f"[{example_value}, {example_value2}]"
            return retval
        elif hasattr(self, lang) and hasattr(getattr(self, lang), "get_random_example_value"):
            return getattr(self, lang).get_random_example_value(seed=seed)
        return None

    def __str__(self) -> str:
        return f"<ArgArray name={self.name} element_type={self.element}>"

    def __repr__(self):
        return f"ArgArray(name={self.name}, element_type={self.element})"
