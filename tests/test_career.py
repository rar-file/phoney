import json
from pathlib import Path

import pytest

import phoney
from phoney import (
    Phoney,
    experience_level_from_years,
    generate_employment_history,
    generate_job_title,
    generate_resume,
    generate_salary,
    generate_skills,
)

FAMILIES = list(json.loads((Path(phoney.__file__).parent / "data" / "career" / "job_families.json").read_text(encoding="utf-8")))


@pytest.mark.parametrize("family", FAMILIES)
def test_job_title_and_skills(family):
    job = generate_job_title(family=family)
    assert job["family"] == family and job["title"]
    assert generate_skills(family)


@pytest.mark.parametrize("locale", ["en_US", "en_GB", "de_DE", "fr_FR"])
def test_salary(locale):
    for _ in range(50):
        salary = generate_salary(locale=locale)
        assert 0 < salary["min"] <= salary["max"]
        assert salary["currency"]


def test_employment_history_is_chronological():
    for _ in range(50):
        history = generate_employment_history(years=12)
        assert history
        for job in history:
            assert job["start_date"] <= job["end_date"]
        starts = [job["start_date"] for job in history]
        assert starts == sorted(starts) or starts == sorted(starts, reverse=True)


@pytest.mark.parametrize("years, level", [(0, "Intern"), (50, None)])
def test_experience_level(years, level):
    result = experience_level_from_years(years)
    assert isinstance(result, str) and result
    if level:
        assert result == level


@pytest.mark.parametrize("locale", [None, "en_US", "de_DE", "ja_JP"])
def test_resume(locale):
    cv = generate_resume(locale=locale)
    assert {"personal", "experience", "skills", "education"} <= set(cv)
    text = generate_resume(locale=locale, format="text")
    assert isinstance(text, str) and "Summary" in text


def test_phoney_career_helpers():
    p = Phoney()
    assert p.job_title()["title"]
    assert p.salary()["max"] > 0
    assert p.resume(format="text")
