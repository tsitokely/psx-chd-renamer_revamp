from pathlib import Path
import tempfile

from lib.identify.iso_util import extract_serial_from_iso


def test_extract_serial_from_iso(tmp_path):
    data = b"prefix DATA SLES_123.45 moredata"
    tmp = tmp_path / "game.iso"
    tmp.write_bytes(data)

    serial = extract_serial_from_iso(tmp)
    assert serial == "SLES-12345"
