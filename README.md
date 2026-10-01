# 🌐 Phoney — Realistic Fake Data Generator

Zero-dependency Python library for locale-aware fake personal data. Names for 19 locales, phone numbers for 43 countries, complete profiles, and checksum-valid identifiers (IMEI, VIN, ISBN-13, EAN-13, UPC-A) — for testing, demos, and anonymization pipelines.

`pip install phoney`

[![PyPI Version](https://img.shields.io/pypi/v/phoney?color=blue)](https://pypi.org/project/phoney/)
[![PyPI Downloads](https://static.pepy.tech/badge/phoney)](https://pepy.tech/projects/phoney)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/phoney)](https://pypi.org/project/phoney/)
[![Tests](https://github.com/rar-file/phoney/actions/workflows/tests.yml/badge.svg)](https://github.com/rar-file/phoney/actions/workflows/tests.yml)

Generate locale-aware fake personal data for testing, development, and anonymization. Perfect for populating databases and creating test users.

---

## 🆕 What’s new in 0.3.2

Bug fixes and project cleanup:

- Names are now capitalized (`Marco Rossi`, not `marco rossi`), including Turkish dotted/dotless `İ`/`I`
- Phone numbers for `en_AU`, `fil_PH` and `zh_TW` no longer fail with `ValueError`; `id_ID` numbers no longer get a doubled leading `8`
- No more `DEBUG:` lines printed to stdout from phone generation
- VIN check digits are now correct for VINs containing the letters J–Z
- `generate_age(min_age, max_age)` never returns an age below `min_age`, and rejects `min_age > max_age`
- `Phoney().password(length)` returns exactly `length` characters; `generate_password(min_length)` no longer crashes when `min_length` > 18
- `phoney.__version__` is available
- New pytest suite and GitHub Actions CI (Python 3.10–3.14); releases publish to PyPI from GitHub

## What’s new in 0.3.0

- New identifiers: IMEI, VIN, EAN-13, UPC-A, ISBN-13
- All identifier generators are importable directly:
  - `from phoney import generate_imei, generate_vin, generate_ean13, generate_upca, generate_isbn13`
- The `Phoney` class exposes both explicit and generate_* convenience methods:
  - `p.imei()`, `p.vin()`, `p.ean13()`, `p.upca()`, `p.isbn13()`
  - `p.generate_imei()`, `p.generate_vin()`, `p.generate_ean13()`, ...
- Internet module hardened:
  - Locale/country-aware IPv4/IPv6 with regional fallbacks; canonical IPv6 formatting
  - TLD preferences per-country; robust domain/hostname/url builders
- Career module: job titles, salary ranges (by locale), skills, employment history
- CLI: `phoney-build-prefixes` to generate per-country IPv4/IPv6 prefix files from RIR datasets
- Packaging cleanup and Python >= 3.10

Quick test after install:
```python
from phoney import generate_imei, Phoney
print(generate_imei())
p = Phoney()
print(p.imei())
print(p.generate_imei())
```

---

## ✨ Features

- **Names for 19 locales** and **phone numbers for 43 countries**, including `en_US`, `fr_FR`, `ja_JP`, `de_DE`, and more
- **Complete profiles** with names, emails, phones, birthdates, and online presence
- **Gender-specific** name generation
- **Usernames, passwords, UUIDs, user agents, and social handles**
- **Financial data** (credit card, IBAN, BIC, etc.)
- **Zero dependencies** — lightweight and fast

---

## 📦 Installation

```bash
pip install phoney
```

---

## 🚀 Basic Usage

```python
from phoney import Phoney

phoney = Phoney()

# Individual data
print(phoney.first_name(locale="it_IT"))  # → "Marco"
print(phoney.phone(locale="ja_JP"))       # → "+81 90 1234 5678"
print(phoney.email(first_name="Anna", last_name="Rossi", locale="it_IT"))

# Complete profile
profile = phoney.profile(locale="es_ES")
print(profile)

# Online presence
print(phoney.username("John", "Smith"))
print(phoney.password())
print(phoney.social_handle("John", "Smith", "twitter"))
print(phoney.online_presence("John", "Smith"))

# User agent and UUID
print(phoney.user_agent())
print(phoney.uuid())
```

---

## 📚 High-Level API: `Phoney` Class

| Method              | Description                                                      |
|---------------------|------------------------------------------------------------------|
| `first_name()`      | Generate first name (optionally by gender/locale)                |
| `last_name()`       | Generate last name (optionally by gender/locale)                 |
| `full_name()`       | Generate full name                                               |
| `gender()`          | Generate gender                                                  |
| `phone()`           | Generate phone number for locale                                 |
| `email()`           | Generate email address                                           |
| `age()`             | Generate random age                                              |
| `birthdate()`       | Generate random birthdate                                        |
| `profile()`         | Generate complete profile (see below)                            |
| `user_agent()`      | Generate browser user agent string                               |
| `uuid()`            | Generate UUID (v1, v3, v4, v5)                                   |
| `username()`        | Generate username from names                                     |
| `password()`        | Generate secure password                                         |
| `social_handle()`   | Generate social media handle for a platform                      |
| `online_presence()` | Generate dict of username, password, and social handles          |
| `tld(locale=None)`  | Generate a TLD with locale bias (e.g., GB → co.uk, JP → .jp)     |
| `domain(tld=None, locale=None)` | Generate a domain name honoring locale/TLD           |
| `hostname(domain=None, locale=None)` | Generate a hostname + domain                   |
| `url(scheme='https', domain=None, path_segments=None, query_params=None, locale=None)` | Generate a URL |
| `ipv4(country=None, locale=None)` | Generate a public-looking IPv4; country/locale-aware |
| `ipv6(global_unicast=True, country=None, locale=None)` | Generate a valid IPv6; country/locale-aware |
| `mac()`             | Generate a locally-administered unicast MAC                      |

---

## 🧩 Profile Structure

```python
{
  'first_name': 'Sophie',
  'last_name': 'Martin',
  'gender': 'female',
  'age': 34,
  'birthdate': datetime.date(1990, 5, 12),
  'email': 'sophie.martin@example.fr',
  'phone': '+33 612 345 678',
  'locale': 'fr_FR'
}
```

---

## 🛠️ Low-Level API: Direct Functions

You can also import and use the following functions directly:

- `generate_person(locale, gender=None)` — dict with first/last name and gender
- `generate_phone(locale)` — phone number for locale
- `generate_email(first_name, last_name, locale, age=None, birth_year=None)`
- `generate_age(min_age=18, max_age=80)` — tuple of (age, birthdate)
- `generate_profile(locale, gender=None, domain=None, uuid_version=4)` — full profile
- `generate_user_agent(device_type="desktop")` — browser user agent string
- `generate_uuid(version=4, domain="example.com", name=None)` — UUID string
- `generate_username(first_name, last_name, locale='en_US')`
- `generate_password(min_length=12, max_length=18)`
- `generate_social_handles(first_name, last_name, platform)`
- `generate_online_presence(first_name, last_name)`

---

## 📦 Modules Overview
**phoney/age.py** — Age and birthdate generation
  - `generate_age(min_age=18, max_age=80)`

**phoney/agent.py** — User agent string generation
  - `generate_user_agent(device_type="desktop")`

**phoney/create_profile.py** — Complete profile generation
  - `generate_profile(locale, gender=None, domain=None, uuid_version=4)`

**phoney/data_loader.py** — Loads locale data, names, phone formats, email domains
  - `load_countries()`, `load_streets()`, `load_cities()`, `load_states()`
  - `get_available_locales()`, `load_names(locale)`, `load_phone_formats()`, `load_email_domains()`

**phoney/emailgen.py** — Email address generation
  - `generate_email(first_name, last_name, locale, age=None, birth_year=None, domain=None)`

**phoney/financial.py** — Financial data generator
  - `FinancialDataGenerator(locale='en_US')` class: `.generate()` for credit card, IBAN, BIC, etc.

**phoney/person.py** — Person name and gender generation
  - `generate_person(locale, gender=None)`

**phoney/phone.py** — Phone number generation
  - `generate_phone(locale=None, max_attempts=500)`

**phoney/username.py** — Username, password, and online presence generation
  - `generate_username()`, `generate_password()`, `generate_social_handles()`, `generate_online_presence()`

**phoney/uuidgen.py** — UUID generation
  - `generate_uuid(version=4, domain="example.com", name=None)`

---

## 🌍 Supported Locales

Name data ships for 19 locales: `ar_EG`, `da_DK`, `de_DE`, `en_GB`, `en_US`, `es_ES`, `fi_FI`, `fr_FR`, `hi_IN`, `it_IT`, `ja_JP`, `ko_KR`, `nl_NL`, `pl_PL`, `pt_BR`, `ru_RU`, `sv_SE`, `tr_TR`, `zh_CN`. Phone numbers cover 43 countries (see `phoney.phone.COUNTRY_CODES`). Unknown locales fall back to generic data rather than raising. To list the name locales:

```python
from phoney.data_loader import get_available_locales
print(get_available_locales())
```

---

## 📜 License

**MIT** — Free for commercial and personal use.
Developed by **rarfile** • [Report Issue](https://github.com/rar-file/phoney/issues)

---

## 🧑‍💼 Career Module

Generate job titles, salary ranges, skills, and employment histories. Data loads from `phoney/data/career` when present.

Examples:
```python
from phoney import phoney
phoney.job_title()
phoney.salary(locale="en_US", family="software_engineer", level="Senior")
phoney.skills("software_engineer", level="Senior", count=10)
phoney.employment_history(years=8, locale="en_US", family="software_engineer")
phoney.experience_level(7)
```

Data files:
- `phoney/data/career/job_families.json`
- `phoney/data/career/skills.json`
- `phoney/data/career/salary_ranges.<locale>.json`
- `phoney/data/career/companies.<locale>.txt`

## 🌐 Internet Module

Generate domains, URLs, hostnames, IP addresses, and MAC addresses. Data loads from `phoney/data/internet` when present.

Examples:
```python
phoney.tld(locale="en_GB")            # → 'co.uk'
phoney.domain(locale="en_GB")         # → 'nova-1abc.co.uk'
phoney.hostname(locale="en_GB")       # → 'api-xyz.nova-1abc.co.uk'
phoney.url(locale="ja_JP")            # → 'https://alpha-zz9.jp/api/q8h2?page=3'
phoney.ipv4(locale="en_GB")           # country-aware IPv4 when data present; RIPE fallback otherwise
phoney.ipv6(locale="ja_JP")           # country/region-aware IPv6; always valid global-unicast
phoney.mac()
```

Data files:
- `phoney/data/internet/tlds.txt`
- `phoney/data/internet/words.txt`
 - `phoney/data/internet/ipv4_prefixes.<CC>.txt`  (optional, one IPv4 CIDR per line)
 - `phoney/data/internet/ipv6_prefixes.<CC>.txt`  (optional, one IPv6 CIDR per line)

Behavior notes:
- Locale parsing accepts `en_GB`, `en-GB`, or bare `GB`.
- IPv4: If `ipv4_prefixes.<CC>.txt` exists, IPs are drawn from those ranges; otherwise a regional fallback is used (e.g., RIPE for Europe, APNIC for Asia/Pacific) and private/reserved ranges are avoided.
- IPv6: If `ipv6_prefixes.<CC>.txt` exists, IPs are drawn from those ranges; otherwise a regional fallback /12 is used:
  - RIPE (Europe): `2a00::/12`
  - APNIC (Asia/Pacific): `2400::/12`
  - ARIN (North America): `2600::/12`
  - LACNIC (LatAm): `2800::/12`
  - AFRINIC (Africa): `2c00::/12`
  If no locale is provided, a valid global-unicast from `2000::/3` is generated. All IPv6 addresses are returned in canonical compressed form.

## 🆔 Other Identifiers

Generate common test identifiers.

Examples:
```python
phoney.imei()                # 15-digit IMEI (Luhn-valid)
phoney.vin()                 # 17-char VIN with check digit
phoney.ean13()               # EAN-13 barcode
phoney.upca()                # UPC-A barcode
phoney.isbn13()              # ISBN-13 (default group '978')
```

Populate per-country prefixes automatically (offline):
1) Download the latest delegated-*-extended-latest files from each RIR to a folder (e.g., `C:/rir-data`):
  - delegated-apnic-extended-latest
  - delegated-arin-extended-latest
  - delegated-ripencc-extended-latest
  - delegated-lacnic-extended-latest
  - delegated-afrinic-extended-latest
2) Run the builder CLI to generate `ipv4_prefixes.<CC>.txt` and `ipv6_prefixes.<CC>.txt` files:
```powershell
phoney-build-prefixes --input-dir C:/rir-data
```
You can also specify a custom output directory:
```powershell
phoney-build-prefixes --input-dir C:/rir-data --output-dir C:/my-prefixes
```

---

## 🧪 Development

```bash
git clone https://github.com/rar-file/phoney
cd phoney
python -m pip install -e ".[test]"
python -m pytest
```

Every push and pull request runs the test suite on Python 3.10–3.14 and builds the package (`.github/workflows/tests.yml`).

### Releasing

1. Bump `__version__` in `phoney/__init__.py`.
2. Create a GitHub release tagged `vX.Y.Z` (matching the version).
3. `.github/workflows/publish.yml` runs the tests, builds, and uploads to PyPI using the `PYPI_API_TOKEN` repository secret.
