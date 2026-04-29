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
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(pattern=r"^[a-zA-Z0-9_ -]+$")
    integer: Optional[int] = Field(default=None, alias="value")
    description: Optional[str] = None


class InterfaceEnum(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str
    enum_items: list[EnumItem] = Field(default_factory=list, alias="values")
    documentation: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None, pattern=r"^[0-9]+(\.[0-9]+){0,2}$")

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
        integer_value = integer if integer is not None else ((max([i.integer for i in self.enum_items]) + 1) if len(self.enum_items) > 0 else 1)
        item = EnumItem(name=value, integer=integer_value, description=description)
        self.enum_items.append(item)

    def has_value(self, integer: int) -> bool:
        for item in self.enum_items:
            if item.integer == integer:
                return True
        return False

    @property
    def class_name(self):
        return stringmanip.upper_camel_case(self.name)

    @property
    def items(self) -> list[EnumItem]:
        if self.has_value(0) and self.enum_items[0].integer != 0:
            # Rearrange so that the item with integer value 0 is first. This is because .proto files require an initial 0-value.
            rearranged_items = [item for item in self.enum_items if item.integer == 0]
            rearranged_items.extend([item for item in self.enum_items if item.integer != 0])
            return rearranged_items
        else:
            return self.enum_items

    @classmethod
    def new_enum_from_stinger(cls, name, enum_spec: YamlIfaceEnum) -> InterfaceEnum:
        if "values" not in enum_spec:
            raise InvalidStingerStructure(f"InterfaceEnum '{name}' spec is missing required 'values'")
        if len(enum_spec["values"]) == 0:
            raise InvalidStingerStructure(f"InterfaceEnum '{name}' must have at least one value")
        try:
            return cls.model_validate({"name": name, **enum_spec})
        except ValidationError as e:
            raise InvalidStingerStructure(f"InterfaceEnum '{name}' spec is invalid: {e}") from e


class InterfaceStruct(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    members: list[Arg] = Field(default_factory=list)
    documentation: Optional[str] = Field(default=None)

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    def add_member(self, arg: Arg):
        self.members.append(arg)

    @property
    def class_name(self):
        return stringmanip.upper_camel_case(self.name)

    @property
    def values(self) -> list[Arg]:
        return self.members

    @classmethod
    def new_struct_from_stinger(
        cls,
        name,
        spec: dict[str, str | list[dict[str, str]]],
        stinger_spec: StingerSpec,
    ) -> InterfaceStruct:
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


# Resolve forward references in arg_models that depend on InterfaceEnum/InterfaceStruct
from stingeripc.arg_models import ArgEnum, ArgStruct  # noqa: E402
ArgEnum.model_rebuild()
ArgStruct.model_rebuild()
