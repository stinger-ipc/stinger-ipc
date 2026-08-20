from stingeripc.lang_symb import ISymbolsProvider


class MarkdownSymbolsProvider(ISymbolsProvider):
    """Plugin that provides markdown symbols for model objects.

    Registers as the ``markdown`` language domain so templates can access
    markdown-rendered types via ``obj.markdown.<property>``.
    """

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
        """Resolve the markdown type string for an argument, with sensible fallbacks.

        Prefers the argument's ``markdown`` symbol provider, then its
        ``arg_type`` name, and finally ``UNKNOWN``.
        """
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
    """Markdown symbols for an :class:`ArgEnum`."""

    @property
    def markdown_type(self) -> str:
        """Markdown link to the enum's documentation section."""
        return f"[Enum {self._arg.enum.class_name}](#enum-{self._arg.enum.class_name})"


class MarkdownArgStructSymbols(MarkdownArgSymbols):
    """Markdown symbols for an :class:`ArgStruct`."""

    @property
    def markdown_type(self) -> str:
        """Markdown link to the struct's documentation section."""
        return f"[Struct {self._arg.interface_struct.class_name}](#enum-{self._arg.interface_struct.class_name})"


class MarkdownArgDateTimeSymbols(MarkdownArgSymbols):
    """Markdown symbols for an :class:`ArgDateTime`."""

    @property
    def markdown_type(self) -> str:
        """Markdown link to the datetime documentation section."""
        return "[DateTime](#datetime)"


class MarkdownArgDurationSymbols(MarkdownArgSymbols):
    """Markdown symbols for an :class:`ArgDuration`."""

    @property
    def markdown_type(self) -> str:
        """Markdown link to the duration documentation section."""
        return "[Duration](#duration)"


class MarkdownArgBinarySymbols(MarkdownArgSymbols):
    """Markdown symbols for an :class:`ArgBinary`."""

    @property
    def markdown_type(self) -> str:
        """Markdown link to the binary documentation section."""
        return "[Binary](#binary)"


class MarkdownArgArraySymbols(MarkdownArgSymbols):
    """Markdown symbols for an :class:`ArgArray`."""

    @property
    def markdown_type(self) -> str:
        """Markdown description of the array, including its element type."""
        return f"Array of {self._type_for(self._arg.element)}"
