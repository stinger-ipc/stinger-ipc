"""Configuration models for Stinger IPC."""

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pathlib import Path
from typing import Any, List, Literal, Optional, Union
import re
import tomllib


class ServerConfig(BaseModel):
    """Configuration options for generating server/provider code."""

    enabled: bool = Field(default=True, description="Whether to generate server code")


class ClientConfig(BaseModel):
    """Configuration options for generating client code."""

    enabled: bool = Field(default=True, description="Whether to generate client code")


class PropertyConfig(BaseModel):
    """Configuration options for properties."""

    stinger_owned_values: bool = Field(default=True, description="Whether the stinger-server owns property values")
    version_tracking: bool = Field(
        default=True,
        description="Whether properties carry a monotonic version counter (the 'PropertyVersion' user property) used to reject out-of-sync updates",
    )


class PythonConfig(BaseModel):
    """Python-specific configuration options."""

    python37: bool = Field(default=False, description="Generate Python 3.7 compatible code")
    legacy_protobuf: bool = Field(
        default=False,
        description="Generate protobuf bindings for the old protobuf 3.x runtime (3.9 and later, before 4). For targets whose installed protobuf predates 3.20",
    )
    package_suffix: str = Field(default="ipc", description="Suffix to append to generated Python package names")


class RustConfig(BaseModel):
    """Rust-specific configuration options."""

    package_suffix: str = Field(default="ipc", description="Suffix to append to generated Rust module names")


class CppConfig(BaseModel):
    """C++-specific configuration options."""

    namespace: List[str] = Field(
        default_factory=lambda: ["stinger", "gen"], description="List of nested namespaces for generated C++ code.  The interface name is appended to this as the innermost namespace."
    )
    package_suffix: str = Field(default="ipc", description="Suffix to append to generated C++ namespace and filenames")


class LanguagePluginConfig(BaseModel):
    """Configuration for languages that are provided via plugins"""

    name: str = Field(..., description="Name of the language plugin")
    model_config = ConfigDict(extra="allow")


_DOTTED_IDENTIFIER = re.compile(r"^[A-Za-z_]\w*(\.[A-Za-z_]\w*)*$")
_RUST_PATH = re.compile(r"^(::)?[A-Za-z_]\w*(::[A-Za-z_]\w*)*$")


class ExternalProtobufConfig(BaseModel):
    """Where each language finds protobuf bindings that the host supplies, used when ``[protobuf] mode = "external"``."""

    python_package: str = Field(
        default="",
        description="Python package the externally supplied _pb2 modules are imported from. Empty means they are top-level modules on sys.path",
    )
    cpp_include_dir: str = Field(
        default="",
        description="Directory prefix of the externally supplied .pb.h headers, as used in an #include. Empty means the headers are at the top of the include path",
    )
    cpp_cmake_target: str = Field(
        default="",
        description="CMake target providing the externally supplied C++ bindings, linked PUBLIC to the generated library. Empty means the consumer links them",
    )
    rust_module: str = Field(
        default="",
        description="Rust module path holding the externally supplied prost types, e.g. 'camera_protos'",
    )
    rust_dependency: str = Field(
        default="",
        description="A Cargo.toml dependency line, written verbatim, that makes rust_module available to the generated crate. Optional",
    )

    @field_validator("python_package")
    @classmethod
    def validate_python_package(cls, v: str) -> str:
        if v and not _DOTTED_IDENTIFIER.match(v):
            raise ValueError(f"python_package '{v}' is not a dotted Python module path")
        return v

    @field_validator("rust_module")
    @classmethod
    def validate_rust_module(cls, v: str) -> str:
        if v and not _RUST_PATH.match(v):
            raise ValueError(f"rust_module '{v}' is not a Rust module path (expected something like 'camera_protos' or 'crate::bindings')")
        return v


