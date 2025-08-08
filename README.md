# 🌐 Phoney - Realistic Fake Data Generator

[![PyPI Version](https://img.shields.io/pypi/v/phoney?color=blue)](https://pypi.org/project/phoney/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/phoney)](https://pypi.org/project/phoney/)

Phoney is a lightweight Python library for generating realistic fake personal data. Designed for developers, testers, and data engineers, Phoney supports over 50 locales and produces customizable profiles for testing, anonymization, or populating dummy datasets.

## Features

* 50+ supported locales (e.g., `en_US`, `fr_FR`, `ja_JP`)
* Complete personal profiles with names, birthdates, phones, and emails
* Gender-specific name generation
* Zero dependencies

## Installation

```bash
pip install phoney
```

## Usage Example

```python
from phoney import Phoney

phoney = Phoney()

print(phoney.first_name(locale="it_IT"))
print(phoney.phone(locale="ja_JP"))
print(phoney.profile(locale="es_ES"))
```

## API Overview

| Method         | Description                           |
| -------------- | ------------------------------------- |
| `first_name()` | Generate a first name                 |
| `last_name()`  | Generate a last name                  |
| `full_name()`  | Full name with optional gender/locale |
| `phone()`      | Locale-aware phone number             |
| `email()`      | Generate a synthetic email address    |
| `profile()`    | Generate a complete personal profile  |

## Sample Profile Output

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

## License

MIT License

Developed by [rarfile](https://github.com/YTstyo/phoney). [Issue Tracker](https://github.com/YTstyo/phoney/issues)
