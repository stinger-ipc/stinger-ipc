from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("stinger-ipc")
except PackageNotFoundError:
    __version__ = "unknown"

from .interface import StingerInterface

__all__ = ["StingerInterface", "__version__"]
