from typing import Optional, Any, Dict, IO, Union
import yaml
import yamlloader

from .components import StingerSpec, InvalidStingerStructure
from .config import StingerConfig

VERSIONS_SUPPORTED = ["0.0.7", "0.1.0"]


class StingerInterface(StingerSpec):

    def __init__(self, stinger: Dict[str, Any], config: StingerConfig):
        super().__init__(stinger["interface"], config)

    @classmethod
    def from_yaml(cls, yaml_input: Union[str, IO], config: StingerConfig) -> StingerSpec:
        yaml_obj = yaml.load(yaml_input, Loader=yamlloader.ordereddict.Loader)
        return cls.new_spec_from_stinger(yaml_obj, config)

    @classmethod
    def from_dict(cls, stinger_dict: Dict[str, Any], config: StingerConfig) -> StingerSpec:
        return cls.new_spec_from_stinger(stinger_dict, config)