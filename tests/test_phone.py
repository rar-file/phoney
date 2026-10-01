import re

import pytest

from phoney import generate_phone
from phoney.phone import COUNTRY_CODES, DEFAULT_FORMATS, VALIDATORS


@pytest.mark.parametrize("locale", sorted(COUNTRY_CODES))
def test_every_locale_generates_a_valid_number(locale, capsys):
    for _ in range(25):
        number = generate_phone(locale)
        prefix = f"+{COUNTRY_CODES[locale]} "
        assert number.startswith(prefix)
        national = re.sub(r"\D", "", number[len(prefix):])
        assert len(national) == DEFAULT_FORMATS[locale].count("#")
        if locale in VALIDATORS:
            assert VALIDATORS[locale].fullmatch(national), number
    assert capsys.readouterr().out == ""


def test_unknown_locale_still_returns_a_number():
    for _ in range(100):
        assert re.match(r"^\+\d+ ", generate_phone("xx_XX"))


def test_none_locale_returns_a_number():
    assert generate_phone(None).startswith("+")


def test_format_examples():
    assert re.fullmatch(r"\+1 \(\d{3}\) \d{3}-\d{4}", generate_phone("en_US"))
    assert re.fullmatch(r"\+44 7\d{3} \d{6}", generate_phone("en_GB"))
