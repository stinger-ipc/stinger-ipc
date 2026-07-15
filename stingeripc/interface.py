from typing import Any, Dict, IO, Union
from pathlib import Path

from .loading import parse_yaml_file, parse_yaml_io
from .components import InvalidStingerStructure, StingerSpec
from .config import StingerConfig

VERSIONS_SUPPORTED = ["0.0.7", "0.1.0"]


class StingerInterface(StingerSpec):

    def __init__(self, stinger: Dict[str, Any], config: StingerConfig):
        super().__init__(stinger["interface"], config)

    @classmethod
    def from_yaml(cls, yaml_input: Union[str, IO], config: StingerConfig) -> StingerSpec:
        yaml_obj = parse_yaml_file(yaml_input) if isinstance(yaml_input, (str, Path)) else parse_yaml_io(yaml_input)
        return cls.new_spec_from_stinger(yaml_obj, config)

    @classmethod
    def from_dict(cls, stinger_dict: Dict[str, Any], config: StingerConfig) -> StingerSpec:
        return cls.new_spec_from_stinger(stinger_dict, config)
