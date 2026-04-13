from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .components import InterfaceComponent, Arg, LanguageSymbolMixin
from .exceptions import InvalidStingerStructure
from . import topic_util

if TYPE_CHECKING:
    from .components import StingerSpec


class IpcSignal(InterfaceComponent, LanguageSymbolMixin):

    def __init__(self, name: str, root: StingerSpec):
        InterfaceComponent.__init__(self, name, root)
        LanguageSymbolMixin.__init__(self, self._config)
        self._arg_list: list[Arg] = []

    def add_arg(self, arg: Arg) -> IpcSignal:
        if arg.name in [a.name for a in self._arg_list]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._arg_list.append(arg)
        return self

    @property
    def arg_list(self) -> list[Arg]:
        return self._arg_list

    def topic(self, **kwargs) -> str:
        template_topic = self._config.topics.signals
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, signal_name=self.name, **kwargs)
        return template_topic

    @classmethod
    def new_signal_from_stinger(
        cls,
        name: str,
        signal_spec: dict[str, Any],
        stinger_spec: StingerSpec,
    ) -> IpcSignal:
        """Alternative constructor from a Stinger signal structure."""
        signal = cls(name, stinger_spec)
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
