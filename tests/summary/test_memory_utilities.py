import sys

import pytest
from dirstuff.summary.memory_utilities import MemoryUnits, from_size_str, size_str_to_bytes, to_size_str


class TestMemoryUtilities:
    @pytest.mark.parametrize(
        ("n_bytes", "expected"),
        [
            (0, "  0.0 B"),
            (1, "  1.0 B"),
            (1000, "  1.0 KB"),
            (1000000, "  1.0 MB"),
            (1000000000, "  1.0 GB"),
            (32000000000, " 32.0 GB"),
            (1000000000000, "  1.0 TB"),
            (1000000000000000, "  1.0 PB"),
        ],
    )
    def test_to_size_str(self, n_bytes: int, expected: str) -> None:
        assert to_size_str(n_bytes) == expected

    def test_to_size_str_with_negative_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Bytes could not be converted to a size: -1"):
            to_size_str(-1)

    def test_to_size_str_too_large_raises_error(self) -> None:
        with pytest.raises(ValueError, match=f"Bytes could not be converted to a size: {sys.maxsize}"):
            to_size_str(sys.maxsize)

    @pytest.mark.parametrize(
        ("size", "expected"),
        [
            # No units
            ("0", 0),
            ("1", 1),
            # With units
            ("1 B", 1),
            ("3 KB", 3000),
            ("6 MB", 6000000),
            ("9 GB", 9000000000),
            ("12 TB", 12000000000000),
            ("15 PB", 15000000000000000),
            # No space
            ("1B", 1),
            ("1KB", 1000),
            ("1MB", 1000000),
            # Lower case
            ("1 b", 1),
            ("1 kb", 1000),
            ("1 mb", 1000000),
        ],
    )
    def test_size_str_to_bytes(self, size: str, expected: int) -> None:
        assert size_str_to_bytes(size) == expected

    def test_size_str_to_bytes_with_invalid_size_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Size could not be converted to bytes and units: invalid"):
            size_str_to_bytes("invalid")

    def test_size_str_to_bytes_with_negative_size_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Size could not be converted to bytes and units: -3 B"):
            size_str_to_bytes("-3 B")

    def test_size_str_to_bytes_with_invalid_units_raises_error(self) -> None:
        with pytest.raises(ValueError, match="'ZB' is not a valid MemoryUnits"):
            size_str_to_bytes("3 ZB")

    @pytest.mark.parametrize(
        ("size", "expected_number", "expected_units"),
        [
            ("2 MB", 2, MemoryUnits.MB),
            ("3 GB", 3, MemoryUnits.GB),
            ("4 TB", 4, MemoryUnits.TB),
        ],
    )
    def test_from_size_str(self, size: str, expected_number: int, expected_units: MemoryUnits) -> None:
        assert from_size_str(size) == (expected_number, expected_units)
