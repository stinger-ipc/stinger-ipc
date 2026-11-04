"""Tests for the protobuf.js JSON descriptor the generated web page loads.

The conversion is exercised against descriptor sets built ahead of time and
checked in beside these tests, so no protobuf compiler is needed to run them.

The shape assertions below pin down what protobuf.js's ``Root.fromJSON`` expects.
Getting one of them subtly wrong would not raise anywhere: it would produce a
page that decodes a message into the wrong fields, which is why they are spelled
out exactly rather than checked loosely.
"""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from google.protobuf.descriptor_pb2 import FileDescriptorSet

from stingeripc.exceptions import ProtobufError
from stingeripc.payload import ProtobufMessageRef
from stingeripc.protobuf_compiler import ProtobufSources, well_known_file_descriptors
from stingeripc.protobufjs import descriptor_set_to_protobufjs

FIXTURES = Path(__file__).parent / "fixtures"


def _descriptor_set(name: str) -> FileDescriptorSet:
    descriptor_set = FileDescriptorSet()
    descriptor_set.ParseFromString((FIXTURES / name).read_bytes())
    return descriptor_set


def _bundle(name: str) -> dict:
    return descriptor_set_to_protobufjs(_descriptor_set(name).file)


def _lookup(bundle: dict, dotted: str) -> dict:
    """Walk a bundle by a dotted path, stepping through each 'nested' level."""
    node = bundle
    for part in dotted.split("."):
        node = node["nested"][part]
    return node


class TestPackageNesting(unittest.TestCase):
    def test_package_becomes_one_namespace_per_segment(self):
        bundle = _bundle("weather.desc")
        self.assertIn("weather", bundle["nested"])
        self.assertIn("v1", bundle["nested"]["weather"]["nested"])
        self.assertIn("CurrentConditions", bundle["nested"]["weather"]["nested"]["v1"]["nested"])

    def test_message_nested_in_a_message_stays_nested(self):
        wind = _lookup(_bundle("weather.desc"), "weather.v1.CurrentConditions.Wind")
        self.assertEqual(wind["fields"], {"speed": {"type": "float", "id": 1}})


class TestFields(unittest.TestCase):
    def test_scalar_field(self):
        conditions = _lookup(_bundle("weather.desc"), "weather.v1.CurrentConditions")
        self.assertEqual(conditions["fields"]["temperature"], {"type": "float", "id": 1})

    def test_repeated_message_field_keeps_the_leading_dot(self):
        """protobuf.js resolves a reference starting with '.' from the document root.

        Stripping it would make the name relative to whatever namespace the field
        sits in, which resolves differently for a nested message.
        """
        forecast = _lookup(_bundle("weather.desc"), "weather.v1.Forecast")
        self.assertEqual(
            forecast["fields"]["days"],
            {"rule": "repeated", "type": ".weather.v1.CurrentConditions", "id": 1},
        )


class TestMaps(unittest.TestCase):
    """A map is a repeated field over a synthetic entry message in the descriptor.

    protobuf.js models maps directly, so a converter that does not recognise the
    lowering emits a list of key/value structs instead -- which encodes to the
    same bytes but presents an entirely different shape to the page.
    """

    def setUp(self):
        self.reading = _lookup(_bundle("traps.desc"), "traps.v1.Reading")

    def test_scalar_valued_map(self):
        self.assertEqual(self.reading["fields"]["labels"], {"keyType": "string", "type": "int32", "id": 1})

    def test_message_valued_map(self):
        self.assertEqual(
            self.reading["fields"]["nested_by_name"],
            {"keyType": "string", "type": ".traps.v1.Reading.Nested", "id": 2},
        )

    def test_synthetic_entry_messages_are_not_emitted(self):
        nested = self.reading.get("nested", {})
        self.assertEqual(sorted(nested), ["Nested"])


