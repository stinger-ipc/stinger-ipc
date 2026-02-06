"""Configuration models for Stinger IPC."""

from pydantic import BaseModel, Field, ConfigDict
from pathlib import Path
from typing import List, Optional
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

class PythonConfig(BaseModel):
    """Python-specific configuration options."""
    python37: bool = Field(default=False, description="Generate Python 3.7 compatible code")

class TopicConfig(BaseModel):
    """ Configuration for which topic schemas to use """
    params: List[str] = Field(default_factory=list, description="List of parameters to include in topic templates")
    signals: str = Field(default="{interface_name}/{service_id}/signal/{signal_name}", description="Topic template for signals")
    property_values: str = Field(default="{interface_name}/{service_id}/property/{property_name}/value", description="Topic template for property values")
    property_updates: str = Field(default="{interface_name}/{service_id}/property/{property_name}/update", description="Topic template for property updates")
    property_update_response: str = Field(default="client/{client_id}/{interface_name}/responses", description="Topic template for property update responses")
    method_requests: str = Field(default="{interface_name}/{service_id}/method/{method_name}/request", description="Topic template for method requests")
    method_responses: str = Field(default="client/{client_id}/{interface_name}/responses", description="Topic template for method responses")
    interface_discovery: str = Field(default="{interface_name}/{service_id}/interface", description="Topic template for interface discovery")

class LanguagePluginConfig(BaseModel):
    """ Configuration for languages that are provided via plugins """
    name: str = Field(..., description="Name of the language plugin")
    model_config = ConfigDict(extra='allow')

class StingerConfig(BaseModel):
    """Root configuration model for Stinger IPC code generation."""
    python: PythonConfig = Field(default_factory=PythonConfig, description="Python generation options")
    properties: PropertyConfig = Field(default_factory=PropertyConfig, description="Property generation options")
    server: ServerConfig = Field(default_factory=ServerConfig, description="Server code generation options")
    client: ClientConfig = Field(default_factory=ClientConfig, description="Client code generation options")
    topics: TopicConfig = Field(default_factory=TopicConfig, description="Topic schema configuration")
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
    
    with config_path.open("rb") as f:
        config_dict = tomllib.load(f)
    
    return StingerConfig(**config_dict)
