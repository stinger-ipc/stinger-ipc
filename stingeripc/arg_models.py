from __future__ import annotations

import random
from abc import abstractmethod
from copy import copy
from typing import Any, Optional, Mapping, TYPE_CHECKING

from stevedore import ExtensionManager
from jacobsjinjatoo import stringmanip

from stingeripc.config import StingerConfig
from .args import ArgType, ArgPrimitiveType
from .exceptions import InvalidStingerStructure

if TYPE_CHECKING:
    from stingeripc.components import InterfaceEnum, InterfaceStruct, StingerSpec

YamlArg = Mapping[str, str | bool]
YamlArgList = list[YamlArg]
YamlIfaceEnum = dict[str, str | YamlArgList]
YamlIfaceEnums = dict[str, YamlIfaceEnum]
YamlIfaceProperty = dict[str, str | bool | YamlArgList]

# These names cannot be used for method/property/signal names because they are reserved keywords.
RESTRICTED_NAMES = ["type", "class", "struct", "enum", "list", "map", "set", "optional", "bool", "int", "float", "string", "datetime", "duration", "binary"]


class LanguageSymbolMixin:
    """ When this class is provided as a mixin to a child class, it allows the child class to search for plugins that can provide language-specific symbols for the child class.
    
    Plugins are registered by providing a `project.entry-points."stinger_symbols"` entry in `pyproject.toml`.  Plugins have a name/domain that is used to identify the language.
    """

    def __init__(self, config: StingerConfig|None = None):
        """ The ExtensionManager searches for all `stinger_symbols` plugins.  For each discovered plugin, it invokes the plugin's `for_model`
        method to determine a symbol-providing class to attached to the child class (if any).  The symbol-providing class is then attached 
        as an attribute to the child class, with the attribute name equal to the plugin's name/domain.  
        """
        mgr: ExtensionManager = ExtensionManager(
            namespace="stinger_symbols",
            invoke_on_load=True,
            invoke_kwds={"config": config},
        )
        for ext in mgr:
            domain = ext.name
            if ext.obj is not None:
                symbols = ext.obj.for_model(self.__class__.__name__, self)
                if symbols is not None:
                    setattr(self, domain, symbols)

class Arg:
    """Represents an argument to a method, signal, or property.  This is the base class for all argument types."""

    def __init__(self, name: str, description: Optional[str] = None):
        self._name = name
        self._description = description.strip() if description else None
        self._default_value = None
        self._type: ArgType = ArgType.UNKNOWN
        self._optional: bool = False

    def set_description(self, description: str) -> Arg:
        self._description = description.strip()
        return self

    def try_set_description_from_spec(self, spec: Mapping[str, Any]) -> Arg:
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
                spec["name"], stinger_spec.get_interface_enum(spec["enumName"])
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
                spec["name"], stinger_spec.structs[spec["structName"]]
            )
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                st_arg.optional = opt
            st_arg.try_set_description_from_spec(spec)
            return st_arg
        
        if spec["type"] == "datetime":
            dt_arg = ArgDateTime(spec["name"])
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                dt_arg.optional = opt
            dt_arg.try_set_description_from_spec(spec)
            return dt_arg

        if spec["type"] == "duration":
            dur_arg = ArgDuration(spec["name"])
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                dur_arg.optional = opt
            dur_arg.try_set_description_from_spec(spec)
            return dur_arg
        
        if spec["type"] == "binary":
            bin_arg = ArgBinary(spec["name"])
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
            array_arg = ArgArray(spec["name"], element_arg)
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


