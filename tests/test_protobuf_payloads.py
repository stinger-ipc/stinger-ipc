"""Tests for protobuf payloads: parsing them out of a stinger file, and resolving
the message names against .proto sources.

Resolution normally shells out to protoc.  These tests feed it a descriptor set
built ahead of time and checked in beside them, so they exercise the real
matching logic without needing a protobuf compiler on the machine running them.
"""

import unittest
from pathlib import Path
from unittest import mock

from google.protobuf.descriptor_pb2 import FileDescriptorSet

from stingeripc.components import StingerSpec
from stingeripc.config import ProtobufConfig, StingerConfig
from stingeripc.exceptions import InvalidStingerStructure, ProtobufError
from stingeripc.cpp_symb import CppProtobufRefSymbols
from stingeripc.payload import PayloadRole, ProtobufMessageRef
from stingeripc.protobuf_compiler import ProtobufSources, find_protoc, well_known_message_index
from stingeripc.python_symb import PythonProtobufRefSymbols
from stingeripc.rust_symb import RustProtobufRefSymbols

FIXTURES = Path(__file__).parent / "fixtures"


def _fixture_descriptor_set() -> FileDescriptorSet:
    descriptor_set = FileDescriptorSet()
    descriptor_set.ParseFromString((FIXTURES / "weather.desc").read_bytes())
    return descriptor_set


def _sources() -> ProtobufSources:
    """A ProtobufSources whose descriptor set comes from the fixture, not protoc."""
    sources = ProtobufSources(FIXTURES)
    sources.descriptor_set = _fixture_descriptor_set  # type: ignore[method-assign]
    return sources


def _spec(elements: dict) -> StingerSpec:
    stinger = {
        "stingeripc": {"version": "0.3.0"},
        "interface": {"name": "pbtest", "version": "0.0.1"},
    }
    stinger.update(elements)
    return StingerSpec.new_spec_from_stinger(stinger, StingerConfig())


class TestProtobufMessageRef(unittest.TestCase):
    def test_splits_package_from_message_name(self):
        ref = ProtobufMessageRef(full_name="weather.v1.CurrentConditions")
        self.assertEqual(ref.package, "weather.v1")
        self.assertEqual(ref.message_name, "CurrentConditions")

    def test_message_with_no_package(self):
        ref = ProtobufMessageRef(full_name="Standalone")
        self.assertEqual(ref.package, "")
        self.assertEqual(ref.message_name, "Standalone")

    def test_is_unresolved_until_matched(self):
        ref = ProtobufMessageRef(full_name="weather.v1.CurrentConditions")
        self.assertFalse(ref.is_resolved)
        with self.assertRaises(ValueError):
            ref.proto_file

    def test_fields_are_empty_pending_descriptor_support(self):
        ref = ProtobufMessageRef(full_name="weather.v1.CurrentConditions")
        self.assertEqual(ref.fields, [])


class TestResolution(unittest.TestCase):
    def test_resolves_a_known_message(self):
        ref = ProtobufMessageRef(full_name="weather.v1.CurrentConditions")
        _sources().resolve(ref)
        self.assertTrue(ref.is_resolved)
        self.assertEqual(ref.proto_file, "weather.proto")

    def test_resolves_a_nested_message(self):
        ref = ProtobufMessageRef(full_name="weather.v1.CurrentConditions.Wind")
        _sources().resolve(ref)
        self.assertTrue(ref.is_resolved)

    def test_unknown_message_suggests_close_matches(self):
        ref = ProtobufMessageRef(full_name="weather.v1.Forcast")
        with self.assertRaises(ProtobufError) as caught:
            _sources().resolve(ref)
        self.assertIn("weather.v1.Forecast", str(caught.exception))

    def test_lists_every_message_including_nested(self):
        self.assertEqual(
            _sources().message_names,
            ["weather.v1.CurrentConditions", "weather.v1.CurrentConditions.Wind", "weather.v1.Forecast"],
        )



