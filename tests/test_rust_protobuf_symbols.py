"""Tests for the Rust names and types of a protobuf message's fields.

A generated Rust function takes one parameter per member of the prost struct, so
these check that the members are the ones prost would declare, in the order the
generated API hands them over, spelled the way prost spells them.

Resolution normally shells out to protoc.  These tests feed it the descriptor set
checked in beside them, so they exercise the real matching logic without needing a
protobuf compiler on the machine running them.
"""

import unittest
from pathlib import Path

from google.protobuf.descriptor_pb2 import FileDescriptorSet

from stingeripc.payload import Payload, PayloadRole, ProtobufField, ProtobufMessageRef
from stingeripc.protobuf_compiler import ProtobufSources

FIXTURES = Path(__file__).parent / "fixtures"


def _sources() -> ProtobufSources:
    """A ProtobufSources whose descriptor set is the traps fixture, not protoc's output."""

    def descriptor_set() -> FileDescriptorSet:
        parsed = FileDescriptorSet()
        parsed.ParseFromString((FIXTURES / "traps.desc").read_bytes())
        return parsed

    sources = ProtobufSources(FIXTURES)
    sources.descriptor_set = descriptor_set  # type: ignore[method-assign]
    return sources


def _resolved(full_name: str) -> ProtobufMessageRef:
    ref = ProtobufMessageRef(full_name=full_name)
    _sources().resolve(ref)
    return ref


class TestRustStructFields(unittest.TestCase):
    """The members of the prost struct, in the order a generated function takes them."""

    def setUp(self):
        self.reading = _resolved("traps.v1.Reading")

    def test_members_are_required_first_then_optional(self):
        """A oneof is one member, and everything a caller may leave out comes last."""
        self.assertEqual(
            [member.rust.field_name for member in self.reading.rust.struct_fields],
            ["labels", "nested_by_name", "severity", "history", "blob", "big", "source", "note"],
        )

    def test_member_types_are_what_prost_generates(self):
        self.assertEqual(
            [(member.rust.field_name, member.rust.type) for member in self.reading.rust.struct_fields],
            [
                ("labels", "::std::collections::HashMap<String, i32>"),
                ("nested_by_name", "::std::collections::HashMap<String, crate::proto::reading::Nested>"),
                # prost keeps an enum field as its raw i32.
                ("severity", "i32"),
                ("history", "Vec<crate::proto::reading::Nested>"),
                ("blob", "Vec<u8>"),
                ("big", "i64"),
                ("source", "Option<crate::proto::reading::Source>"),
                ("note", "Option<String>"),
            ],
        )

    def test_external_types_reach_messages_through_the_proto_module(self):
        """Examples and integration tests are separate crates, so `crate::` is not theirs."""
        by_name = {member.rust.field_name: member for member in self.reading.rust.struct_fields}
        self.assertEqual(by_name["nested_by_name"].rust.external_type, "::std::collections::HashMap<String, proto::reading::Nested>")
        self.assertEqual(by_name["history"].rust.external_type, "Vec<proto::reading::Nested>")
        self.assertEqual(by_name["source"].rust.external_type, "Option<proto::reading::Source>")
        self.assertEqual(by_name["big"].rust.external_type, "i64", "a scalar is spelled the same on both sides")

    def test_own_module_is_where_prost_puts_a_message_s_nested_items(self):
        self.assertEqual(self.reading.rust.own_module, "reading")
        self.assertEqual(_resolved("traps.v1.Reading.Nested").rust.own_module, "reading::nested")

    def test_example_values_fit_the_member_types(self):
        self.assertEqual(
            {member.rust.field_name: member.rust.example_value() for member in self.reading.rust.struct_fields},
            {
                "labels": "Default::default()",
                "nested_by_name": "Default::default()",
                "severity": "0",
                "history": "Vec::new()",
                "blob": 'b"apples".to_vec()',
                "big": "42",
                "source": "None",
                "note": 'Some("apples".to_string())',
            },
        )

    def test_comparable_fields_are_the_ones_a_test_can_assert_on(self):
        """A float, a container, a message and a oneof all have nothing exact to check."""
        self.assertEqual([member.rust.field_name for member in self.reading.rust.comparable_fields], ["blob", "big", "note"])

    def test_a_double_is_not_comparable(self):
        nested = _resolved("traps.v1.Reading.Nested")
        self.assertEqual([member.rust.field_name for member in nested.rust.struct_fields], ["name", "value"])
        self.assertEqual([member.rust.field_name for member in nested.rust.comparable_fields], ["name"])


