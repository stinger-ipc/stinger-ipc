"""Configuration models for Stinger IPC."""

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pathlib import Path
from typing import List, Optional, Union
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


class ProtobufConfig(BaseModel):
    """Configuration for the hand-written protocol buffer definitions an interface draws on."""

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
