import re


MEMORY_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def _bytes_per_units(units):
    scale = MEMORY_UNITS.index(units)
    return 10 ** (3 * scale)


def bytes_to_size(n_bytes):
    for units in MEMORY_UNITS:
        multiplier = _bytes_per_units(units)
        if n_bytes < multiplier * 1000:
            value = round(n_bytes / multiplier, 1)
            return '{:5.1f} {}'.format(value, units)
    raise ValueError(f"Bytes could not be converted to a size: {n_bytes}")


def size_to_bytes(size):
    # Already bytes
    match = re.search(r'^[0-9]+$', size)
    if match is not None:
        return int(match.group(0))

    # With units
    units_regex = '|'.join(MEMORY_UNITS)
    match = re.search(r'^([0-9]+)(?:\s)?(' + units_regex + r')$', size)
    if match is not None:
        return int(match.group(1)) * _bytes_per_units(match.group(2))

    raise ValueError(f"Size could not be converted to bytes: {size}")
