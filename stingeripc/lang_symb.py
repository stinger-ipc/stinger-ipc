from typing import Any, TYPE_CHECKING

from stevedore import ExtensionManager

if TYPE_CHECKING:
    from stingeripc.config import StingerConfig


class LanguageSymbolMixin:
    """ Enhances an object by searching for plugins that can provide language-specific symbols for it.
    
    Plugins are registered by providing a `project.entry-points."stinger_symbols"` entry in `pyproject.toml`.  Plugins have a name/domain that is used to identify the language.
    """

    @staticmethod
    def enhance(obj, config: "StingerConfig | None" = None):
        """ The ExtensionManager searches for all `stinger_symbols` plugins.  For each discovered plugin, it invokes the plugin's `for_model`
        method to determine a symbol-providing class to attached to the object (if any).  The symbol-providing class is then attached 
        as an attribute to the object, with the attribute name equal to the plugin's name/domain.  
        """
        mgr: ExtensionManager = ExtensionManager(
            namespace="stinger_symbols",
            invoke_on_load=True,
            invoke_kwds={"config": config},
        )
        for ext in mgr:
            domain = ext.name
            if ext.obj is not None:
                symbols = ext.obj.for_model(obj.__class__.__name__, obj)
                if symbols is not None:
                    setattr(obj, domain, symbols)


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

