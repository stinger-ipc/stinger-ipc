from __future__ import annotations
from enum import Enum
import random
import stringcase
from abc import abstractmethod
from typing import Dict, List, Optional, Any, Union
from .topic import SignalTopicCreator, InterfaceTopicCreator, MethodTopicCreator
from .args import ArgType, ArgValueType
from .exceptions import InvalidStingerStructure
from jacobsjinjatoo import stringmanip


class Arg:
    def __init__(self, name: str, description: Optional[str] = None):
        self._name = name
        self._description = description
        self._default_value = None
        self._type: ArgType = ArgType.UNKNOWN

    def set_description(self, description: str) -> Arg:
        self._description = description
        return self

    @property
    def name(self) -> str:
        return self._name

    @property
    def arg_type(self) -> ArgType:
        return self._type

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def python_type(self) -> str:
        return self.name

    @property
    def python_local_type(self) -> str:
        return self.python_type.split('.')[-1]

    @property
    def rust_type(self) -> str:
        return self.name

    @property
    def rust_local_type(self) -> str:
        return self.rust_type

    @classmethod
    def new_arg_from_stinger(cls, arg_spec: Dict[str, str], stinger_spec: Optional[StingerSpec]=None) -> Arg:
        if "type" not in arg_spec:
            raise InvalidStingerStructure("No 'type' in arg structure")
        if "name" not in arg_spec:
            raise InvalidStingerStructure("No 'name' in arg structure")

        if hasattr(ArgValueType, arg_spec["type"].upper()):
            arg = ArgValue.new_arg_value_from_stinger(arg_spec)
            return arg
        else:
            if stinger_spec is None:
                raise RuntimeError("Need the root StingerSpec when creating an enum or schema Arg")

        if arg_spec["type"] == 'enum':
            if "enumName" not in arg_spec:
                raise InvalidStingerStructure("Enum args need a 'enumName'")
            if arg_spec["enumName"] not in stinger_spec.enums:
                raise InvalidStingerStructure(f"Enum arg '{arg_spec['enumName']}' was not found in the list of stinger spec enums")
            arg = ArgEnum(arg_spec["name"], stinger_spec.enums[arg_spec['enumName']])
            return arg
        raise RuntimeError("unknown arg type: {arg_spec['type']}")

    @abstractmethod
    def get_random_example_value(self, lang="python"):
        ...

class ArgEnum(Arg):
    def __init__(self, name: str, enum: InterfaceEnum, description: Optional[str] = None):
        super().__init__(name, description)
        self._enum = enum
        self._type = ArgType.ENUM

    @property
    def enum(self) -> InterfaceEnum:
        return self._enum

    @property
    def python_type(self) -> str:
        return self._enum.python_type

    @property
    def cpp_type(self) -> str:
        return self._enum.cpp_type

    @property
    def rust_type(self) -> str:
        return self._enum.rust_type

    @property
    def rust_local_type(self) -> str:
        return self._enum.rust_local_type

    @property
    def cpp_temp_type(self) -> str:
        return self.cpp_type

    @property
    def cpp_rapidjson_type(self) -> str:
        return ArgValueType.to_cpp_rapidjson_type_str(ArgValueType.INTEGER)

    @property
    def markdown_type(self) -> str:
        return f"[Enum {self._enum.class_name}](#enum-{self._enum.class_name})"

    def get_random_example_value(self, lang="python") -> str:
        random_state = random.getstate()
        random.seed(1)
        value = random.choice(self._enum.values) 
        if lang == "python":
            retval = f"{self._enum.get_module_alias()}.{self._enum.class_name}.{stringcase.constcase(value) }"
        elif lang == "c++":
            retval = f"{self._enum.class_name}::{stringcase.constcase(value)}"
        elif lang == "rust":
            retval = f"connection::payloads::{self._enum.class_name}::{value}"
        random.setstate(random_state)
        return retval

    def __repr__(self) -> str:
        return f"<ArgEnum name={self._name}>"


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
    def rust_type(self) -> str:
        return ArgValueType.to_rust_type(self._arg_type)

    @property
    def cpp_type(self) -> str:
        return ArgValueType.to_cpp_type(self._arg_type)

    @property
    def cpp_temp_type(self) -> str:
        if self._arg_type == ArgValueType.STRING:
            return "std::string"
        else:
            return self.cpp_type
            
    @property
    def json_type(self) -> str:
        return ArgValueType.to_json_type(self._arg_type)

    @property
    def cpp_rapidjson_type(self) -> str:
        return ArgValueType.to_cpp_rapidjson_type_str(self._arg_type)

    def get_random_example_value(self, lang="python") -> str|float|int|bool|None:
        random_state = random.getstate()
        random.seed(2)
        retval: str|float|int|bool|None = None
        if self._arg_type == ArgValueType.BOOLEAN:
            retval = random.choice([True, False])
            if lang != "python":
                retval = str(retval).lower()
        elif self._arg_type == ArgValueType.FLOAT:
            retval = random.choice([3.14, 1.0, 2.5, 97.9, 1.53])
        elif self._arg_type == ArgValueType.INTEGER:
            retval = random.choice([42, 1981, 2020, 2022])
        elif self._arg_type == ArgValueType.STRING:
            retval = random.choice(['"apples"', '"Joe"', '"example"', '"foo"'])
            if lang == "rust":
                retval = f"{retval}.to_string()"
        random.setstate(random_state)
        return retval

    def __repr__(self) -> str:
        return f"<ArgValue name={self._name} type={ArgValueType.to_python_type(self.type)}>"

    @classmethod
    def new_arg_value_from_stinger(cls, stinger: Dict[str, str]) -> Arg:
        if "type" not in stinger:
            raise InvalidStingerStructure("No 'type' in arg structure")
        if "name" not in stinger:
            raise InvalidStingerStructure("No 'name' in arg structure")

        arg_value_type = ArgValueType.from_string(stinger["type"])
        arg: Arg = cls(name=stinger["name"], arg_type=arg_value_type)

        if "description" in stinger and isinstance(stinger["description"], str):
            arg.set_description(stinger["description"])
        return arg


