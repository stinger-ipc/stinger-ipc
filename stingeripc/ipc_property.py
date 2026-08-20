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

    A property carries exactly one value and may be read-only or read/write.
    Its current value is published on the property's value topic, updates
    requested by clients on its update topic, and the results of those updates
    on its response topic — all computed from the configured topic templates.
    """

    def __init__(self, name: str, root: StingerSpec):
        InterfaceComponent.__init__(self, name, root)
        LanguageSymbolMixin.enhance(self, self._config)
        self._value: Optional[Arg] = None
        self._read_only = False
        self._version: Optional[str] = None

    def set_value(self, value: Arg) -> IpcProperty:
        """Set the property's single value and return self.

        A property holds exactly one value, so setting a value on a property
        that already has one is rejected.
        """
        if self._value is not None:
            raise InvalidStingerStructure(f"A value named '{self._value.name}' has already been set; a property has exactly one value.")
        self._value = value
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
    def value(self) -> Arg:
        """The single value that makes up the property."""
        if self._value is None:
            raise InvalidStingerStructure(f"Property '{self.name}' has no value.")
        return self._value

    @property
    def arg_list(self) -> list[Arg]:
        """The property's value as a single-element list.

        Templates that render the property payload iterate over this so that
        properties and the other interface components share one code path.
        """
        return [self.value]

    @property
    def read_only(self) -> bool:
        """True if the property is read-only (clients cannot update it)."""
        return self._read_only

    @staticmethod
    def _value_spec_from_stinger(name: str, prop_spec: dict[str, Any]) -> dict[str, Any]:
        """Return the arg spec for the property's value.

        A property declares its value with a single ``value`` mapping.  The
        ``values`` list of earlier spec versions is rejected outright rather
        than half-read, since a property now holds exactly one value.
        """
        if "values" in prop_spec:
            raise InvalidStingerStructure(f"Property '{name}' uses 'values', which was replaced by a single 'value' in stinger spec version 0.3.0.  Use a struct to hold several fields together.")

        if "value" not in prop_spec:
            raise InvalidStingerStructure(f"Property '{name}' specification must have a 'value'")

        value_spec = prop_spec["value"]
        if not isinstance(value_spec, dict):
            raise InvalidStingerStructure(f"Value for '{name}' property must be a single arg structure.  It is '{type(value_spec)}'")
        return value_spec

    @classmethod
    def new_property_from_stinger(
        cls,
        name: str,
        prop_spec: dict[str, Any],
        stinger_spec: StingerSpec,
    ) -> IpcProperty:
        """Alternative constructor from a Stinger property structure."""
        prop_obj = cls(name, stinger_spec)

        value_spec = cls._value_spec_from_stinger(name, prop_spec)
        if "name" not in value_spec or "type" not in value_spec:
            raise InvalidStingerStructure("Value must have name and type.")
        prop_obj.set_value(Arg.new_arg_from_stinger(value_spec, stinger_spec))

        if r_o := prop_spec.get("readOnly", False):
            if not isinstance(r_o, bool):
                raise InvalidStingerStructure("'readOnly' in property structure must be a boolean")
            prop_obj._read_only = r_o

        if "version" in prop_spec:
            prop_obj._version = prop_spec["version"]

        prop_obj.try_set_documentation_from_spec(prop_spec)

        return prop_obj

    def __str__(self) -> str:
        return f"IpcProperty<name={self.name} value={self.value.name}>"
