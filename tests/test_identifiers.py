import pytest

from phoney import (
    generate_ean13,
    generate_financial_data,
    generate_imei,
    generate_isbn13,
    generate_upca,
    generate_uuid,
    generate_vin,
)


def luhn_valid(number: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(number)):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def gs1_valid(number: str) -> bool:
    """EAN-13 / UPC-A / ISBN-13 check digit (weights 1,3 from the right of the body)."""
    body, check = number[:-1], int(number[-1])
    total = sum(int(d) * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(body)))
    return (10 - total % 10) % 10 == check


VIN_VALUES = dict(zip("ABCDEFGHJKLMNPRSTUVWXYZ", [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 7, 9, 2, 3, 4, 5, 6, 7, 8, 9]))
VIN_VALUES.update({str(i): i for i in range(10)})
VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]


def vin_valid(vin: str) -> bool:
    remainder = sum(VIN_VALUES[c] * w for c, w in zip(vin, VIN_WEIGHTS)) % 11
    return vin[8] == ("X" if remainder == 10 else str(remainder))


def test_imei():
    for _ in range(500):
        imei = generate_imei()
        assert len(imei) == 15 and imei.isdigit()
        assert luhn_valid(imei), imei


def test_imei_with_tac():
    imei = generate_imei(tac="35-123456")
    assert imei.startswith("35123456")
    assert luhn_valid(imei)


def test_imei_rejects_bad_tac():
    with pytest.raises(ValueError):
        generate_imei(tac="123")


def test_vin_check_digit_matches_known_vin():
    from phoney.vin import _check_digit

    known = "1M8GDM9AXKP042788"  # standard worked example, check digit X
    assert _check_digit(known[:8] + "0" + known[9:]) == known[8]
    assert vin_valid(known)


def test_vin():
    for _ in range(500):
        vin = generate_vin()
        assert len(vin) == 17
        assert not set(vin) & set("IOQ")
        assert vin_valid(vin), vin


def test_ean13():
    for _ in range(500):
        code = generate_ean13()
        assert len(code) == 13 and code.isdigit()
        assert gs1_valid(code), code
    assert generate_ean13(prefix="590").startswith("590")


def test_upca():
    for _ in range(500):
        code = generate_upca()
        assert len(code) == 12 and code.isdigit()
        assert gs1_valid(code), code


def test_isbn13():
    for _ in range(500):
        code = generate_isbn13()
        assert len(code) == 13 and code.startswith("978")
        assert gs1_valid(code), code
    assert generate_isbn13(group_prefix="979").startswith("979")


@pytest.mark.parametrize("version", [1, 3, 4, 5])
def test_uuid_versions(version):
    import uuid

    assert uuid.UUID(generate_uuid(version)).version == version


def test_credit_cards():
    prefixes = {
        "Visa": ("4",),
        "MasterCard": ("51", "52", "53", "54", "55"),
        "American Express": ("34", "37"),
        "Discover": ("6011", "65"),
    }
    for _ in range(500):
        card = generate_financial_data()["credit_card"]
        number = card["number"]
        assert number.startswith(prefixes[card["issuer"]])
        assert len(number) == (15 if card["issuer"] == "American Express" else 16)
        assert luhn_valid(number), card
        assert len(card["cvv"]) == (4 if card["issuer"] == "American Express" else 3)
        month, year = card["expiry"].split("/")
        assert 1 <= int(month) <= 12 and len(year) == 4


def test_iban_and_bic_shape():
    data = generate_financial_data("de_DE")
    assert data["iban"].startswith("DE")
    assert len(data["bic"]) == 9 and data["bic"][4:6] == "DE"
