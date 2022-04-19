from typing import Optional, Any, Dict, IO, Union
import yaml
import yamlloader

from .components import StingerSpec, InvalidStingerStructure
from .topic import InterfaceTopicCreator

VERSION_SUPPORTED = "0.0.5"


class StingerInterface(StingerSpec):
    def __init__(self, stinger: Dict[str, Any], topic_prefix: Optional[str] = None):
        itc = self._create_topic_creator(stinger)
        super().__init__(itc, stinger['interface'])

    @staticmethod
    def _create_topic_creator(stinger: Dict[str, Any], topic_prefix: Optional[str] = None) -> InterfaceTopicCreator:
        if (
            "stingeripc" not in stinger
            or "version" not in stinger["stingeripc"]
            or stinger["stingeripc"]["version"] not in [VERSION_SUPPORTED]
        ):
            raise InvalidStingerStructure(
                f"Provided Stinger Spec does not claim to be version {VERSION_SUPPORTED}"
            )
        if "interface" not in stinger or "name" not in stinger["interface"]:
            raise InvalidStingerStructure(
                "Could not find interface name in Stinger Spec"
            )
        itc = InterfaceTopicCreator(stinger["interface"]["name"], root=topic_prefix)
        return itc

    @classmethod
    def from_yaml(cls, yaml_input: Union[str, IO]) -> StingerSpec:
        yaml_obj = yaml.load(yaml_input, Loader=yamlloader.ordereddict.Loader)
        itc = cls._create_topic_creator(yaml_obj)
        return cls.new_from_stinger(itc, yaml_obj)