class TestWellKnownTypes(unittest.TestCase):
    """Protobuf's own types resolve without the interface declaring them."""

    def _resolved(self, full_name: str) -> ProtobufMessageRef:
        ref = ProtobufMessageRef(full_name=full_name)
        _sources().resolve(ref)
        return ref

    def test_recognises_the_google_protobuf_package(self):
        self.assertTrue(ProtobufMessageRef(full_name="google.protobuf.Empty").is_well_known)
        self.assertFalse(ProtobufMessageRef(full_name="weather.v1.Forecast").is_well_known)
        self.assertFalse(
            ProtobufMessageRef(full_name="google.protobuf.nested.Thing").is_well_known,
            "only the well-known package itself, not anything beneath it",
        )

    def test_resolves_without_any_local_sources(self):
        ref = self._resolved("google.protobuf.Empty")
        self.assertTrue(ref.is_resolved)
        self.assertEqual(ref.proto_file, "google/protobuf/empty.proto")

    def test_resolves_with_no_proto_directory_at_all(self):
        """An interface using only well-known types needs no .proto sources."""
        sources = ProtobufSources(FIXTURES / "no_such_directory")
        self.assertFalse(sources.has_sources)
        ref = ProtobufMessageRef(full_name="google.protobuf.Empty")
        sources.resolve(ref)
        self.assertTrue(ref.is_resolved)

    def test_index_covers_the_whole_well_known_set(self):
        index = well_known_message_index()
        for name in ("Empty", "Timestamp", "Duration", "Any", "Struct", "FieldMask", "StringValue"):
            self.assertIn(f"google.protobuf.{name}", index)

    def test_unknown_well_known_type_is_reported_against_the_right_place(self):
        ref = ProtobufMessageRef(full_name="google.protobuf.Emty")
        with self.assertRaises(ProtobufError) as caught:
            _sources().resolve(ref)
        message = str(caught.exception)
        self.assertIn("well-known types", message)
        self.assertIn("google.protobuf.Empty", message, "a near miss is suggested")

    def test_interface_reports_that_it_uses_them(self):
        spec = _spec({"commands": {"c": {"protobuf": "google.protobuf.Empty"}}})
        self.assertTrue(spec.uses_protobuf())
        self.assertTrue(spec.uses_well_known_protobuf())

    def test_interface_of_its_own_messages_only_does_not(self):
        spec = _spec({"commands": {"c": {"protobuf": "weather.v1.Forecast"}}})
        self.assertTrue(spec.uses_protobuf())
        self.assertFalse(spec.uses_well_known_protobuf())

    def test_python_imports_from_the_installed_runtime(self):
        symbols = PythonProtobufRefSymbols(self._resolved("google.protobuf.Empty"))
        self.assertEqual(symbols.import_statement, "from google.protobuf import empty_pb2")
        self.assertEqual(symbols.qualified_name, "empty_pb2.Empty")

    def test_python_imports_the_interfaces_own_messages_from_its_package(self):
        symbols = PythonProtobufRefSymbols(self._resolved("weather.v1.Forecast"))
        self.assertEqual(symbols.import_statement, "from .proto import weather_pb2")

    def test_cpp_includes_the_libprotobuf_header(self):
        symbols = CppProtobufRefSymbols(self._resolved("google.protobuf.Empty"))
        self.assertEqual(symbols.include, "<google/protobuf/empty.pb.h>")
        self.assertEqual(symbols.qualified_name, "::google::protobuf::Empty")

    def test_cpp_includes_the_interfaces_own_headers_relatively(self):
        symbols = CppProtobufRefSymbols(self._resolved("weather.v1.Forecast"))
        self.assertEqual(symbols.include, '"proto/weather.pb.h"')

    def test_rust_uses_the_substitute_prost_gives_empty(self):
        symbols = RustProtobufRefSymbols(self._resolved("google.protobuf.Empty"))
        self.assertEqual(symbols.qualified_name, "()", "prost maps Empty onto the unit type")
        self.assertEqual(symbols.external_name, "()")

    def test_rust_uses_prost_types_for_the_rest(self):
        symbols = RustProtobufRefSymbols(self._resolved("google.protobuf.Timestamp"))
        self.assertEqual(symbols.qualified_name, "::prost_types::Timestamp")
        self.assertEqual(symbols.external_name, "::prost_types::Timestamp")

    def test_rust_still_reaches_the_interfaces_own_messages_through_the_crate(self):
        symbols = RustProtobufRefSymbols(self._resolved("weather.v1.Forecast"))
        self.assertEqual(symbols.qualified_name, "crate::proto::Forecast")
        self.assertEqual(symbols.external_name, "proto::Forecast")


class TestFindProtoc(unittest.TestCase):
    def test_prefers_protoc_on_path(self):
        with mock.patch("shutil.which", side_effect=lambda name: "/usr/bin/protoc" if name == "protoc" else None):
            self.assertEqual(find_protoc(), ["/usr/bin/protoc"])

    def test_falls_back_to_the_pinned_wrapper(self):
        with mock.patch("shutil.which", side_effect=lambda name: "/usr/bin/uvx" if name == "uvx" else None):
            self.assertEqual(find_protoc()[0], "uvx")

    def test_raises_when_nothing_can_run_protoc(self):
        with mock.patch("shutil.which", return_value=None):
            with self.assertRaises(ProtobufError):
                find_protoc()

    def test_rejects_a_configured_executable_that_does_not_exist(self):
        with mock.patch("shutil.which", return_value=None):
            with self.assertRaises(ProtobufError):
                find_protoc("/nonexistent/protoc")