class TestRustPayloadParams(unittest.TestCase):
    """How many parameters a function carrying a payload takes."""

    def _payload(self, full_name: str) -> Payload:
        return Payload(owner_name="anElement", role=PayloadRole.COMMAND, protobuf=_resolved(full_name))

    def test_a_message_with_fields_has_one_parameter_per_prost_member(self):
        payload = self._payload("traps.v1.Reading")
        self.assertTrue(payload.rust.has_params)
        self.assertEqual(payload.rust.param_count, 8)
        self.assertFalse(payload.rust.is_unit)

    def test_google_protobuf_empty_has_no_parameters(self):
        """prost substitutes `()` for Empty, so there is nothing to take or to build."""
        payload = self._payload("google.protobuf.Empty")
        self.assertFalse(payload.rust.has_params)
        self.assertEqual(payload.rust.param_count, 0)
        self.assertEqual(payload.rust.struct_name, "()")
        self.assertTrue(payload.rust.is_unit)


class TestRustIdentifiers(unittest.TestCase):
    """A protobuf field is free to be called `type`; a Rust one is not."""

    def _field(self, name: str) -> ProtobufField:
        return ProtobufField(name=name, number=1, kind="string")

    def test_a_keyword_becomes_a_raw_identifier(self):
        field = self._field("type")
        self.assertEqual(field.rust.field_name, "r#type")
        self.assertEqual(field.rust.param_name(), "r#type")

    def test_a_prefixed_keyword_is_an_ordinary_identifier_again(self):
        """`_type` is not a keyword, so raw-ifying it would be wrong (and `_r#type` is not syntax)."""
        self.assertEqual(self._field("type").rust.param_name("_"), "_type")
        self.assertEqual(self._field("match").rust.param_name("_"), "_match")

    def test_the_keywords_that_cannot_be_raw_are_suffixed_instead(self):
        for name in ("self", "super", "extern", "crate"):
            self.assertEqual(self._field(name).rust.field_name, f"{name}_")
        self.assertEqual(self._field("self").rust.param_name("_"), "_self")

    def test_an_ordinary_name_is_only_snake_cased(self):
        self.assertEqual(self._field("sensorId").rust.field_name, "sensor_id")
        self.assertEqual(self._field("sensor_id").rust.param_name("_"), "_sensor_id")


class TestRustOneof(unittest.TestCase):
    """A real oneof is a single `Option<Enum>` member, not one member per alternative."""

    def setUp(self):
        (self.source,) = _resolved("traps.v1.Reading").oneofs

    def test_the_group_is_named_below_the_message_that_declares_it(self):
        self.assertEqual(self.source.rust.field_name, "source")
        self.assertEqual(self.source.rust.type, "Option<crate::proto::reading::Source>")
        self.assertEqual(self.source.rust.external_type, "Option<proto::reading::Source>")

    def test_the_example_leaves_the_group_unset(self):
        self.assertEqual(self.source.rust.example_value(), "None")
        self.assertFalse(self.source.rust.is_comparable)

    def test_a_proto3_optional_is_not_a_oneof(self):
        """protoc wraps `optional string note` in a synthetic one-member oneof."""
        self.assertEqual([oneof.name for oneof in _resolved("traps.v1.Reading").oneofs], ["source"])


if __name__ == "__main__":
    unittest.main()
