"""Turning protobuf descriptors into the JSON document protobuf.js loads.

The generated web page speaks protobuf in the browser, which needs both a
runtime and a schema.  The runtime is protobuf.js, loaded from a CDN; the schema
is this module's output, a plain JSON document of the shape protobuf.js's
``Root.fromJSON`` accepts.

Building it here rather than shipping the raw ``FileDescriptorSet`` for the
browser to interpret is what keeps the generated page free of a bundler: the
protobuf.js extension that reads descriptors is CommonJS-only, with no browser
build, while ``Root.fromJSON`` is part of even the light distribution.

Field names are emitted exactly as the ``.proto`` file spells them, in
snake_case.  protobuf.js's own ``pbjs`` tool camelCases them by default; matching
the descriptor instead means a field is called the same thing in the browser as
it is in the .proto source, in :class:`~stingeripc.payload.ProtobufField`, and in
the Python, Rust and C++ output.
"""

from __future__ import annotations

from typing import Any, Iterable

from google.protobuf.descriptor_pb2 import DescriptorProto, EnumDescriptorProto, FieldDescriptorProto, FileDescriptorProto

from .exceptions import ProtobufError
from .payload import _FIELD_KINDS

# protoc records a field's cardinality as a label; protobuf.js spells the two
# that are not the default as a "rule".
_LABEL_OPTIONAL = 1
_LABEL_REQUIRED = 2
_LABEL_REPEATED = 3

_TYPE_GROUP = 10
_TYPE_MESSAGE = 11
_TYPE_ENUM = 14
_TYPE_STRING = 9
_TYPE_BYTES = 12
_TYPE_BOOL = 8

_FLOAT_KINDS = frozenset({"double", "float"})


def _type_name(field: FieldDescriptorProto) -> str:
    """The protobuf.js spelling of a field's type.

    A message or enum field keeps the descriptor's fully-qualified reference
    *including its leading dot*.  protobuf.js resolves a name whose first segment
    is empty from the root of the document, so passing it through untouched is
    both the simplest and the only unambiguous option -- a relative name would be
    resolved against whatever namespace the field happens to sit in.
    """
    if field.type in (_TYPE_MESSAGE, _TYPE_ENUM):
        return field.type_name
    kind = _FIELD_KINDS.get(field.type)
    if kind is None:
        raise ProtobufError(f"Protobuf field '{field.name}' has unsupported type number {field.type}.")
    return kind


def _default_value(field: FieldDescriptorProto) -> Any:
    """A proto2 field's declared default, coerced to the JSON type it belongs to.

    protoc records every default as the string the .proto file wrote, so a
    numeric or boolean default has to be converted back or protobuf.js would
    compare a number against a string.
    """
    text = field.default_value
    if field.type == _TYPE_BOOL:
        return text == "true"
    if field.type in (_TYPE_STRING, _TYPE_BYTES) or field.type == _TYPE_ENUM:
        # An enum default is a value *name*, which is how protobuf.js wants it.
        return text
    kind = _FIELD_KINDS.get(field.type, "")
    if kind in _FLOAT_KINDS:
        return float(text)
    try:
        return int(text)
    except ValueError:
        # 64-bit defaults outside JavaScript's exact integer range stay strings,
        # which is also how protobuf.js hands such values back.
        return text


def _convert_field(field: FieldDescriptorProto, map_entries: dict[str, DescriptorProto]) -> dict[str, Any]:
    """One field, as protobuf.js describes it."""
    if field.type == _TYPE_GROUP:
        raise ProtobufError(
            f"Protobuf field '{field.name}' uses a proto2 group, which protobuf.js cannot represent.  Declare a nested message instead."
        )

    entry = map_entries.get(field.type_name) if field.label == _LABEL_REPEATED else None
    if entry is not None:
        key_field = next(f for f in entry.field if f.name == "key")
        value_field = next(f for f in entry.field if f.name == "value")
        converted: dict[str, Any] = {
            "keyType": _type_name(key_field),
            "type": _type_name(value_field),
            "id": field.number,
        }
        return converted

    converted = {"type": _type_name(field), "id": field.number}
    if field.label == _LABEL_REPEATED:
        converted["rule"] = "repeated"
    elif field.label == _LABEL_REQUIRED:
        converted["rule"] = "required"

    options: dict[str, Any] = {}
    if field.options.HasField("packed") and not field.options.packed:
        # Only ever worth stating when turned off: protobuf.js packs by default.
        options["packed"] = False
    if field.HasField("default_value"):
        options["default"] = _default_value(field)
    if options:
        converted["options"] = options

    # protobuf.js orders a field's keys rule, type, id; dicts preserve insertion
    # order in JSON, so rebuild rather than leaving "rule" at the end.
    ordered: dict[str, Any] = {}
    for key in ("rule", "keyType", "type", "id", "options"):
        if key in converted:
            ordered[key] = converted[key]
    return ordered


