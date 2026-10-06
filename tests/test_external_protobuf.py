"""Tests for ``[protobuf] mode = "external"``.

In external mode the host application supplies its own compiled protobuf bindings,
so the generator must not bundle a second copy (two copies of one .proto file
cannot live in the same process's descriptor pool).  Everything here runs against
descriptor sets checked in beside the tests, so no protobuf compiler is needed.
"""

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from google.protobuf.descriptor_pb2 import FileDescriptorSet
from pydantic import ValidationError

from stingeripc.config import ExternalProtobufConfig, ProtobufConfig, StingerConfig, load_configs
from stingeripc.exceptions import InvalidStingerStructure
from stingeripc.payload import ProtobufMessageRef
from stingeripc.protobuf_compiler import ProtobufSources
from stingeripc.tools import generic_generator

FIXTURES = Path(__file__).parent / "fixtures"
TEMPLATES = Path(generic_generator.__file__).resolve().parents[1] / "templates"


def _config(**external) -> StingerConfig:
    return StingerConfig(protobuf={"mode": "external", "external": external})


def _sources() -> ProtobufSources:
    sources = ProtobufSources(FIXTURES)
    sources.descriptor_set = lambda: FileDescriptorSet.FromString((FIXTURES / "traps.desc").read_bytes())  # type: ignore[method-assign]
    return sources


def _resolved(full_name: str, config: StingerConfig | None = None) -> ProtobufMessageRef:
    ref = ProtobufMessageRef(full_name=full_name)
    _sources().resolve(ref)
    if config is not None:
        ref.bind_config(config)
    return ref


class TestExternalProtobufConfig(unittest.TestCase):
    def test_bundled_is_the_default(self):
        self.assertEqual(StingerConfig().protobuf.mode, "bundled")
        self.assertEqual(ProtobufConfig().external, ExternalProtobufConfig())

    def test_unknown_mode_is_rejected(self):
        with self.assertRaises(ValidationError):
            StingerConfig(protobuf={"mode": "vendored"})

    def test_python_package_must_be_a_dotted_module_path(self):
        self.assertEqual(ExternalProtobufConfig(python_package="generated.grpc").python_package, "generated.grpc")
        for bad in ("generated/grpc", ".generated", "a..b", "1abc"):
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                ExternalProtobufConfig(python_package=bad)

    def test_rust_module_must_be_a_rust_path(self):
        for good in ("camera_protos", "crate::bindings", "::camera_protos::v1"):
            with self.subTest(good=good):
                self.assertEqual(ExternalProtobufConfig(rust_module=good).rust_module, good)
        for bad in ("camera-protos", "a.b", "a::", "::"):
            with self.subTest(bad=bad), self.assertRaises(ValidationError):
                ExternalProtobufConfig(rust_module=bad)


class TestConfigMerging(unittest.TestCase):
    def _load(self, *documents: str) -> StingerConfig:
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for i, document in enumerate(documents):
                path = Path(tmp) / f"{i}.toml"
                path.write_text(document)
                paths.append(path)
            return load_configs(paths)

    def test_no_files_gives_the_defaults(self):
        self.assertEqual(load_configs(None), StingerConfig())
        self.assertEqual(load_configs([]), StingerConfig())

    def test_a_later_file_adds_to_a_section_rather_than_replacing_it(self):
        config = self._load('[protobuf]\npath = "mine"\n', '[protobuf]\nmode = "external"\n')
        self.assertEqual(config.protobuf.path, "mine")
        self.assertEqual(config.protobuf.mode, "external")

    def test_a_later_file_does_not_drop_earlier_python_settings(self):
        config = self._load("[python]\npython37 = true\n", "[python]\nlegacy_protobuf = true\n")
        self.assertTrue(config.python.python37)
        self.assertTrue(config.python.legacy_protobuf)

    def test_merging_reaches_nested_tables(self):
        config = self._load('[protobuf.external]\npython_package = "a"\nrust_module = "r"\n', '[protobuf.external]\npython_package = "b"\n')
        self.assertEqual(config.protobuf.external.python_package, "b")
        self.assertEqual(config.protobuf.external.rust_module, "r")

    def test_a_later_file_wins_a_conflict(self):
        config = self._load('[protobuf]\nmode = "external"\n', '[protobuf]\nmode = "bundled"\n')
        self.assertEqual(config.protobuf.mode, "bundled")

    def test_a_later_file_does_not_reset_what_it_leaves_out(self):
        config = self._load('[protobuf]\nmode = "external"\n', "[server]\nenabled = false\n")
        self.assertEqual(config.protobuf.mode, "external")


