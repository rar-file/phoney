from __future__ import annotations

import random
from typing import Tuple


def _luhn(digits: str) -> int:
    s = 0
    alt = False
    for ch in digits[::-1]:
        d = int(ch)
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        s += d
        alt = not alt
    return (10 - (s % 10)) % 10


def _ean13_checksum(digits12: str) -> int:
    s = 0
    for i, ch in enumerate(digits12):
        d = int(ch)
        s += d if i % 2 == 0 else 3 * d
    return (10 - (s % 10)) % 10


def generate_ean13(prefix: str = "") -> str:
    body = (prefix + "".join(str(random.randint(0, 9)) for _ in range(max(0, 12 - len(prefix)))))[:12]
    cd = _ean13_checksum(body)
    return body + str(cd)


def generate_upca(prefix: str = "") -> str:
    # UPC-A is 12 digits; EAN-13 with leading 0
    upc11 = (prefix + "".join(str(random.randint(0, 9)) for _ in range(max(0, 11 - len(prefix)))))[:11]
    # EAN-13 checksum on 0 + upc11
    cd = _ean13_checksum("0" + upc11)
    return upc11 + str(cd)


def generate_isbn13(group_prefix: str = "978") -> str:
    body = (group_prefix + "".join(str(random.randint(0, 9)) for _ in range(max(0, 12 - len(group_prefix)))))[:12]
    cd = _ean13_checksum(body)
    return body + str(cd)


__all__ = [
    "generate_ean13",
    "generate_upca",
    "generate_isbn13",
]
