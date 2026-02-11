VERSION = "0.1.2"


def is_compatible(version: str) -> bool:
    """Check if a version string is compatible with the current VERSION.

    Follows semantic versioning compatibility rules:
    - For versions >= 1.0.0: Compatible if major versions match
    - For versions < 1.0.0: Compatible if major and minor versions match

    Args:
        version: Version string in the format "major.minor.patch"

    Returns:
        True if the provided version is compatible, False otherwise.
    """

    def parse_version(v: str) -> tuple[int, int, int]:
        """Parse a version string into (major, minor, patch) tuple."""
        parts = v.split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid version format: {v}")
        try:
            return (int(parts[0]), int(parts[1]), int(parts[2]))
        except ValueError:
            raise ValueError(f"Invalid version format: {v}")

    try:
        current_major, current_minor, current_patch = parse_version(VERSION)
        provided_major, provided_minor, provided_patch = parse_version(version)
    except ValueError:
        return False

    # For 0.x.y versions, both major and minor must match
    if current_major == 0:
        return provided_major == 0 and provided_minor == current_minor

    # For 1.0.0+, major version must match
    return provided_major == current_major
