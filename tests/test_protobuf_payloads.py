"""Tests for protobuf payloads: parsing them out of a stinger file, and resolving
the message names against .proto sources.

Resolution normally shells out to protoc.  These tests feed it a descriptor set
built ahead of time and checked in beside them, so they exercise the real
matching logic without needing a protobuf compiler on the machine running them.
"""

import tempfile
import tomllib
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
from stingeripc.tools.generic_generator import apply_rewrites

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

    def test_fields_are_empty_until_resolved(self):
        ref = ProtobufMessageRef(full_name="weather.v1.CurrentConditions")
        self.assertEqual(ref.fields, [])
        self.assertEqual(ref.example_fields, [])


class TestFields(unittest.TestCase):
    def _resolved(self, full_name: str) -> ProtobufMessageRef:
        ref = ProtobufMessageRef(full_name=full_name)
        _sources().resolve(ref)
        return ref

    def test_reads_fields_off_the_descriptor(self):
        ref = self._resolved("weather.v1.CurrentConditions")
        self.assertEqual([(f.name, f.number, f.kind) for f in ref.fields], [("temperature", 1, "float"), ("description", 2, "string")])

    def test_marks_a_repeated_message_field(self):
        (days,) = self._resolved("weather.v1.Forecast").fields
        self.assertTrue(days.repeated)
        self.assertFalse(days.is_scalar)
        self.assertEqual(days.type_name, "weather.v1.CurrentConditions")

    def test_example_fields_are_the_singular_scalars(self):
        ref = self._resolved("weather.v1.CurrentConditions")
        self.assertEqual([f.name for f in ref.example_fields], ["temperature", "description"])

    def test_example_fields_skips_a_repeated_message(self):
        self.assertEqual(self._resolved("weather.v1.Forecast").example_fields, [])

    def test_example_values_are_spelled_per_language(self):
        temperature, description = self._resolved("weather.v1.CurrentConditions").example_fields
        # A C++ `float` setter takes a float, so the literal carries the suffix.
        self.assertTrue(temperature.get_random_example_value("c++").endswith("f"))
        self.assertEqual(temperature.get_random_example_value("python"), temperature.get_random_example_value("rust"))
        self.assertTrue(description.get_random_example_value("rust").endswith(".to_string()"))
        self.assertEqual(description.get_random_example_value("c++"), description.get_random_example_value("python"))

    def test_no_example_value_for_a_field_that_needs_another_declaration(self):
        (days,) = self._resolved("weather.v1.Forecast").fields
        self.assertIsNone(days.get_random_example_value("c++"))

    def test_a_message_with_nothing_to_fill_in_has_no_example_fields(self):
        ref = ProtobufMessageRef(full_name="google.protobuf.Empty")
        _sources().resolve(ref)
        self.assertEqual(ref.example_fields, [])


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

    def test_resolution_says_where_the_package_ends(self):
        """Only the declaring file can tell a package apart from an enclosing message."""
        ref = ProtobufMessageRef(full_name="weather.v1.CurrentConditions.Wind")
        self.assertEqual(ref.package, "weather.v1.CurrentConditions", "the guess before resolution")
        _sources().resolve(ref)
        self.assertEqual(ref.package, "weather.v1")
        self.assertEqual(ref.scope, ["CurrentConditions"])
        self.assertEqual(ref.scoped_name, "CurrentConditions.Wind")
        self.assertEqual(ref.message_name, "Wind")

    def test_an_unnested_message_has_no_scope(self):
        ref = ProtobufMessageRef(full_name="weather.v1.Forecast")
        _sources().resolve(ref)
        self.assertEqual(ref.scope, [])
        self.assertEqual(ref.scoped_name, "Forecast")

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


