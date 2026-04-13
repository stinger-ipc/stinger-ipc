from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from stingeripc.config import StingerConfig


class ISymbolsProvider:
    """An interface for plugins that provide language symbols for model objects.

    The plugin system discovers providers through
    `project.entry-points."stinger_symbols"`.
    """

    def __init__(self, config: "StingerConfig | None" = None):
        """The constructor takes stinger generation configuration as an argument."""
        self.config = config

    def for_model(self, model_class_name: str, model) -> object | None:
        """Return symbols for the given model class, or None if unsupported."""
        return None


class ModelSymbols:

    def __init__(self, model):
        self._model = model

