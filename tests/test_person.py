import pytest

from phoney import Phoney, generate_person, get_available_locales
from phoney.data_loader import _capitalize_name, load_names
from phoney.person import feminine_surname, format_full_name

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
            # Only cased scripts (Latin, Cyrillic, ...) can be checked. Surname
            # particles may stay lowercase ("van Veen", "da Silva"), so require
            # at least one capitalised word.
            words = [w for w in name.replace("-", " ").split() if w[0].lower() != w[0].upper()]
            if words:
                assert any(w[0].isupper() for w in words), f"{locale}: {name!r}"


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
        ("i\u0307de", "tr_TR", "\u0130de"),
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


@pytest.mark.parametrize(
    "first, last, locale, expected",
    [
        ("Anna", "Smith", "en_US", "Anna Smith"),
        ("伟", "王", "zh_CN", "王伟"),
        ("健太", "佐藤", "ja_JP", "佐藤健太"),
        ("민준", "김", "ko_KR", "김민준"),
        ("Văn An", "Nguyễn", "vi_VN", "Nguyễn Văn An"),
        ("Gábor", "Nagy", "hu_HU", "Nagy Gábor"),
    ],
)
def test_format_full_name(first, last, locale, expected):
    assert format_full_name(first, last, locale) == expected


@pytest.mark.parametrize(
    "surname, locale, expected",
    [
        ("Иванов", "ru_RU", "Иванова"),
        ("Достоевский", "ru_RU", "Достоевская"),
        ("Толстой", "ru_RU", "Толстая"),
        ("Шевченко", "ru_RU", "Шевченко"),
        ("Kowalski", "pl_PL", "Kowalska"),
        ("Nowak", "pl_PL", "Nowak"),
        ("Novák", "cs_CZ", "Nováková"),
        ("Černý", "cs_CZ", "Černá"),
        ("Svoboda", "cs_CZ", "Svobodová"),
        ("Hájek", "cs_CZ", "Hájková"),
        ("Krejčí", "cs_CZ", "Krejčí"),
        ("Παπαδόπουλος", "el_GR", "Παπαδοπούλου"),
        ("Παπαδάκης", "el_GR", "Παπαδάκη"),
        ("Ιωαννίδης", "el_GR", "Ιωαννίδου"),
        ("Γεωργίου", "el_GR", "Γεωργίου"),
        ("Smith", "en_US", "Smith"),
    ],
)
def test_feminine_surname(surname, locale, expected):
    assert feminine_surname(surname, locale) == expected


def test_female_person_gets_feminine_surname():
    for _ in range(50):
        person = generate_person("pl_PL", "female")
        assert not person["last_name"].endswith(("ski", "cki"))


def test_full_name_key_matches_locale_order():
    person = generate_person("en_US")
    assert person["full_name"] == f"{person['first_name']} {person['last_name']}"


def test_already_cased_names_are_kept():
    assert _capitalize_name("van Dijk") == "van Dijk"
    assert _capitalize_name("McDonald") == "McDonald"


def test_capitalized_turkish_i_is_nfc():
    import unicodedata

    assert _capitalize_name("i̇hsan", "tr_TR") == "İhsan"
    assert unicodedata.is_normalized("NFC", _capitalize_name("i̇hsan", "tr_TR"))