class TestNestedMessageNames(unittest.TestCase):
    """A message declared inside another is named through its parent, per language."""

    def _resolved(self, full_name: str) -> ProtobufMessageRef:
        ref = ProtobufMessageRef(full_name=full_name)
        _sources().resolve(ref)
        return ref

    def test_python_nests_the_class_inside_its_parents(self):
        symbols = PythonProtobufRefSymbols(self._resolved("weather.v1.CurrentConditions.Wind"))
        self.assertEqual(symbols.import_statement, "from .proto import weather_pb2")
        self.assertEqual(symbols.qualified_name, "weather_pb2.CurrentConditions.Wind")

    def test_cpp_nests_the_class_inside_its_parents(self):
        symbols = CppProtobufRefSymbols(self._resolved("weather.v1.CurrentConditions.Wind"))
        self.assertEqual(symbols.qualified_name, "::weather::v1::CurrentConditions::Wind")

    def test_rust_puts_the_struct_in_a_module_named_after_the_parent(self):
        symbols = RustProtobufRefSymbols(self._resolved("weather.v1.CurrentConditions.Wind"))
        self.assertEqual(symbols.qualified_name, "crate::proto::current_conditions::Wind")
        self.assertEqual(symbols.external_name, "proto::current_conditions::Wind")


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
        self.assertEqual(payload.content_type, "application/protobuf")  # default value from config

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