class TestOneofs(unittest.TestCase):
    def setUp(self):
        self.reading = _lookup(_bundle("traps.desc"), "traps.v1.Reading")

    def test_declared_oneof_is_reported_with_its_members(self):
        self.assertEqual(self.reading["oneofs"], {"source": {"oneof": ["sensor_id", "sensor_index"]}})

    def test_proto3_optional_is_not_reported_as_a_oneof(self):
        """protoc wraps a proto3 `optional` field in a one-member oneof of its own.

        That is presence bookkeeping, not a choice the .proto file declared, so
        reporting it would show the page a decision that does not exist.
        """
        self.assertNotIn("_note", self.reading["oneofs"])
        self.assertEqual(self.reading["fields"]["note"], {"type": "string", "id": 5})


class TestEnums(unittest.TestCase):
    def test_enum_values_are_name_to_number(self):
        severity = _lookup(_bundle("traps.desc"), "traps.v1.Severity")
        self.assertEqual(
            severity["values"],
            {"SEVERITY_UNSPECIFIED": 0, "SEVERITY_WARNING": 1, "SEVERITY_CRITICAL": 2},
        )

    def test_enum_typed_field_refers_to_the_enum(self):
        reading = _lookup(_bundle("traps.desc"), "traps.v1.Reading")
        self.assertEqual(reading["fields"]["severity"], {"type": ".traps.v1.Severity", "id": 6})


class TestProto2(unittest.TestCase):
    def setUp(self):
        self.old = _lookup(_bundle("traps.desc"), "traps.legacy.Old")

    def test_defaults_are_coerced_to_their_json_type(self):
        """protoc records every default as text; protobuf.js compares by type."""
        self.assertEqual(self.old["fields"]["count"]["options"]["default"], 7)
        self.assertEqual(self.old["fields"]["label"]["options"]["default"], "unnamed")
        self.assertIs(self.old["fields"]["active"]["options"]["default"], True)
        self.assertEqual(self.old["fields"]["ratio"]["options"]["default"], 1.5)

    def test_required_becomes_a_rule(self):
        self.assertEqual(self.old["fields"]["id"]["rule"], "required")

    def test_explicitly_unpacked_repeated_field_says_so(self):
        self.assertIs(self.old["fields"]["unpacked"]["options"]["packed"], False)


class TestWellKnownTypes(unittest.TestCase):
    def test_well_known_file_descriptors_are_keyed_by_import_path(self):
        files = well_known_file_descriptors()
        self.assertIn("google/protobuf/empty.proto", files)
        self.assertEqual(files["google/protobuf/empty.proto"].package, "google.protobuf")

    def test_empty_converts_to_a_message_with_no_fields(self):
        bundle = descriptor_set_to_protobufjs([well_known_file_descriptors()["google/protobuf/empty.proto"]])
        self.assertEqual(_lookup(bundle, "google.protobuf.Empty"), {"fields": {}})

    def test_unimported_well_known_type_is_spliced_in(self):
        """A well-known type named only from the stinger file is in no .proto import.

        protoc's --include_imports cannot reach it, so it has to come from the
        runtime instead or the page would have no schema for it.
        """
        sources = ProtobufSources(FIXTURES)
        sources.descriptor_set = lambda: _descriptor_set("weather.desc")  # type: ignore[method-assign]
        ref = ProtobufMessageRef(full_name="google.protobuf.Empty")
        sources.resolve(ref)

        names = [f.name for f in sources.descriptor_files_for([ref])]
        self.assertIn("google/protobuf/empty.proto", names)
        self.assertIn("weather.proto", names)

    def test_dependency_closure_is_included(self):
        """google.protobuf.Api imports source_context.proto and type.proto.

        A reference left dangling makes Root.fromJSON throw, taking the whole
        page with it, so the files a spliced-in type imports come along too.
        """
        sources = ProtobufSources(FIXTURES)
        sources.descriptor_set = lambda: _descriptor_set("weather.desc")  # type: ignore[method-assign]
        ref = ProtobufMessageRef(full_name="google.protobuf.Api")
        sources.resolve(ref)

        names = {f.name for f in sources.descriptor_files_for([ref])}
        self.assertIn("google/protobuf/api.proto", names)
        self.assertIn("google/protobuf/source_context.proto", names)
        self.assertIn("google/protobuf/type.proto", names)
        self.assertIn("google/protobuf/any.proto", names)

    def test_a_file_reached_twice_appears_once(self):
        sources = ProtobufSources(FIXTURES)
        sources.descriptor_set = lambda: _descriptor_set("weather.desc")  # type: ignore[method-assign]
        refs = [ProtobufMessageRef(full_name="google.protobuf.Empty") for _ in range(3)]
        for ref in refs:
            sources.resolve(ref)

        names = [f.name for f in sources.descriptor_files_for(refs)]
        self.assertEqual(len(names), len(set(names)))

    def test_works_with_no_proto_sources_at_all(self):
        """An interface whose only protobuf payload is a well-known type has no .proto dir."""
        with tempfile.TemporaryDirectory() as empty:
            sources = ProtobufSources(Path(empty))
            ref = ProtobufMessageRef(full_name="google.protobuf.Empty")
            sources.resolve(ref)
            names = [f.name for f in sources.descriptor_files_for([ref])]
        self.assertEqual(names, ["google/protobuf/empty.proto"])


