# Phoney

Phoney is a Python library for generating realistic fake personal data, similar to Faker. It can create names, phone numbers, emails, ages, birthdates, and full profiles for many locales.

## Features
- Generate first names, last names, and full names
- Locale-aware phone numbers and emails
- Realistic age and birthdate generation
- Complete fake profiles (name, gender, age, birthdate, email, phone, locale)
- Easy-to-use API: `phoney = Phoney()`

## Installation
```bash
pip install phoney
```

## Usage
```python
from phoney import Phoney
phoney = Phoney()

print(phoney.first_name(gender="male", locale="en_GB"))
print(phoney.last_name(locale="fr_FR"))
print(phoney.phone(locale="en_US"))
print(phoney.email(first_name="jim", last_name="cooley", locale="en_US"))
print(phoney.profile(locale="de_DE"))
```

## License
MIT

## Author
rarfile
