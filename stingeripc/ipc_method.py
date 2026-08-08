from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .components import InterfaceComponent, Arg
from .lang_symb import LanguageSymbolMixin
from .exceptions import InvalidStingerStructure
from . import topic_util

if TYPE_CHECKING:
    from .components import StingerSpec


class IpcMethod(InterfaceComponent):
    """A request/response method exposed by the interface.

    A method accepts an ordered list of arguments (its request) and may return
    zero or more values (its response).  Requests are published on the method's
    request topic and responses on its response topic; both are computed from
    the configured topic templates.
    """

    def __init__(self, name: str, root: StingerSpec):
        InterfaceComponent.__init__(self, name, root)
        LanguageSymbolMixin.enhance(self, self._config)
        self._arg_list: list[Arg] = []
        self._return_value: Arg | list[Arg] | None = None
        self._return_arg_list: list[Arg] = []
        self._version: Optional[str] = None

    def add_arg(self, arg: Arg) -> IpcMethod:
        """Append an argument to the method's request and return self.

        Duplicate argument names are rejected.
        """
        if arg.name in [a.name for a in self._arg_list]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._arg_list.append(arg)
        return self

    def add_return_value(self, value: Arg) -> IpcMethod:
        """Append a return value to the method's response and return self.

        A single return value is stored directly; multiple return values are
        accumulated into a list.  Duplicate names within a multi-value response
        are rejected.
        """
        self._return_arg_list.append(value)
        if self._return_value is None:
            self._return_value = value
        elif isinstance(self._return_value, list):
            if value.name in [a.name for a in self._return_value]:
                raise InvalidStingerStructure(f"A return value named '{value.name}' has been already added.")
            self._return_value.append(value)
        elif isinstance(self._return_value, Arg):
            if value.name == self._return_value.name:
                raise InvalidStingerStructure(f"Attempt to add '{value.name}' to return value when it is already been added.")
            self._return_value = [self._return_value, value]
        return self

    def request_topic(self, **kwargs) -> str:
        """Return the topic that method request messages are published on.

        The topic is derived from the configured ``method_requests`` topic
        template, with the interface name and method name filled in.
        """
        template_topic = self._config.topics.method_requests
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, method_name=self.name, **kwargs)
        return template_topic

    def response_topic(self, **kwargs) -> str:
        """Return the topic that method response messages are published on.

        The topic is derived from the configured ``method_responses`` topic
        template, with the interface name and method name filled in.
        """
        template_topic = self._config.topics.method_responses
        template_topic = topic_util.topic_template_fill_in(template_topic, interface_name=self._root.name, method_name=self.name, **kwargs)
        return template_topic

    @property
    def arg_list(self) -> list[Arg]:
        """The ordered list of arguments that make up the method's request."""
        return self._arg_list

    @property
    def return_arg_list(self) -> list[Arg]:
        """The ordered list of values that make up the method's response."""
        return self._return_arg_list

    @property
    def return_value(self) -> Arg | list[Arg] | None:
        """The method's return value: a single Arg, a list of Args, or None.

        A single return value is returned directly, multiple return values are
        returned as a list, and a method with no return values returns None.
        """
        return self._return_value

    @property
    def return_value_name(self) -> str:
        """Human-readable name for the method's return value(s)."""
        return f"{self.name} return values"

    @property
    def return_value_property_name(self) -> str:
        """The property name used to expose the method's return value.

        For a single return value this is the argument's name; otherwise it
        falls back to the method's name.
        """
        if isinstance(self._return_value, Arg):
            return self._return_value.name
        else:
            return self.name

    @property
    def version(self) -> Optional[str]:
        """Version of the method, or None if not declared."""
        return self._version

    @property
    def return_value_type(self) -> str | bool:
        """A short string describing the shape of the method's return value.

        Returns the lower-cased arg type name (e.g. ``'primitive'``) for a
        single return value, ``'multiple'`` for a list of return values, or
        ``False`` when the method has no return value.
        """
        if self._return_value is None:
            return False
        elif isinstance(self._return_value, Arg):
            return self._return_value.arg_type.name.lower()
        elif isinstance(self._return_value, list):
            return "multiple"
        raise RuntimeError("Method return value type was not recognized")

    def get_return_value_random_example_value(self, lang: str = "python", seed: int = 2):
        """Return a randomly generated example value for the method's return value.

        The example is expressed in the requested target ``lang`` (e.g.
        ``'python'`` or ``'c++'``) and is used by demos, tests, and
        documentation.  A method with no return value yields ``None`` (or
        ``nullptr`` for C++).
        """
        if lang == "python":
            if self._return_value is None:
                return "None"
            elif isinstance(self._return_value, Arg):
                return self._return_value.get_random_example_value(lang, seed)
            elif isinstance(self._return_value, list):
                s = ", ".join([f"{a.name}={a.get_random_example_value(lang,seed)}" for a in self._return_value])
                return f"{self.python.response_class_name}({s})"  # type: ignore[attr-defined]
            else:
                raise RuntimeError(f"Did not handle return value type for: {self._return_value}")
        if lang in ["c++", "cpp", "qt"]:
            if self._return_value is None:
                return "nullptr"
            elif isinstance(self._return_value, Arg):
                return self._return_value.get_random_example_value(lang, seed)
            elif isinstance(self._return_value, list):
                return ", ".join([str(a.get_random_example_value(lang, seed)) for a in self._return_value])
        raise RuntimeError(f"No random example for return value for {lang}")

    @classmethod
    def new_method_from_stinger(
        cls,
        name: str,
        method_spec: dict[str, Any],
        stinger_spec: StingerSpec,
    ) -> IpcMethod:
        """Alternative constructor from a Stinger method structure."""
        method = cls(name, stinger_spec)
        if "arguments" not in method_spec:
            raise InvalidStingerStructure(f"Method '{name}' specification must have 'arguments'")
        if not isinstance(method_spec["arguments"], list):
            raise InvalidStingerStructure(f"Arguments for '{name}' method must be a list.  It is '{type(method_spec['arguments'])}' ")

        for arg_spec in method_spec["arguments"]:
            if "name" not in arg_spec or "type" not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            method.add_arg(new_arg)

        if "returnValues" in method_spec:
            if not isinstance(method_spec["returnValues"], list):
                raise InvalidStingerStructure(f"ReturnValues must be a list.")

            for arg_spec in method_spec["returnValues"]:
                if "name" not in arg_spec or "type" not in arg_spec:
                    raise InvalidStingerStructure("Return value must have name and type.")
                new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
                method.add_return_value(new_arg)

        if "version" in method_spec:
            method._version = method_spec["version"]

        method.try_set_documentation_from_spec(method_spec)

        return method