class ArgEnum(Arg, LanguageSymbolMixin):
    
    def __init__(self, name: str, enum: InterfaceEnum, description: Optional[str] = None):
        Arg.__init__(self, name, description)
        LanguageSymbolMixin.__init__(self)
        self._enum = enum
        self._type = ArgType.ENUM

    @property
    def enum(self) -> InterfaceEnum:
        return self._enum

    def get_random_example_value(self, lang="python", seed: int = 2) -> str:
        random_state = random.getstate()
        random.seed(seed)
        random_enum_item = random.choice(self._enum.items)
        if lang == "python":
            retval = f"{self._enum.class_name}.{stringmanip.const_case(random_enum_item.name) }"
        elif lang == "c++":
            retval = f"{self._enum.class_name}::{stringmanip.const_case(random_enum_item.name)}"
        elif lang == "rust":
            if self.optional:
                retval = f"Some({self._enum.class_name}::{stringmanip.upper_camel_case(random_enum_item.name)})"
            else:
                retval = f"{self._enum.class_name}::{stringmanip.upper_camel_case(random_enum_item.name)}"
        elif lang == "json":
            retval = str(random_enum_item.integer)
        elif hasattr(self, lang) and hasattr(getattr(self, lang), "get_random_example_value"):
            retval = getattr(self, lang).get_random_example_value(seed=seed)
        else:
            raise RuntimeError(f"Unknown language for enum random example value: {lang}")
        random.setstate(random_state)
        return retval

    def __repr__(self) -> str:
        return f"<ArgEnum name={self._name}>"


class ArgPrimitive(Arg, LanguageSymbolMixin):
    
    def __init__(
        self, name: str, arg_type: ArgPrimitiveType, description: Optional[str] = None
    ):
        Arg.__init__(self, name, description)
        LanguageSymbolMixin.__init__(self)
        self._arg_type = arg_type
        self._type = ArgType.PRIMITIVE

    @property
    def type(self) -> ArgPrimitiveType:
        return self._arg_type

    @property
    def primitive_type(self) -> ArgPrimitiveType:
        return self._arg_type

    @property
    def protobuf_type(self) -> str:
        return ArgPrimitiveType.to_protobuf_type(self._arg_type)

    @property
    def json_type(self) -> str:
        return ArgPrimitiveType.to_json_type(self._arg_type)

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
                retval = f'std::make_optional(std::string({retval}))'
        if self.optional and lang == "rust":
            retval = f"Some({retval})"
        random.setstate(random_state)
        return retval

    def __repr__(self) -> str:
        return f"<ArgPrimitive name={self._name} type={ArgPrimitiveType.to_python_type(self.type)}>"

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
        arg: ArgPrimitive = cls(name=arg_spec["name"], arg_type=arg_primitive_type)

        arg.try_set_description_from_spec(arg_spec)
        return arg


class ArgStruct(Arg, LanguageSymbolMixin):

    def __init__(self, name: str, iface_struct: InterfaceStruct):
        Arg.__init__(self, name)
        LanguageSymbolMixin.__init__(self)
        from stingeripc.components import InterfaceStruct as _InterfaceStruct
        assert isinstance(
            iface_struct, _InterfaceStruct
        ), f"Passed {iface_struct=} is type {type(iface_struct)} which is not InterfaceStruct"
        self._interface_struct: InterfaceStruct = iface_struct
        self._type = ArgType.STRUCT

    @property
    def struct(self) -> InterfaceStruct:
        return self._interface_struct

    @property
    def interface_struct(self) -> InterfaceStruct:
        return self._interface_struct

    @property
    def members(self) -> list[Arg]:
        return self._interface_struct.members

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
            return f"{self._interface_struct.python.type}({init_list})"  # type: ignore[attr-defined]
        elif lang == "rust":
            return "%s%s {%s}%s" % (
                "Some(" if self.optional else "",
                self._interface_struct.rust.type,  # type: ignore[attr-defined]
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
        return f"ArgStruct(name={self.name}, iface_struct={self._interface_struct})"

class ArgDateTime(Arg, LanguageSymbolMixin):
    
    def __init__(self, name: str):
        Arg.__init__(self, name)
        LanguageSymbolMixin.__init__(self)
        self._type = ArgType.DATETIME

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

class ArgDuration(Arg, LanguageSymbolMixin):
    
    def __init__(self, name: str):
        Arg.__init__(self, name)
        LanguageSymbolMixin.__init__(self)
        self._type = ArgType.DURATION

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
    

class ArgBinary(Arg, LanguageSymbolMixin):
    
    def __init__(self, name: str):
        Arg.__init__(self, name)
        LanguageSymbolMixin.__init__(self)
        self._type = ArgType.BINARY

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
    

class ArgArray(Arg, LanguageSymbolMixin):
    
    def __init__(self, name: str, element_type: Arg):
        Arg.__init__(self, name)
        LanguageSymbolMixin.__init__(self)
        self._element = element_type
        self._type = ArgType.ARRAY

    @property
    def element(self) -> Arg:
        return self._element

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
