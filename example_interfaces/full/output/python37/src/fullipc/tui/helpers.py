from importlib.metadata import metadata, PackageNotFoundError
from typing import Tuple


def get_package_version() -> Tuple[str, str]:
    try:
        meta = metadata("full-37-ipc")
        return meta["Name"], meta["Version"]
    except PackageNotFoundError:
        return "full-37-ipc", "0.0.2+UNPACKAGED"
