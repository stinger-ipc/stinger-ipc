from importlib.metadata import metadata, PackageNotFoundError
from typing import Tuple


def get_package_version() -> Tuple[str, str]:
    try:
        meta = metadata("signal-only-37-ipc")
        return meta["Name"], meta["Version"]
    except PackageNotFoundError:
        return "signal-only-37-ipc", "0.0.1+UNPACKAGED"
