import re
from enum import StrEnum


class MemoryUnits(StrEnum):
    """Units of computer memory."""

    B = "B"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"
    PB = "PB"

    def to_bytes(self) -> int:
        """Convert memory units to bytes.

        Returns:
            int: Number of bytes.
        """
        match self:
            case self.B:
                return 1
            case self.KB:
                return 10**3
            case self.MB:
                return 10**6
            case self.GB:
                return 10**9
            case self.TB:
                return 10**12
            case self.PB:
                return 10**15
            case _:
                msg = f"Memory unit not recognized: {self}"
                raise ValueError(msg)


def to_bytes(n: int, units: MemoryUnits) -> int:
    """Convert memory size to bytes.

    Args:
        n (int): Amount of memory.
        units (MemoryUnits): Units of memory.

    Returns:
        int: Number of bytes.
    """
    return n * units.to_bytes()


def to_size_str(n_bytes: int) -> str:
    """Convert bytes to a size with units.

    Args:
        n_bytes (int): Number of bytes.

    Returns:
        str: Size of file/dir with reasonable units.
    """
    if n_bytes < 0:
        msg = f"Bytes could not be converted to a size: {n_bytes}"
        raise ValueError(msg)

    for units in MemoryUnits:
        multiplier = units.to_bytes()
        units_str = units.name.upper()
        if n_bytes < multiplier * 1000:
            value = round(n_bytes / multiplier, 1)
            return f"{value:5.1f} {units_str}"

    msg = f"Bytes could not be converted to a size: {n_bytes}"
    raise ValueError(msg)


def from_size_str(size_str: str) -> tuple[int, MemoryUnits]:
    """Convert memory size string to number and units.

    Args:
        size_str (str): Memory size string with units.

    Returns:
        tuple[int, MemoryUnits]: Numeric memory size and units.
    """
    pattern = r"^([0-9]+)(?:\s)?([a-zA-Z]*)$"
    match = re.match(pattern, size_str)
    if match is None:
        msg = f"Size could not be converted to bytes and units: {size_str}"
        raise ValueError(msg)

    number_str = match.group(1)
    units_str = match.group(2)

    if units_str is None or units_str == "":
        units_str = "B"

    number = int(number_str)
    units = MemoryUnits(units_str.upper())

    return number, units


def size_str_to_bytes(size_str: str) -> int:
    """Convert memory size string to bytes.

    Args:
        size_str (str): Memory size string with units.

    Returns:
        int: Number of bytes.
    """
    number, units = from_size_str(size_str)
    return to_bytes(number, units)
