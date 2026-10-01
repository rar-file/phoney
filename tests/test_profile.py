import re
from datetime import date

import pytest

from phoney import (
    Phoney,
    generate_age,
    generate_email,
    generate_password,
    generate_profile,
    generate_social_handles,
    generate_user_agent,
    generate_username,
    get_available_locales,
)
from phoney.person import format_full_name

EMAIL_RE = re.compile(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$")


@pytest.mark.parametrize("min_age, max_age", [(18, 80), (0, 1), (30, 30), (18, 19)])
def test_age_within_bounds(min_age, max_age):
    today = date.today()
    for _ in range(2000):
        age, birthdate = generate_age(min_age, max_age)
        assert min_age <= age <= max_age
        expected = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        assert age == expected


def test_age_rejects_inverted_range():
    with pytest.raises(ValueError):
        generate_age(50, 20)


@pytest.mark.parametrize("locale", sorted(get_available_locales()) + ["xx_XX"])
def test_profile(locale):
    for _ in range(10):
        profile = generate_profile(locale)
        for key in ("uuid", "first_name", "last_name", "full_name", "gender", "age",
                    "birthdate", "email", "phone", "user_agent", "username", "credit_card", "locale"):
            assert key in profile, key
        assert EMAIL_RE.match(profile["email"]), profile["email"]
        assert profile["phone"].startswith("+")
        assert profile["full_name"] == format_full_name(profile["first_name"], profile["last_name"], profile["locale"])


def test_profile_gender():
    assert generate_profile("en_US", gender="female")["gender"] == "female"


@pytest.mark.parametrize("locale", sorted(get_available_locales()))
def test_email_is_ascii_and_valid(locale):
    p = Phoney()
    for _ in range(25):
        assert EMAIL_RE.match(p.email(locale=locale))


def test_email_uses_given_name():
    email = generate_email("Anna", "Rossi", "it_IT")
    assert "anna" in email or "rossi" in email


def test_username_and_handles():
    assert re.fullmatch(r"[\w.\-]+", generate_username("John", "Smith"))
    handle = generate_social_handles("John", "Smith", "twitter")
    assert handle


@pytest.mark.parametrize("length", [8, 12, 32])
def test_phoney_password_has_exact_length(length):
    pw = Phoney().password(length)
    assert len(pw) == length
    assert any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)


def test_generate_password_length_range():
    for _ in range(100):
        assert 10 <= len(generate_password(10, 14)) <= 14
    # A minimum above the default maximum must not crash.
    assert len(generate_password(32)) == 32


@pytest.mark.parametrize("device", ["desktop", "mobile"])
def test_user_agent(device):
    assert generate_user_agent(device).startswith("Mozilla/5.0")


def test_online_presence():
    data = Phoney().online_presence("John", "Smith")
    assert {"username", "password", "social_media"} <= set(data)
