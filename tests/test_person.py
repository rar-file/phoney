import pytest

from phoney import Phoney, generate_person, get_available_locales
from phoney.data_loader import _capitalize_name, load_names

LOCALES = sorted(get_available_locales())


@pytest.mark.parametrize("locale", LOCALES)
def test_person_has_names_and_gender(locale):
    for _ in range(25):
        person = generate_person(locale)
        assert person["first_name"].strip()
        assert person["last_name"].strip()
        assert person["gender"] in ("male", "female")


@pytest.mark.parametrize("locale", LOCALES)
def test_names_are_not_all_lowercase(locale):
    for _ in range(25):
        person = generate_person(locale)
        for name in (person["first_name"], person["last_name"]):
            first = name[0]
            # Only cased scripts (Latin, Cyrillic, ...) can be checked.
            if first.lower() != first.upper():
                assert first.isupper(), f"{locale}: {name!r}"


@pytest.mark.parametrize("gender", ["male", "female"])
def test_requested_gender_is_respected(gender):
    for _ in range(25):
        assert generate_person("en_US", gender)["gender"] == gender


def test_unknown_locale_falls_back():
    person = generate_person("xx_XX")
    assert person["first_name"] and person["last_name"]


def test_load_names_returns_all_keys():
    names = load_names("en_US")
    assert set(names) == {"male", "female", "last"}
    assert all(names.values())


@pytest.mark.parametrize(
    "raw, locale, expected",
    [
        ("anna", "", "Anna"),
        ("jean-luc", "", "Jean-Luc"),
        ("o'brien", "", "O'Brien"),
        ("mcdonald", "", "Mcdonald"),
        ("иван", "ru_RU", "Иван"),
        ("佐藤", "ja_JP", "佐藤"),
        ("irmak", "tr_TR", "İrmak"),
        ("ırmak", "tr_TR", "Irmak"),
        ("i̇de", "tr_TR", "İde"),
        ("irmak", "en_US", "Irmak"),
    ],
)
def test_capitalize_name(raw, locale, expected):
    assert _capitalize_name(raw, locale) == expected


def test_phoney_name_helpers():
    p = Phoney()
    assert p.first_name(locale="it_IT")
    assert p.last_name(locale="it_IT")
    assert len(p.full_name(locale="it_IT").split()) >= 2
    assert p.gender() in ("male", "female")
