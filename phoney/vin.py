from __future__ import annotations

import random
import string

# VIN excludes I, O, Q
VIN_CHARS = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
# Transliteration values
TRANSLIT = {c: v for c, v in zip("ABCDEFGHJKLMNPRSTUVWXYZ", [1,2,3,4,5,6,7,8,9,1,2,3,4,5,7,9,2,3,4,5,6,7,8,9])}
for i in range(10):
    TRANSLIT[str(i)] = i
# Position weights for check digit
WEIGHTS = [8,7,6,5,4,3,2,10,0,9,8,7,6,5,4,3,2]


def _random_wmi() -> str:
    # Use generic WMI-like prefixes (not tied to specific manufacturers)
    # WMI: 1st = region/manufacturer, 2nd = manufacturer, 3rd = vehicle type/division (allow alnum except I/O/Q)
    first = random.choice("123456789JHTWKLZVSY")
    second = random.choice("ABCDEFGHJKLMNPRSTUVWXYZ")
    third = random.choice("ABCDEFGHJKLMNPRSTUVWXYZ0123456789")
    return first + second + third


def _check_digit(vin14: str) -> str:
    total = 0
    for i, ch in enumerate(vin14):
        val = TRANSLIT.get(ch, 0)
        total += val * WEIGHTS[i]
    remainder = total % 11
    return "X" if remainder == 10 else str(remainder)


def generate_vin() -> str:
    wmi = _random_wmi()
    # VDS: 5 chars (positions 4-8), use VIN_CHARS (excludes I/O/Q)
    vds = "".join(random.choice(VIN_CHARS) for _ in range(5))
    # VIS: 8 chars (positions 10-17). Commonly last 6 are digits; keep first 2 alnum.
    vis_head = "".join(random.choice(VIN_CHARS) for _ in range(2))
    vis_tail = "".join(random.choice(string.digits) for _ in range(6))
    vis = vis_head + vis_tail
    vin14 = wmi + vds + "0" + vis  # placeholder for check digit at pos 9 (index 8)
    cd = _check_digit(vin14)
    vin = vin14[:8] + cd + vin14[9:]
    return vin


__all__ = ["generate_vin"]
