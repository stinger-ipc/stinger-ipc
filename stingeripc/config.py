"""Configuration models for Stinger IPC."""

from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional
import tomllib


class PropertyConfig(BaseModel):
    """Configuration options for properties."""
    stinger_owned_values: bool = Field(default=True, description="Whether the stinger-server owns property values")

class PythonConfig(BaseModel):
    """Python-specific configuration options."""
    python37: bool = Field(default=False, description="Generate Python 3.7 compatible code")


class StingerConfig(BaseModel):
    """Root configuration model for Stinger IPC code generation."""
    python: PythonConfig = Field(default_factory=PythonConfig, description="Python generation options")
    properties: PropertyConfig = Field(default_factory=PropertyConfig, description="Property generation options")


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
