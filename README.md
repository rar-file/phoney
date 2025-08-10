
# Phoney - Realistic Fake Data Generator

[![PyPI Version](https://img.shields.io/pypi/v/phoney?color=blue)](https://pypi.org/project/phoney/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/phoney)](https://pypi.org/project/phoney/)

Generate locale-aware fake personal data for testing, development, and anonymization. Perfect for populating databases and creating test users.

---

## ✨ Features

- **50+ locales** including `en_US`, `fr_FR`, `ja_JP`, `de_DE`, and more
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
print(phoney.phone(locale="ja_JP"))       # → "+81 90-1234-5678"
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
  'phone': '+33 6 12 34 56 78',
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

**phoney/finacial.py** — Financial data generator
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

Phoney supports 50+ locales across Asia, Europe, the Middle East, and the Americas. To list all available locales:

```python
from phoney.data_loader import get_available_locales
print(get_available_locales())
```

---

## 📜 License

**MIT** — Free for commercial and personal use.
Developed by **rarfile** • [Report Issue](https://github.com/YTstyo/phoney/issues)