class TestParsingProtobufElements(unittest.TestCase):
    def test_signal_carries_a_protobuf_payload(self):
        spec = _spec({"signals": {"s": {"protobuf": "weather.v1.CurrentConditions"}}})
        payload = spec.signals["s"].payload
        self.assertTrue(payload.is_protobuf)
        self.assertEqual(payload.role, PayloadRole.SIGNAL)
        self.assertEqual(payload.arg_list, [], "a protobuf payload has no JSON arguments to iterate")
        self.assertEqual(payload.content_type, "application/protobuf")

    def test_command_carries_a_protobuf_payload(self):
        spec = _spec({"commands": {"c": {"protobuf": "weather.v1.Forecast"}}})
        self.assertTrue(spec.commands["c"].payload.is_protobuf)

    def test_property_carries_a_protobuf_payload(self):
        spec = _spec({"properties": {"p": {"protobuf": "weather.v1.CurrentConditions"}}})
        prop = spec.properties["p"]
        self.assertTrue(prop.payload.is_protobuf)
        self.assertEqual(prop.arg_list, [])
        with self.assertRaises(InvalidStingerStructure):
            prop.value

    def test_method_carries_protobuf_on_both_sides(self):
        spec = _spec({"methods": {"m": {"protobuf": "weather.v1.Forecast", "returnProtobuf": "weather.v1.CurrentConditions"}}})
        method = spec.methods["m"]
        self.assertTrue(method.request_payload.is_protobuf)
        self.assertTrue(method.response_payload.is_protobuf)
        self.assertTrue(method.has_response)
        self.assertIsNone(method.return_value)

    def test_method_with_only_a_protobuf_request_is_rejected(self):
        with self.assertRaises(InvalidStingerStructure):
            _spec({"methods": {"m": {"protobuf": "weather.v1.Forecast"}}})

    def test_declaring_both_arguments_and_protobuf_is_rejected(self):
        with self.assertRaises(InvalidStingerStructure):
            _spec({"signals": {"s": {"values": [{"name": "x", "type": "integer"}], "protobuf": "weather.v1.Forecast"}}})

    def test_protobuf_name_must_be_a_string(self):
        with self.assertRaises(InvalidStingerStructure):
            _spec({"signals": {"s": {"protobuf": 42}}})

    def test_documentation_and_version_survive_the_protobuf_branch(self):
        spec = _spec({"signals": {"s": {"protobuf": "weather.v1.Forecast", "version": "1.2.3", "documentation": "A forecast."}}})
        self.assertEqual(spec.signals["s"].version, "1.2.3")
        self.assertEqual(spec.signals["s"].documentation, "A forecast.")


class TestInterfaceLevelHelpers(unittest.TestCase):
    def setUp(self):
        self.spec = _spec(
            {
                "signals": {"pb": {"protobuf": "weather.v1.CurrentConditions"}, "json": {"values": [{"name": "x", "type": "integer"}]}},
                "commands": {"c": {"protobuf": "weather.v1.CurrentConditions"}},
            }
        )

    def test_reports_both_encodings_in_a_mixed_interface(self):
        self.assertTrue(self.spec.uses_protobuf())
        self.assertTrue(self.spec.uses_json())

    def test_messages_are_deduplicated_and_sorted(self):
        names = [ref.full_name for ref in self.spec.protobuf_messages()]
        self.assertEqual(names, ["weather.v1.CurrentConditions"], "one message used twice is listed once")

    def test_json_only_interface_uses_no_protobuf(self):
        spec = _spec({"signals": {"s": {"values": [{"name": "x", "type": "integer"}]}}})
        self.assertFalse(spec.uses_protobuf())
        self.assertEqual(spec.protobuf_messages(), [])

    def test_proto_files_lists_the_declaring_files(self):
        sources = _sources()
        sources.resolve_all(self.spec.protobuf_messages())
        self.assertEqual(self.spec.protobuf_files(), ["weather.proto"])


class TestProtobufConfig(unittest.TestCase):
    def test_absent_by_default(self):
        self.assertIsNone(StingerConfig().protobuf)

    def test_path_defaults_to_protos(self):
        self.assertEqual(ProtobufConfig().path, "protos")

    def test_accepts_a_plain_string_path_under_strict_mode(self):
        config = StingerConfig(protobuf={"path": "my_protos"})
        assert config.protobuf is not None
        self.assertEqual(config.protobuf.path, "my_protos")


if __name__ == "__main__":
    unittest.main()