class TestPythonBindingImportRewrites(unittest.TestCase):
    """The Python recipe's ``[[rewrite]]`` rules, run over real protoc output shapes.

    protoc writes an import naming the .proto file it came from, assuming its
    output directory is on sys.path.  The bindings actually live in the generated
    package's ``proto`` subpackage, so those imports have to become relative ones
    or importing the package fails with ModuleNotFoundError.
    """

    # Lines protoc really emits, taken from its output for a .proto that imports a
    # sibling, one in a subdirectory, and a well-known type.
    MODULE = """\
from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import builder as _builder
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
import camera_pb2 as camera__pb2
from sub import lens_pb2 as sub_dot_lens__pb2
"""

    STUB = """\
import datetime
from google.protobuf import timestamp_pb2 as _timestamp_pb2
import camera_pb2 as _camera_pb2
from sub import lens_pb2 as _lens_pb2
from typing import ClassVar as _ClassVar
"""

    @staticmethod
    def _rules() -> list[dict]:
        recipe = Path("stingeripc/templates/python/partials/protoc.toml")
        return tomllib.loads(recipe.read_text())["rewrite"]

    def _rewritten(self, name: str, text: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            apply_rewrites(Path(tmp), self._rules())
            return path.read_text().splitlines()

    def test_sibling_import_becomes_relative(self):
        lines = self._rewritten("analytics_pb2.py", self.MODULE)
        self.assertIn("from . import camera_pb2 as camera__pb2", lines)
        self.assertNotIn("import camera_pb2 as camera__pb2", lines)

    def test_subdirectory_import_becomes_relative(self):
        lines = self._rewritten("analytics_pb2.py", self.MODULE)
        self.assertIn("from .sub import lens_pb2 as sub_dot_lens__pb2", lines)

    def test_well_known_types_are_left_alone(self):
        """Those come from the installed protobuf runtime, not from this package."""
        lines = self._rewritten("analytics_pb2.py", self.MODULE)
        self.assertIn(
            "from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2",
            lines,
        )
        self.assertIn("from google.protobuf import descriptor as _descriptor", lines)
        self.assertIn("from google.protobuf.internal import builder as _builder", lines)

    def test_stubs_are_rewritten_too(self):
        lines = self._rewritten("analytics_pb2.pyi", self.STUB)
        self.assertIn("from . import camera_pb2 as _camera_pb2", lines)
        self.assertIn("from .sub import lens_pb2 as _lens_pb2", lines)
        self.assertIn("from google.protobuf import timestamp_pb2 as _timestamp_pb2", lines)
        self.assertIn("import datetime", lines, "a plain stdlib import is not a binding")

    def test_a_binding_in_a_subdirectory_climbs_back_to_the_root(self):
        """protoc mirrors the .proto layout, so a nested binding sits a level down."""
        lines = self._rewritten("sub/deep_pb2.py", "import camera_pb2 as camera__pb2\n")
        self.assertEqual(lines, ["from .. import camera_pb2 as camera__pb2"])

    def test_a_binding_in_a_subdirectory_reaches_a_sibling_subdirectory(self):
        lines = self._rewritten("sub/deep_pb2.py", "from other import lens_pb2 as _lens\n")
        self.assertEqual(lines, ["from ..other import lens_pb2 as _lens"])


class TestProtobufConfig(unittest.TestCase):
    def test_present_with_defaults_even_when_unconfigured(self):
        """Every payload can be asked for its content type, protobuf or not, so the
        protobuf config is always there rather than optional."""
        protobuf = StingerConfig().protobuf
        self.assertIsNotNone(protobuf)
        self.assertEqual(protobuf.path, "protos")
        self.assertEqual(protobuf.mime_type, "application/protobuf")

    def test_path_defaults_to_protos(self):
        self.assertEqual(ProtobufConfig().path, "protos")

    def test_accepts_a_plain_string_path_under_strict_mode(self):
        config = StingerConfig(protobuf={"path": "my_protos"})
        self.assertEqual(config.protobuf.path, "my_protos")


if __name__ == "__main__":
    unittest.main()


def _traps_sources() -> ProtobufSources:
    """A ProtobufSources over the trap fixtures -- maps, oneofs, enums, proto2."""
    sources = ProtobufSources(FIXTURES)
    sources.descriptor_set = lambda: FileDescriptorSet.FromString((FIXTURES / "traps.desc").read_bytes())  # type: ignore[method-assign]
    return sources


class TestFieldModeling(unittest.TestCase):
    """What a generated per-field API needs to know about a message's members."""

    @classmethod
    def setUpClass(cls):
        cls.reading = ProtobufMessageRef(full_name="traps.v1.Reading")
        _traps_sources().resolve(cls.reading)

    def _field(self, name: str):
        return next(field for field in self.reading.fields if field.name == name)

    def test_fields_are_built_once_and_kept(self):
        self.assertIs(self.reading.fields[0], self.reading.fields[0], "resolving a field's type must write back to the field templates see")

    def test_a_map_carries_its_key_and_value(self):
        labels = self._field("labels")
        self.assertTrue(labels.is_map)
        self.assertEqual((labels.map_key.kind, labels.map_value.kind), ("string", "int32"))

    def test_a_map_of_messages_resolves_its_value_type(self):
        nested_by_name = self._field("nested_by_name")
        self.assertTrue(nested_by_name.is_map)
        self.assertEqual(nested_by_name.map_value.type_ref.full_name, "traps.v1.Reading.Nested")
        self.assertTrue(nested_by_name.map_value.type_ref.is_resolved)

    def test_members_of_a_real_oneof_name_it(self):
        self.assertEqual(self._field("sensor_id").oneof_name, "source")
        self.assertEqual(self._field("sensor_index").oneof_name, "source")

    def test_a_proto3_optional_is_not_a_oneof_member(self):
        note = self._field("note")
        self.assertIsNone(note.oneof_name)
        self.assertTrue(note.optional)
        self.assertTrue(note.is_optional_param)

    def test_oneofs_lists_only_the_real_one(self):
        self.assertEqual([group.name for group in self.reading.oneofs], ["source"])
        (source,) = self.reading.oneofs
        self.assertEqual([field.name for field in source.fields], ["sensor_id", "sensor_index"])
        self.assertIs(source.parent, self.reading)

    def test_an_enum_field_resolves_to_an_enum(self):
        severity = self._field("severity")
        self.assertTrue(severity.is_enum)
        self.assertTrue(severity.type_ref.is_resolved)
        self.assertTrue(severity.type_ref.is_enum)
        self.assertEqual(severity.type_ref.fields, [], "an enum has no fields of its own")

    def test_every_reference_to_a_type_is_resolved_not_just_the_first(self):
        history = self._field("history")
        self.assertTrue(history.repeated)
        self.assertFalse(history.is_map)
        self.assertTrue(history.type_ref.is_resolved, "the same type reached twice resolves both times")
        self.assertEqual(history.type_ref.scoped_name, "Reading.Nested")

    def test_optional_parameters_come_last(self):
        self.assertEqual(
            [field.name for field in self.reading.param_fields],
            ["labels", "nested_by_name", "severity", "history", "blob", "big", "sensor_id", "sensor_index", "note"],
        )

    def test_referenced_types_are_what_a_signature_names(self):
        self.assertEqual([ref.full_name for ref in self.reading.referenced_types], ["traps.v1.Reading.Nested", "traps.v1.Severity"])

    def test_an_enum_lists_the_values_it_declares(self):
        severity = self._field("severity").type_ref
        self.assertEqual(severity.enum_values, ["SEVERITY_UNSPECIFIED", "SEVERITY_WARNING", "SEVERITY_CRITICAL"])
        self.assertEqual(self.reading.enum_values, [], "a message declares no enum values of its own")

    def test_a_message_with_no_fields_takes_no_parameters(self):
        empty = ProtobufMessageRef(full_name="google.protobuf.Empty")
        _traps_sources().resolve(empty)
        self.assertEqual(empty.param_fields, [])

    def test_proto2_singular_fields_track_presence(self):
        old = ProtobufMessageRef(full_name="traps.legacy.Old")
        _traps_sources().resolve(old)
        self.assertEqual(old.syntax, "proto2")
        by_name = {field.name: field for field in old.fields}
        self.assertTrue(by_name["count"].optional, "a proto2 'optional' has explicit presence")
        self.assertFalse(by_name["id"].optional, "a proto2 'required' does not")
        self.assertFalse(by_name["unpacked"].optional, "a repeated field has no presence to track")

    def test_proto3_singular_fields_do_not(self):
        self.assertEqual(self.reading.syntax, "proto3")
        self.assertFalse(self._field("big").optional)


class TestInterfaceCoversFieldTypes(unittest.TestCase):
    """Imports and includes have to reach the types a payload's fields are spelled with."""

    def test_messages_include_the_types_fields_name(self):
        spec = _spec({"signals": {"s": {"protobuf": "weather.v1.Forecast"}}})
        _sources().resolve_all(spec.all_protobuf_refs())
        self.assertEqual(
            [ref.full_name for ref in spec.protobuf_messages()],
            ["weather.v1.CurrentConditions", "weather.v1.Forecast"],
            "the repeated CurrentConditions a Forecast holds is named by the generated signature",
        )

    def test_a_well_known_field_type_counts_as_using_them(self):
        spec = _spec({"signals": {"s": {"protobuf": "weather.v1.Forecast"}}})
        _sources().resolve_all(spec.all_protobuf_refs())
        self.assertFalse(spec.uses_well_known_protobuf())


class TestAsyncApiDescribesProtobuf(unittest.TestCase):
    """The AsyncAPI document has to describe a protobuf payload, not assume JSON."""

    def setUp(self):
        from stingeripc.asyncapi import stinger_to_asyncapi

        self.spec = _spec(
            {
                "signals": {"pb": {"protobuf": "weather.v1.CurrentConditions"}},
                "properties": {"pbprop": {"protobuf": "weather.v1.CurrentConditions"}},
                "commands": {"pbcmd": {"protobuf": "weather.v1.Forecast"}},
            }
        )
        _sources().resolve_all(self.spec.all_protobuf_refs())
        self.document = stinger_to_asyncapi(self.spec, StingerConfig())

    def _messages_for(self, channel_name: str) -> list[dict]:
        return list(self.document["channels"][channel_name]["messages"].values())

    def test_a_protobuf_property_does_not_raise(self):
        """A protobuf property has no single Arg, which used to abort the whole document."""
        self.assertIn("pbprop_value", self.document["channels"])

    def test_the_payload_is_described_as_the_message(self):
        (message,) = self._messages_for("pb")
        payload = message["payload"]
        self.assertEqual(payload["title"], "weather.v1.CurrentConditions")
        self.assertEqual(payload["format"], "binary")
        self.assertIn("weather.proto", payload["description"])
        self.assertIn("temperature", payload["description"], "the fields a caller passes are named")

    def test_the_content_type_is_protobuf(self):
        (message,) = self._messages_for("pb")
        self.assertEqual(message["contentType"], "application/protobuf")

    def test_a_json_interface_is_still_described_as_json(self):
        from stingeripc.asyncapi import stinger_to_asyncapi

        spec = _spec({"signals": {"s": {"values": [{"name": "x", "type": "integer"}]}}})
        document = stinger_to_asyncapi(spec, StingerConfig())
        (message,) = list(document["channels"]["s"]["messages"].values())
        self.assertEqual(message["contentType"], "application/json")
        self.assertEqual(message["payload"]["type"], "object")
