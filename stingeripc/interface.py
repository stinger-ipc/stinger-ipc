
from typing import Optional, Any, Dict, IO
import yaml
import yamlloader

from .components import StingerSpec, InvalidStingerStructure
from .topic import InterfaceTopicCreator

VERSION_SUPPORTED = "0.0.3"

class StingerInterface(StingerSpec):

    def __init__(self, stinger: Dict[str, Any], topic_prefix: Optional[str]=None):

        if 'stingeripc' not in stinger or 'version' not in stinger['stingeripc'] or stinger['stingeripc']['version'] not in [VERSION_SUPPORTED]:
            raise InvalidStingerStructure(f"Provided Stinger Spec does not claim to be version {VERSION_SUPPORTED}")
        if 'interface' not in stinger or 'name' not in stinger['interface']:
            raise InvalidStingerStructure("Could not find interface name in Stinger Spec")
        itc = InterfaceTopicCreator(stinger['interface']['name'], root=topic_prefix)

        super().__init__(itc, stinger)

    @classmethod
    def from_yaml(cls, yaml_input: Union[str, IO]) -> StingerSpec:
        yaml_obj = yaml.load(yaml_input, Loader=yamlloader.ordereddict.Loader)
        return cls(yaml_obj)
