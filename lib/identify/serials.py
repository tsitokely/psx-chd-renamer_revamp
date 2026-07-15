import re
from typing import Optional

SERIAL_PATTERN = re.compile(
    rb"(SLES|SLUS|SLPS|SLED|SCES|SCUS|SCED|SLPM|SIPS|SLKA)[_.](\d{3})\.?(\d{2})"
)


def format_serial_from_match(match: re.Match) -> str:
    prefix, num1, num2 = match.groups()
    return f"{prefix.decode()}-{num1.decode()}{num2.decode()}"


def find_serial_in_bytes(data: bytes) -> Optional[str]:
    match = SERIAL_PATTERN.search(data)
    if match:
        return format_serial_from_match(match)
    return None
