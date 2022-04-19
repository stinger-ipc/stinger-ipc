from __future__ import annotations
from enum import Enum
import random
from typing import Dict, List, Optional
from .topic import SignalTopicCreator, InterfaceTopicCreator
from jacobsjinjatoo import stringmanip

ALLOWED_ARG_TYPES = []


class InvalidStingerStructure(Exception):
    pass


class ArgType(Enum):
    UNKNOWN = 0
    VALUE = 1
    ENUM = 2
    JSON_SCHEMA = 3


class ArgValueType(Enum):
    BOOLEAN = 0
    INTEGER = 1
    FLOAT = 2
    STRING = 3

    @classmethod
    def from_string(cls, arg_type: str) -> ArgValueType:
        if hasattr(cls, arg_type.upper()):
            return getattr(cls, arg_type.upper())
        else:
            raise InvalidStingerStructure(f"No ArgType called '{arg_type}'")

    @classmethod
    def to_python_type(cls, arg_type: ArgValueType) -> str:
        if arg_type == cls.BOOLEAN:
            return "bool"
        elif arg_type == cls.INTEGER:
            return "int"
        elif arg_type == cls.FLOAT:
            return "float"
        elif arg_type == cls.STRING:
            return "str"
        raise InvalidStingerStructure("Unhandled arg type")


class Arg:
    def __init__(self, name: str, description: Optional[str] = None):
        self._name = name
        self._description = description
        self._default_value = None
        self._type = ArgType.UNKNOWN

    def set_description(self, description: str) -> Arg:
        self._description = description
        return self

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @classmethod
    def new_from_stinger(cls, arg_spec: Dict[str, str], stinger_spec: Optional[StingerSpec]=None) -> Arg:
        if "type" not in arg_spec:
            raise InvalidStingerStructure("No 'type' in arg structure")
        if "name" not in arg_spec:
            raise InvalidStingerStructure("No 'name' in arg structure")

        if hasattr(ArgValueType, arg_spec["type"].upper()):
            arg = ArgValue.new_from_stinger(arg_spec)
            return arg
        else:
            if stinger_spec is None:
                raise RuntimeError("Need the root StingerSpec when creating an enum or schema Arg")

        if arg_spec["type"] == 'enum':
            if "enumName" not in arg_spec:
                raise InvalidStingerStructure("Enum args need a 'enumName'")
            if arg_spec["enumName"] not in stinger_spec.enums:
                raise InvalidStingerStructure(f"Enum arg '{arg_spec['enumName']}' was not found in the list of stinger spec enums")
            arg = ArgEnum(arg_spec["name"], stinger_spec.enums['enumName'])
            return arg


class ArgEnum(Arg):
    def __init__(self, name: str, enum: InterfaceEnum, ArgValueType, description: Optional[str] = None):
        super().__init__(name, description)
        self._enum = enum
        self._type = ArgType.ENUM

    @property
    def python_type(self) -> str:
        return self._enum.python_type


