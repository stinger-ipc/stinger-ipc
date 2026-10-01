"""The wire body of an interface element.

Every signal, command and property carries exactly one payload; a method carries
two (its request and its response).  A payload is described either by a list of
JSON arguments or by a reference to a hand-written protocol buffer message --
never both.  Modelling that choice here, rather than as a flag on the element,
keeps the code generation templates from having to ask the question twice for a
method, which is the only element with two independent wire bodies.
"""

from __future__ import annotations

import random
from enum import Enum
from typing import Any, Optional

from google.protobuf.descriptor_pb2 import EnumDescriptorProto
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from .arg_models import _BOOLEAN_EXAMPLES, _FLOAT_EXAMPLES, _INTEGER_EXAMPLES, _STRING_EXAMPLES, Arg
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


# protoc's FieldDescriptorProto.Type numbers, spelled the way the .proto file does.
_FIELD_KINDS: dict[int, str] = {
    1: "double",
    2: "float",
    3: "int64",
    4: "uint64",
    5: "int32",
    6: "fixed64",
    7: "fixed32",
    8: "bool",
    9: "string",
    10: "group",
    11: "message",
    12: "bytes",
    13: "uint32",
    14: "enum",
    15: "sfixed32",
    16: "sfixed64",
    17: "sint32",
    18: "sint64",
}

# protoc's FieldDescriptorProto.Label numbers.  In proto2 `optional` is a label a
# field carries explicitly; in proto3 every singular field carries it, which is why
# reading presence off it needs to know the file's syntax.
_LABEL_OPTIONAL = 1
_LABEL_REPEATED = 3

# The field kinds an example value can be made up for.  A message, group or enum
# field needs the shape of another declaration to fill in, which an example built
# from one message's descriptor does not have.
_EXAMPLE_KINDS = frozenset(_FIELD_KINDS.values()) - {"message", "group", "enum"}

_INTEGER_KINDS = frozenset({"int32", "int64", "uint32", "uint64", "sint32", "sint64", "fixed32", "fixed64", "sfixed32", "sfixed64"})


class ProtobufField(BaseModel):
    """One field of a protobuf message, as its descriptor declares it."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    name: str = Field(..., description="The field's name, exactly as the .proto file spells it")
    number: int = Field(..., description="The field's wire tag number")
    kind: str = Field(..., description="The field's protobuf type, e.g. 'string', 'uint32' or 'message'")
    repeated: bool = Field(default=False, description="True for a repeated field")
    optional: bool = Field(default=False, description="True for a field that tracks presence explicitly: a proto3 'optional', or any singular proto2 'optional'")
    type_name: str = Field(default="", description="Fully-qualified name of the message or enum type, empty for a scalar")
    type_ref: Optional["ProtobufMessageRef"] = Field(default=None, description="The message or enum this field's type names, so a generated signature can spell it in any language")
    is_map: bool = Field(default=False, description="True for a map field, which protoc lowers to a repeated synthetic entry message")
    map_key: Optional["ProtobufField"] = Field(default=None, description="A map field's key, read off the synthetic entry message")
    map_value: Optional["ProtobufField"] = Field(default=None, description="A map field's value, read off the synthetic entry message")
    oneof_name: Optional[str] = Field(
        default=None, description="The real oneof this field belongs to, or None -- including for a proto3 'optional', whose one-member oneof is protobuf's own bookkeeping"
    )

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    @property
    def is_scalar(self) -> bool:
        """True when the field's type is one protobuf itself defines.

        A message, group or enum field is not: naming its type is not enough to
        know its shape, which is why such a field carries a :attr:`type_name`.
        """
        return self.kind not in ("message", "group", "enum")

    @property
    def is_message(self) -> bool:
        """True when the field's type is another message.

        A map field is a repeated message field as far as the descriptor is
        concerned, so callers that care about maps ask :attr:`is_map` first.
        """
        return self.kind in ("message", "group")

    @property
    def is_enum(self) -> bool:
        """True when the field's type is an enum."""
        return self.kind == "enum"

    @property
    def is_optional_param(self) -> bool:
        """True for a field a caller may leave unset.

        That is a field with explicit presence -- a proto3 ``optional`` or a proto2
        ``optional`` -- or a member of a real ``oneof``, where setting one member
        clears the others so no member can be mandatory.  A repeated or map field is
        never one of these: it has no presence to track, and its empty value is
        simply no entries.
        """
        return self.optional or self.oneof_name is not None

    def get_random_example_value(self, lang: str = "python", seed: int = 2) -> Optional[str]:
        """Return an example value for this field as a snippet of ``lang``.

        None for a field no example can be made up for -- a repeated field, or one
        whose type is another message or an enum -- so callers filter on
        :attr:`ProtobufMessageRef.example_fields` rather than on the result here.
        """
        if self.repeated or self.kind not in _EXAMPLE_KINDS:
            return None
        random_state = random.getstate()
        random.seed(seed)
        try:
            if self.kind == "bool":
                flag = random.choice(_BOOLEAN_EXAMPLES)
                return str(flag) if lang == "python" else str(flag).lower()
            if self.kind in ("float", "double"):
                number = random.choice(_FLOAT_EXAMPLES)
                # A C++ `float` setter takes a float, and an unsuffixed literal is a double.
                return f"{number}f" if lang in ("cpp", "c++") and self.kind == "float" else str(number)
            if self.kind in _INTEGER_KINDS:
                return str(random.choice(_INTEGER_EXAMPLES))
            text = random.choice(_STRING_EXAMPLES)
            if self.kind == "bytes":
                if lang == "python":
                    return f'b"{text}"'
                if lang == "rust":
                    return f'b"{text}".to_vec()'
                return f'"{text}"'
            if lang == "rust":
                return f'"{text}".to_string()'
            return f'"{text}"'
        finally:
            random.setstate(random_state)

    def __str__(self) -> str:
        return f"ProtobufField<{self.name}: {'repeated ' if self.repeated else ''}{self.type_name or self.kind}>"


