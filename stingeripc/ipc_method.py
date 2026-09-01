from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .components import InterfaceComponent, Arg
from .lang_symb import LanguageSymbolMixin
from .payload import Payload, PayloadRole, protobuf_ref_from_spec
from .exceptions import InvalidStingerStructure
from . import topic_util

if TYPE_CHECKING:
    from .components import StingerSpec


class IpcMethod(InterfaceComponent):
    """A request/response method exposed by the interface.

    A method accepts an ordered list of arguments (its request) and returns at
    most one value (its response).  Requests are published on the method's
    request topic and responses on its response topic; both are computed from
    the configured topic templates.
    """

    def __init__(self, name: str, root: StingerSpec):
        InterfaceComponent.__init__(self, name, root)
        LanguageSymbolMixin.enhance(self, self._config)
        self._request_payload = Payload(owner_name=name, role=PayloadRole.METHOD_REQUEST, config=self._config)
        self._response_payload = Payload(owner_name=name, role=PayloadRole.METHOD_RESPONSE, config=self._config)
        self._version: Optional[str] = None

    def add_arg(self, arg: Arg) -> IpcMethod:
        """Append an argument to the method's request and return self.

        Duplicate argument names are rejected.
        """
        if arg.name in [a.name for a in self._request_payload.args]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._request_payload.args.append(arg)
        return self

    def set_return_value(self, value: Arg) -> IpcMethod:
        """Set the method's single return value and return self.

        A method returns at most one value, so setting a return value on a
        method that already has one is rejected.
        """
        if self._response_payload.args:
            raise InvalidStingerStructure(f"A return value named '{self._response_payload.args[0].name}' has already been set; a method has at most one return value.")
        self._response_payload.args.append(value)
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
    def request_payload(self) -> Payload:
        """The method's request wire body."""
        return self._request_payload

    @property
    def response_payload(self) -> Payload:
        """The method's response wire body."""
        return self._response_payload

    @property
    def has_response(self) -> bool:
        """True when the method sends anything back beyond a return code.

        Prefer this to testing ``return_value is None``: a method whose response is
        a protobuf message has no single ``Arg`` to return but still has a response.
        """
        return not self._response_payload.is_empty

    @property
    def arg_list(self) -> list[Arg]:
        """The ordered list of arguments that make up the method's request."""
        return self._request_payload.arg_list

    @property
    def return_arg_list(self) -> list[Arg]:
        """The method's response as a list: empty, or a single-element list.

        Templates that render the response payload iterate over this so that
        methods with and without a return value can share one code path.
        """
        return self._response_payload.arg_list

    @property
    def return_value(self) -> Optional[Arg]:
        """The method's return value, or None when the method returns nothing."""
        return self._response_payload.args[0] if self._response_payload.args else None

    @property
    def return_value_name(self) -> str:
        """Human-readable name for the method's return value."""
        return f"{self.name} return value"

    @property
    def return_value_property_name(self) -> str:
        """The property name used to expose the method's return value.

        This is the return value's own name, falling back to the method's name
        when the method has no return value.
        """
        if self.return_value is not None:
            return self.return_value.name
        return self.name

    @property
    def version(self) -> Optional[str]:
        """Version of the method, or None if not declared."""
        return self._version

    @property
    def return_value_type(self) -> str | bool:
        """A short string describing the shape of the method's return value.

        Returns the lower-cased arg type name (e.g. ``'primitive'``) for the
        return value, or ``False`` when the method has no return value.
        """
        if self.return_value is None:
            return False
        return self.return_value.arg_type.name.lower()

    def get_return_value_random_example_value(self, lang: str = "python", seed: int = 2):
        """Return a randomly generated example value for the method's return value.

        The example is expressed in the requested target ``lang`` (e.g.
        ``'python'`` or ``'c++'``) and is used by demos, tests, and
        documentation.  A method with no return value yields ``None`` (or
        ``nullptr`` for C++).
        """
        return_value = self.return_value
        if lang == "python":
            if return_value is None:
                return "None"
            return return_value.get_random_example_value(lang, seed)
        if lang in ["c++", "cpp", "qt"]:
            if return_value is None:
                return "nullptr"
            return return_value.get_random_example_value(lang, seed)
        raise RuntimeError(f"No random example for return value for {lang}")

    @staticmethod
    def _return_value_spec_from_stinger(name: str, method_spec: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Return the arg spec for the method's return value, or None if it returns nothing.

        A method declares its response with a single ``returnValue`` mapping.
        The ``returnValues`` list of earlier spec versions is rejected outright
        rather than half-read, since a method now returns at most one value.
        """
        if "returnValues" in method_spec:
            raise InvalidStingerStructure(f"Method '{name}' uses 'returnValues', which was replaced by a single 'returnValue' in stinger spec version 0.3.0.  Return a struct to send several fields together.")

        if "returnValue" not in method_spec:
            return None

        return_value_spec = method_spec["returnValue"]
        if not isinstance(return_value_spec, dict):
            raise InvalidStingerStructure(f"ReturnValue for '{name}' method must be a single arg structure.  It is '{type(return_value_spec)}'")
        return return_value_spec

    @classmethod
    def new_method_from_stinger(
        cls,
        name: str,
        method_spec: dict[str, Any],
        stinger_spec: StingerSpec,
    ) -> IpcMethod:
        """Alternative constructor from a Stinger method structure."""
        method = cls(name, stinger_spec)

        # The schema pairs these: a protobuf method declares both its request and
        # its response as messages, so neither side is silently left as JSON.
        request_ref = protobuf_ref_from_spec(name, method_spec, "arguments", "protobuf")
        response_ref = protobuf_ref_from_spec(name, method_spec, "returnValue", "returnProtobuf")
        if (request_ref is None) != (response_ref is None):
            declared, missing = ("protobuf", "returnProtobuf") if request_ref else ("returnProtobuf", "protobuf")
            raise InvalidStingerStructure(f"Method '{name}' declares '{declared}' but not '{missing}'; a protobuf method describes both its request and its response as messages.")
        if request_ref is not None:
            method._request_payload.protobuf = request_ref
            method._response_payload.protobuf = response_ref
            if "version" in method_spec:
                method._version = method_spec["version"]
            method.try_set_documentation_from_spec(method_spec)
            return method

        if "arguments" not in method_spec:
            raise InvalidStingerStructure(f"Method '{name}' specification must have 'arguments'")
        if not isinstance(method_spec["arguments"], list):
            raise InvalidStingerStructure(f"Arguments for '{name}' method must be a list.  It is '{type(method_spec['arguments'])}' ")

        for arg_spec in method_spec["arguments"]:
            if "name" not in arg_spec or "type" not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            method.add_arg(new_arg)

        return_value_spec = cls._return_value_spec_from_stinger(name, method_spec)
        if return_value_spec is not None:
            if "name" not in return_value_spec or "type" not in return_value_spec:
                raise InvalidStingerStructure("Return value must have name and type.")
            method.set_return_value(Arg.new_arg_from_stinger(return_value_spec, stinger_spec))

        if "version" in method_spec:
            method._version = method_spec["version"]

        method.try_set_documentation_from_spec(method_spec)

        return method
