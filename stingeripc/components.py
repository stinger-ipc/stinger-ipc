from __future__ import annotations
from enum import Enum
import random
from typing import Dict, List, Optional
from .topic import SignalTopicCreator, InterfaceTopicCreator

ALLOWED_ARG_TYPES = []


class InvalidStingerStructure(Exception):
    pass


class PayloadType(Enum):
    JSON_SCHEMA = 0
    ARG_LIST = 1


class ArgType(Enum):
    BOOLEAN = 0
    INTEGER = 1
    FLOAT = 2
    STRING = 3

    @classmethod
    def from_string(cls, arg_type: str) -> ArgType:
        if hasattr(cls, arg_type.upper()):
            return getattr(cls, arg_type.upper())
        else:
            raise InvalidStingerStructure(f"No ArgType called '{arg_type}'")

    @classmethod
    def to_python_type(cls, arg_type: ArgType) -> str:
        if arg_type == cls.BOOLEAN:
            return "bool"
        elif arg_type == cls.INTEGER:
            return "int"
        elif arg_type == cls.FLOAT:
            return "float"
        elif arg_type == cls.STRING:
            return "str"
        raise InvalidStingerStructure(
            "Unhandled arg type"
        )

class Arg(object):
    def __init__(self, name: str, arg_type: ArgType, description: Optional[str] = None):
        self._name = name
        self._arg_type = arg_type
        self._description = description

    def set_description(self, description: str) -> Arg:
        self._description = description
        return self

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> PayloadType:
        return self._arg_type

    @property
    def python_type(self) -> str:
        return ArgType.to_python_type(self._arg_type)

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def random_example_value(self) -> Union[str, float, int, bool]:
        if self._arg_type == ArgType.BOOLEAN:
            return random.choice([True, False])
        elif self._arg_type == ArgType.FLOAT:
            return random.choice([3.14, 1.0, 2.5, 97.9])
        elif self._arg_type == ArgType.INTEGER:
            return random.choice([42, 1981, 2020])
        elif self._arg_type == ArgType.STRING:
            return random.choice(['"apples"', '"Joe"', '"example"', '"foo"'])

    @classmethod
    def new_from_stinger(cls, name: str, stinger: Dict[str, str]) -> Arg:
        if "type" not in stinger:
            raise InvalidStingerStructure("No 'type' in arg structure")
        arg = cls(name, ArgType.from_string(stinger["type"]))
        if "description" in stinger and isinstance(stinger["description"], str):
            arg.set_description(stinger["description"])
        return arg


class Schema(object):
    """Eventually this will do more than simply be a dumb object.
    It will probably do some parsing of the schema to make it more
    accessible/powerful.
    """

    def __init__(self, schema):
        self._schema = schema


class Signal(object):
    def __init__(self, topic_creator: SignalTopicCreator, name: str):
        self._topic_creator = topic_creator
        self._name = name
        self._payload_type = PayloadType.ARG_LIST
        self._schema = None  # type: Optional[Schema]
        self._arg_list = []  # type: List[Arg]

    def set_schema(self, schema: Schema) -> Signal:
        self._schema = schema
        self._payload_type = PayloadType.JSON_SCHEMA
        return self

    def set_arg_list(self, arg_list: List[Arg]) -> Signal:
        self._arg_list = arg_list
        self._payload_type = PayloadType.ARG_LIST
        return self

    @property
    def arg_list(self) -> List[Arg]:
        return self._arg_list

    @property
    def name(self) -> str:
        return self._name

    @property
    def topic(self) -> str:
        return self._topic_creator.signal_topic(self.name)

    @classmethod
    def new_from_stinger(
        cls, topic_creator: SignalTopicCreator, name: str, spec: Dict[str, str]
    ) -> "Signal":
        """Alternative constructor from a Stinger signal structure."""
        signal = cls(topic_creator, name)
        if 'payload' not in spec:
            raise InvalidStingerStructure("Signal specification must have 'payload'")
        if (("args" in spec['payload'] and 1 or 0) + ("schema" in spec['payload'] and 1 or 0)) != 1:
            raise InvalidStingerStructure(
                f"Signal specification must have 'args' xor 'schema': {spec}"
            )
        if "args" in spec['payload']:
            arg_list = []
            for k, v in spec['payload']["args"].items():
                new_arg = Arg.new_from_stinger(name=k, stinger=v)
                arg_list.append(new_arg)
            signal.set_arg_list(arg_list)
            return signal
        elif "schema" in spec['payload']:
            return signal.set_schema(spec['payload']["schema"])

class InterfaceEnum:
    def __init__(self, name: str):
        self._name = name
        self._values = []
    
    def add_value(self, name):
        self._values = name

    @property
    def values(self):
        return self._values
    
    @classmethod
    def new_from_stinger(cls, name, values: List[Dict[str, str]]) -> InterfaceEnum:
        ie = cls(name)
        for enum_obj in values:
            if 'name' in enum_obj:
                ie.add_value(enum_obj['name'])
            else:
                raise InvalidSchemaStructure("InterfaceEnum item must have a name")
        return ie


class StingerSpec:
    def __init__(self, topic_creator: InterfaceTopicCreator, interface):
        self._topic_creator = topic_creator
        try:
            self._name = interface["name"]
            self._version = interface["version"]
        except KeyError as e:
            raise InvalidStingerStructure(f"Missing interface property in {interface}: {e}")
        except TypeError:
            raise InvalidStingerStructure(
                f"Interface didn't appear to have a correct type"
            )
        self.signals = {}
        self.params = {}

    def add_signal(self, signal: Signal):
        assert signal is not None
        self.signals[signal.name] = signal

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @classmethod
    def new_from_stinger(cls, topic_creator, stinger: Dict) -> StingerSpec:
        if "stingeripc" not in stinger:
            raise InvalidStingerStructure("Missing 'stingeripc' format version")
        if 'version' not in stinger["stingeripc"]:
            raise InvalidStingerStructure("Stinger spec version not present")
        if stinger['stingeripc']['version'] not in ["0.0.3"]:
            raise InvalidStingerStructure(f"Unsupported stinger spec version {stinger['stingeripc']['version']}")

        stinger_spec = StingerSpec(topic_creator, stinger["interface"])

        try:
            if "signals" in stinger:
                for signal_name, signal_spec in stinger["signals"].items():
                    signal = Signal.new_from_stinger(
                        topic_creator.signal_topic_creator(),
                        signal_name,
                        signal_spec,
                    )
                    assert signal is not None, f"Did not create signal from {signal_name} and {signal_spec}"
                    stinger_spec.add_signal(signal)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Signal specification appears to be invalid: {e}"
            )

        return stinger_spec
