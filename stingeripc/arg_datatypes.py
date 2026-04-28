from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from jacobsjinjatoo import stringmanip
from pydantic import BaseModel, ConfigDict, PrivateAttr

from stingeripc.exceptions import InvalidStingerStructure
from stingeripc.lang_symb import LanguageSymbolMixin
from stingeripc.arg_models import YamlIfaceEnum, Arg

if TYPE_CHECKING:
    from stingeripc.components import StingerSpec


class InterfaceEnum(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    _items: list = PrivateAttr(default_factory=list)
    _documentation: Optional[str] = PrivateAttr(default=None)

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    @dataclass
    class EnumItem:
        name: str
        integer: int
        description: Optional[str] = None

    def add_item(self, value: str, integer: Optional[int] = None, description: Optional[str] = None):
        integer_value = integer if integer is not None else ((max([i.integer for i in self._items]) + 1) if len(self._items) > 0 else 1)
        item = InterfaceEnum.EnumItem(name=value, integer=integer_value, description=description)
        self._items.append(item)

    def has_value(self, integer: int) -> bool:
        for item in self._items:
            if item.integer == integer:
                return True
        return False

    @property
    def documentation(self) -> str | None:
        return self._documentation

    @property
    def class_name(self):
        return stringmanip.upper_camel_case(self.name)

    @property
    def items(self) -> list[InterfaceEnum.EnumItem]:
        if self.has_value(0) and self._items[0].integer != 0:
            # Rearrange so that the item with integer value 0 is first. This is because .proto files require an initial 0-value.
            rearranged_items = [item for item in self._items if item.integer == 0]
            rearranged_items.extend([item for item in self._items if item.integer != 0])
            return rearranged_items
        else:
            return self._items

    @classmethod
    def new_enum_from_stinger(cls, name, enum_spec: YamlIfaceEnum) -> InterfaceEnum:
        ie = cls(name=name)
        for enum_obj in enum_spec.get("values", []):
            assert isinstance(enum_obj, dict), f"Enum values must be a dicts."
            if "name" in enum_obj and isinstance(enum_obj["name"], str):
                value_description = enum_obj.get("description", None)
                if value_description is not None and not isinstance(value_description, str):
                    raise InvalidStingerStructure(
                        f"InterfaceEnum '{name}' item descriptions must be strings."
                    )
                value_integer = enum_obj.get("value", None)
                if value_integer is not None and not isinstance(value_integer, int):
                    raise InvalidStingerStructure(
                        f"InterfaceEnum '{name}' item values must be integers."
                    )
                if value_integer is not None and ie.has_value(value_integer):
                    raise InvalidStingerStructure(
                        f"InterfaceEnum '{name}' already has an item with value {value_integer}."
                    )
                ie.add_item(enum_obj["name"], integer=value_integer, description=value_description)
            else:
                raise InvalidStingerStructure(
                    f"InterfaceEnum '{name}' items must have string names."
                )
        doc = enum_spec.get("documentation", None)
        if doc is not None and isinstance(doc, str):
            ie._documentation = doc
        return ie


class InterfaceStruct(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    _members: list[Arg] = PrivateAttr(default_factory=list)
    _documentation: Optional[str] = PrivateAttr(default=None)

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    def add_member(self, arg: Arg):
        self._members.append(arg)

    @property
    def documentation(self) -> str | None:
        return self._documentation

    @property
    def class_name(self):
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
        istruct = cls(name=name)
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


# Resolve forward references in arg_models that depend on InterfaceEnum/InterfaceStruct
from stingeripc.arg_models import ArgEnum, ArgStruct  # noqa: E402
ArgEnum.model_rebuild()
ArgStruct.model_rebuild()
