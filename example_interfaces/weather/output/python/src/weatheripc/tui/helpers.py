
from importlib.metadata import metadata, PackageNotFoundError
from typing import Tuple

def get_package_version() -> Tuple[str, str]:
    try:
        meta = metadata("weather-ipc")
        return meta["Name"], meta["Version"]
    except PackageNotFoundError:
        return "weather-ipc", "0.1.2+UNPACKAGED"