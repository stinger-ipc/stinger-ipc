import re
import keyword
from typing import Any

from jacobsjinjatoo import stringmanip

from stingeripc.args import ArgPrimitiveType
from stingeripc.config import StingerConfig
from stingeripc.exceptions import ProtobufError
from stingeripc.lang_symb import ISymbolsProvider


class PythonSymbolsProvider(ISymbolsProvider):
    """Plugin that provides Python symbols for model objects.

    Registers as the ``python`` language domain so templates can access Python
    names and types via ``obj.python.<property>``.
    """

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "ProtobufMessageRef":
            return PythonProtobufRefSymbols(model, self.config)
        elif model_class_name == "ProtobufField":
            return PythonProtobufFieldSymbols(model, self.config)
        elif model_class_name == "Payload":
            return PythonPayloadSymbols(model, self.config)
        elif model_class_name == "StingerSpec":
            return PythonInterfaceSymbols(model, self.config)
        elif model_class_name == "InterfaceStruct":
            return PythonStructSymbols(model, self.config)
        elif model_class_name == "InterfaceEnum":
            return PythonEnumSymbols(model)
        elif model_class_name == "IpcMethod":
            return PythonMethodSymbols(model, self.config)
        elif model_class_name == "IpcCommand":
            return PythonCommandSymbols(model, self.config)
        elif model_class_name == "IpcProperty":
            return PythonPropertySymbols(model, self.config)
        elif model_class_name == "ArgEnum":
            return PythonArgEnumSymbols(model)
        elif model_class_name == "ArgPrimitive":
            return PythonArgPrimitiveSymbols(model)
        elif model_class_name == "ArgStruct":
            return PythonArgStructSymbols(model)
        elif model_class_name == "ArgDateTime":
            return PythonArgDateTimeSymbols(model)
        elif model_class_name == "ArgDuration":
            return PythonArgDurationSymbols(model)
        elif model_class_name == "ArgBinary":
            return PythonArgBinarySymbols(model)
        elif model_class_name == "ArgArray":
            return PythonArgArraySymbols(model)
        elif model_class_name == "InterfaceConstant":
            return PythonConstantSymbols(model)
        return None


class PythonSymbols:
    """Base class for Python symbol providers.

    Holds the generation ``config`` (used to derive package names and
    suffixes) and exposes shared properties such as the type-definition module
    name.
    """

    def __init__(self, config: StingerConfig | None = None):
        self.config = config

    @property
    def type_definition_module(self) -> str:
        """Name of the module that defines the interface's data types."""
        return "interface_types"


class PythonInterfaceSymbols(PythonSymbols):
    """Python symbols for the top-level :class:`StingerSpec` (the interface)."""

    def __init__(self, interface, config: StingerConfig | None = None):
        super().__init__(config)
        self._iface = interface

    @property
    def package_directory(self) -> str:
        """Name of the generated Python package directory."""
        s = f"{stringmanip.lower_only(self._iface.name).lower()}{stringmanip.lower_only(self.config.python.package_suffix) or 'ipc'}"  # type: ignore[union-attr]
        return s

    @property
    def package_name(self):
        """Distribution name of the generated Python package."""
        s = f"{stringmanip.hyphen_case(self._iface.name).lower()}-{stringmanip.hyphen_case(self.config.python.package_suffix) or 'ipc'}"  # type: ignore[union-attr]
        return s

    @property
    def module_name(self) -> str:
        """Importable module name of the generated package (same as ``package_directory``)."""
        return self.package_directory

    @property
    def client_class_name(self) -> str:
        """Name of the python class for the interface client."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Client"

    @property
    def server_class_name(self) -> str:
        """Name of the python class for the interface server."""
        return f"{stringmanip.upper_camel_case(self._iface.name)}Server"


class PythonStructSymbols(PythonSymbols):
    """Python symbols for an :class:`InterfaceStruct`."""

    def __init__(self, iface_struct, config: StingerConfig | None = None):
        super().__init__(config)
        self._iface_struct = iface_struct

    @property
    def type(self) -> str:
        """Fully-qualified Python type name for the struct."""
        return stringmanip.upper_camel_case(self._iface_struct.name)

    @property
    def local_type(self) -> str:
        """Unqualified Python class name for the struct."""
        return stringmanip.upper_camel_case(self._iface_struct.name)


class PythonEnumSymbols(PythonSymbols):
    """Python symbols for an :class:`InterfaceEnum`."""

    def __init__(self, enum):
        super().__init__()
        self._enum = enum

    @property
    def type(self) -> str:
        """Fully-qualified Python type name for the enum."""
        return stringmanip.upper_camel_case(self._enum.name)

    @property
    def local_type(self) -> str:
        """Unqualified Python class name for the enum."""
        return stringmanip.upper_camel_case(self._enum.name)


class PythonArgSymbols(PythonSymbols):
    """Base Python symbols for Arg objects."""

    def __init__(self, arg):
        super().__init__()
        self._arg = arg

    @property
    def param_name(self) -> str:
        """Name of the generated parameter that carries this argument.

        Spelled the same way for a JSON argument and for a protobuf field, so a
        template that documents or forwards "whatever a payload's parameters are"
        needs only the one attribute whichever encoding the payload uses.
        """
        return stringmanip.snake_case(self._arg.name)

    @property
    def type(self) -> str:
        """Python type name for this argument."""
        return self._arg.name

    @property
    def class_name(self) -> str:
        """Python class name for this argument's type."""
        return self.type

    @property
    def local_type(self) -> str:
        """Unqualified Python type name for this argument."""
        return self.type.split(".")[-1]

    @property
    def annotation(self) -> str:
        """Python type annotation for this argument."""
        return self.class_name


class PythonArgEnumSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgEnum`."""

    @property
    def type(self) -> str:
        """Python type name of the referenced enum."""
        return self._arg.enum.python.type

    @property
    def local_type(self) -> str:
        """Unqualified Python type name of the referenced enum."""
        return self._arg.enum.python.local_type

    @property
    def class_name(self) -> str:
        """Python class name of the referenced enum."""
        return self._arg.enum.python.type

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return f"Optional[{self._arg.enum.python.type}]"
        return self._arg.enum.python.type


class PythonArgPrimitiveSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgPrimitive`."""

    @property
    def type(self) -> str:
        """Python type name for the primitive (e.g. ``int``)."""
        return ArgPrimitiveType.to_python_type(self._arg.primitive_type)

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        return ArgPrimitiveType.to_python_type(self._arg.primitive_type, optional=self._arg.optional)


class PythonArgStructSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgStruct`."""

    @property
    def type(self) -> str:
        """Python type name of the referenced struct."""
        return self._arg.interface_struct.python.local_type

    @property
    def local_type(self) -> str:
        """Unqualified Python type name of the referenced struct."""
        return self._arg.interface_struct.python.local_type

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return f"Optional[{self.type}]"
        return self.type


class PythonArgDateTimeSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgDateTime`."""

    @property
    def type(self) -> str:
        """Python type name for datetimes (``datetime``)."""
        return "datetime"

    @property
    def local_type(self) -> str:
        """Unqualified Python type name for datetimes (``datetime``)."""
        return "datetime"

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return "Optional[datetime]"
        return "datetime"


class PythonArgDurationSymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgDuration`."""

    @property
    def type(self) -> str:
        """Python type name for durations (``timedelta``)."""
        return "timedelta"

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return "Optional[timedelta]"
        return "timedelta"


class PythonArgBinarySymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgBinary`."""

    @property
    def type(self) -> str:
        """Python type name for binary data (``bytes``)."""
        return "bytes"

    @property
    def annotation(self) -> str:
        """Python type annotation, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return f"Optional[{self.type}]"
        return self.type


class PythonArgArraySymbols(PythonArgSymbols):
    """Python symbols for an :class:`ArgArray`."""

    @property
    def type(self) -> str:
        """Python type name for arrays (``list``)."""
        return "list"

    @property
    def annotation(self) -> str:
        """Python type annotation of the element list, wrapped in ``Optional`` when the arg is optional."""
        if self._arg.optional:
            return f"Optional[List[{self._arg.element.python.annotation}]]"
        return f"List[{self._arg.element.python.annotation}]"


class PythonConstantSymbols(PythonSymbols):
    """Python symbols for an :class:`InterfaceConstant`."""

    def __init__(self, constant):
        super().__init__()
        self._constant = constant

    @property
    def type(self) -> str:
        """Python type name for the constant's declared type."""
        type_map = {
            "integer": "int",
            "float": "float",
            "boolean": "bool",
            "string": "str",
        }
        return type_map.get(self._constant.constant_type, "str")

    @property
    def local_type(self) -> str:
        """Unqualified Python type name for the constant."""
        return self.type


