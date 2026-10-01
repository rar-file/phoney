<div align="center">

# 📞 Phoney

**Realistic, locale-aware fake data for Python, with zero dependencies.**

Names, phone numbers, emails, full profiles, résumés, network data and checksum-valid identifiers for tests, demos, seed data and anonymisation.

[![PyPI Version](https://img.shields.io/pypi/v/phoney?color=blue)](https://pypi.org/project/phoney/)
[![Python Versions](https://img.shields.io/pypi/pyversions/phoney)](https://pypi.org/project/phoney/)
[![Tests](https://github.com/rar-file/phoney/actions/workflows/tests.yml/badge.svg)](https://github.com/rar-file/phoney/actions/workflows/tests.yml)
[![PyPI Downloads](https://static.pepy.tech/badge/phoney)](https://pepy.tech/projects/phoney)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/rar-file/phoney/blob/main/LICENSE)

</div>

```bash
pip install phoney
```

```python
from phoney import Phoney

fake = Phoney()

fake.full_name(locale="en_GB")   # 'Nicola Sullivan'
fake.phone(locale="en_GB")       # '+44 7789 328792'
fake.email(locale="it_IT")       # 'annarossi7682@gmail.com'
fake.vin()                       # 'LEJAAPPL4LV538323'  (valid check digit)
```

## ✨ Why Phoney?

- **🌍 Locale-aware**: real names and correctly formatted phone numbers for 43 countries, written in each language's own script and name order.
- **🎲 Huge variety**: 47,000+ given names and 122,000+ surnames, roughly 717 million distinct full names, all drawn from real, openly licensed name datasets.
- **✅ Valid where it matters**: IMEI, VIN, EAN-13, UPC-A, ISBN-13 and card numbers all pass their checksums.
- **🧑 Whole people, not just fields**: one call builds a consistent profile in which the email and username come from the person's own name.
- **💼 Career data**: job titles, salary ranges, skills, employment history and full résumés.
- **🌐 Network data**: domains, URLs, IPv4/IPv6 from real regional ranges, and MAC addresses.
- **🪶 Zero dependencies**: pure standard library, Python 3.10+.

---

## 🚀 Quick start

### A complete profile

```python
from phoney import Phoney

fake = Phoney()
fake.profile(locale="en_GB")
```

```python
{
    'uuid': '8fc39f2e-e8b2-4bd0-bf92-a84f5844ee4a',
    'first_name': 'Nicola',
    'last_name': 'Sullivan',
    'full_name': 'Nicola Sullivan',
    'gender': 'female',
    'age': 39,
    'birthdate': '1987-07-12',
    'birth_year': 1987,
    'email': 'nicolasullivan62@gmail.com',
    'phone': '+44 7789 328792',
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 ...',
    'username': 'nicnavillus',
    'credit_card': {'issuer': 'Visa', 'number': '4033907579383471', 'expiry': '01/2027', 'cvv': '468'},
    'locale': 'en_GB',
    'created_at': '2026-10-01T15:03:19.842651'
}
```

### People and contact details

```python
fake.first_name(locale="it_IT")                 # 'Napoleone'
fake.full_name(gender="female", locale="de_DE") # 'Jeannette Trommler'
fake.full_name(locale="ru_RU")                  # 'Копылова Меркушева'
fake.phone(locale="en_US")                      # '+1 (291) 855-7893'
fake.phone(locale="fr_FR")                      # '+33 353 045 340'
fake.email(first_name="Anna", last_name="Rossi", locale="it_IT")  # 'annarossi7682@gmail.com'
fake.age(min_age=18, max_age=30)                # 24
fake.birthdate()                                # datetime.date(1987, 7, 12)
```

### Online presence

```python
fake.username("John", "Smith")                  # 'joHnSMITh'
fake.password(16)                               # 'F*w#yYt!>#332tyk'
fake.social_handle("John", "Smith", "twitter")  # '@john_smith'
fake.online_presence("John", "Smith")           # username, password and handles for 7 platforms
fake.user_agent("mobile")                       # 'Mozilla/5.0 (iPhone; CPU iPhone OS 17 like Mac OS X) ...'
fake.uuid()                                     # 'ba5684a5-a08f-4191-ab8d-c5d5c0d30795'
```

### Identifiers and finance

```python
fake.imei()     # '193036426212990'   15 digits, Luhn-valid
fake.vin()      # 'LEJAAPPL4LV538323' 17 chars, valid check digit, no I/O/Q
fake.ean13()    # '6405622415494'
fake.upca()     # '909514547523'
fake.isbn13()   # '9787720405605'

from phoney import generate_financial_data
generate_financial_data("de_DE")
# {'credit_card': {'issuer': 'Discover', 'number': '6569070293137587', 'expiry': '06/2031', 'cvv': '256'},
#  'iban': 'DE29 1D02 4B8D MV7M 7TLL GC', 'bic': 'SIMSDEMMT'}
```

### Careers and résumés

```python
fake.job_title(family="software_engineer", level="Senior")
# {'title': 'Senior Platform Engineer', 'family': 'software_engineer', 'level': 'Senior', 'locale': 'en_US'}

fake.salary(locale="en_GB", family="software_engineer", level="Senior")
# {'min': 65000, 'max': 90000, 'currency': 'GBP', 'period': 'year', ...}

fake.skills("software_engineer", count=5)
fake.employment_history(years=8, family="software_engineer")
fake.experience_level(7)                        # 'Senior'

print(fake.resume(family="software_engineer", years=6, format="text"))
```

```text
Krista Villa — Mid Full-Stack Engineer
kri.villa12@yahoo.com | +1 (474) 452-9078 | Los Angeles, NY United States
...
Summary
6+ years as Mid Full-Stack Engineer. Strong in CI/CD, Java, Unit Testing, SQL, JavaScript.
```

Use `format="dict"` (the default) to get structured data: experience, education, projects, certifications, languages and more.

### Internet

```python
fake.tld(locale="en_GB")        # 'co.uk'
fake.domain(locale="en_GB")     # 'pixel-zcpw.co.uk'
fake.hostname(locale="en_GB")   # 'cache-q30.echo-dc5v.co.uk'
fake.url(locale="ja_JP")        # 'https://acme-ii0g.jp/v1/1xjd0?q=umbrella&page=3'
fake.ipv4(locale="en_GB")       # '90.251.2.27'               (public, from the RIPE region)
fake.ipv6(locale="ja_JP")       # '2400::9ed2:aa0c:ffd2:1f0a' (global unicast, from the APNIC region)
fake.mac()                      # '56:e8:f9:a2:f5:8c'
```

> Every `Phoney` method also has a plain function you can import directly, e.g. `from phoney import generate_phone, generate_vin, generate_resume`.

---

## 📚 API reference

<details>
<summary><b>All <code>Phoney</code> methods</b></summary>

| Area | Method | Returns |
|---|---|---|
| **People** | `first_name(gender=None, locale='en_US')` | First name |
| | `last_name(gender=None, locale='en_US')` | Last name |
| | `full_name(gender=None, locale='en_US')` | `"First Last"` |
| | `gender(locale='en_US')` | `'male'` or `'female'` |
| | `age(min_age=18, max_age=80)` | `int` |
| | `birthdate(min_age=18, max_age=80)` | `datetime.date` |
| | `profile(locale='en_US', gender=None)` | Full profile `dict` |
| **Contact** | `phone(locale='en_US')` | International-format number |
| | `email(first_name=None, last_name=None, locale='en_US', age=None, birth_year=None)` | Email address |
| **Online** | `username(first_name=None, last_name=None, locale='en_US')` | Username |
| | `password(length=12)` | Password containing upper, lower, digit and symbol |
| | `social_handle(first_name=None, last_name=None, platform='twitter', locale='en_US')` | Handle (`twitter`, `instagram`, `tiktok`, `github`, ...) |
| | `online_presence(first_name=None, last_name=None, locale='en_US')` | Username, password and social handles |
| | `user_agent(device_type='desktop')` | Browser UA (`'desktop'` or `'mobile'`) |
| | `uuid(version=4)` | UUID v1, v3, v4 or v5 |
| **Identifiers** | `imei(tac=None)` | 15-digit IMEI |
| | `vin()` | 17-character VIN |
| | `ean13(prefix='')` / `upca(prefix='')` | Barcodes |
| | `isbn13(group_prefix='978')` | ISBN-13 |
| **Career** | `job_title(family=None, level=None, locale='en_US')` | Title, family, level |
| | `salary(family=None, level=None, title=None, locale='en_US')` | Range, currency, period |
| | `skills(family, level=None, count=None)` | List of skills |
| | `employment_history(years=10, locale='en_US', family=None, min_jobs=1, max_jobs=5)` | List of jobs |
| | `experience_level(years)` | `'Intern'` … `'Principal'` |
| | `resume(locale=None, family=None, years=8, format='dict')` | Résumé as a `dict` or `'text'` |
| **Internet** | `tld(locale=None)` | TLD, weighted by locale (GB → `co.uk`) |
| | `domain(tld=None, locale=None)` | Domain name |
| | `hostname(domain=None, locale=None)` | Hostname |
| | `url(scheme='https', domain=None, path_segments=None, query_params=None, locale=None)` | URL |
| | `ipv4(country=None, locale=None)` | Public IPv4 |
| | `ipv6(global_unicast=True, country=None, locale=None)` | IPv6, compressed form |
| | `mac()` | Locally administered unicast MAC |

Each method also has a `generate_*` twin on the instance and at module level: `fake.generate_vin()` and `phoney.generate_vin()`.

</details>

---

## 🌍 Locales

Names and phone numbers cover the same 43 locales:

| Region | Locales |
|---|---|
| Europe | `cs_CZ` `da_DK` `de_DE` `el_GR` `en_GB` `es_ES` `fi_FI` `fr_FR` `hu_HU` `it_IT` `nl_NL` `no_NO` `pl_PL` `pt_PT` `ro_RO` `ru_RU` `sv_SE` `tr_TR` |
| Americas | `en_CA` `en_US` `es_AR` `es_CL` `es_CO` `es_MX` `pt_BR` |
| Asia | `fil_PH` `hi_IN` `id_ID` `ja_JP` `ko_KR` `ms_MY` `th_TH` `vi_VN` `zh_CN` `zh_TW` |
| Middle East | `ar_EG` `ar_SA` `he_IL` |
| Africa | `en_ZA` `ha_NG` `sw_KE` |
| Oceania | `en_AU` `en_NZ` |

Names follow local conventions:
- **Script:** Cyrillic, Greek, Arabic, Hebrew, Devanagari, Thai, Hangul and CJK where the language uses it.
- **Order:** family name first for Chinese, Japanese, Korean, Vietnamese and Hungarian (`王伟`, `Nguyễn Văn An`, `Nagy Gábor`).
- **Feminine surnames:** Russian, Polish, Czech and Greek women get the feminine form (`Иванова`, `Kowalska`, `Nováková`).
- **Patronymics:** Malay names use `bin`/`binti` (`Aisyah binti Umar`).

Name lists come from Faker (MIT), the CC0 popular-names-by-country dataset, US Social Security baby names, public-domain surname lists and an MIT-licensed Japanese name dataset. See [`phoney/data/name_data/NOTICE.md`](https://github.com/rar-file/phoney/blob/main/phoney/data/name_data/NOTICE.md) for sources and licences. `tools/build_name_data.py` rebuilds them.
**Salaries** are localised for `en_US`, `en_GB` and `de_DE`. Unknown locales fall back to generic data rather than raising an error.

```python
from phoney import get_available_locales
get_available_locales()
```

---

## 🛰️ Country-accurate IP ranges (optional)

Out of the box, IPs come from the right regional registry block (RIPE, APNIC, ARIN, LACNIC, AFRINIC). For per-country accuracy, generate prefix files from the registries' published datasets:

1. Download the five `delegated-*-extended-latest` files (APNIC, ARIN, RIPE NCC, LACNIC, AFRINIC) into a folder.
2. Build the prefix files:

```bash
phoney-build-prefixes --input-dir ./rir-data
phoney-build-prefixes --input-dir ./rir-data --output-dir ./my-prefixes   # custom output folder
```

On Windows, `tools/fetch_and_build_prefixes.ps1` downloads the files and builds the prefixes in one step.

---

## 🧪 Development

```bash
git clone https://github.com/rar-file/phoney
cd phoney
python -m pip install -e ".[test]"
python -m pytest
```

Every push and pull request runs the tests on Python 3.10–3.14 and checks that the package builds.

**Releasing:** bump `__version__` in `phoney/__init__.py`, then publish a GitHub release tagged `vX.Y.Z`. The publish workflow tests, builds and uploads to PyPI.

---

## 📝 Changelog

<details open>
<summary><b>0.4.0</b>: real names for 43 countries</summary>

- Name data rebuilt from real, openly licensed datasets: 43 locales (up from 19), 47,000+ given names and 122,000+ surnames
- Family-name-first order for Chinese, Japanese, Korean, Vietnamese and Hungarian
- Feminine surname forms for Russian, Polish, Czech and Greek; Malay `bin`/`binti` patronymics
- `generate_person()` now also returns `full_name`
- Fixed broken lists: Egyptian names were a copy of the US list, Japanese had 2 names, Hindi names had lost their vowel signs, and French first names were run together
- Includes all 0.3.2 fixes below (0.3.2 was not published to PyPI)

</details>

<details>
<summary><b>0.3.2</b>: bug fixes and cleanup</summary>

- Names are now capitalised (`Marco Rossi`, not `marco rossi`), including Turkish `İ`/`I`
- Phone numbers for `en_AU`, `fil_PH` and `zh_TW` no longer fail; `id_ID` numbers no longer get a doubled leading `8`
- Phone generation no longer prints `DEBUG:` lines
- VIN check digits are now correct for VINs containing the letters J–Z
- `generate_age()` never goes below `min_age`, and rejects `min_age > max_age`
- `password(length)` returns exactly `length` characters
- Added `phoney.__version__`, a pytest suite and GitHub Actions CI

</details>

<details>
<summary><b>0.3.0</b>: identifiers, internet and career modules</summary>

- New identifiers: IMEI, VIN, EAN-13, UPC-A, ISBN-13
- Locale-aware IPv4/IPv6 with regional fallbacks; per-country TLD preferences
- Career module: job titles, salary ranges, skills, employment history
- `phoney-build-prefixes` CLI
- Requires Python 3.10+

</details>

---

<div align="center">

**MIT licensed** · Made by **rarfile** · [Report an issue](https://github.com/rar-file/phoney/issues)

</div>
