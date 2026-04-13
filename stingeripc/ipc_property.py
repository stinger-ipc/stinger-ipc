from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .components import InterfaceComponent, Arg, LanguageSymbolMixin
from .exceptions import InvalidStingerStructure
from . import topic_util

if TYPE_CHECKING:
    from .components import StingerSpec


class IpcProperty(InterfaceComponent, LanguageSymbolMixin):

    def __init__(self, name: str, root: StingerSpec):
        InterfaceComponent.__init__(self, name, root)
        LanguageSymbolMixin.__init__(self, self._config)
        self._arg_list: list[Arg] = []
        self._read_only = False

    def add_arg(self, arg: Arg) -> IpcProperty:
        if arg.name in [a.name for a in self._arg_list]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._arg_list.append(arg)
        return self

    def value_topic(self, **kwargs) -> str:
        template_topic = self._config.topics.property_values
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, property_name=self.name, **kwargs)
        return template_topic

    def update_topic(self, **kwargs) -> str:
        template_topic = self._config.topics.property_updates
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, property_name=self.name, **kwargs)
        return template_topic

    def response_topic(self, **kwargs) -> str:
        template_topic = self._config.topics.property_update_responses
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, property_name=self.name, **kwargs)
        return template_topic

    @property
    def arg_list(self) -> list[Arg]:
        return self._arg_list

    @property
    def read_only(self) -> bool:
        return self._read_only

    @classmethod
    def new_property_from_stinger(
        cls,
        name: str,
        prop_spec: dict[str, Any],
        stinger_spec: StingerSpec,
    ) -> IpcProperty:
        """Alternative constructor from a Stinger property structure."""
        prop_obj = cls(name, stinger_spec)
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
        return f"IpcProperty<name={self.name} values=[{', '.join([a.name for a in self.arg_list])}]>"
