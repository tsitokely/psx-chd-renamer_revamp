from pathlib import Path
from typing import Optional

from .serials import find_serial_in_bytes


def extract_serial_from_iso(iso_path: Path, read_size: int = 4_000_000) -> Optional[str]:
    with open(iso_path, "rb") as f:
        data = f.read(read_size)

    serial = find_serial_in_bytes(data)
    if serial:
        return serial

    cnf_idx = data.find(b"SYSTEM.CNF")
    if cnf_idx != -1:
        window = data[cnf_idx:cnf_idx + 4096]
        serial = find_serial_in_bytes(window)
        if serial:
            return serial

    return None
