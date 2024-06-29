import sys

import pytest
from dirstuff.summary.memory_utilities import bytes_to_size, size_to_bytes


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
    def test_bytes_to_size(self, n_bytes: int, expected: str) -> None:
        assert bytes_to_size(n_bytes) == expected

    def test_bytes_to_size_with_negative_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Bytes could not be converted to a size: -1"):
            bytes_to_size(-1)

    def test_bytes_to_size_too_large_raises_error(self) -> None:
        with pytest.raises(ValueError, match=f"Bytes could not be converted to a size: {sys.maxsize}"):
            bytes_to_size(sys.maxsize)

    @pytest.mark.parametrize(
        ("size", "expected"),
        [
            ("0", 0),
            ("1", 1),
            ("1 B", 1),
            ("1 KB", 1000),
            ("1 MB", 1000000),
            ("1 GB", 1000000000),
            ("1 TB", 1000000000000),
            ("1 PB", 1000000000000000),
        ],
    )
    def test_size_to_bytes(self, size: str, expected: int) -> None:
        assert size_to_bytes(size) == expected

    def test_size_to_bytes_with_invalid_size_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Size could not be converted to bytes: invalid"):
            size_to_bytes("invalid")