class TestPythonImports(unittest.TestCase):
    def _import(self, ref_name: str, config: StingerConfig | None) -> str:
        return _resolved(ref_name, config).python.import_statement

    def test_bundled_imports_from_the_bundled_subpackage(self):
        self.assertEqual(self._import("traps.v1.Reading", StingerConfig()), "from .proto import traps_pb2")

    def test_an_unbound_reference_behaves_as_bundled(self):
        self.assertEqual(self._import("traps.v1.Reading", None), "from .proto import traps_pb2")

    def test_external_with_no_package_imports_a_top_level_module(self):
        self.assertEqual(self._import("traps.v1.Reading", _config()), "import traps_pb2")

    def test_external_with_a_package(self):
        self.assertEqual(self._import("traps.v1.Reading", _config(python_package="generated.grpc")), "from generated.grpc import traps_pb2")

    def test_a_well_known_type_always_comes_from_the_protobuf_runtime(self):
        ref = ProtobufMessageRef(full_name="google.protobuf.Empty")
        ProtobufSources(FIXTURES).resolve(ref)
        ref.bind_config(_config(python_package="generated"))
        self.assertEqual(ref.python.import_statement, "from google.protobuf import empty_pb2")
        self.assertEqual(ref.python.absolute_import_statement("pkgipc"), "from google.protobuf import empty_pb2")

    def test_absolute_import_bundled_names_the_generated_package(self):
        ref = _resolved("traps.v1.Reading", StingerConfig())
        self.assertEqual(ref.python.absolute_import_statement("trapsipc"), "from trapsipc.proto import traps_pb2")

    def test_absolute_import_external_ignores_the_generated_package(self):
        self.assertEqual(_resolved("traps.v1.Reading", _config()).python.absolute_import_statement("trapsipc"), "import traps_pb2")
        self.assertEqual(
            _resolved("traps.v1.Reading", _config(python_package="gen")).python.absolute_import_statement("trapsipc"),
            "from gen import traps_pb2",
        )

    def test_a_file_in_a_subdirectory_keeps_its_directory(self):
        """protoc mirrors the source directory, so `sub/lens.proto` is the module `sub.lens_pb2`."""
        ref = _resolved("traps.v1.Reading")
        ref._proto_file = "sub/deeper/lens.proto"
        for config, expected in (
            (StingerConfig(), "from .proto.sub.deeper import lens_pb2"),
            (_config(), "from sub.deeper import lens_pb2"),
            (_config(python_package="gen"), "from gen.sub.deeper import lens_pb2"),
        ):
            with self.subTest(mode=config.protobuf.mode):
                ref.bind_config(config)
                self.assertEqual(ref.python.import_statement, expected)
                # The class is still named through the leaf module alone.
                self.assertEqual(ref.python.qualified_name, "lens_pb2.Reading")

    def test_the_external_module_path_is_the_dotted_name_of_the_module(self):
        ref = _resolved("traps.v1.Reading", _config(python_package="gen"))
        self.assertEqual(ref.python.external_module_path, "gen.traps_pb2")


class TestBindingConfig(unittest.TestCase):
    def test_binding_reaches_the_messages_a_message_names(self):
        """Generated code imports the types a message's fields use, so they need the config too."""
        reading = _resolved("traps.v1.Reading")
        nested = reading.referenced_types
        self.assertTrue(nested)
        self.assertTrue(all(ref.python.config is None for ref in nested))
        reading.bind_config(_config(python_package="gen"))
        for ref in nested:
            self.assertEqual(ref.python.import_statement, "from gen import traps_pb2")

    def test_binding_again_replaces_the_earlier_config(self):
        reading = _resolved("traps.v1.Reading", _config(python_package="first"))
        reading.bind_config(_config(python_package="second"))
        self.assertEqual(reading.python.import_statement, "from second import traps_pb2")


