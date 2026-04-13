from stingeripc.lang_symb import ISymbolsProvider


class MarkdownSymbolsProvider(ISymbolsProvider):

    def for_model(self, model_class_name: str, model) -> object | None:
        if model_class_name == "Arg":
            return MarkdownArgSymbols(model)
        elif model_class_name == "ArgPrimitive":
            return MarkdownArgSymbols(model)
        elif model_class_name == "ArgEnum":
            return MarkdownArgEnumSymbols(model)
        elif model_class_name == "ArgStruct":
            return MarkdownArgStructSymbols(model)
        elif model_class_name == "ArgDateTime":
            return MarkdownArgDateTimeSymbols(model)
        elif model_class_name == "ArgDuration":
            return MarkdownArgDurationSymbols(model)
        elif model_class_name == "ArgBinary":
            return MarkdownArgBinarySymbols(model)
        elif model_class_name == "ArgArray":
            return MarkdownArgArraySymbols(model)
        return None


class MarkdownArgSymbols:
    """Base markdown symbols for Arg objects."""

    def __init__(self, arg):
        self._arg = arg

    @staticmethod
    def _type_for(arg) -> str:
        if hasattr(arg, "markdown") and hasattr(arg.markdown, "markdown_type"):
            return arg.markdown.markdown_type
        if hasattr(arg, "arg_type"):
            return arg.arg_type.name
        return "UNKNOWN"

    @property
    def markdown_type(self) -> str:
        """Default markdown representation for an Arg.

        Subclasses may override this to provide richer markdown links.
        """
        return self._arg.arg_type.name


class MarkdownArgEnumSymbols(MarkdownArgSymbols):

    @property
    def markdown_type(self) -> str:
        return f"[Enum {self._arg.enum.class_name}](#enum-{self._arg.enum.class_name})"


class MarkdownArgStructSymbols(MarkdownArgSymbols):

    @property
    def markdown_type(self) -> str:
        return f"[Struct {self._arg.interface_struct.class_name}](#enum-{self._arg.interface_struct.class_name})"


class MarkdownArgDateTimeSymbols(MarkdownArgSymbols):

    @property
    def markdown_type(self) -> str:
        return "[DateTime](#datetime)"


class MarkdownArgDurationSymbols(MarkdownArgSymbols):

    @property
    def markdown_type(self) -> str:
        return "[Duration](#duration)"


class MarkdownArgBinarySymbols(MarkdownArgSymbols):

    @property
    def markdown_type(self) -> str:
        return "[Binary](#binary)"


class MarkdownArgArraySymbols(MarkdownArgSymbols):

    @property
    def markdown_type(self) -> str:
        return f"Array of {self._type_for(self._arg.element)}"
