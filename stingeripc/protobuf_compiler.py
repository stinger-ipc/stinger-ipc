"""Running ``protoc`` and resolving the messages an interface refers to.

An interface element may name a protobuf message instead of listing JSON
arguments.  Only the name appears in the stinger file, so before anything can be
generated the name has to be matched against the hand-written ``.proto`` sources:
that both verifies the message exists and records which file declares it, which
is what the generated code needs in order to import it.

Matching is done from a descriptor set produced by ``protoc`` rather than by
parsing ``.proto`` text, so imports, packages and nested messages resolve exactly
the way the protobuf compiler resolves them.

Protobuf's own well-known types -- ``google.protobuf.Empty`` and its siblings --
are resolvable without appearing in the interface's sources at all, since they
are declared by the protobuf project and shipped with every language's runtime.
"""

from __future__ import annotations

import difflib
import importlib
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Sequence

from google.protobuf.descriptor_pb2 import DescriptorProto, FileDescriptorProto, FileDescriptorSet

from .exceptions import ProtobufError
from .payload import ProtobufMessageRef

# protoc is not always installed system-wide.  This wrapper package ships the
# compiler and is the same one the repository's own protobuf checks use, so the
# fallback produces the same compiler version the project already tests against.
PROTOC_WRAPPER_VERSION = "33.0"

# Since protoc 25, generated Python bindings stamp a `runtime_version` import that
# only exists in protobuf>=4.25 -- which in turn dropped Python 3.7 support.  A
# python37 target is pinned to protobuf==4.24.4 (the last release still compatible
# with 3.7), so its bindings must come from a protoc old enough not to add that
# stamp.
PROTOC_WRAPPER_VERSION_PYTHON37 = "22.0.0"


def find_protoc(configured: Optional[str] = None, python37: bool = False) -> list[str]:
    """Return the command that runs ``protoc``, as an argv prefix.

    Prefers an explicitly configured executable, then one on ``PATH``, and
    finally the pinned wrapper package.  Raises if none of those can be used.
    """
    if configured:
        resolved = shutil.which(configured) or (configured if Path(configured).is_file() else None)
        if resolved is None:
            raise ProtobufError(f"Configured protoc executable not found: '{configured}'.  Check [protobuf] protoc in your config.")
        return [resolved]

    # A python37 target needs a specific protoc version -- whatever happens to be
    # on PATH is not good enough, since its gencode must match the pinned,
    # 3.7-compatible protobuf runtime rather than whatever is newest.
    if not python37:
        on_path = shutil.which("protoc")
        if on_path:
            return [on_path]

    if shutil.which("uvx"):
        version = PROTOC_WRAPPER_VERSION_PYTHON37 if python37 else PROTOC_WRAPPER_VERSION
        return ["uvx", f"--from=protoc-wrapper@{version}", "protoc"]

    raise ProtobufError(
        "protoc was not found.  Install the protobuf compiler and put it on PATH, "
        "set [protobuf] protoc = \"/path/to/protoc\" in your config, or install 'uv' "
        f"so stinger can fall back to 'uvx --from=protoc-wrapper@{PROTOC_WRAPPER_VERSION} protoc'."
    )


def _message_names(proto_file: FileDescriptorProto) -> list[tuple[str, DescriptorProto]]:
    """Every message a file declares, as (fully-qualified name, descriptor) pairs.

    Nested messages are included under their dotted path, so a message declared
    inside another is addressable the same way protoc addresses it.
    """
    found: list[tuple[str, DescriptorProto]] = []

    def walk(prefix: str, messages) -> None:
        for message in messages:
            full_name = f"{prefix}.{message.name}" if prefix else message.name
            found.append((full_name, message))
            walk(full_name, message.nested_type)

    walk(proto_file.package, proto_file.message_type)
    return found


# The .proto files the protobuf project ships as its "well-known types".  Every
# protobuf runtime carries them, so a message from one of these resolves without
# the interface declaring anything, and nothing here is ever copied or compiled
# into the generated output.  Listed by module rather than discovered, because the
# set is fixed by the protobuf specification and reading it from the runtime's
# descriptor pool would only report whichever modules happened to be imported.
_WELL_KNOWN_MODULES = (
    "any_pb2",
    "api_pb2",
    "duration_pb2",
    "empty_pb2",
    "field_mask_pb2",
    "source_context_pb2",
    "struct_pb2",
    "timestamp_pb2",
    "type_pb2",
    "wrappers_pb2",
)

_well_known_index: Optional[dict[str, tuple[str, str, DescriptorProto]]] = None