class TestCppInclude(unittest.TestCase):
    def _include(self, config: StingerConfig | None) -> str:
        return _resolved("traps.v1.Reading", config).cpp.include

    def test_bundled_includes_from_the_bundled_directory(self):
        self.assertEqual(self._include(StingerConfig()), '"proto/traps.pb.h"')
        self.assertEqual(self._include(None), '"proto/traps.pb.h"')

    def test_external_with_no_directory_includes_from_the_include_path(self):
        self.assertEqual(self._include(_config()), '"traps.pb.h"')

    def test_external_with_a_directory(self):
        self.assertEqual(self._include(_config(cpp_include_dir="gen/protos")), '"gen/protos/traps.pb.h"')
        self.assertEqual(self._include(_config(cpp_include_dir="/gen/")), '"gen/traps.pb.h"')

    def test_a_well_known_type_always_comes_from_libprotobuf(self):
        ref = ProtobufMessageRef(full_name="google.protobuf.Empty")
        ProtobufSources(FIXTURES).resolve(ref)
        ref.bind_config(_config(cpp_include_dir="gen"))
        self.assertEqual(ref.cpp.include, "<google/protobuf/empty.pb.h>")


class TestRustPaths(unittest.TestCase):
    def test_bundled_is_the_crates_own_module(self):
        ref = _resolved("traps.v1.Reading", StingerConfig())
        self.assertEqual(ref.rust.qualified_name, "crate::proto::Reading")
        self.assertEqual(ref.rust.external_name, "proto::Reading")

    def test_external_nests_the_protobuf_package_below_the_module(self):
        ref = _resolved("traps.v1.Reading", _config(rust_module="camera_protos"))
        self.assertEqual(ref.rust.qualified_name, "camera_protos::traps::v1::Reading")
        # Reachable from the crate and from outside it alike.
        self.assertEqual(ref.rust.external_name, "camera_protos::traps::v1::Reading")

    def test_external_nested_messages_keep_their_parent_module(self):
        ref = _resolved("traps.v1.Reading.Nested", _config(rust_module="camera_protos"))
        self.assertEqual(ref.rust.qualified_name, "camera_protos::traps::v1::reading::Nested")

    def test_external_without_a_module_says_what_is_missing(self):
        ref = _resolved("traps.v1.Reading", _config())
        with self.assertRaisesRegex(InvalidStingerStructure, "rust_module"):
            ref.rust.qualified_name

    def test_a_well_known_type_still_comes_from_prost_types(self):
        ref = ProtobufMessageRef(full_name="google.protobuf.Timestamp")
        ProtobufSources(FIXTURES).resolve(ref)
        ref.bind_config(_config(rust_module="camera_protos"))
        self.assertTrue(ref.rust.qualified_name.startswith("::prost_types"))


class _StubSources:
    """Stands in for ProtobufSources so emit_protobuf_bindings can run without protoc."""

    has_sources = True

    def __init__(self, proto_dir: Path):
        self.proto_dir = proto_dir
        self.proto_files = sorted(proto_dir.rglob("*.proto"))
        self.compiled_with: list[str] | None = None

    def run(self, *flags: str) -> None:
        self.compiled_with = list(flags)


class TestEmitProtobufBindings(unittest.TestCase):
    def _emit(self, config: StingerConfig) -> tuple[Path, _StubSources]:
        source_dir = Path(self._source.name)
        (source_dir / "camera.proto").write_text('syntax = "proto3";\nmessage Camera {}\n')
        sources = _StubSources(source_dir)
        stinger = SimpleNamespace(
            uses_protobuf=lambda: True,
            python=SimpleNamespace(package_directory="cameraipc"),
            name="camera",
        )
        outdir = Path(self._out.name)
        with mock.patch.object(generic_generator, "protobuf_sources", return_value=sources):
            generic_generator.emit_protobuf_bindings(TEMPLATES / "python", outdir, stinger, config, Path("camera.stinger.yaml"))
        return outdir, sources

    def setUp(self):
        self._source = tempfile.TemporaryDirectory()
        self._out = tempfile.TemporaryDirectory()
        self.addCleanup(self._source.cleanup)
        self.addCleanup(self._out.cleanup)

    def test_bundled_copies_and_compiles(self):
        outdir, sources = self._emit(StingerConfig())
        self.assertTrue((outdir / "src/cameraipc/proto/camera.proto").is_file())
        self.assertTrue((outdir / "src/cameraipc/proto/__init__.py").is_file())
        self.assertIsNotNone(sources.compiled_with)

    def test_external_writes_nothing_and_runs_no_compiler(self):
        outdir, sources = self._emit(_config())
        self.assertEqual(list(outdir.rglob("*")), [])
        self.assertIsNone(sources.compiled_with)


if __name__ == "__main__":
    unittest.main()