class TestUnsupported(unittest.TestCase):
    def test_proto2_group_is_rejected(self):
        """protobuf.js has no representation for a group, so emitting one would
        produce a bundle that silently decodes the field wrongly."""
        from google.protobuf.descriptor_pb2 import FieldDescriptorProto, FileDescriptorProto

        file_proto = FileDescriptorProto(name="grouped.proto", package="g")
        message = file_proto.message_type.add(name="HasGroup")
        message.field.add(name="legacy", number=1, type=FieldDescriptorProto.TYPE_GROUP, label=FieldDescriptorProto.LABEL_OPTIONAL)

        with self.assertRaises(ProtobufError) as caught:
            descriptor_set_to_protobufjs([file_proto])
        self.assertIn("group", str(caught.exception))


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class TestAgainstRealProtobufJs(unittest.TestCase):
    """Encode with protobuf.js from our bundle; decode with the Python runtime.

    This is the only check that proves the bundle is *wire*-correct rather than
    merely well-shaped.  It needs protobuf.js, so it is skipped unless a local
    install happens to be available; the shape assertions above run everywhere.
    """

    @classmethod
    def setUpClass(cls):
        probe = subprocess.run(
            ["node", "-e", "require.resolve('protobufjs'); console.log('ok')"],
            capture_output=True,
            text=True,
        )
        if probe.returncode != 0:
            raise unittest.SkipTest("protobufjs is not installed for node")

    def test_bundle_loads_and_round_trips(self):
        bundle = _bundle("traps.desc")
        script = """
            const protobuf = require('protobufjs');
            const root = protobuf.Root.fromJSON(JSON.parse(process.argv[1]));
            const T = root.lookupType('traps.v1.Reading');
            const message = T.fromObject({
                labels: {alpha: 1},
                sensor_id: 'sensor-7',
                severity: 'SEVERITY_CRITICAL',
                history: [{name: 'h1', value: 1.5}]
            });
            const err = T.verify(message);
            if (err) throw new Error(err);
            console.log(Buffer.from(T.encode(message).finish()).toString('hex'));
        """
        result = subprocess.run(["node", "-e", script, json.dumps(bundle)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

        import sys

        sys.path.insert(0, str(FIXTURES))
        try:
            from google.protobuf import descriptor_pool, message_factory

            pool = descriptor_pool.DescriptorPool()
            for file_proto in _descriptor_set("traps.desc").file:
                pool.Add(file_proto)
            reading_class = message_factory.GetMessageClass(pool.FindMessageTypeByName("traps.v1.Reading"))
        finally:
            sys.path.pop(0)

        reading = reading_class.FromString(bytes.fromhex(result.stdout.strip()))
        self.assertEqual(dict(reading.labels), {"alpha": 1})
        self.assertEqual(reading.WhichOneof("source"), "sensor_id")
        self.assertEqual(reading.sensor_id, "sensor-7")
        self.assertEqual(reading.severity, 2)
        self.assertEqual([h.name for h in reading.history], ["h1"])
        self.assertAlmostEqual(reading.history[0].value, 1.5)


if __name__ == "__main__":
    unittest.main()
