from stingeripc.exceptions import InvalidStingerStructure
from stingeripc.lang_symb import ISymbolsProvider, ModelSymbols
from stingeripc.args import ArgPrimitiveType
from jacobsjinjatoo import stringmanip

class ProtocolBufferSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name:str, model) -> object|None:
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
        return None

class ProtocolBufferEnumSymbols(ModelSymbols):

    @property
    def message_name(self) -> str:
        return stringmanip.upper_camel_case(self._model.name)

class ProtocolBufferStructSymbols(ModelSymbols):

    @property
    def message_name(self) -> str:
        return stringmanip.upper_camel_case(self._model.name)

class ProtocolBufferArgArraySymbols(ModelSymbols):

    @property
    def item_type(self) -> str:
        return self._model.element.pb.data_type
    
class ProtocolBufferArgPrimitiveSymbols(ModelSymbols):

    @property
    def data_type(self) -> str:
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

    @property
    def data_type(self) -> str:
        return self._model.enum.pb.message_name

class ProtocolBufferArgStructSymbols(ModelSymbols):

    @property
    def data_type(self) -> str:
        return self._model.struct.pb.message_name
