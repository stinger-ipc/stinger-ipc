from stingeripc.exceptions import InvalidStingerStructure
from stingeripc.lang_symb import ISymbolsProvider, ModelSymbols
from stingeripc.args import ArgPrimitiveType
from jacobsjinjatoo import stringmanip


class ProtocolBufferSymbolsProvider(ISymbolsProvider):
    """Plugin that provides protocol buffer symbols for model objects.

    Registers as the ``pb`` language domain so templates can access protobuf
    names/types via ``obj.pb.<property>``.
    """

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "ArgArray":
            return ProtocolBufferArgArraySymbols(model)
        elif model_class_name == "ArgPrimitive":
            return ProtocolBufferArgPrimitiveSymbols(model)
        elif model_class_name == "ArgEnum":
            return ProtocolBufferArgEnumSymbols(model)
        elif model_class_name == "ArgStruct":
            return ProtocolBufferArgStructSymbols(model)
        elif model_class_name == "InterfaceEnum":
            return ProtocolBufferEnumSymbols(model)
        elif model_class_name == "InterfaceStruct":
            return ProtocolBufferStructSymbols(model)
        elif model_class_name == "ArgDateTime":
            return ProtocolBufferArgFitsInStringSymbols(model)
        elif model_class_name == "ArgDuration":
            return ProtocolBufferArgFitsInStringSymbols(model)
        elif model_class_name == "ArgBinary":
            return ProtocolBufferArgFitsInStringSymbols(model)
        return None


class ProtocolBufferEnumSymbols(ModelSymbols):
    """Protocol buffer symbols for an :class:`InterfaceEnum`."""

    @property
    def message_name(self) -> str:
        """The proto message name for the enum."""
        return stringmanip.upper_camel_case(self._model.name)


class ProtocolBufferStructSymbols(ModelSymbols):
    """Protocol buffer symbols for an :class:`InterfaceStruct`."""

    @property
    def message_name(self) -> str:
        """The proto message name for the struct."""
        return stringmanip.upper_camel_case(self._model.name)


class ProtocolBufferArgArraySymbols(ModelSymbols):
    """Protocol buffer symbols for an :class:`ArgArray`."""

    @property
    def item_type(self) -> str:
        """The proto data type of the array's element."""
        return self._model.element.pb.data_type


class ProtocolBufferArgPrimitiveSymbols(ModelSymbols):
    """Protocol buffer symbols for an :class:`ArgPrimitive`."""

    @property
    def data_type(self) -> str:
        """The proto scalar type for the primitive (e.g. ``int32``)."""
        if self._model.type == ArgPrimitiveType.BOOLEAN:
            return "bool"
        elif self._model.type == ArgPrimitiveType.INTEGER:
            return "int32"
        elif self._model.type == ArgPrimitiveType.FLOAT:
            return "float"
        elif self._model.type == ArgPrimitiveType.STRING:
            return "string"
        raise InvalidStingerStructure("Unhandled arg type")


class ProtocolBufferArgEnumSymbols(ModelSymbols):
    """Protocol buffer symbols for an :class:`ArgEnum`."""

    @property
    def data_type(self) -> str:
        """The proto message name of the referenced enum."""
        return self._model.enum.pb.message_name


class ProtocolBufferArgStructSymbols(ModelSymbols):
    """Protocol buffer symbols for an :class:`ArgStruct`."""

    @property
    def data_type(self) -> str:
        """The proto message name of the referenced struct."""
        return self._model.struct.pb.message_name


class ProtocolBufferArgFitsInStringSymbols(ModelSymbols):
    """Protocol buffer symbols for args represented as proto strings.

    Datetime, duration, and binary arguments are all serialized as strings in
    the proto schema.
    """

    @property
    def data_type(self) -> str:
        """The proto type string for these arguments (always ``string``)."""
        return "string"
