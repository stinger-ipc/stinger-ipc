from importlib.metadata import metadata, PackageNotFoundError
from typing import Tuple


def get_package_version() -> Tuple[str, str]:
    try:
        meta = metadata("full-ipc")
        return meta["Name"], meta["Version"]
    except PackageNotFoundError:
        return "full-ipc", "0.0.2+UNPACKAGED"