def _convert_enum(enum: EnumDescriptorProto) -> dict[str, Any]:
    """One enum, as protobuf.js describes it."""
    converted: dict[str, Any] = {"values": {value.name: value.number for value in enum.value}}
    if enum.options.allow_alias:
        converted["options"] = {"allow_alias": True}
    return converted


def _convert_message(message: DescriptorProto) -> dict[str, Any]:
    """One message, with its fields, oneofs and anything declared inside it."""
    # A `map<K, V>` is lowered by protoc to a repeated field over a hidden
    # two-field message nested here.  protobuf.js models maps directly, so these
    # entry messages are matched back to the field that uses them and are never
    # emitted as messages of their own.  The field's type reference is fully
    # qualified while the entry is known only by its own name, so they are
    # matched on the tail the two have in common.
    map_entries = {f".{message.name}.{nested.name}": nested for nested in message.nested_type if nested.options.map_entry}
    resolved_entries: dict[str, DescriptorProto] = {}
    for field in message.field:
        for suffix, entry in map_entries.items():
            if field.type_name.endswith(suffix):
                resolved_entries[field.type_name] = entry

    converted: dict[str, Any] = {}

    oneofs: dict[str, Any] = {}
    for index, oneof in enumerate(message.oneof_decl):
        members = [f.name for f in message.field if f.HasField("oneof_index") and f.oneof_index == index and not f.proto3_optional]
        # A proto3 `optional` field is wrapped in a one-member oneof that the
        # .proto file never wrote.  Reporting it would turn presence tracking
        # into a visible choice between alternatives.
        if members:
            oneofs[oneof.name] = {"oneof": members}
    if oneofs:
        converted["oneofs"] = oneofs

    converted["fields"] = {field.name: _convert_field(field, resolved_entries) for field in message.field}

    nested = _convert_declarations(
        messages=[m for m in message.nested_type if not m.options.map_entry],
        enums=message.enum_type,
    )
    if nested:
        converted["nested"] = nested

    return converted


def _convert_declarations(messages: Iterable[DescriptorProto], enums: Iterable[EnumDescriptorProto]) -> dict[str, Any]:
    """The messages and enums declared at one level, keyed by name."""
    declarations: dict[str, Any] = {}
    for enum in enums:
        declarations[enum.name] = _convert_enum(enum)
    for message in messages:
        declarations[message.name] = _convert_message(message)
    return declarations


def _nest_under_package(root: dict[str, Any], package: str, declarations: dict[str, Any]) -> None:
    """Merge one file's declarations into the tree at its package path.

    Several files may share a package, and a package is a path of namespaces
    rather than a single name, so this walks and creates rather than assigning.
    """
    node = root
    for part in package.split(".") if package else []:
        nested = node.setdefault("nested", {})
        node = nested.setdefault(part, {})
    node.setdefault("nested", {}).update(declarations)


def descriptor_set_to_protobufjs(files: Iterable[FileDescriptorProto]) -> dict[str, Any]:
    """Convert protobuf file descriptors to a protobuf.js ``Root.fromJSON`` document.

    Services are skipped: an interface's transport is stinger's concern, not gRPC's.
    """
    root: dict[str, Any] = {"nested": {}}
    for file_proto in files:
        declarations = _convert_declarations(
            messages=[m for m in file_proto.message_type if not m.options.map_entry],
            enums=file_proto.enum_type,
        )
        if declarations:
            _nest_under_package(root, file_proto.package, declarations)
    return root