class PythonMethodSymbols(PythonSymbols):
    """Python symbols for an :class:`IpcMethod`."""

    def __init__(self, method, config: StingerConfig | None = None):
        super().__init__(config)
        self._method = method

    @property
    def return_value_annotation(self) -> str:
        """Python return type annotation for the method's return value.

        A protobuf method has no single named return value to annotate: its
        response *is* the message, so that is what a handler returns and what
        the caller's future resolves to.
        """
        if self._method.response_payload.is_protobuf:
            return self._method.response_payload.python.class_name
        if self._method.return_value is None:
            return "None"
        return self._method.return_value.python.annotation

    @property
    def response_class_name(self) -> str:
        """Python class name of the generated method response payload."""
        return self._method.response_payload.python.class_name

    @property
    def request_class_name(self) -> str:
        """Python class name of the generated method request payload."""
        return self._method.request_payload.python.class_name


class PythonCommandSymbols(PythonSymbols):
    """Python symbols for an :class:`IpcCommand`."""

    def __init__(self, command, config: StingerConfig | None = None):
        super().__init__(config)
        self._command = command

    @property
    def payload_class_name(self) -> str:
        """Python class name of the generated command payload."""
        return self._command.payload.python.class_name

    @property
    def callback_type_name(self) -> str:
        """Name of the callback type alias for handlers of this command."""
        return f"{stringmanip.upper_camel_case(self._command.name)}CommandCallbackType"


class PythonPropertySymbols(PythonSymbols):
    """Python symbols for an :class:`IpcProperty`."""

    def __init__(self, prop, config: StingerConfig | None = None):
        super().__init__(config)
        self._prop = prop

    @property
    def is_protobuf(self) -> bool:
        """True when the property holds a protobuf message rather than a JSON value."""
        return self._prop.payload.is_protobuf

    @property
    def class_name(self) -> str:
        """Python class name for the property's value type.

        A protobuf property's value is the message itself: there is no wrapper
        model with a single named field, so the value type and the payload type
        are the same thing.
        """
        if self.is_protobuf:
            return self._prop.payload.python.class_name
        return self._prop.value.python.class_name

    @property
    def type(self) -> str:
        """Python type name for the property's value."""
        return self.class_name

    @property
    def local_type(self) -> str:
        """Unqualified Python type name for the property's value.

        A protobuf message has no unqualified name in a generated module's scope:
        it is only ever reached through its ``_pb2`` module, so the qualified name
        is the local one.
        """
        if self.is_protobuf:
            return self.class_name
        return self.class_name.split(".")[-1]

    @property
    def annotation(self) -> str:
        """Python type annotation for the property's value."""
        if self.is_protobuf:
            return self._prop.payload.python.class_name
        return self._prop.value.python.annotation

    @property
    def getter_value_annotation(self) -> str:
        """Python type annotation used by the property getter."""
        return self.annotation

    @property
    def setter_value_annotation(self) -> str:
        """Python type annotation used by the property setter.

        A JSON property accepts either the bare value or the model wrapping it; a
        protobuf property has only the one form, so the union would be redundant.
        """
        if self.is_protobuf:
            return self.annotation
        return f"Union[{self.annotation}, {self.model_class_name}]"

    @property
    def model_class_name(self) -> str:
        """Python class name of the generated property model."""
        return self._prop.payload.python.class_name

    @property
    def is_optional(self) -> bool:
        """True when the property's value may be absent.

        A protobuf message is never optional in this sense: an unset message is
        still a message, with its fields at their defaults.
        """
        if self.is_protobuf:
            return False
        return bool(self._prop.value.optional)

    @property
    def value_param_name(self) -> str:
        """Name of the parameter a setter takes for this property's value.

        A JSON property names it after its single value; a protobuf property has
        no field name to borrow, so it is simply the message.
        """
        if self.is_protobuf:
            return "value"
        return stringmanip.snake_case(self._prop.value.name)


# The name of the generated class for each kind of payload.  These reproduce
# exactly the names the templates used to spell inline, so that routing them through
# the payload changes no generated output.
_PYTHON_PAYLOAD_NAMES = {
    "SIGNAL": lambda name: f"{stringmanip.upper_camel_case(name)}SignalPayload",
    "COMMAND": lambda name: f"{stringmanip.upper_camel_case(name)}CommandPayload",
    "METHOD_REQUEST": lambda name: f"{stringmanip.upper_camel_case(name)}MethodRequest",
    "METHOD_RESPONSE": lambda name: f"{stringmanip.upper_camel_case(name)}MethodResponse",
    "PROPERTY": lambda name: f"{stringmanip.upper_camel_case(name)}Property",
}


