from importlib.metadata import metadata, PackageNotFoundError
from typing import Tuple


def get_package_version() -> Tuple[str, str]:
    try:
        meta = metadata("simple-ipc")
        return meta["Name"], meta["Version"]
    except PackageNotFoundError:
        return "simple-ipc", "0.0.1+UNPACKAGED"
