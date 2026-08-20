from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .components import InterfaceComponent, Arg
from .lang_symb import LanguageSymbolMixin
from .exceptions import InvalidStingerStructure
from . import topic_util

if TYPE_CHECKING:
    from .components import StingerSpec


class IpcProperty(InterfaceComponent):
    """A named, typed property exposed by the interface.

    A property carries an ordered list of values and may be read-only or
    read/write.  Its current value is published on the property's value topic,
    updates requested by clients on its update topic, and the results of those
    updates on its response topic — all computed from the configured topic
    templates.
    """

    def __init__(self, name: str, root: StingerSpec):
        InterfaceComponent.__init__(self, name, root)
        LanguageSymbolMixin.enhance(self, self._config)
        self._arg_list: list[Arg] = []
        self._read_only = False
        self._version: Optional[str] = None

    def add_arg(self, arg: Arg) -> IpcProperty:
        """Append a value to the property and return self.

        Duplicate value names are rejected.
        """
        if arg.name in [a.name for a in self._arg_list]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._arg_list.append(arg)
        return self

    def value_topic(self, **kwargs) -> str:
        """Return the topic that the property's current value is published on.

        The topic is derived from the configured ``property_values`` topic
        template, with the interface name and property name filled in.
        """
        template_topic = self._config.topics.property_values
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, property_name=self.name, **kwargs)
        return template_topic

    def update_topic(self, **kwargs) -> str:
        """Return the topic that property update requests are published on.

        The topic is derived from the configured ``property_updates`` topic
        template, with the interface name and property name filled in.
        """
        template_topic = self._config.topics.property_updates
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, property_name=self.name, **kwargs)
        return template_topic

    def response_topic(self, **kwargs) -> str:
        """Return the topic that property update responses are published on.

        The topic is derived from the configured ``property_update_responses``
        topic template, with the interface name and property name filled in.
        """
        template_topic = self._config.topics.property_update_responses
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, property_name=self.name, **kwargs)
        return template_topic

    @property
    def version(self) -> Optional[str]:
        """Version of the property, or None if not declared."""
        return self._version

    @property
    def arg_list(self) -> list[Arg]:
        """The ordered list of values that make up the property."""
        return self._arg_list

    @property
    def read_only(self) -> bool:
        """True if the property is read-only (clients cannot update it)."""
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
            raise InvalidStingerStructure(f"Values must be a list.  It is '{type(prop_spec['values'])}' ")

        for arg_spec in prop_spec["values"]:
            if "name" not in arg_spec or "type" not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            prop_obj.add_arg(new_arg)

        if r_o := prop_spec.get("readOnly", False):
            if not isinstance(r_o, bool):
                raise InvalidStingerStructure("'readOnly' in property structure must be a boolean")
            prop_obj._read_only = r_o

        if "version" in prop_spec:
            prop_obj._version = prop_spec["version"]

        prop_obj.try_set_documentation_from_spec(prop_spec)

        return prop_obj

    def __str__(self) -> str:
        return f"IpcProperty<name={self.name} values=[{', '.join([a.name for a in self.arg_list])}]>"
