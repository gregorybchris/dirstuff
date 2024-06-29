import re

MEMORY_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def _bytes_per_units(units: str) -> int:
    scale = MEMORY_UNITS.index(units)
    return 10 ** (3 * scale)


def bytes_to_size(n_bytes: int) -> str:
    """Convert bytes to a size with units.

    Args:
        n_bytes (int): Number of bytes.

    Returns:
        str: Size of file/dir with reasonable units.
    """
    if n_bytes < 0:
        msg = f"Bytes could not be converted to a size: {n_bytes}"
        raise ValueError(msg)

    for units in MEMORY_UNITS:
        multiplier = _bytes_per_units(units)
        if n_bytes < multiplier * 1000:
            value = round(n_bytes / multiplier, 1)
            return f"{value:5.1f} {units}"

    msg = f"Bytes could not be converted to a size: {n_bytes}"
    raise ValueError(msg)


def size_to_bytes(size: str) -> int:
    """Convert file size with or without units to bytes.

    Args:
        size (str): Size of file/dir, possibly with units.

    Returns:
        int: Size of file/dir in bytes.
    """
    # Already bytes
    match = re.search(r"^[0-9]+$", size)
    if match is not None:
        return int(match.group(0))

    # With units
    units_regex = "|".join(MEMORY_UNITS)
    match = re.search(r"^([0-9]+)(?:\s)?(" + units_regex + r")$", size)
    if match is not None:
        return int(match.group(1)) * _bytes_per_units(match.group(2))

    msg = f"Size could not be converted to bytes: {size}"
    raise ValueError(msg)
