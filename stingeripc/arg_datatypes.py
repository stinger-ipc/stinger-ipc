from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from jacobsjinjatoo import stringmanip
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from stingeripc.exceptions import InvalidStingerStructure
from stingeripc.lang_symb import LanguageSymbolMixin
from stingeripc.arg_models import YamlIfaceEnum, Arg

if TYPE_CHECKING:
    from stingeripc.components import StingerSpec


class EnumItem(BaseModel):
    """A single member of an :class:`InterfaceEnum`.

    Each member has a ``name``, an optional integer ``integer`` value (the
    underlying wire value), and an optional ``description``.
    """

    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(..., description="The name of the enum member", pattern=r"^[a-zA-Z0-9_ -]+$")
    integer: Optional[int] = Field(default=None, alias="value", description="The integer wire value of the member; auto-assigned if omitted")
    description: Optional[str] = Field(default=None, description="A brief description of the enum member")


class InterfaceEnum(BaseModel):
    """A named enumerated type defined by the interface.

    An enum is an ordered collection of :class:`EnumItem` members, each bound
    to a distinct integer value.  The collection is also assigned a language
    ``class_name`` (upper camel case) used by the generated code.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str = Field(..., description="The name of the enum")
    enum_items: list[EnumItem] = Field(default_factory=list, alias="values", description="The members of the enum, in declaration order")
    documentation: Optional[str] = Field(default=None, description="A brief description of the enum")
    version: Optional[str] = Field(default=None, description="The version of the enum", pattern=r"^[0-9]+(\.[0-9]+){0,2}$")

    @model_validator(mode="after")
    def _assign_and_check_integers(self) -> InterfaceEnum:
        seen: set[int] = set()
        next_int = 1
        for item in self.enum_items:
            if item.integer is None:
                while next_int in seen:
                    next_int += 1
                item.integer = next_int
            if item.integer in seen:
                raise ValueError(f"duplicate integer value {item.integer}")
            seen.add(item.integer)
            next_int = item.integer + 1
        return self

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    def add_item(self, value: str, integer: Optional[int] = None, description: Optional[str] = None):
        """Append a member to the enum.

        If ``integer`` is omitted it is derived from the highest existing member
        value plus one (starting at 1 for an empty enum).
        """
        integer_value = integer if integer is not None else ((max(i.integer for i in self.enum_items if i.integer is not None) + 1) if len(self.enum_items) > 0 else 1)
        item = EnumItem(name=value, value=integer_value, description=description)
        self.enum_items.append(item)

    def has_value(self, integer: int) -> bool:
        """Return True if any member of the enum has the given integer value."""
        for item in self.enum_items:
            if item.integer == integer:
                return True
        return False

    @property
    def class_name(self):
        """The upper-camel-case class name used for this enum in generated code."""
        return stringmanip.upper_camel_case(self.name)

    @property
    def items(self) -> list[EnumItem]:
        """The enum members, with any zero-valued member placed first.

        Protocol buffer definitions require an initial zero value, so if the
        enum declares a member with integer value 0 it is moved to the front.
        """
        if self.has_value(0) and self.enum_items[0].integer != 0:
            # Rearrange so that the item with integer value 0 is first. This is because .proto files require an initial 0-value.
            rearranged_items = [item for item in self.enum_items if item.integer == 0]
            rearranged_items.extend([item for item in self.enum_items if item.integer != 0])
            return rearranged_items
        else:
            return self.enum_items

    @classmethod
    def new_enum_from_stinger(cls, name, enum_spec: YamlIfaceEnum) -> InterfaceEnum:
        """Construct an InterfaceEnum from a parsed Stinger enum spec dict."""
        if "values" not in enum_spec:
            raise InvalidStingerStructure(f"InterfaceEnum '{name}' spec is missing required 'values'")
        if len(enum_spec["values"]) == 0:
            raise InvalidStingerStructure(f"InterfaceEnum '{name}' must have at least one value")
        try:
            return cls.model_validate({"name": name, **enum_spec})
        except ValidationError as e:
            raise InvalidStingerStructure(f"InterfaceEnum '{name}' spec is invalid: {e}") from e


class InterfaceStruct(BaseModel):
    """A named structured type defined by the interface.

    A struct is an ordered collection of member :class:`Arg` objects.  It is
    assigned a language ``class_name`` (upper camel case) used by the generated
    code.
    """

    model_config = ConfigDict(extra="allow")

    name: str = Field(..., description="The name of the struct")
    members: list[Arg] = Field(default_factory=list, description="The ordered list of member arguments that make up the struct")
    documentation: Optional[str] = Field(default=None, description="A brief description of the struct")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    def add_member(self, arg: Arg):
        """Append a member argument to the struct."""
        self.members.append(arg)

    @property
    def class_name(self):
        """The upper-camel-case class name used for this struct in generated code."""
        return stringmanip.upper_camel_case(self.name)

    @property
    def values(self) -> list[Arg]:
        """The struct's member arguments (alias for ``members``)."""
        return self.members

    @classmethod
    def new_struct_from_stinger(
        cls,
        name,
        spec: dict[str, str | list[dict[str, str]]],
        stinger_spec: StingerSpec,
    ) -> InterfaceStruct:
        """Construct an InterfaceStruct from a parsed Stinger struct spec dict.

        Each entry in the spec's ``members`` list is parsed into an :class:`Arg`
        using the owning :class:`StingerSpec` to resolve referenced enums and
        structs.
        """
        istruct = cls(name=name)
        for memb in spec.get("members", []):
            if not isinstance(memb, dict):
                raise InvalidStingerStructure("Struct members must be dicts")
            arg = Arg.new_arg_from_stinger(memb, stinger_spec=stinger_spec)
            istruct.add_member(arg)
        documentation = spec.get("documentation", None)
        if documentation is not None and not isinstance(documentation, str):
            raise InvalidStingerStructure("Struct documentation must be a string")
        istruct.documentation = documentation
        return istruct

    def __str__(self) -> str:
        return f"<InterfaceStruct members={[m.name for m in self.members]}>"

    def __repr__(self):
        return f"InterfaceStruct(name={self.name})"


