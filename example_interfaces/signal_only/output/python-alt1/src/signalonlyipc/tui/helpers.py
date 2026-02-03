from importlib.metadata import metadata, PackageNotFoundError
from typing import Tuple


def get_package_version() -> Tuple[str, str]:
    try:
        meta = metadata("signal-only-ipc")
        return meta["Name"], meta["Version"]
    except PackageNotFoundError:
        return "signal-only-ipc", "0.0.1+UNPACKAGED"
