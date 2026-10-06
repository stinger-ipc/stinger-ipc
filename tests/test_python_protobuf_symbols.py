"""Tests for the Python symbols of a protobuf message's fields.

A protobuf payload's generated Python API is built out of these: the parameter a
function takes for each field, the constructor keyword that puts it back on the
message, and the expression that reads it off again.  The fixtures are descriptor
sets built ahead of time and checked in beside these tests, so no protobuf
compiler is needed to run them.
"""

import unittest
from pathlib import Path

from google.protobuf.descriptor_pb2 import FileDescriptorSet

from stingeripc.lang_symb import LanguageSymbolMixin
from stingeripc.payload import Payload, PayloadRole, ProtobufField, ProtobufMessageRef
from stingeripc.protobuf_compiler import ProtobufSources

FIXTURES = Path(__file__).parent / "fixtures"


def _traps_sources() -> ProtobufSources:
    """A ProtobufSources over the trap fixtures -- maps, oneofs, enums, proto2."""
    sources = ProtobufSources(FIXTURES)
    sources.descriptor_set = lambda: FileDescriptorSet.FromString((FIXTURES / "traps.desc").read_bytes())  # type: ignore[method-assign]
    return sources


def _resolved(full_name: str) -> ProtobufMessageRef:
    ref = ProtobufMessageRef(full_name=full_name)
    _traps_sources().resolve(ref)
    return ref


class TestPythonFieldSymbols(unittest.TestCase):
    """What a generated Python function says about each field of traps.v1.Reading."""

    @classmethod
    def setUpClass(cls):
        cls.reading = _resolved("traps.v1.Reading")

    def _field(self, name: str) -> ProtobufField:
        return next(field for field in self.reading.fields if field.name == name)

    def test_annotation_of_a_map(self):
        self.assertEqual(self._field("labels").python.annotation, "Dict[str, int]")

    def test_annotation_of_a_map_of_messages(self):
        self.assertEqual(self._field("nested_by_name").python.annotation, "Dict[str, traps_pb2.Reading.Nested]")

    def test_annotation_of_a_repeated_message(self):
        self.assertEqual(self._field("history").python.annotation, "List[traps_pb2.Reading.Nested]")

    def test_annotation_of_an_enum_names_the_enum(self):
        """protoc's stubs reject a plain int where an enum is expected.

        The value is an int at runtime, but the generated code has to type-check
        against those stubs, so the annotation names the enum protoc generated.  It
        does so as a string: at runtime the enum is an EnumTypeWrapper instance, and
        a module-level ``Callable[[...]]`` or ``List[...]`` holding it as a bare name
        fails to import on Python before 3.11 ("each arg must be a type").
        """
        self.assertEqual(self._field("severity").python.annotation, '"traps_pb2.Severity"')

    def test_an_enum_is_quoted_wherever_typing_would_inspect_it(self):
        """Every spelling that puts the enum inside a typing subscript has to be a string."""
        severity = self._field("severity")
        for label, field, expected in (
            ("repeated", severity.model_copy(update={"repeated": True}), 'List["traps_pb2.Severity"]'),
            ("optional", severity.model_copy(update={"optional": True}), 'Optional["traps_pb2.Severity"]'),
            ("map value", self._field("labels").model_copy(update={"map_value": severity}), 'Dict[str, "traps_pb2.Severity"]'),
        ):
            with self.subTest(label):
                # model_copy skips model_post_init, so the symbols are attached again.
                LanguageSymbolMixin.enhance(field)
                self.assertEqual(field.python.annotation, expected)

    def test_a_message_is_not_quoted(self):
        """A message class is a real type at runtime, so it is named directly."""
        self.assertNotIn('"', self._field("history").python.annotation)
        self.assertNotIn('"', self._field("nested_by_name").python.annotation)

    def test_an_enum_example_still_names_the_enum_unquoted(self):
        """The quoting is for annotations; an example value is an expression."""
        self.assertNotIn('"', self._field("severity").python.example_value())

    def test_annotation_of_bytes_and_int64(self):
        self.assertEqual(self._field("blob").python.annotation, "bytes")
        self.assertEqual(self._field("big").python.annotation, "int")

    def test_annotation_of_a_oneof_member_is_optional(self):
        self.assertEqual(self._field("sensor_id").python.annotation, "Optional[str]")
        self.assertEqual(self._field("sensor_index").python.annotation, "Optional[int]")

    def test_annotation_of_a_proto3_optional_is_optional(self):
        self.assertEqual(self._field("note").python.annotation, "Optional[str]")

    def test_annotation_of_a_singular_message(self):
        nested = _resolved("traps.v1.Reading.Nested")
        by_name = {field.name: field for field in nested.fields}
        self.assertEqual(by_name["name"].python.annotation, "str")
        self.assertEqual(by_name["value"].python.annotation, "float")

    def test_a_signature_takes_the_optional_parameters_last(self):
        signature = ", ".join(f"{field.python.param_name}: {field.python.annotation}" + (" = None" if field.is_optional_param else "") for field in self.reading.param_fields)
        self.assertEqual(
            signature,
            "labels: Dict[str, int], "
            "nested_by_name: Dict[str, traps_pb2.Reading.Nested], "
            'severity: "traps_pb2.Severity", '
            "history: List[traps_pb2.Reading.Nested], "
            "blob: bytes, "
            "big: int, "
            "sensor_id: Optional[str] = None, "
            "sensor_index: Optional[int] = None, "
            "note: Optional[str] = None",
        )

    def test_read_expr_copies_a_map_and_a_repeated_field_out(self):
        self.assertEqual(self._field("labels").python.read_expr("payload"), "dict(payload.labels)")
        self.assertEqual(self._field("history").python.read_expr("payload"), "list(payload.history)")

    def test_read_expr_of_a_plain_field_is_the_attribute(self):
        self.assertEqual(self._field("big").python.read_expr("model"), "model.big")

    def test_read_expr_reports_an_unset_optional_as_none(self):
        self.assertEqual(self._field("note").python.read_expr("payload"), 'payload.note if payload.HasField("note") else None')
        self.assertEqual(self._field("sensor_id").python.read_expr("msg"), 'msg.sensor_id if msg.HasField("sensor_id") else None')

    def test_ctor_kwarg_is_the_field_name(self):
        self.assertEqual(self._field("big").python.ctor_kwarg, "big=big")

    def test_example_value_per_kind(self):
        self.assertEqual(self._field("labels").python.example_value(), "{}")
        self.assertEqual(self._field("nested_by_name").python.example_value(), "{}")
        self.assertEqual(self._field("history").python.example_value(), "[]")
        # The wrapper protoc generates for an enum is not callable, so an example
        # has to name one of the enum's own values.
        self.assertEqual(self._field("severity").python.example_value(), "traps_pb2.Severity.SEVERITY_UNSPECIFIED")
        self.assertEqual(self._field("blob").python.example_value(), 'b"apples"')
        self.assertEqual(self._field("big").python.example_value(), "42")
        self.assertEqual(self._field("note").python.example_value(), '"apples"')

    def test_a_singular_message_is_named_by_its_generated_class(self):
        """A map's value is the one singular message field the trap fixtures declare."""
        value = self._field("nested_by_name").map_value
        self.assertEqual(value.python.annotation, "traps_pb2.Reading.Nested")
        self.assertEqual(value.python.example_value(), "traps_pb2.Reading.Nested()")


