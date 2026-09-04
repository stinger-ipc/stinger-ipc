"""The wire body of an interface element.

Every signal, command and property carries exactly one payload; a method carries
two (its request and its response).  A payload is described either by a list of
JSON arguments or by a reference to a hand-written protocol buffer message --
never both.  Modelling that choice here, rather than as a flag on the element,
keeps the code generation templates from having to ask the question twice for a
method, which is the only element with two independent wire bodies.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from .arg_models import Arg
from .lang_symb import LanguageSymbolMixin


class PayloadRole(Enum):
    """Which wire body of which kind of element a payload is.

    The role decides the generated type's name (a signal payload and a command
    payload are named differently even when they carry the same arguments), so
    it travels with the payload rather than being re-derived by each template.
    """

    SIGNAL = "signal"
    COMMAND = "command"
    METHOD_REQUEST = "method request"
    METHOD_RESPONSE = "method response"
    PROPERTY = "property"


class ProtobufMessageRef(BaseModel):
    """A reference to a hand-written protobuf message, by fully-qualified name.

    Only the name is known when the reference is first parsed.  Resolving it
    against the protobuf source directory fills in the descriptor and the file
    it came from; until then :attr:`is_resolved` is False.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    full_name: str = Field(..., description="Fully-qualified message name, e.g. 'weather.v1.CurrentConditions'")

    _descriptor: Any = PrivateAttr(default=None)
    _proto_file: Optional[str] = PrivateAttr(default=None)
    _package: Optional[str] = PrivateAttr(default=None)

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    @property
    def package(self) -> str:
        """The message's protobuf package, or '' for a message at the top level.

        Only the declaring file says where the package ends and the message path
        begins -- ``a.b.C`` is a message ``C`` in package ``a.b`` just as readily
        as a message ``C`` nested in message ``b`` at the top level -- so this is
        exact once resolved and, before then, guesses the common case of an
        unnested message so that :attr:`is_well_known` can be asked early.
        """
        if self._package is not None:
            return self._package
        return self.full_name.rpartition(".")[0]

    @property
    def message_name(self) -> str:
        """The message's own name, without its package or any enclosing messages."""
        return self.full_name.rpartition(".")[2]

    @property
    def scope(self) -> list[str]:
        """The messages this one is declared inside, outermost first.

        Empty for a message declared at the top level of its file.  A nested
        message is named through its parents in every target language, so the
        leaf name alone does not identify it.
        """
        return self.scoped_name.split(".")[:-1]

    @property
    def scoped_name(self) -> str:
        """The message's name relative to its package, e.g. ``Analytics.DetectionEvent``.

        The same as :attr:`message_name` for a message declared at the top level
        of its file, and prefixed with each enclosing message for a nested one.
        """
        package = self.package
        if package and self.full_name.startswith(f"{package}."):
            return self.full_name[len(package) + 1 :]
        return self.full_name

    @property
    def is_resolved(self) -> bool:
        """True once the reference has been matched to a message in the .proto sources."""
        return self._descriptor is not None

    @property
    def is_well_known(self) -> bool:
        """True for one of protobuf's own well-known types, e.g. ``google.protobuf.Empty``.

        These are declared by the protobuf project rather than by this interface,
        so they are neither found in the interface's .proto directory nor compiled
        alongside it: every language's protobuf runtime already ships them, and
        generated code reaches for that copy instead.
        """
        return self.package == "google.protobuf"

    @property
    def proto_file(self) -> str:
        """The .proto file that declares this message, relative to the source directory."""
        if self._proto_file is None:
            raise ValueError(f"Protobuf message '{self.full_name}' has not been resolved against any .proto source.")
        return self._proto_file

    @property
    def fields(self) -> list[Any]:
        """The message's fields.

        Always empty for now: stinger resolves protobuf messages by name only.
        Reading the field list out of the descriptor is a later change, and
        every caller of this property is written against the empty case first.
        """
        return []

    def __str__(self) -> str:
        return f"ProtobufMessageRef<{self.full_name}>"


class Payload(BaseModel):
    """One wire body of an interface element.

    Carries either a list of JSON ``args`` or a ``protobuf`` message reference.
    :attr:`arg_list` is empty in the protobuf case rather than raising, so that
    templates iterating a payload's arguments simply render nothing for a
    protobuf payload instead of needing a guard at every site.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    owner_name: str = Field(..., description="Name of the signal, command, method or property this payload belongs to")
    role: PayloadRole = Field(..., description="Which wire body of which kind of element this is")
    args: list[Arg] = Field(default_factory=list, description="The JSON arguments, empty for a protobuf payload")
    protobuf: Optional[ProtobufMessageRef] = Field(default=None, description="The protobuf message, when this payload is protobuf-encoded")

    _config: Any = PrivateAttr(default=None)

    def __init__(self, config: Any = None, **kwargs):
        super().__init__(**kwargs)
        self._config = config
        LanguageSymbolMixin.enhance(self, config)

    @property
    def is_protobuf(self) -> bool:
        """True when this payload is a protobuf message rather than a JSON argument list."""
        return self.protobuf is not None

    @property
    def arg_list(self) -> list[Arg]:
        """The payload's arguments; empty for a protobuf payload."""
        return self.args

    @property
    def is_empty(self) -> bool:
        """True when this payload carries nothing at all (e.g. a method that returns nothing)."""
        return not self.is_protobuf and not self.args

    @property
    def content_type(self) -> str:
        """The MQTT content type that messages carrying this payload are published with."""
        return "application/protobuf" if self.is_protobuf else "application/json"

    @property
    def value_schemas(self) -> list[Arg]:
        """The arguments that declare a JSON schema constraint."""
        return [arg for arg in self.args if arg.value_schema]

    def __str__(self) -> str:
        what = self.protobuf.full_name if self.protobuf else f"{len(self.args)} args"
        return f"Payload<{self.role.value} of {self.owner_name}: {what}>"


def protobuf_ref_from_spec(owner_name: str, spec: dict[str, Any], arg_key: str, pb_key: str = "protobuf") -> Optional[ProtobufMessageRef]:
    """Return the protobuf message an element declares, or None if it lists JSON arguments.

    An element describes its payload one way or the other, never both.  The
    reference comes back unresolved: matching the name against the .proto sources
    is a separate pass, because it needs the protobuf source directory, which the
    interface file itself does not know about.
    """
    from .exceptions import InvalidStingerStructure

    has_args = arg_key in spec
    has_protobuf = pb_key in spec
    if has_args and has_protobuf:
        raise InvalidStingerStructure(f"'{owner_name}' declares both '{arg_key}' and '{pb_key}'; a payload is described one way or the other, not both.")
    if not has_protobuf:
        return None
    name = spec[pb_key]
    if not isinstance(name, str) or not name:
        raise InvalidStingerStructure(f"'{pb_key}' for '{owner_name}' must be a fully-qualified protobuf message name, but was {name!r}.")
    return ProtobufMessageRef(full_name=name)
