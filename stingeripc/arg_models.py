from __future__ import annotations

import json
import math
import random
from abc import abstractmethod
from copy import copy
from typing import Any, Callable, Optional, Mapping, Sequence, TYPE_CHECKING

import jsonschema_rs
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


# Draft 4 validators, keyed by the schema they were built from.  Building one is not
# free and the same handful of schemas are asked about repeatedly while rendering.
_VALIDATOR_CACHE: dict[str, Any] = {}

# How many integers to walk when deriving a value from a numeric constraint.
_DERIVE_SCAN_LIMIT = 2000

# The stock example values for each primitive type.  They are the plain JSON values rather
# than language-rendered snippets, so a candidate can be checked against a 'schema'
# constraint before it is rendered.
_BOOLEAN_EXAMPLES: tuple[bool, ...] = (True, False)
_FLOAT_EXAMPLES: tuple[float, ...] = (3.14, 1.0, 2.5, 97.9, 1.53, 2.718, 1.618, 1.4142, 0.333333333, 98.6)
_INTEGER_EXAMPLES: tuple[int, ...] = (42, 1981, 2020, 2022, 1200, 5, 99, 123, 2025, 1955, 2, 0, 10, 100, 25, 216, 256)
_STRING_EXAMPLES: tuple[str, ...] = ("apples", "Joe", "example", "foo", "bar", "tiger", "bear", "root beer", "smart home", "pegasus", "general", "be wise")


def _draft4_validator(schema: dict[str, Any]) -> Any:
    """Return a cached Draft 4 validator for an argument's ``schema`` constraint.

    Argument schemas are Draft 4 — the subset the RapidJSON C++ validator implements —
    so this generator and the generated code agree on what a constraint means.
    """
    key = json.dumps(schema, sort_keys=True, default=str)
    validator = _VALIDATOR_CACHE.get(key)
    if validator is None:
        validator = jsonschema_rs.Draft4Validator(schema)
        _VALIDATOR_CACHE[key] = validator
    return validator


def _derive_integers(schema: dict[str, Any]) -> list[int]:
    """Integers to try when no stock example satisfies a constraint.

    The bounds narrow the walk; the validator decides which of the values is acceptable,
    so ``exclusiveMinimum``, ``multipleOf``, and friends need no special handling here.
    """
    low, high = schema.get("minimum"), schema.get("maximum")
    if low is not None:
        start = int(math.ceil(low))
    elif high is not None:
        start = int(math.floor(high)) - _DERIVE_SCAN_LIMIT
    else:
        start = 0
    end = int(math.floor(high)) if high is not None else start + _DERIVE_SCAN_LIMIT
    if end < start:
        return []
    return list(range(start, min(end, start + _DERIVE_SCAN_LIMIT) + 1))


def _derive_floats(schema: dict[str, Any]) -> list[float]:
    """Floats to try when no stock example satisfies a constraint."""
    low, high = schema.get("minimum"), schema.get("maximum")
    step = schema.get("multipleOf")
    probes: list[float] = []
    if low is not None and high is not None:
        span = high - low
        probes += [low + span * fraction for fraction in (0.5, 0.25, 0.75, 0.1, 0.9)]
        probes += [float(low), float(high)]
    elif low is not None:
        probes += [float(low), low + 0.5, low + 1.0, low + 10.0]
    elif high is not None:
        probes += [float(high), high - 0.5, high - 1.0, high - 10.0]
    if step:
        base = low if low is not None else 0.0
        first = step * math.ceil(base / step)
        probes += [first + step * n for n in range(4)]
    return probes


