from typing import Optional, Any, Dict, IO, Union
import yaml
import yamlloader

from .components import StingerSpec, InvalidStingerStructure


VERSIONS_SUPPORTED = ["0.0.7", "0.1.0"]


class StingerInterface(StingerSpec):

    def __init__(self, stinger: Dict[str, Any], topic_prefix: Optional[str] = None):
        super().__init__(itc, stinger["interface"])


    @classmethod
    def from_yaml(cls, yaml_input: Union[str, IO], placeholder:str='{}') -> StingerSpec:
        yaml_obj = yaml.load(yaml_input, Loader=yamlloader.ordereddict.Loader)
        return cls.new_spec_from_stinger(yaml_obj)

    @classmethod
    def from_dict(cls, stinger_dict: Dict[str, Any], placeholder:str='{}') -> StingerSpec:
        return cls.new_spec_from_stinger(stinger_dict)