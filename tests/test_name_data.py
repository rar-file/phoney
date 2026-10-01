"""Sanity checks on the bundled name lists (built by tools/build_name_data.py)."""
import unicodedata
from pathlib import Path

import pytest

import phoney
from phoney import generate_person
from phoney.phone import COUNTRY_CODES

NAME_DATA = Path(phoney.__file__).parent / "data" / "name_data"
LOCALE_DIRS = {d.name: d for d in NAME_DATA.glob("*/*") if d.is_dir()}


def read(locale, kind):
    path = LOCALE_DIRS[locale] / f"{kind}.txt"
    return path.read_text(encoding="utf-8").splitlines() if path.exists() else []


def test_every_phone_locale_has_name_data():
    assert set(COUNTRY_CODES) <= set(LOCALE_DIRS)


@pytest.mark.parametrize("locale", sorted(LOCALE_DIRS))
def test_lists_are_clean(locale):
    for kind in ("male", "female", "last"):
        names = read(locale, kind)
        assert len({n.casefold() for n in names}) == len(names), f"{locale}/{kind} has duplicates"
        for n in names:
            assert n == n.strip() and n, f"{locale}/{kind}: {n!r}"
            assert unicodedata.is_normalized("NFC", n), f"{locale}/{kind}: {n!r}"
            assert not any(ch.isdigit() for ch in n), f"{locale}/{kind}: {n!r}"


@pytest.mark.parametrize("locale", sorted(LOCALE_DIRS))
def test_male_and_female_lists_are_distinct(locale):
    male, female = set(read(locale, "male")), set(read(locale, "female"))
    assert len(male) >= 10 and len(female) >= 10
    assert len(male & female) / min(len(male), len(female)) < 0.5


def test_notice_ships_with_data():
    notice = (NAME_DATA / "NOTICE.md").read_text(encoding="utf-8")
    assert "Faker" in notice and "MIT" in notice


@pytest.mark.parametrize("gender, particle", [("male", "bin "), ("female", "binti ")])
def test_malay_patronymic(gender, particle):
    person = generate_person("ms_MY", gender)
    assert person["last_name"].startswith(particle)