class PythonPayloadSymbols(PythonSymbols):
    """Python symbols for a :class:`Payload`."""

    def __init__(self, payload, config: StingerConfig | None = None):
        super().__init__(config)
        self._payload = payload

    @property
    def class_name(self) -> str:
        """Python name of the type that carries this payload."""
        if self._payload.is_protobuf:
            return self._payload.protobuf.python.qualified_name
        return _PYTHON_PAYLOAD_NAMES[self._payload.role.name](self._payload.owner_name)

    @property
    def struct_name(self) -> str:
        """Alias for :attr:`class_name`, so templates can use one spelling across languages."""
        return self.class_name

    @property
    def params(self) -> list:
        """What the generated API takes, or hands over, for this payload.

        A JSON payload spreads into its declared arguments; a protobuf payload
        spreads into the fields of its message, ordered so that the ones a caller
        may leave out come last.  Either way the entries answer to
        ``param_name`` and ``annotation``, so a template writes the parameter
        list once.
        """
        if self._payload.is_protobuf:
            return self._payload.protobuf.param_fields
        return self._payload.args

    @property
    def example_params(self) -> list:
        """The parameters an example call fills in, in :attr:`params` order.

        At most one member of any real ``oneof`` is offered: setting a second
        would silently clear the first, so an example that passed both would not
        round-trip.  A proto3 ``optional`` field is exempt -- its one-member
        oneof is protobuf's own bookkeeping rather than a choice the .proto file
        declared -- and a JSON payload has no such grouping at all.
        """
        if not self._payload.is_protobuf:
            return self._payload.args
        chosen: list = []
        claimed_oneofs: set = set()
        for field in self._payload.protobuf.param_fields:
            if field.oneof_name is not None:
                if field.oneof_name in claimed_oneofs:
                    continue
                claimed_oneofs.add(field.oneof_name)
            chosen.append(field)
        return chosen


class PythonProtobufRefSymbols(PythonSymbols):
    """Python symbols for a :class:`ProtobufMessageRef`."""

    def __init__(self, ref, config: StingerConfig | None = None):
        super().__init__(config)
        self._ref = ref

    @property
    def module(self) -> str:
        """Name of the protoc-generated module that defines this message.

        protoc names the module after the .proto *file*, not the protobuf package,
        so this needs the reference to have been resolved against the sources.
        """
        stem = self._ref.proto_file.rsplit("/", 1)[-1]
        if stem.endswith(".proto"):
            stem = stem[: -len(".proto")]
        # protoc turns characters invalid in a module name into underscores.
        stem = re.sub(r"\W", "_", stem)
        return f"{stem}_pb2"

    @property
    def import_statement(self) -> str:
        """The import that brings this message's module into a generated module.

        A well-known type comes from the installed protobuf runtime; everything
        else from the bindings protoc wrote beside the generated package.
        """
        package = "google.protobuf" if self._ref.is_well_known else ".proto"
        return f"from {package} import {self.module}"

    @property
    def qualified_name(self) -> str:
        """How generated Python code names this message, e.g. ``weather_pb2.CurrentConditions``.

        protoc nests a nested message's class inside its parent's, so the path
        from the module down through every enclosing message is what names it.
        """
        return f"{self.module}.{self._ref.scoped_name}"


# The Python type each protobuf scalar kind maps to.  protoc's generated classes
# accept and hand back exactly these, so a per-field API that spells anything else
# would not type-check against the message it builds.
_PYTHON_FIELD_TYPES = {
    "double": "float",
    "float": "float",
    "int32": "int",
    "int64": "int",
    "uint32": "int",
    "uint64": "int",
    "sint32": "int",
    "sint64": "int",
    "fixed32": "int",
    "fixed64": "int",
    "sfixed32": "int",
    "sfixed64": "int",
    "bool": "bool",
    "string": "str",
    "bytes": "bytes",
    # protoc's Python runtime represents an enum value as a plain int, and the
    # generated module exposes the names as module-level constants rather than as
    # a type a signature could name.
    "enum": "int",
}