def well_known_message_index() -> dict[str, tuple[str, str, DescriptorProto]]:
    """Fully-qualified name -> (declaring file, package, descriptor) for the well-known types.

    Read out of the protobuf runtime that stinger itself imports, so the messages
    match the ones the generated code will use, and no protoc invocation is needed
    to know they exist.
    """
    global _well_known_index
    if _well_known_index is None:
        index: dict[str, tuple[str, str, DescriptorProto]] = {}
        for module_name in _WELL_KNOWN_MODULES:
            module = importlib.import_module(f"google.protobuf.{module_name}")
            file_descriptor = module.DESCRIPTOR
            file_proto = FileDescriptorProto()
            file_descriptor.CopyToProto(file_proto)
            for full_name, descriptor in _message_names(file_proto):
                index[full_name] = (file_descriptor.name, file_proto.package, descriptor)
        _well_known_index = index
    return _well_known_index


class ProtobufSources:
    """The ``.proto`` files an interface draws its messages from."""

    def __init__(self, proto_dir: Path, protoc: Optional[str] = None, python37: bool = False):
        self.proto_dir = Path(proto_dir)
        self._protoc = find_protoc(protoc, python37=python37)
        self._index: Optional[dict[str, tuple[str, str, DescriptorProto]]] = None

    @property
    def proto_files(self) -> list[Path]:
        """Every .proto file under the source directory, in a stable order."""
        if not self.proto_dir.is_dir():
            raise ProtobufError(f"Protobuf source directory not found: {self.proto_dir}")
        return sorted(self.proto_dir.rglob("*.proto"))

    @property
    def has_sources(self) -> bool:
        """True when the directory exists and holds at least one .proto file.

        An interface whose only protobuf payloads are well-known types declares no
        .proto files of its own, so the absence of sources is not an error until
        something actually needs to be compiled.
        """
        return self.proto_dir.is_dir() and any(self.proto_dir.rglob("*.proto"))

    def run(self, *flags: str) -> None:
        """Run protoc over every source file with the given flags."""
        files = self.proto_files
        if not files:
            raise ProtobufError(f"No .proto files found in {self.proto_dir}")
        argv = [*self._protoc, "-I", str(self.proto_dir), *flags, *(str(f) for f in files)]
        completed = subprocess.run(argv, capture_output=True, text=True)
        if completed.returncode != 0:
            raise ProtobufError(f"protoc failed ({' '.join(argv)}):\n{completed.stderr.strip()}")

    def descriptor_set(self) -> FileDescriptorSet:
        """Compile the sources to a descriptor set and return it."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "descriptor_set.pb"
            self.run("--include_imports", f"--descriptor_set_out={out}")
            descriptor_set = FileDescriptorSet()
            descriptor_set.ParseFromString(out.read_bytes())
            return descriptor_set

    def _message_index(self) -> dict[str, tuple[str, str, DescriptorProto]]:
        """Fully-qualified message name -> (declaring file, package, descriptor), compiled once."""
        if self._index is None:
            index: dict[str, tuple[str, str, DescriptorProto]] = {}
            if self.has_sources:
                for proto_file in self.descriptor_set().file:
                    for full_name, descriptor in _message_names(proto_file):
                        index[full_name] = (proto_file.name, proto_file.package, descriptor)
            self._index = index
        return self._index

    @property
    def message_names(self) -> list[str]:
        """Every message the sources declare, sorted."""
        return sorted(self._message_index())

    def resolve(self, ref: ProtobufMessageRef) -> None:
        """Match a reference to a message in the sources, filling in its descriptor.

        A well-known type is matched against the protobuf runtime instead of the
        sources, since it is not the interface's to declare.  Otherwise this raises
        with the closest matching names, since a typo in a fully-qualified name is
        tedious to spot.
        """
        index = well_known_message_index() if ref.is_well_known else self._message_index()
        found = index.get(ref.full_name)
        if found is None:
            known = sorted(index)
            suggestions = difflib.get_close_matches(ref.full_name, known, n=3)
            hint = f"  Did you mean: {', '.join(suggestions)}?" if suggestions else f"  Available messages: {', '.join(known) or '(none)'}"
            where = "protobuf's well-known types" if ref.is_well_known else str(self.proto_dir)
            raise ProtobufError(f"Protobuf message '{ref.full_name}' was not found in {where}.{hint}")
        proto_file, package, descriptor = found
        ref._proto_file = proto_file
        ref._package = package
        ref._descriptor = descriptor

    def resolve_all(self, refs: Sequence[ProtobufMessageRef]) -> None:
        """Resolve every reference, so a bad name fails at generation rather than at compile time."""
        for ref in refs:
            self.resolve(ref)
