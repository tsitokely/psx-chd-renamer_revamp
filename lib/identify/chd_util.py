import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

from .serials import find_serial_in_bytes


def resolve_chdman(explicit_path: str) -> str:
    if explicit_path and Path(explicit_path).is_file():
        return explicit_path
    found = shutil.which("chdman")
    if found:
        return found
    raise FileNotFoundError(
        "chdman not found. Either add it to PATH or set CHDMAN_PATH to its full location."
    )


def extract_serial_from_chd(chd_path: Path, chdman: str, poll_interval: float = 0.2) -> Optional[str]:
    temp_dir = chd_path.parent / f"_tmp_{chd_path.stem}"
    temp_dir.mkdir(exist_ok=True)
    cue_path = temp_dir / f"{chd_path.stem}.cue"
    bin_path = temp_dir / f"{chd_path.stem}.bin"

    proc = subprocess.Popen(
        [chdman, "extractcd", "-i", str(chd_path), "-o", str(cue_path), "-ob", str(bin_path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    serial = None
    try:
        while proc.poll() is None:
            if bin_path.exists() and bin_path.stat().st_size > 200_000:
                with open(bin_path, "rb") as f:
                    data = f.read(500_000)
                serial = find_serial_in_bytes(data)
                if serial:
                    break
            time.sleep(poll_interval)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            pass
        shutil.rmtree(temp_dir, ignore_errors=True)

    return serial