def _derive_strings(schema: dict[str, Any]) -> list[str]:
    """Strings to try when no stock example satisfies a length constraint.

    A ``pattern`` constraint cannot be satisfied by construction, so nothing here tries
    to; the caller reports an unsatisfiable constraint instead of guessing.
    """
    min_length = int(schema.get("minLength", 0) or 0)
    max_length = schema.get("maxLength")
    filler = "example value long enough to satisfy a generous maxLength constraint"
    lengths = {max(min_length, 1)}
    if max_length is not None:
        lengths.add(int(max_length))
    if min_length == 0:
        lengths.add(0)
    probes: list[str] = []
    for length in sorted(lengths):
        if length <= 0:
            probes.append("")
            continue
        probes.append((filler * (length // len(filler) + 1))[:length])
    return probes


def _spec_version_at_least(version: Optional[str], minimum: tuple[int, ...]) -> bool:
    """Return True if the dotted version string is >= the given minimum version tuple."""
    if not version:
        return False
    try:
        parts = tuple(int(p) for p in version.split("."))
    except ValueError:
        return False
    return parts >= minimum


class Arg(BaseModel):
    """Represents an argument to a method, signal, or property.  This is the base class for all argument types."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    name: str = Field(..., description="The name of the argument")
    description: str | None = Field(default=None, description="A description of the argument")
    optional: bool = Field(default=False, description="Whether the argument is optional")
    arg_type: ArgType = Field(default=ArgType.UNKNOWN, description="The type of the argument")
    value_schema: dict[str, Any] | None = Field(
        default=None,
        alias="schema",
        description="An optional JSON Schema (limited to the subset supported by the RapidJSON C++ validator) that further constrains the value.",
    )

    def try_set_description_from_spec(self, spec: Mapping[str, Any]) -> "Arg":
        """Set ``description`` from a parsed spec dict if it has a string value."""
        if "description" in spec and isinstance(spec["description"], str):
            self.description = spec["description"].strip()
        return self

    def schema_allows(self, value: Any) -> bool:
        """True if ``value`` satisfies this argument's ``schema`` constraint.

        An argument that declares no constraint allows everything.
        """
        if not self.value_schema:
            return True
        return bool(_draft4_validator(self.value_schema).is_valid(value))

    def _pick_example_value(self, candidates: Sequence[Any], derive: Optional[Callable[[dict[str, Any]], Sequence[Any]]] = None) -> Any:
        """Choose a random example value that satisfies this argument's ``schema`` constraint.

        An argument with no constraint gets a plain random choice, so its example values
        are exactly what they were before constraints were taken into account.  When a
        constraint is declared, the stock candidates are narrowed to the conforming ones;
        if none conform, the constraint's own ``enum`` and then values derived from its
        bounds are tried.  The point is that generated demos, tests, and documentation
        never carry a value that the generated validation code would reject.
        """
        if not self.value_schema:
            return random.choice(list(candidates))

        conforming = [candidate for candidate in candidates if self.schema_allows(candidate)]
        if conforming:
            return random.choice(conforming)

        schema_enum = self.value_schema.get("enum")
        if isinstance(schema_enum, list):
            for candidate in schema_enum:
                if self.schema_allows(candidate):
                    return candidate

        if derive is not None:
            for candidate in derive(self.value_schema):
                if self.schema_allows(candidate):
                    return candidate

        raise InvalidStingerStructure(
            f"Could not build an example value for the '{self.name}' argument that satisfies its "
            f"'schema' constraint {self.value_schema}.  Example values are used by the generated "
            f"demos, tests, and documentation, so the constraint needs at least one value that a "
            f"generated example can actually take.  Widen the constraint, or state it in a form "
            f"that a concrete value can satisfy (a 'pattern' cannot be satisfied by construction)."
        )

    def try_set_schema_from_spec(self, spec: Mapping[str, Any]) -> "Arg":
        """Set ``value_schema`` from a parsed spec dict's ``schema`` block if present."""
        if "schema" in spec and isinstance(spec["schema"], Mapping):
            self.value_schema = dict(spec["schema"])
        return self

    def __str__(self) -> str:
        return repr(self)

    @classmethod
    def new_arg_from_stinger(cls, arg_spec: YamlArg, stinger_spec: Optional[StingerSpec] = None) -> Arg:
        """Build the appropriate Arg subclass from a parsed Stinger arg spec dict.

        Dispatches on the ``type`` key to construct primitives, enums, structs,
        datetimes, durations, binary, and array arguments.  Enum and struct args
        require the owning :class:`StingerSpec` to resolve their referenced
        enum/struct definitions.
        """
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
                raise RuntimeError("Need the root StingerSpec when creating an enum or struct Arg")

        if spec["type"] == "enum":
            if "enumName" not in arg_spec:
                raise InvalidStingerStructure(f"Enum args need a 'enumName'")
            if not isinstance(arg_spec["enumName"], str):
                raise InvalidStingerStructure("'enumName' in arg structure must be a string")
            if arg_spec["enumName"] not in stinger_spec.enums:
                raise InvalidStingerStructure(f"Enum arg '{arg_spec['enumName']}' was not found in the list of stinger spec enums")
            enum_arg = ArgEnum(name=spec["name"], enum=stinger_spec.get_interface_enum(spec["enumName"]))
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                enum_arg.optional = opt
            enum_arg.try_set_description_from_spec(spec)
            enum_arg.try_set_schema_from_spec(spec)
            return enum_arg

        if spec["type"] == "struct":
            if "structName" not in spec:
                raise InvalidStingerStructure("Struct args need a 'structName'")
            if not isinstance(spec["structName"], str):
                raise InvalidStingerStructure("'structName' in arg structure must be a string")
            if spec["structName"] not in stinger_spec.structs:
                raise InvalidStingerStructure(f"Struct arg '{spec["structName"]}' was not found in the list of stinger spec structs")
            st_arg = ArgStruct(name=spec["name"], interface_struct=stinger_spec.structs[spec["structName"]])
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                st_arg.optional = opt
            st_arg.try_set_description_from_spec(spec)
            st_arg.try_set_schema_from_spec(spec)
            return st_arg

        if spec["type"] == "datetime":
            dt_arg = ArgDateTime(name=spec["name"])
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                dt_arg.optional = opt
            dt_arg.try_set_description_from_spec(spec)
            dt_arg.try_set_schema_from_spec(spec)
            return dt_arg

        if spec["type"] == "duration":
            dur_arg = ArgDuration(name=spec["name"])
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                dur_arg.optional = opt
            dur_arg.try_set_description_from_spec(spec)
            dur_arg.try_set_schema_from_spec(spec)
            return dur_arg

        if spec["type"] == "binary":
            bin_arg = ArgBinary(name=spec["name"])
            if opt := spec.get("optional", False):
                if not isinstance(opt, bool):
                    raise InvalidStingerStructure("'optional' in arg structure must be a boolean")
                bin_arg.optional = opt
            bin_arg.content_type = spec.get("contentType")
            if bin_arg.content_type is None and _spec_version_at_least(stinger_spec.spec_version, (0, 2, 0)):
                raise InvalidStingerStructure(f"Binary arg '{spec['name']}' requires a 'contentType' for stinger spec version 0.2.0 or later")
            bin_arg.try_set_description_from_spec(spec)
            bin_arg.try_set_schema_from_spec(spec)
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
            array_arg.try_set_schema_from_spec(spec)
            return array_arg

        raise RuntimeError(f"unknown arg type: {arg_spec['type']}")

    @abstractmethod
    def get_random_example_value(self, lang="python", seed: int = 0):
        """Return a randomly generated example value for this argument.

        The returned value is expressed as a code snippet in the requested
        target ``lang`` (e.g. ``'python'``, ``'rust'``, ``'c++'``, or
        ``'json'``) and is used by demos, tests, and documentation.
        """
        pass


class ArgEnum(Arg):
    """An argument whose value is restricted to one of an enum's members."""

    enum: InterfaceEnum = Field(..., description="The InterfaceEnum that restricts the values this ArgEnum represents.")
    arg_type: ArgType = Field(default=ArgType.ENUM, description="The type of the argument, which is 'enum' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    def get_random_example_value(self, lang="python", seed: int = 2) -> str:
        """Return a randomly chosen enum member expressed for the target language.

        An enum value travels the wire as its integer, so a ``schema`` constraint on the
        argument narrows which members an example may use.
        """
        random_state = random.getstate()
        random.seed(seed)
        allowed_items = [item for item in self.enum.items if self.schema_allows(item.integer)]
        if not allowed_items:
            random.setstate(random_state)
            raise InvalidStingerStructure(
                f"No member of the '{self.enum.name}' enum satisfies the 'schema' constraint "
                f"{self.value_schema} declared on the '{self.name}' argument, so no example value can be built."
            )
        random_enum_item = random.choice(allowed_items)
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
    """An argument whose value is a single primitive (boolean, integer, float, or string)."""

    arg_type: ArgType = Field(default=ArgType.PRIMITIVE, description="The type of the argument, which is 'primitive' for this class")
    primitive_type: ArgPrimitiveType = Field(..., description="The specific primitive type that this argument represents (e.g. boolean, integer, float, string)")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    @property
    def type(self) -> ArgPrimitiveType:
        """The primitive type of this argument (alias for ``primitive_type``)."""
        return self.primitive_type

    @property
    def protobuf_type(self) -> str:
        """The protocol buffer type string for this argument (e.g. ``int32``)."""
        return ArgPrimitiveType.to_protobuf_type(self.primitive_type)

    @property
    def json_type(self) -> str:
        """The JSON schema type string for this argument (e.g. ``integer``)."""
        return ArgPrimitiveType.to_json_type(self.primitive_type)

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | float | int | bool | None:
        """Return a random example value for this primitive in the target language.

        When the argument declares a ``schema`` constraint, the value satisfies it, so the
        generated demos and tests never carry a value the generated code would reject.
        """
        random_state = random.getstate()
        random.seed(seed)
        try:
            retval: str | float | int | bool | None = None
            if self.primitive_type == ArgPrimitiveType.BOOLEAN:
                retval = self._pick_example_value(_BOOLEAN_EXAMPLES)
                if lang != "python":
                    retval = str(retval).lower()
            elif self.primitive_type == ArgPrimitiveType.FLOAT:
                retval = self._pick_example_value(_FLOAT_EXAMPLES, _derive_floats)
            elif self.primitive_type == ArgPrimitiveType.INTEGER:
                retval = self._pick_example_value(_INTEGER_EXAMPLES, _derive_integers)
            elif self.primitive_type == ArgPrimitiveType.STRING:
                retval = f'"{self._pick_example_value(_STRING_EXAMPLES, _derive_strings)}"'
                if lang == "rust":
                    retval = f"{retval}.to_string()"
                if self.optional and lang in ["cpp", "c++"]:
                    retval = f"std::make_optional(std::string({retval}))"
            if self.optional and lang == "rust":
                retval = f"Some({retval})"
            return retval
        finally:
            random.setstate(random_state)

    def __repr__(self) -> str:
        return f"<ArgPrimitive name={self.name} type={ArgPrimitiveType.to_python_type(self.primitive_type)}>"

    @classmethod
    def new_arg_primitive_from_stinger(cls, arg_spec: Mapping[str, Any]) -> ArgPrimitive:
        """Build an ArgPrimitive from a parsed Stinger arg spec dict.

        The ``type`` key must name one of the supported primitive types (e.g.
        ``boolean``, ``integer``, ``float``, ``string``).
        """
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
        arg.try_set_schema_from_spec(arg_spec)
        return arg


class ArgStruct(Arg):
    """An argument whose value is an instance of a named struct."""

    interface_struct: InterfaceStruct = Field(..., description="The InterfaceStruct that defines the structure used for this argument.")
    arg_type: ArgType = Field(default=ArgType.STRUCT, description="The type of the argument, which is 'struct' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    @property
    def struct(self) -> InterfaceStruct:
        """The InterfaceStruct this argument references (alias for ``interface_struct``)."""
        return self.interface_struct

    @property
    def values(self) -> list[Arg]:
        """The values of the referenced struct."""
        return self.interface_struct.values

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        """Return a random example struct value expressed in the target language."""
        # Build a dict of example values keyed appropriately depending on language.
        example_list: dict[str, str]
        if lang in ["rust", "python"]:
            example_list = {stringmanip.snake_case(a.name): str(a.get_random_example_value(lang, seed=seed)) for a in self.values}
        else:
            example_list = {a.name: str(a.get_random_example_value(lang, seed=seed)) for a in self.values}
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
    """An argument whose value is a date/time instant."""

    arg_type: ArgType = Field(default=ArgType.DATETIME, description="The type of the argument, which is 'datetime' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        """Return a random datetime example expressed in the target language."""
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
    """An argument whose value is a duration (a span of time)."""

    arg_type: ArgType = Field(default=ArgType.DURATION, description="The type of the argument, which is 'duration' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        """Return a random duration example expressed in the target language."""
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
    """An argument whose value is arbitrary binary data (e.g. a file)."""

    arg_type: ArgType = Field(default=ArgType.BINARY, description="The type of the argument, which is 'binary' for this class")
    content_type: Optional[str] = Field(default=None, description="The MIME content type of the binary data. Required for schema version 0.2+, optional for earlier versions.")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        """Return a random binary example expressed in the target language."""
        if lang == "python":
            return f'b"example binary data"'
        elif lang == "rust":
            if self.optional:
                return "Some(vec![101, 120, 97, 109, 112, 108, 101])"  # "example" in ASCII bytes
            return "vec![101, 120, 97, 109, 112, 108, 101]"  # "example" in ASCII bytes
        elif lang in ["c++", "cpp"]:
            return "std::vector<uint8_t>{101, 120, 97, 109, 112, 108, 101}"  # "example" in ASCII bytes
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
    """An argument whose value is a list of elements of a single element type."""

    element: Arg = Field(..., description="The type of the elements in the array")
    arg_type: ArgType = Field(default=ArgType.ARRAY, description="The type of the argument, which is 'array' for this class")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    def _example_element_count(self, default: int) -> int:
        """How many example elements to emit, clamped to any ``minItems``/``maxItems`` constraint."""
        schema = self.value_schema or {}
        count = default
        min_items = schema.get("minItems")
        max_items = schema.get("maxItems")
        if isinstance(min_items, int):
            count = max(count, min_items)
        if isinstance(max_items, int):
            count = min(count, max_items)
        return max(count, 0)

    def _example_elements(self, lang: str, seed: int, count: int) -> str:
        """Render ``count`` example elements, each from its own seed, as a comma-separated list."""
        return ", ".join(str(self.element.get_random_example_value(lang, seed=seed + offset)) for offset in range(count))

    def get_random_example_value(self, lang="python", seed: int = 2) -> str | None:
        """Return a random array example expressed in the target language.

        A ``schema`` constraint on the array itself decides how many elements an example
        carries, and one on the element type constrains each element.
        """
        if lang == "python":
            return f"[{self._example_elements(lang, seed, self._example_element_count(2))}]"
        elif lang == "rust":
            if self.optional:
                return f"Some(vec![{self._example_elements(lang, seed, self._example_element_count(3))}])"
            return f"vec![{self._example_elements(lang, seed, self._example_element_count(2))}]"
        elif lang in ["c++", "cpp"]:
            return f"std::vector<{self.element.cpp.temp_type}>{{{self._example_elements(lang, seed, self._example_element_count(3))}}}"  # type: ignore[attr-defined]
        elif lang == "json":
            # An empty array or a null is only offered when the constraint actually permits it.
            if self.optional and self.schema_allows(None) and random.choice([True, False, False, False, False]):
                retval = "null"
            elif self.schema_allows([]) and random.choice([True, False, False, True, False]):
                retval = "[]"
            else:
                retval = f"[{self._example_elements(lang, seed, self._example_element_count(2))}]"
            return retval
        elif hasattr(self, lang) and hasattr(getattr(self, lang), "get_random_example_value"):
            return getattr(self, lang).get_random_example_value(seed=seed)
        return None

    def __str__(self) -> str:
        return f"<ArgArray name={self.name} element_type={self.element}>"

    def __repr__(self):
        return f"ArgArray(name={self.name}, element_type={self.element})"