class PythonProtobufFieldSymbols(PythonSymbols):
    """Python symbols for one field of a protobuf message.

    These are what turns a protobuf payload into the same kind of per-field API a
    JSON payload has always had: the parameter a generated function takes for the
    field, the constructor keyword that puts it back on the message, and the
    expression that reads it off again.
    """

    def __init__(self, field, config: StingerConfig | None = None):
        super().__init__(config)
        self._field = field

    @property
    def param_name(self) -> str:
        """Name of the generated parameter that carries this field.

        The proto field name itself, because protoc's constructor takes the field
        names as keywords and a renamed parameter would have to be translated back
        at every call site.  A name Python reserves gets a trailing underscore,
        which is the only case where the two differ.
        """
        name = self._field.name
        if keyword.iskeyword(name) or name == "self":
            return f"{name}_"
        return name

    @property
    def base_type(self) -> str:
        """The Python type of one value of this field, ignoring repetition.

        A group is proto2's abandoned nesting syntax; protoc still parses it but
        no supported generator models it, so a field that uses one is rejected
        here rather than mis-generated.
        """
        if self._field.kind == "group":
            raise ProtobufError(f"Protobuf field '{self._field.name}' uses a 'group', which stinger does not support; use a nested message instead.")
        if self._field.is_message or self._field.is_enum:
            # protoc's stubs type an enum field as the enum, not as a plain int, and
            # reject an int where one is expected -- so the generated annotation has
            # to name it too, or the generated code fails its own type check.
            return self._field.type_ref.python.qualified_name
        return _PYTHON_FIELD_TYPES[self._field.kind]

    @property
    def annotation(self) -> str:
        """Python type annotation for this field's parameter.

        A map becomes a ``Dict``, a repeated field a ``List`` and a field a caller
        may leave unset an ``Optional`` -- the ``typing`` spellings rather than the
        builtin generics, since the generated package still supports Python 3.7.
        """
        if self._field.is_map:
            return f"Dict[{self._field.map_key.python.annotation}, {self._field.map_value.python.annotation}]"
        if self._field.repeated:
            return f"List[{self.base_type}]"
        if self._field.is_optional_param:
            return f"Optional[{self.base_type}]"
        return self.base_type

    @property
    def ctor_kwarg(self) -> str:
        """This field's contribution to a protobuf message constructor call.

        A field whose parameter had to be renamed cannot be passed as a keyword at
        all -- ``Msg(from=x)`` does not parse -- so it goes through a mapping
        unpacking instead.  Passing ``None`` is how a field is left unset: the
        protobuf runtime treats a ``None`` keyword as "not given", for repeated and
        map fields as much as for singular ones, so an optional parameter needs no
        guard around it.
        """
        name = self._field.name
        if self.param_name != name:
            return f'**{{"{name}": {self.param_name}}}'
        return f"{name}={self.param_name}"

    def read_expr(self, obj_expr: str) -> str:
        """Expression reading this field back off the message ``obj_expr``.

        A repeated or map field is copied out of its protobuf container into a
        plain ``list``/``dict``, so a handler is given an ordinary Python value it
        can keep after the message goes away.  A field with explicit presence
        reports ``None`` when it is unset, which is the difference between "not
        given" and "given as the default" that its ``Optional`` parameter promises.
        """
        name = self._field.name
        access = f'getattr({obj_expr}, "{name}")' if self.param_name != name else f"{obj_expr}.{name}"
        if self._field.is_map:
            return f"dict({access})"
        if self._field.repeated:
            return f"list({access})"
        if self._field.is_optional_param:
            return f'{access} if {obj_expr}.HasField("{name}") else None'
        return access

    def example_value(self, seed: int = 2) -> str:
        """An example value for this field, as a Python literal.

        Only a scalar has an example that can be made up from the descriptor
        alone; anything else gets its empty value, which is still a value the
        generated parameter accepts.
        """
        if self._field.is_map:
            return "{}"
        if self._field.repeated:
            return "[]"
        if self._field.is_message:
            return f"{self.base_type}()"
        if self._field.is_enum:
            # The wrapper object protoc generates for an enum is not callable, so an
            # example names one of the enum's own values rather than casting a number.
            values = self._field.type_ref.enum_values
            return f"{self.base_type}.{values[0]}" if values else "0"
        return self._field.get_random_example_value(lang="python", seed=seed)