class ProtobufConfig(BaseModel):
    """Configuration for the hand-written protocol buffer definitions an interface draws on."""

    mode: Literal["bundled", "external"] = Field(
        default="bundled",
        description="'bundled' copies the .proto files into the generated output and compiles them there. 'external' leaves that to the host, which supplies the bindings itself (see 'external')",
    )
    external: ExternalProtobufConfig = Field(
        default_factory=ExternalProtobufConfig,
        description="Where the externally supplied bindings live, per language. Used only when mode is 'external'",
    )

    path: str = Field(
        default="protos",
        description="Directory holding the .proto files, resolved relative to the .stinger.yaml file",
    )
    protoc: Optional[str] = Field(
        default=None,
        description="The protoc executable to use; auto-detected when unset",
    )
    mime_type: Union[str, bool] = Field(default="application/protobuf", description="The mime type used in the MQTTv5 content-type property")

    @field_validator("mime_type")
    @classmethod
    def validate_method_responses(cls, v: Union[str, bool]) -> Union[str, bool]:
        if isinstance(v, str):
            if "/" not in v:
                raise ValueError("Protobuf mime type does not look like a valid mime type (missing '/')")
        elif v is True:
            raise ValueError("A TRUE value for protobuf mime type does not have a valid meaning")
        return v


class DiscoveryConfig(BaseModel):
    """Configuration options for service discovery."""

    client_id: str = Field(default="{client_id}", description="Template for client ID.")
    advert_interval_seconds: int = Field(default=120, description="Interval in seconds for re-advertising the server's presence")


class StingerConfig(BaseModel):
    """Root configuration model for Stinger IPC code generation."""

    python: PythonConfig = Field(default_factory=PythonConfig, description="Python generation options")
    cpp: CppConfig = Field(default_factory=CppConfig, description="C++ generation options")
    rust: RustConfig = Field(default_factory=RustConfig, description="Rust generation options")
    properties: PropertyConfig = Field(default_factory=PropertyConfig, description="Property generation options")
    server: ServerConfig = Field(default_factory=ServerConfig, description="Server code generation options")
    client: ClientConfig = Field(default_factory=ClientConfig, description="Client code generation options")
    discovery: DiscoveryConfig = Field(default_factory=DiscoveryConfig, description="Service discovery configuration")
    protobuf: ProtobufConfig = Field(default_factory=ProtobufConfig, description="Protobuf related configuration")
    language: dict[str, LanguagePluginConfig] = Field(default_factory=dict, description="Language plugin configurations")

    model_config = ConfigDict(strict=True)


def load_config(config_path: Path) -> StingerConfig:
    """
    Load and parse a TOML configuration file.

    Args:
        config_path: Path to the TOML configuration file.

    Returns:
        A StingerConfig instance with the parsed configuration.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        ValueError: If the TOML is invalid or doesn't match the schema.
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open(mode="rb") as f:
        config_dict = tomllib.load(f)

    if "topics" in config_dict:
        raise ValueError(f"{config_path}: topic templates are declared in the interface's .stinger.yaml file (under a top-level 'topics:' key), not in a config file")

    return StingerConfig(**config_dict)


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge ``override`` into ``base``, descending into tables both sides define."""
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def merge_configs(configs: List[StingerConfig]) -> StingerConfig:
    """Combine configs in order, later ones overriding earlier ones.

    The merge descends into each section, so a later file that sets one key of a
    section (say ``[protobuf] mode``) leaves the other keys an earlier file set
    for that section (``[protobuf] path``) alone.  Only keys a file actually set
    take part, so a file never resets a value to its default.
    """
    merged: dict[str, Any] = {}
    for config in configs:
        merged = _deep_merge(merged, config.model_dump(exclude_unset=True))
    return StingerConfig.model_validate(merged)


def load_configs(config_paths: Optional[List[Path]]) -> StingerConfig:
    """Load each config file and merge them, later files overriding earlier ones."""
    return merge_configs([load_config(path) for path in config_paths or []])
