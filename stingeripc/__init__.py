from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("stinger-ipc")
except PackageNotFoundError:
    __version__ = "unknown"

from .interface import StingerInterface
from .asyncapi import StingerToAsyncApi

__all__ = ["StingerInterface", "StingerToAsyncApi", "__version__"]
