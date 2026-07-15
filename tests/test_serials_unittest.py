import pytest

from lib.identify.serials import find_serial_in_bytes


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (b"garbageDATA SLES_123.45 moregarbage", "SLES-12345"),
        (b"prefix SYSTEM.CNF some text SLUS.98765 trailing", "SLUS-98765"),
    ],
)
def test_find_serial_in_bytes_matches_expected_serial(data, expected):
    assert find_serial_in_bytes(data) == expected
