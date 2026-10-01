__all__ = ['generate_person', 'format_full_name', 'feminine_surname']
# phoney/person.py
"""Person information generator."""
import random
import os
from .data_loader import load_names, get_available_locales

_fallback_names_cache = {}

def generate_person(locale, gender=None):
    """
    Generate a person with first name, last name, and gender.
    
    Args:
        locale: The locale to use for name generation (e.g., 'en_US')
        gender: Specific gender to generate ('male' or 'female'), or random if None
        
    Returns:
        dict: Dictionary with first_name, last_name, and gender
    """
    names = load_names(locale)
    
    if gender is None:
        gender = random.choice(['male', 'female'])
    
    first_name = None
    if gender == 'male' and names['male']:
        first_name = random.choice(names['male'])
    elif gender == 'female' and names['female']:
        first_name = random.choice(names['female'])
    
    if not first_name:
        all_first = names['male'] + names['female']
        if all_first:
            first_name = random.choice(all_first)
        else:
            if locale not in _fallback_names_cache:
                _fallback_names_cache[locale] = _get_locale_fallback_names(locale)
            fallback = _fallback_names_cache[locale]
            first_name = random.choice(fallback['first'])
    
    last_name = None
    if names['last']:
        last_name = random.choice(names['last'])
    
    if not last_name:
        if locale not in _fallback_names_cache:
            _fallback_names_cache[locale] = _get_locale_fallback_names(locale)
        fallback = _fallback_names_cache[locale]
        last_name = random.choice(fallback['last'])
    
    if gender == 'female':
        last_name = feminine_surname(last_name, locale)

    return {
        'first_name': first_name,
        'last_name': last_name,
        'full_name': format_full_name(first_name, last_name, locale),
        'gender': gender
    }

# Locales that write the family name first, and whether a space separates the parts.
_FAMILY_NAME_FIRST = {'zh': '', 'ja': '', 'ko': '', 'vi': ' ', 'hu': ' '}

def format_full_name(first_name, last_name, locale='en_US'):
    """Join a given and family name in the order used by the locale.

    "Anna Smith" for en_US, "王伟" for zh_CN, "Nguyễn Văn An" for vi_VN.
    """
    sep = _FAMILY_NAME_FIRST.get((locale or '').split('_')[0])
    if sep is None:
        return f"{first_name} {last_name}"
    return f"{last_name}{sep}{first_name}"

# (masculine ending, feminine ending), longest endings first.
_FEMININE_ENDINGS = {
    'ru': [('ский', 'ская'), ('цкий', 'цкая'), ('ий', 'ая'), ('ый', 'ая'), ('ой', 'ая'),
           ('ов', 'ова'), ('ев', 'ева'), ('ёв', 'ёва'), ('ин', 'ина'), ('ын', 'ына')],
    'pl': [('ski', 'ska'), ('cki', 'cka'), ('dzki', 'dzka')],
    'cs': [('ý', 'á'), ('í', 'í'), ('ů', 'ů'), ('o', 'o'), ('ek', 'ková'), ('ec', 'cová'),
           ('a', 'ová'), ('e', 'ová'), ('ě', 'ová'), ('', 'ová')],
    'el': [('όπουλος', 'οπούλου'), ('ίδης', 'ίδου'), ('άδης', 'άδου'), ('ής', 'ή'), ('ης', 'η'),
           ('ός', 'ού'), ('ος', 'ου'), ('άς', 'ά'), ('ας', 'α')],
}

def feminine_surname(last_name, locale='en_US'):
    """Return the feminine form of a gendered surname (Иванов -> Иванова, Novák -> Nováková).

    Surnames in locales without gendered forms are returned unchanged.
    """
    rules = _FEMININE_ENDINGS.get((locale or '').split('_')[0])
    if not rules:
        return last_name
    for masculine, feminine in sorted(rules, key=lambda r: -len(r[0])):
        if last_name.endswith(masculine):
            return last_name[:len(last_name) - len(masculine)] + feminine
    return last_name

def _get_locale_fallback_names(locale):
    """Get culturally appropriate fallback names for a locale"""
    fallback = {
        'first': ['Min', 'Ji', 'Ahn', 'Soo', 'Jae'],
        'last': ['Kim', 'Lee', 'Park', 'Choi', 'Jung']
    }
    
    if locale.startswith('ko'):
        fallback = {
            'first': ['Min', 'Ji', 'Ahn', 'Soo', 'Jae'],
            'last': ['Kim', 'Lee', 'Park', 'Choi', 'Jung']
        }
    elif locale.startswith('ja'):
        fallback = {
            'first': ['Aki', 'Haru', 'Kai', 'Ren', 'Yui'],
            'last': ['Sato', 'Suzuki', 'Takahashi', 'Tanaka', 'Watanabe']
        }
    elif locale.startswith('zh'):
        fallback = {
            'first': ['Wei', 'Ming', 'Jian', 'Li', 'Mei'],
            'last': ['Wang', 'Li', 'Zhang', 'Liu', 'Chen']
        }
    elif locale.startswith('ar'):
        fallback = {
            'first': ['Mohamed', 'Ahmed', 'Ali', 'Fatima', 'Aisha'],
            'last': ['Hassan', 'Ali', 'Ahmed', 'Mohamed', 'Ibrahim']
        }
    elif locale.startswith('ru'):
        fallback = {
            'first': ['Alexei', 'Dmitri', 'Ivan', 'Olga', 'Natalia'],
            'last': ['Ivanov', 'Smirnov', 'Kuznetsov', 'Popov', 'Sokolov']
        }
    
    return fallback