class ArgStruct(Arg):
    def __init__(self, name: str, members: Optional[List[Arg]]=None):
        super().__init__(name)
        self._members = members or []
        self._type = ArgType.STRUCT

    @property
    def members(self) -> list[Arg]:
        return self._members

    def add_member(self, member: Arg):
        self._members.append(member)

    @property
    def cpp_type(self) -> str:
        return stringcase.pascalcase(self.name)

    @property
    def python_type(self) -> str:
        return f"stinger_types.{self.python_local_type}"

    @property
    def python_local_type(self) -> str:
        return stringcase.pascalcase(self.name)

    @property
    def rust_type(self) -> str:
        return f"connection::payloads::{self.rust_local_type}"

    @property
    def rust_local_type(self) -> str:
        return stringcase.pascalcase(self.name)

    def get_random_example_value(self, lang="python") -> str|None:
        example_list: dict[str] = {a.name: str(a.get_random_example_value(lang)) for a in self.members}
        if lang == 'c++':
            return "{" + ", ".join(example_list.values()) + "}"
        elif lang == 'python':
            init_list = ", ".join([f"{k}={v}" for k, v in example_list.items()])
            return f"{self.python_type}({init_list})"
        return None


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
        if arg.name in [a.name for a in self._arg_list]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._arg_list.append(arg)
        return self

    @property
    def arg_list(self) -> list[Arg]:
        return self._arg_list

    @property
    def name(self) -> str:
        return self._name

    @property
    def topic(self) -> str:
        return self._topic_creator.signal_topic(self.name)

    @classmethod
    def new_signal_from_stinger(
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
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            signal.add_arg(new_arg)

        return signal

class Method(object):
    def __init__(self, topic_creator: MethodTopicCreator, name: str):
        self._topic_creator = topic_creator
        self._name = name
        self._arg_list = []  # type: List[Arg]
        self._return_value: Arg|None = None

    def add_arg(self, arg: Arg) -> Method:
        if arg.name in [a.name for a in self._arg_list]:
            raise InvalidStingerStructure(f"An arg named '{arg.name}' has been added.")
        self._arg_list.append(arg)
        return self

    def add_return_value(self, value: Arg) -> Method:
        if self._return_value is None:
            self._return_value = value
        elif isinstance(self._return_value, ArgStruct):
            if value.name in [a.name for a in self._return_value.members]:
                raise InvalidStingerStructure(f"A return value named '{value.name}' has been already added.")
            self._return_value.add_member(value)
        else:
            if value.name == self._return_value.name:
                raise InvalidStingerStructure(f"Attempt to add '{value.name}' to return value when it is already been added.")
            struct_return_value = ArgStruct(f"{self._name}ReturnValue", [self._return_value, value])
            self._return_value = struct_return_value

        return self

    @property
    def arg_list(self) -> list[Arg]:
        return self._arg_list

    @property
    def return_value(self) -> Arg|None:
        return self._return_value

    @property
    def name(self) -> str:
        return self._name

    @property
    def topic(self) -> str:
        return self._topic_creator.method_topic(self.name)

    def response_topic(self, client_id) -> str:
        return self._topic_creator.method_response_topic(self.name, client_id)

    @classmethod
    def new_method_from_stinger(
        cls, topic_creator: MethodTopicCreator, name: str, method_spec: Dict[str, str], stinger_spec: Optional[StingerSpec]=None
    ) -> "Method":
        """Alternative constructor from a Stinger method structure."""
        method = cls(topic_creator, name)
        if "arguments" not in method_spec:
            raise InvalidStingerStructure("Method specification must have 'arguments'")
        if not isinstance(method_spec['arguments'], list):
            raise InvalidStingerStructure(f"Arguments must be a list.  It is '{type(method_spec['arguments'])}' ")

        for arg_spec in method_spec["arguments"]:
            if 'name' not in arg_spec or 'type' not in arg_spec:
                raise InvalidStingerStructure("Arg must have name and type.")
            new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
            method.add_arg(new_arg)

        if "returnValues" in method_spec:
            if not isinstance(method_spec['returnValues'], list):
                raise InvalidStingerStructure(f"ReturnValues must be a list.")
            
            for arg_spec in method_spec["returnValues"]:
                if 'name' not in arg_spec or 'type' not in arg_spec:
                    raise InvalidStingerStructure("Return value must have name and type.")
                new_arg = Arg.new_arg_from_stinger(arg_spec, stinger_spec)
                method.add_return_value(new_arg)

        return method

class InterfaceEnum:

    def __init__(self, name: str):
        self._name = name
        self._values: list[Any] = []

    def add_value(self, value: str):
        self._values.append(value)

    @property
    def name(self):
        return self._name

    @property
    def class_name(self):
        return stringmanip.upper_camel_case(self.name)

    @staticmethod
    def get_module_name(lang="python") -> str:
        return "interface_types"

    @staticmethod
    def get_module_alias(lang="python") -> str:
        return "stinger_types"

    @property
    def python_type(self) -> str:
        return f"{self.get_module_alias()}.{stringmanip.upper_camel_case(self.name)}"

    @property
    def rust_local_type(self) -> str:
        return stringmanip.upper_camel_case(self.name)

    @property
    def rust_type(self) -> str:
        return f"connection::payloads::{self.rust_local_type}"

    @property
    def cpp_type(self) -> str:
        return stringmanip.upper_camel_case(self.name)

    @property
    def values(self):
        return self._values

    @classmethod
    def new_enum_from_stinger(cls, name, values: List[Dict[str, str]]) -> InterfaceEnum:
        ie = cls(name)
        for enum_obj in values:
            if "name" in enum_obj:
                ie.add_value(enum_obj["name"])
            else:
                raise InvalidStingerStructure("InterfaceEnum item must have a name")
        return ie

class MqttTransportProtocol(Enum):
    TCP = 0
    WEBSOCKETS = 1

class Broker:
    def __init__(self, name: str="Default"):
        self._name: str = name
        self._host: Optional[str] = None
        self._port: Optional[int] = None
        self._auth = None
        self._transport_protocol: MqttTransportProtocol = MqttTransportProtocol.TCP
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def class_name(self) -> str:
        return f"{stringcase.pascalcase(self.name)}Connection"

    @property
    def hostname(self) -> Optional[str]:
        return self._host

    @hostname.setter
    def hostname(self, value: str):
        self._host = value

    @property
    def port(self) -> Optional[int]:
        return self._port

    @port.setter
    def port(self, port: int):
        self._port = port

    @classmethod
    def new_broker_from_stinger(cls, name: str, spec: Dict[str, Any]) -> Broker:
        new_broker = cls(name=name)
        if 'host' in spec:
            new_broker.hostname = spec['host']
        if 'port' in spec:
            new_broker.port = int(spec['port'])
        return new_broker

    def __repr__(self) -> str:
        return f"<Broker name={self.name} host={self.hostname}:{self.port}>"


class StingerSpec:
    def __init__(self, topic_creator: InterfaceTopicCreator, interface):
        self._topic_creator = topic_creator
        try:
            self._name: str = interface["name"]
            self._version: str = interface["version"]
        except KeyError as e:
            raise InvalidStingerStructure(
                f"Missing interface property in {interface}: {e}"
            )
        except TypeError:
            raise InvalidStingerStructure(
                f"Interface didn't appear to have a correct type"
            )
        
        self._summary = interface['summary'] if 'summary' in interface else None
        self._title = interface['title'] if 'title' in interface else None

        self.signals: dict[str, Signal] = {}
        self.params: dict[str, Any] = {}
        self.methods: dict[str, Method] = {}
        self.enums: dict[str, InterfaceEnum] = {}
        self._brokers: dict[str, Broker] = {}

    @property
    def method_return_codes(self) -> dict[int, str]:
        return {
            0: "Success",
            1: "Client Error",
            2: "Server Error",
            3: "Transport Error",
            4: "Payload Error",
        }

    @property
    def interface_info(self) -> tuple[str, dict[str, Any]]:
        info = {
            "name": self._name, 
            "version": self._version,
            "title": self._title or self._name,
            "summary": self._summary or '',
        }
        return (
            self._topic_creator.interface_info_topic(),
            info
        )

    def add_broker(self, broker: Broker):
        assert broker is not None
        self._brokers[broker.name] = broker

    @property
    def brokers(self) -> Dict[str, Broker]:
        if len(self._brokers) == 0:
            default_broker = Broker()
            return {default_broker.name: default_broker}
        else:
            return self._brokers

    def get_example_broker(self) -> Broker|None:
        for broker in self.brokers.values():
            return broker
        return None

    def add_signal(self, signal: Signal):
        assert isinstance(signal, Signal)
        self.signals[signal.name] = signal

    def add_method(self, method: Method):
        assert isinstance(method, Method)
        self.methods[method.name] = method

    def add_enum(self, interface_enum: InterfaceEnum):
        assert interface_enum is not None
        self.enums[interface_enum.name] = interface_enum

    def uses_enums(self) -> bool:
        return bool(self.enums)

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @staticmethod
    def get_enum_module_name() -> str:
        return InterfaceEnum.get_module_name()

    @staticmethod
    def get_enum_module_alias() -> str:
        return InterfaceEnum.get_module_alias()

    @classmethod
    def new_spec_from_stinger(cls, topic_creator, stinger: Dict) -> StingerSpec:
        if "stingeripc" not in stinger:
            raise InvalidStingerStructure("Missing 'stingeripc' format version")
        if "version" not in stinger["stingeripc"]:
            raise InvalidStingerStructure("Stinger spec version not present")
        if stinger["stingeripc"]["version"] not in ["0.0.6"]:
            raise InvalidStingerStructure(
                f"Unsupported stinger spec version {stinger['stingeripc']['version']}"
            )

        stinger_spec = StingerSpec(topic_creator, stinger["interface"])

        # Enums must come before other components because other components may use enum values.
        try:
            if "enums" in stinger:
                for enum_name, enum_spec in stinger["enums"].items():
                    ie = InterfaceEnum.new_enum_from_stinger(enum_name, enum_spec)
                    assert (ie is not None), f"Did not create enum from {enum_name} and {enum_spec}"
                    stinger_spec.add_enum(ie)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Signal specification appears to be invalid: {e}"
            )

        try:
            if "brokers" in stinger:
                for broker_name, broker_spec in stinger["brokers"].items():
                    broker = Broker.new_broker_from_stinger(broker_name, broker_spec)
                    assert (broker is not None), f"Did not create broker from {broker_name} and {broker_spec}"
                    stinger_spec.add_broker(broker)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Broker specification appears to be invalid: {e}"
            )

        try:
            if "signals" in stinger:
                for signal_name, signal_spec in stinger["signals"].items():
                    signal = Signal.new_signal_from_stinger(
                        topic_creator.signal_topic_creator(),
                        signal_name,
                        signal_spec,
                        stinger_spec
                    )
                    assert (
                        signal is not None
                    ), f"Did not create signal from {signal_name} and {signal_spec}"
                    stinger_spec.add_signal(signal)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Signal specification appears to be invalid: {e}"
            )

        try:
            if "methods" in stinger:
                for method_name, method_spec in stinger["methods"].items():
                    method = Method.new_method_from_stinger(
                        topic_creator.method_topic_creator(),
                        method_name,
                        method_spec,
                        stinger_spec
                    )
                    assert (
                        method is not None
                    ), f"Did not create method from {method_name} and {method_spec}"
                    stinger_spec.add_method(method)
        except TypeError as e:
            raise InvalidStingerStructure(
                f"Method specification appears to be invalid: {e}"
            )

        return stinger_spec
