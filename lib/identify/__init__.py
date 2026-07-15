from pathlib import Path
from .serials import find_serial_in_bytes
from .iso_util import extract_serial_from_iso
from .chd_util import extract_serial_from_chd, resolve_chdman

CHDMAN_PATH = ""

CHDMAN = None
try:
    CHDMAN = resolve_chdman(CHDMAN_PATH)
except FileNotFoundError:
    CHDMAN = None


def extract_serial(disc_path: Path, chdman: str | None = None, poll_interval: float = 0.2) -> str | None:
    suffix = disc_path.suffix.lower()
    if suffix == ".iso":
        return extract_serial_from_iso(disc_path)

    if suffix == ".chd":
        chdman = chdman or CHDMAN
        if not chdman:
            raise FileNotFoundError("chdman not found. Set CHDMAN_PATH or pass `chdman`.")
        return extract_serial_from_chd(disc_path, chdman, poll_interval)

    return None
