from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .components import InterfaceComponent, Arg
from .lang_symb import LanguageSymbolMixin
from .payload import Payload, PayloadRole, protobuf_ref_from_spec
from .exceptions import InvalidStingerStructure
from . import topic_util

if TYPE_CHECKING:
    from .components import StingerSpec


class IpcCommand(InterfaceComponent):
    """A command sent to the interface by its clients.

    A command is the mirror image of a signal: it is a fire-and-forget message,
    but it travels from client to server rather than server to client.  Put
    another way, it is a method with no response — the client publishes the
    command's arguments and never learns whether the server acted on them.

    A command carries an ordered list of ``arguments`` and may declare a
    ``version``.  Commands are published on the command topic; a server
    subscribes to it and may register any number of handlers (including none,
    in which case received commands are dropped).
    """

    def __init__(self, name: str, root: StingerSpec):
        InterfaceComponent.__init__(self, name, root)
        LanguageSymbolMixin.enhance(self, self._config)
        self._payload = Payload(owner_name=name, role=PayloadRole.COMMAND, config=self._config)
        self._version: Optional[str] = None

    def add_arg(self, arg: Arg) -> IpcCommand:
        """Append an argument to the command's payload and return self.

        Duplicate argument names are rejected.
        """
        if arg.name in [a.name for a in self._payload.args]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._payload.args.append(arg)
        return self

    @property
    def version(self) -> Optional[str]:
        """Version of the command, or None if not declared."""
        return self._version

    @property
    def payload(self) -> Payload:
        """The command's wire body."""
        return self._payload

    @property
    def arg_list(self) -> list[Arg]:
        """The ordered list of arguments that make up the command's payload."""
        return self._payload.arg_list

    def topic(self, **kwargs) -> str:
        """Return the topic that command messages are published on.

        The topic is derived from the configured ``commands`` topic template,
        with the interface name and command name filled in.
        """
        template_topic = self._config.topics.commands
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, command_name=self.name, **kwargs)
        return template_topic

    @classmethod
    def new_command_from_stinger(
        cls,
        name: str,
        command_spec: dict[str, Any],
        stinger_spec: StingerSpec,
    ) -> IpcCommand:
        """Alternative constructor from a Stinger command structure."""
        command = cls(name, stinger_spec)

        command._payload.protobuf = protobuf_ref_from_spec(name, command_spec, "arguments")
        if command._payload.is_protobuf:
            if "version" in command_spec:
                command._version = command_spec["version"]
            command.try_set_documentation_from_spec(command_spec)
            return command

        if "arguments" not in command_spec:
            raise InvalidStingerStructure(f"Command '{name}' specification must have 'arguments' or 'protobuf'")
        if not isinstance(command_spec["arguments"], list):
            raise InvalidStingerStructure(f"Arguments for '{name}' command must be a list.  It is '{type(command_spec['arguments'])}' ")

        for arg_spec in command_spec["arguments"]:
            if "name" not in arg_spec or "type" not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            command.add_arg(new_arg)

        if "version" in command_spec:
            command._version = command_spec["version"]

        command.try_set_documentation_from_spec(command_spec)

        return command