class InterfaceConstant(BaseModel):
    """A named constant value defined by the interface.

    Constants have a ``name``, a ``constant_type`` (e.g. ``integer``,
    ``float``, ``boolean``, ``string``), a literal ``value``, and an optional
    ``description``.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str = Field(..., description="The name of the constant")
    constant_type: str = Field(alias="type", description="The type of the constant (e.g. integer, float, boolean, string)")
    value: str | int | float | bool = Field(..., description="The literal value of the constant")
    description: Optional[str] = Field(default=None, description="A brief description of the constant")

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    @property
    def class_name(self):
        """The upper-camel-case class name used for this constant in generated code."""
        return stringmanip.upper_camel_case(self.name)

    @classmethod
    def new_constant_from_stinger(cls, name: str, constant_spec: dict) -> InterfaceConstant:
        """Construct an InterfaceConstant from a parsed Stinger constant spec dict."""
        if "type" not in constant_spec:
            raise InvalidStingerStructure(f"InterfaceConstant '{name}' spec is missing required 'type'")
        if "value" not in constant_spec:
            raise InvalidStingerStructure(f"InterfaceConstant '{name}' spec is missing required 'value'")
        try:
            return cls.model_validate({"name": name, **constant_spec})
        except ValidationError as e:
            raise InvalidStingerStructure(f"InterfaceConstant '{name}' spec is invalid: {e}") from e


# Resolve forward references in arg_models that depend on InterfaceEnum/InterfaceStruct
from stingeripc.arg_models import ArgEnum, ArgStruct  # noqa: E402

ArgEnum.model_rebuild()
ArgStruct.model_rebuild()