class ArgValue(Arg):
    def __init__(self, name: str, arg_type: ArgValueType, description: Optional[str] = None):
        super().__init__(name, description)
        self._arg_type = arg_type
        self._type = ArgType.VALUE

    @property
    def type(self) -> ArgValueType:
        return self._arg_type

    @property
    def python_type(self) -> str:
        return ArgValueType.to_python_type(self._arg_type)

    @property
    def random_example_value(self) -> Union[str, float, int, bool]:
        if self._arg_type == ArgValueType.BOOLEAN:
            return random.choice([True, False])
        elif self._arg_type == ArgValueType.FLOAT:
            return random.choice([3.14, 1.0, 2.5, 97.9, 1.53])
        elif self._arg_type == ArgValueType.INTEGER:
            return random.choice([42, 1981, 2020, 2022])
        elif self._arg_type == ArgValueType.STRING:
            return random.choice(['"apples"', '"Joe"', '"example"', '"foo"'])

    def __repr__(self) -> str:
        return f"<ArgValue name={self._name} type={ArgValueType.to_python_type(self.type)}>"

    @classmethod
    def new_from_stinger(cls, stinger: Dict[str, str]) -> Arg:
        if "type" not in stinger:
            raise InvalidStingerStructure("No 'type' in arg structure")
        if "name" not in stinger:
            raise InvalidStingerStructure("No 'name' in arg structure")

        arg_value_type = ArgValueType.from_string(stinger["type"])
        arg = cls(name=stinger["name"], arg_type=arg_value_type)

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
        self._arg_list = []  # type: List[Arg]

    def add_arg(self, arg: Arg) -> Signal:
        self._arg_list.append(arg)
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
        cls, topic_creator: SignalTopicCreator, name: str, signal_spec: Dict[str, str], stinger_spec: Optional[StingerSpec]=None
    ) -> "Signal":
        """Alternative constructor from a Stinger signal structure."""
        signal = cls(topic_creator, name)
        if "payload" not in signal_spec:
            raise InvalidStingerStructure("Signal specification must have 'payload'")
        if not isinstance(signal_spec['payload'], list):
            raise InvalidStingerStructure(f"Payload must be a list.  It is '{type(signal_spec['payload'])}' ")

        for arg_spec in signal_spec["payload"]:
            if 'name' not in arg_spec or 'type' not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_from_stinger(arg_spec, stinger_spec)
            signal.add_arg(new_arg)

        return signal

class InterfaceEnum:
    def __init__(self, name: str):
        self._name = name
        self._values = []

    def add_value(self, value: str):
        print(f"Adding {value} to {self._name}")
        self._values.append(value)

    @property
    def name(self):
        return self._name

    @property
    def python_type(self) -> str:
        return f"interface_enums.{stringmanip.upper_camel_case(self.name)}"

    @property
    def values(self):
        return self._values

    @classmethod
    def new_from_stinger(cls, name, values: List[Dict[str, str]]) -> InterfaceEnum:
        ie = cls(name)
        for enum_obj in values:
            if "name" in enum_obj:
                ie.add_value(enum_obj["name"])
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
            raise InvalidStingerStructure(
                f"Missing interface property in {interface}: {e}"
            )
        except TypeError:
            raise InvalidStingerStructure(
                f"Interface didn't appear to have a correct type"
            )
        self.signals = {}
        self.params = {}
        self.enums = {}

    def add_signal(self, signal: Signal):
        assert signal is not None
        self.signals[signal.name] = signal

    def add_enum(self, interface_enum: InterfaceEnum):
        assert interface_enum is not None
        self.enums[interface_enum.name] = interface_enum

    def uses_enums(self):
        return bool(self.enums)

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
        if "version" not in stinger["stingeripc"]:
            raise InvalidStingerStructure("Stinger spec version not present")
        if stinger["stingeripc"]["version"] not in ["0.0.5"]:
            raise InvalidStingerStructure(
                f"Unsupported stinger spec version {stinger['stingeripc']['version']}"
            )

        stinger_spec = StingerSpec(topic_creator, stinger["interface"])

        # Enums must come before other components because other components may use enum values.
        try:
            if "enums" in stinger:
                for enum_name, enum_spec in stinger["enums"].items():
                    ie = InterfaceEnum.new_from_stinger(enum_name, enum_spec)
                    assert (ie is not None), f"Did not create enum from {enum_name} and {enum_spec}"
                    stinger_spec.add_enum(ie)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Signal specification appears to be invalid: {e}"
            )

        try:
            if "signals" in stinger:
                for signal_name, signal_spec in stinger["signals"].items():
                    signal = Signal.new_from_stinger(
                        topic_creator.signal_topic_creator(),
                        signal_name,
                        signal_spec,
                    )
                    assert (
                        signal is not None
                    ), f"Did not create signal from {signal_name} and {signal_spec}"
                    stinger_spec.add_signal(signal)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Signal specification appears to be invalid: {e}"
            )



        return stinger_spec
