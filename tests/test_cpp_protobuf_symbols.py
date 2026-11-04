"""What the C++ templates are told about a protobuf message's individual fields.

The generated C++ API for a protobuf signal, command or method takes the message's
fields one by one, so every field has to be given a C++ type, a parameter name, and
the accessors protoc's own generated class exposes.  These tests pin that down
against the checked-in `traps.desc` descriptor set, which covers the shapes an
interface's own .proto files rarely have all at once: maps, a real oneof, a proto3
`optional`, an enum, a nested message, `bytes` and `int64`.

Resolution normally shells out to protoc; as in test_protobuf_payloads.py, the
descriptor set is read from the fixture instead, so no protobuf compiler is needed.
"""

import unittest
from pathlib import Path

from google.protobuf.descriptor_pb2 import FileDescriptorSet

from stingeripc.payload import ProtobufField, ProtobufMessageRef
from stingeripc.protobuf_compiler import ProtobufSources

FIXTURES = Path(__file__).parent / "fixtures"


def _traps_sources() -> ProtobufSources:
    """A ProtobufSources over the trap fixtures -- maps, oneofs, enums, proto2."""
    sources = ProtobufSources(FIXTURES)
    sources.descriptor_set = lambda: FileDescriptorSet.FromString((FIXTURES / "traps.desc").read_bytes())  # type: ignore[method-assign]
    return sources


