from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .components import InterfaceComponent, Arg
from .lang_symb import LanguageSymbolMixin
from .payload import Payload, PayloadRole, protobuf_ref_from_spec
from .exceptions import InvalidStingerStructure
from . import topic_util

if TYPE_CHECKING:
    from .components import StingerSpec


class IpcSignal(InterfaceComponent):
    """A signal published by the interface.

    Signals are fire-and-forget messages: a server emits them and any client
    subscribed to the signal's topic receives its values.  A signal carries an
    ordered list of arguments (its values) and may declare a ``version``.
    """

    def __init__(self, name: str, root: StingerSpec):
        InterfaceComponent.__init__(self, name, root)
        LanguageSymbolMixin.enhance(self, self._config)
        self._payload = Payload(owner_name=name, role=PayloadRole.SIGNAL, config=self._config)
        self._version: Optional[str] = None

    def add_arg(self, arg: Arg) -> IpcSignal:
        """Append an argument to the signal's values and return self.

        Duplicate argument names are rejected.
        """
        if arg.name in [a.name for a in self._payload.args]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._payload.args.append(arg)
        return self

    @property
    def version(self) -> Optional[str]:
        """Version of the signal, or None if not declared."""
        return self._version

    @property
    def payload(self) -> Payload:
        """The signal's wire body."""
        return self._payload

    @property
    def arg_list(self) -> list[Arg]:
        """The ordered list of arguments that make up the signal's values."""
        return self._payload.arg_list

    def topic(self, **kwargs) -> str:
        """Return the topic that signal messages are published on.

        The topic is derived from the configured ``signals`` topic template,
        with the interface name and signal name filled in.
        """
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

        signal._payload.protobuf = protobuf_ref_from_spec(name, signal_spec, "values")
        if signal._payload.is_protobuf:
            if "version" in signal_spec:
                signal._version = signal_spec["version"]
            signal.try_set_documentation_from_spec(signal_spec)
            return signal

        if "values" not in signal_spec:
            raise InvalidStingerStructure(f"Signal '{name}' specification must have 'values' or 'protobuf'")
        if not isinstance(signal_spec["values"], list):
            raise InvalidStingerStructure(f"Values must be a list.  It is '{type(signal_spec['values'])}' ")

        for arg_spec in signal_spec["values"]:
            if "name" not in arg_spec or "type" not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            signal.add_arg(new_arg)

        if "version" in signal_spec:
            signal._version = signal_spec["version"]

        signal.try_set_documentation_from_spec(signal_spec)

        return signal