class ProtobufOneof(BaseModel):
    """A real ``oneof`` declared by a protobuf message.

    Only one member may be set at a time, which is why a generated API treats the
    whole group as a single optional thing rather than as independent fields.  A
    proto3 ``optional`` field is not one of these: protoc wraps it in a synthetic
    one-member oneof that is bookkeeping rather than a choice the .proto declared.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

    name: str = Field(..., description="The oneof's name, exactly as the .proto file spells it")
    fields: list[ProtobufField] = Field(default_factory=list, description="The members of the oneof, in declaration order")

    _parent: Any = PrivateAttr(default=None)

    def model_post_init(self, __context) -> None:
        LanguageSymbolMixin.enhance(self)

    @property
    def parent(self) -> "ProtobufMessageRef":
        """The message that declares this oneof.

        Languages that give the group a type of its own name it below the parent,
        so the group cannot be spelled without knowing which message it came from.
        """
        return self._parent

    def __str__(self) -> str:
        return f"ProtobufOneof<{self.name}: {', '.join(field.name for field in self.fields)}>"


def _field_from_descriptor(
    descriptor: Any,
    syntax: str,
    oneof_names: dict[int, str],
    map_entries: dict[str, Any],
) -> ProtobufField:
    """Model one field off its ``FieldDescriptorProto``.

    ``map_entries`` maps the fully-qualified name of each synthetic map-entry message
    the declaring message holds to its descriptor, which is how a map field is told
    apart from an ordinary repeated message field.
    """
    kind = _FIELD_KINDS.get(descriptor.type, "message")
    repeated = descriptor.label == _LABEL_REPEATED
    entry = map_entries.get(descriptor.type_name)
    oneof_name = None
    if descriptor.HasField("oneof_index") and not descriptor.proto3_optional:
        oneof_name = oneof_names.get(descriptor.oneof_index)
    # proto3 marks explicit presence with `optional`; in proto2 every singular
    # non-required field has it, which is what the `optional` label means there.
    explicit_presence = bool(descriptor.proto3_optional) or (syntax != "proto3" and not repeated and descriptor.label == _LABEL_OPTIONAL)
    field = ProtobufField(
        name=descriptor.name,
        number=descriptor.number,
        kind=kind,
        repeated=repeated,
        optional=explicit_presence,
        type_name=descriptor.type_name.lstrip("."),
        oneof_name=oneof_name,
        is_map=entry is not None,
    )
    if entry is not None:
        # A map entry always declares exactly `key = 1` and `value = 2`, and is
        # itself a proto3 message whatever the syntax of the file around it.
        field.map_key = _field_from_descriptor(entry.field[0], "proto3", {}, {})
        field.map_value = _field_from_descriptor(entry.field[1], "proto3", {}, {})
    elif field.type_name and kind in ("message", "group", "enum"):
        field.type_ref = ProtobufMessageRef(full_name=field.type_name)
    return field


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
    _syntax: str = PrivateAttr(default="proto3")
    _fields: Optional[list[ProtobufField]] = PrivateAttr(default=None)
    _oneofs: Optional[list[ProtobufOneof]] = PrivateAttr(default=None)

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
    def is_enum(self) -> bool:
        """True when this reference names an enum rather than a message.

        Only a field's :attr:`ProtobufField.type_ref` is ever one: a payload is
        always a message, since an enum has no wire body of its own.
        """
        return self._descriptor is not None and isinstance(self._descriptor, EnumDescriptorProto)

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
    def syntax(self) -> str:
        """The syntax of the declaring file, ``proto2`` or ``proto3``.

        It decides whether a singular field tracks presence, which changes the type
        a generated per-field API gives that field.
        """
        return self._syntax

    def _build_fields(self) -> list[ProtobufField]:
        """Model every field off the descriptor, once."""
        descriptor = self._descriptor
        if descriptor is None or isinstance(descriptor, EnumDescriptorProto):
            return []
        map_entries = {f".{self.full_name}.{nested.name}": nested for nested in descriptor.nested_type if nested.options.map_entry}
        oneof_names = {index: oneof.name for index, oneof in enumerate(descriptor.oneof_decl)}
        return [_field_from_descriptor(field, self._syntax, oneof_names, map_entries) for field in descriptor.field]

    @property
    def fields(self) -> list[ProtobufField]:
        """The message's fields, in declaration order.

        Empty until the reference has been resolved against the .proto sources,
        since the field list comes off the descriptor that resolving fills in, and
        empty for a reference that names an enum.

        Built once and kept: resolving a field's own type writes back to the
        :class:`ProtobufField` objects handed out here, and each of them carries
        language symbols that are not worth rebuilding on every access.
        """
        if self._descriptor is None:
            return []
        if self._fields is None:
            self._fields = self._build_fields()
        return self._fields

    @property
    def oneofs(self) -> list[ProtobufOneof]:
        """The real oneofs the message declares, in declaration order.

        A proto3 ``optional`` field's synthetic one-member oneof is left out: it is
        protobuf's way of recording presence, not a choice between fields.
        """
        if self._descriptor is None or isinstance(self._descriptor, EnumDescriptorProto):
            return []
        if self._oneofs is None:
            groups: dict[str, ProtobufOneof] = {}
            for field in self.fields:
                if field.oneof_name is None:
                    continue
                group = groups.get(field.oneof_name)
                if group is None:
                    group = ProtobufOneof(name=field.oneof_name)
                    group._parent = self
                    groups[field.oneof_name] = group
                group.fields.append(field)
            self._oneofs = list(groups.values())
        return self._oneofs

    @property
    def enum_values(self) -> list[str]:
        """The names this enum declares, in declaration order; empty for a message.

        An enum's generated type is usually not constructible from a number -- in
        Python it is a wrapper object rather than a class -- so code that needs a
        value of it has to name one.
        """
        if self._descriptor is None or not isinstance(self._descriptor, EnumDescriptorProto):
            return []
        return [value.name for value in self._descriptor.value]

    @property
    def param_fields(self) -> list[ProtobufField]:
        """The message's fields in the order a generated function takes them.

        Fields a caller must supply come first and those it may leave out come
        after, each group in declaration order.  A language that gives an optional
        parameter a default needs them last, and every language orders them the same
        way so that one element's parameters line up across the generated APIs.
        """
        fields = self.fields
        return [field for field in fields if not field.is_optional_param] + [field for field in fields if field.is_optional_param]

    @property
    def referenced_types(self) -> list["ProtobufMessageRef"]:
        """Every message and enum this message's own fields name, de-duplicated.

        These are the declarations a generated signature mentions besides the
        message itself, so they are what its module has to import or include.
        """
        by_name: dict[str, ProtobufMessageRef] = {}
        for field in self.fields:
            for ref in (field.type_ref, field.map_value.type_ref if field.map_value else None):
                if ref is not None:
                    by_name.setdefault(ref.full_name, ref)
        return [by_name[name] for name in sorted(by_name)]

    @property
    def example_fields(self) -> list[ProtobufField]:
        """The fields an example instance of this message can fill in.

        A message whose fields are all at their defaults encodes to zero bytes,
        and a zero-byte retained publish tells the broker to drop the property's
        retained value rather than to store an empty one, so a generated example
        has to set something.  Only singular scalar fields qualify: a repeated
        field or one whose type is another message or an enum would need a shape
        this descriptor does not describe.  At most one member of any real
        ``oneof`` is offered, since setting a second would silently clear the
        first; a proto3 ``optional`` field is exempt, its one-member oneof being
        protobuf's own bookkeeping rather than a choice the .proto file declared.
        """
        chosen: list[ProtobufField] = []
        claimed_oneofs: set[str] = set()
        for field in self.fields:
            if not field.is_scalar or field.repeated:
                continue
            if field.oneof_name is not None:
                if field.oneof_name in claimed_oneofs:
                    continue
                claimed_oneofs.add(field.oneof_name)
            chosen.append(field)
        return chosen

    def __str__(self) -> str:
        return f"ProtobufMessageRef<{self.full_name}>"


ProtobufField.model_rebuild()


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
        if self.is_protobuf:
            mime_type = self._config.protobuf.mime_type
            return mime_type if isinstance(mime_type, str) else "application/protobuf"
        return "application/json"

    @property
    def enforce_content_type(self) -> bool:
        """Whether a receiver checks the content type of a message carrying this payload.

        Normally it does, in every target language: the content type has to be present
        and has to match, or the message is rejected.  A protobuf payload is exempt when
        ``[protobuf] mime_type`` is ``false``, which says that messages of this interface
        are not labelled with a protobuf media type at all -- so a receiver assumes the
        body is the declared message rather than rejecting it for carrying no label.
        """
        if self.is_protobuf:
            return self._config.protobuf.mime_type is not False
        return True

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
