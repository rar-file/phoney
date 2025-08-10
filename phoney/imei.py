from __future__ import annotations

import random
from typing import Optional


def _luhn_check_digit(digits: str) -> int:
    total = 0
    # For IMEI, double every second digit from right (starting index 0 from right)
    rev = list(map(int, digits[::-1]))
    for i, d in enumerate(rev):
        # When generating the check digit, the first body digit from the right
        # (i == 0) must be doubled so that when the check digit is appended and
        # a standard Luhn check runs (starting with no doubling on the check digit),
        # the parity aligns.
        if i % 2 == 0:
            v = d * 2
            total += v if v < 10 else (v - 9)
        else:
            total += d
    return (10 - (total % 10)) % 10


def generate_imei(tac: Optional[str] = None) -> str:
    """Generate a valid 15-digit IMEI number.

    - tac: optional 8-digit Type Allocation Code. If not provided, random 8 digits.
    """
    if tac is None:
        tac = "".join(str(random.randint(0, 9)) for _ in range(8))
    else:
        tac = ''.join(filter(str.isdigit, tac))
        if len(tac) != 8:
            raise ValueError("tac must be 8 digits")
    snr = "".join(str(random.randint(0, 9)) for _ in range(6))
    body = tac + snr
    cd = _luhn_check_digit(body)
    return body + str(cd)


__all__ = ["generate_imei"]