class TestCppFieldTypes(unittest.TestCase):
    """The C++ type each field of `traps.v1.Reading` is handed over as."""

    @classmethod
    def setUpClass(cls):
        cls.reading = ProtobufMessageRef(full_name="traps.v1.Reading")
        _traps_sources().resolve(cls.reading)

    def _field(self, name: str):
        return next(field for field in self.reading.fields if field.name == name)

    def test_value_type_of_every_field(self):
        expected = {
            # A map is handed over as a std::map, not protobuf's own Map<>.
            "labels": "std::map<std::string, int32_t>",
            "nested_by_name": "std::map<std::string, ::traps::v1::Reading::Nested>",
            # A oneof member may be left unset, so it is optional.
            "sensor_id": "std::optional<std::string>",
            "sensor_index": "std::optional<uint32_t>",
            # As may a proto3 `optional`.
            "note": "std::optional<std::string>",
            # An enum is its own generated type, nested types spelled through their parents.
            "severity": "::traps::v1::Severity",
            "history": "std::vector<::traps::v1::Reading::Nested>",
            # protoc gives `bytes` a std::string.
            "blob": "std::string",
            "big": "int64_t",
        }
        self.assertEqual({field.name: field.cpp.value_type for field in self.reading.fields}, expected)

    def test_param_type_of_every_field(self):
        expected = {
            "labels": "const std::map<std::string, int32_t>&",
            "nested_by_name": "const std::map<std::string, ::traps::v1::Reading::Nested>&",
            "sensor_id": "const std::optional<std::string>&",
            "sensor_index": "const std::optional<uint32_t>&",
            "note": "const std::optional<std::string>&",
            # An enum fits in a register, so it goes by value.
            "severity": "::traps::v1::Severity",
            "history": "const std::vector<::traps::v1::Reading::Nested>&",
            "blob": "const std::string&",
            "big": "int64_t",
        }
        self.assertEqual({field.name: field.cpp.param_type for field in self.reading.fields}, expected)

    def test_a_number_goes_by_value_and_a_string_by_reference(self):
        self.assertEqual(self._field("big").cpp.param_type, "int64_t")
        self.assertEqual(self._field("blob").cpp.param_type, "const std::string&")

    def test_parameter_names_are_lower_camel_case(self):
        self.assertEqual(self._field("nested_by_name").cpp.param_name, "nestedByName")
        self.assertEqual(self._field("sensor_id").cpp.param_name, "sensorId")

    def test_accessors_are_the_ones_protoc_generates(self):
        nested = self._field("nested_by_name").cpp
        self.assertEqual(nested.getter, "nested_by_name")
        self.assertEqual(nested.setter, "set_nested_by_name")
        self.assertEqual(nested.mutable, "mutable_nested_by_name")
        self.assertEqual(self._field("history").cpp.adder, "add_history")
        self.assertEqual(self._field("note").cpp.has, "has_note")

    def test_only_singular_non_float_scalars_are_comparable(self):
        comparable = {field.name for field in self.reading.fields if field.cpp.is_comparable}
        self.assertEqual(comparable, {"blob", "big"})

    def test_set_statements_match_the_shape_of_the_field(self):
        self.assertEqual(self._field("big").cpp.set_statement("msg", "big"), "msg.set_big(big);")
        self.assertEqual(
            self._field("history").cpp.set_statement("msg", "history"),
            "for (const auto& item : history) { *msg.add_history() = item; }",
        )
        self.assertEqual(
            self._field("labels").cpp.set_statement("msg", "labels"),
            "for (const auto& kv : labels) { (*msg.mutable_labels())[kv.first] = kv.second; }",
        )
        self.assertEqual(
            self._field("note").cpp.set_statement("msg", "note"),
            "if (note) { msg.set_note(*note); }",
        )

    def test_extract_expressions_copy_out_of_protobufs_own_containers(self):
        self.assertEqual(self._field("big").cpp.extract_expr("msg"), "msg.big()")
        self.assertEqual(
            self._field("history").cpp.extract_expr("msg"),
            "std::vector<::traps::v1::Reading::Nested>(msg.history().begin(), msg.history().end())",
        )
        self.assertEqual(
            self._field("note").cpp.extract_expr("msg"),
            "msg.has_note() ? std::optional<std::string>(msg.note()) : std::nullopt",
        )
        self.assertIn("out.emplace(kv.first, kv.second)", self._field("labels").cpp.extract_expr("msg"))

    def test_example_values_are_literals_a_demo_can_pass(self):
        self.assertEqual(self._field("big").cpp.example_value(), "42")
        self.assertEqual(self._field("blob").cpp.example_value(), '"apples"')
        self.assertEqual(self._field("note").cpp.example_value(), "std::nullopt")
        self.assertEqual(self._field("history").cpp.example_value(), "std::vector<::traps::v1::Reading::Nested>{}")
        self.assertEqual(self._field("severity").cpp.example_value(), "::traps::v1::Severity{}")

    def test_a_message_with_no_fields_contributes_no_parameters(self):
        empty = ProtobufMessageRef(full_name="google.protobuf.Empty")
        _traps_sources().resolve(empty)
        self.assertEqual([field.cpp.param_name for field in empty.param_fields], [])


class TestCppKeywordFields(unittest.TestCase):
    """A field whose name is a C++ keyword, which protoc renames and so must we."""

    def test_a_keyword_named_field_gets_a_trailing_underscore(self):
        field = ProtobufField(name="class", number=1, kind="string")
        self.assertEqual(field.cpp.param_name, "class_")
        self.assertEqual(field.cpp.accessor, "class_")
        self.assertEqual(field.cpp.getter, "class_")
        self.assertEqual(field.cpp.setter, "set_class_")

    def test_a_field_named_after_a_generated_local_is_renamed_too(self):
        # `msg` is the name the generated receivers give the incoming message, so a
        # parameter of that name would shadow it inside the very statement that
        # reads from it.
        field = ProtobufField(name="msg", number=1, kind="string")
        self.assertEqual(field.cpp.param_name, "msg_")
        self.assertEqual(field.cpp.accessor, "msg", "protoc renames only for its own keywords")

    def test_an_ordinary_name_is_left_alone(self):
        field = ProtobufField(name="sensor_id", number=1, kind="string")
        self.assertEqual(field.cpp.param_name, "sensorId")
        self.assertEqual(field.cpp.accessor, "sensor_id")


if __name__ == "__main__":
    unittest.main()