class TestPythonKeywordFieldNames(unittest.TestCase):
    """A .proto file may name a field something Python reserves."""

    def test_a_reserved_name_gets_a_trailing_underscore(self):
        field = ProtobufField(name="from", number=1, kind="string")
        self.assertEqual(field.python.param_name, "from_")

    def test_a_reserved_name_is_passed_through_a_mapping(self):
        """`Msg(from=x)` does not parse, so the keyword has to be unpacked."""
        field = ProtobufField(name="from", number=1, kind="string")
        self.assertEqual(field.python.ctor_kwarg, '**{"from": from_}')

    def test_a_reserved_name_is_read_with_getattr(self):
        field = ProtobufField(name="from", number=1, kind="string")
        self.assertEqual(field.python.read_expr("payload"), 'getattr(payload, "from")')

    def test_self_is_renamed_too(self):
        """A generated method's first parameter is already `self`."""
        field = ProtobufField(name="self", number=1, kind="bool")
        self.assertEqual(field.python.param_name, "self_")
        self.assertEqual(field.python.ctor_kwarg, '**{"self": self_}')

    def test_an_ordinary_name_is_left_alone(self):
        field = ProtobufField(name="location", number=1, kind="string")
        self.assertEqual(field.python.param_name, "location")
        self.assertEqual(field.python.ctor_kwarg, "location=location")
        self.assertEqual(field.python.read_expr("payload"), "payload.location")


class TestPythonPayloadParams(unittest.TestCase):
    """What a payload hands the templates as "its parameters"."""

    def test_a_protobuf_payload_spreads_into_its_message_fields(self):
        payload = Payload(owner_name="reading", role=PayloadRole.SIGNAL, protobuf=_resolved("traps.v1.Reading"))
        self.assertEqual(
            [field.python.param_name for field in payload.python.params],
            ["labels", "nested_by_name", "severity", "history", "blob", "big", "sensor_id", "sensor_index", "note"],
        )

    def test_an_example_offers_only_one_member_of_a_oneof(self):
        """Setting a second member would silently clear the first."""
        payload = Payload(owner_name="reading", role=PayloadRole.SIGNAL, protobuf=_resolved("traps.v1.Reading"))
        names = [field.python.param_name for field in payload.python.example_params]
        self.assertIn("sensor_id", names)
        self.assertNotIn("sensor_index", names)
        self.assertIn("note", names, "a proto3 optional is not a choice, so it is still offered")

    def test_a_message_with_no_fields_takes_no_parameters(self):
        payload = Payload(owner_name="doNothing", role=PayloadRole.COMMAND, protobuf=_resolved("google.protobuf.Empty"))
        self.assertEqual(payload.python.params, [])
        self.assertEqual(payload.python.example_params, [])


if __name__ == "__main__":
    unittest.main()
