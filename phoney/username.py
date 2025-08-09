import random
import string
import secrets
from typing import Dict, Optional, Union
from .data_loader import load_names, get_available_locales

_fallback_names_cache = {}

__all__ = [
    'generate_online_presence',
    'generate_username',
    'generate_password',
    'generate_social_handles'
]

ADJECTIVES = [
    "epic", "dark", "shadow", "crazy", "wild", "angry", "lucky", "savage", "pixel", "retro",
    "storm", "neon", "mega", "toxic", "silent", "hyper", "frost", "vortex", "legend", "quantum"
]

NOUNS = [
    "tiger", "wolf", "ninja", "wizard", "dragon", "beast", "hacker", "phoenix", "robot", "pirate",
    "sniper", "ghost", "samurai", "cyber", "warrior", "monkey", "otter", "lion", "mage", "bear"
]

def random_case(text: str) -> str:
    return ''.join(random.choice([c.upper(), c.lower()]) for c in text)

def leetspeak(text: str) -> str:
    mapping = str.maketrans({'a':'4','e':'3','i':'1','o':'0','s':'5','t':'7'})
    return text.translate(mapping)

def insert_random_symbol(name: str) -> str:
    symbol = random.choice(['_', '.', '-', ''])
    pos = random.randint(1, len(name)-1)
    return name[:pos] + symbol + name[pos:]

def generate_person(locale, gender=None):
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

    return {
        'first_name': first_name,
        'last_name': last_name,
        'gender': gender
    }

def _get_locale_fallback_names(locale):
    fallback = {
        'first': ['Alex', 'Chris', 'Jordan', 'Taylor', 'Casey', 'Riley', 'Jamie', 'Sky', 'Ash', 'Morgan'],
        'last': ['Smith', 'Johnson', 'Brown', 'Davis', 'Miller', 'Wilson', 'Anderson', 'Thomas', 'Jackson', 'White']
    }
    return fallback

USERNAME_PATTERNS = [
    lambda f, l: f"{f}{l}",
    lambda f, l: f"{f}_{l}",
    lambda f, l: f"{f}.{l}",
    lambda f, l: f"{f}{random.randint(1,9999)}",
    lambda f, l: leetspeak(f+l),
    lambda f, l: insert_random_symbol(f+l),
    lambda f, l: f"{random.choice(ADJECTIVES)}{l}",
    lambda f, l: f"{f}{random.choice(NOUNS)}",
    lambda f, l: f"{f[:3]}{l[::-1]}",
    lambda f, l: random_case(f+l),
    lambda f, l: f"{random.choice(NOUNS)}{random.randint(100,999)}",
    lambda f, l: f"{f}_{random.choice(['op', 'pro', 'dev', 'fan', 'squad'])}",
]

HANDLE_FORMATS = {
    'twitter': [
        lambda f, l: f"{f}{l}",
        lambda f, l: f"{f}_{l}",
        lambda f, l: leetspeak(f+l),
        lambda f, l: f"{random.choice(ADJECTIVES)}_{l}"
    ],
    'instagram': [
        lambda f, l: f"{f}.{random.choice(NOUNS)}",
        lambda f, l: f"{f}_{random.randint(1,99)}",
        lambda f, l: f"{random.choice(ADJECTIVES)}_{l}"
    ],
    'tiktok': [
        lambda f, l: f"{f}{l[::-1]}",
        lambda f, l: f"{random.choice(['official','real'])}{l}",
        lambda f, l: f"{l}_tv"
    ],
    'github': [
        lambda f, l: f"{f}-{l}",
        lambda f, l: f"{l}-{random.choice(['dev', 'code', 'ai'])}",
        lambda f, l: f"{random.choice(['x', 'dev'])}{l}"
    ],
    'linkedin': [
        lambda f, l: f"{f}-{l}",
        lambda f, l: f"{f}.{l}",
        lambda f, l: f"{f[0]}{l}"
    ],
    'discord': [
        lambda f, l: f"{f}{random.randint(1000,9999)}",
        lambda f, l: f"{random.choice(NOUNS)}{f}"
    ],
    'twitch': [
        lambda f, l: f"{f}_plays",
        lambda f, l: f"{f}{random.choice(['tv','live','stream'])}",
        lambda f, l: f"{random.choice(['live','gaming','streams'])}{f}"
    ]
}

def validate_name(name: Optional[str]) -> bool:
    return bool(name and isinstance(name, str) and name.strip())

def generate_username(first_name: Optional[str] = None, last_name: Optional[str] = None, locale: str = 'en_US') -> str:
    if not first_name or not last_name or not validate_name(first_name) or not validate_name(last_name):
        person = generate_person(locale)
        first_name = person['first_name']
        last_name = person['last_name']
    pattern = random.choice(USERNAME_PATTERNS)
    return pattern(first_name.lower(), last_name.lower())

def generate_password(min_length: int = 12, max_length: int = 18) -> str:
    length = random.randint(min_length, max_length)
    chars = string.ascii_letters + string.digits + "!@#$%^&*()[]{}<>?~"
    while True:
        password = ''.join(secrets.choice(chars) for _ in range(length))
        if (any(c.islower() for c in password) and 
            any(c.isupper() for c in password) and 
            any(c.isdigit() for c in password) and 
            any(c in "!@#$%^&*()[]{}<>?~" for c in password)):
            return password

def generate_social_handles(first_name: Optional[str] = None, last_name: Optional[str] = None,
                          platform: str = 'twitter', locale: str = 'en_US') -> str:
    if not first_name or not last_name:
        person = generate_person(locale)
        first_name = person['first_name']
        last_name = person['last_name']
    if platform not in HANDLE_FORMATS:
        platform = 'twitter'
    formatter = random.choice(HANDLE_FORMATS[platform])
    handle = formatter(first_name.lower(), last_name.lower())
    return f"@{handle}" if platform in ['twitter', 'instagram', 'tiktok'] else handle

def generate_online_presence(first_name: Optional[str] = None, last_name: Optional[str] = None,
                           locale: str = 'en_US') -> Dict[str, Union[str, Dict]]:
    import random
    import string
    import secrets
    from .data_loader import load_names
    ADJECTIVES = [
        "epic", "dark", "shadow", "crazy", "wild", "angry", "lucky", "savage", "pixel", "retro",
        "storm", "neon", "mega", "toxic", "silent", "hyper", "frost", "vortex", "legend", "quantum"
    ]
    NOUNS = [
        "tiger", "wolf", "ninja", "wizard", "dragon", "beast", "hacker", "phoenix", "robot", "pirate",
        "sniper", "ghost", "samurai", "cyber", "warrior", "monkey", "otter", "lion", "mage", "bear"
    ]
    def random_case(text: str) -> str:
        return ''.join(random.choice([c.upper(), c.lower()]) for c in text)
    def leetspeak(text: str) -> str:
        mapping = str.maketrans({'a':'4','e':'3','i':'1','o':'0','s':'5','t':'7'})
        return text.translate(mapping)
    def insert_random_symbol(name: str) -> str:
        symbol = random.choice(['_', '.', '-', ''])
        pos = random.randint(1, len(name)-1)
        return name[:pos] + symbol + name[pos:]
    def validate_name(name):
        return bool(name and isinstance(name, str) and name.strip())
    def generate_person(locale, gender=None):
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
                fallback = {
                    'first': ['Alex', 'Chris', 'Jordan', 'Taylor', 'Casey', 'Riley', 'Jamie', 'Sky', 'Ash', 'Morgan'],
                    'last': ['Smith', 'Johnson', 'Brown', 'Davis', 'Miller', 'Wilson', 'Anderson', 'Thomas', 'Jackson', 'White']
                }
                first_name = random.choice(fallback['first'])
        last_name = None
        if names['last']:
            last_name = random.choice(names['last'])
        if not last_name:
            fallback = {
                'first': ['Alex', 'Chris', 'Jordan', 'Taylor', 'Casey', 'Riley', 'Jamie', 'Sky', 'Ash', 'Morgan'],
                'last': ['Smith', 'Johnson', 'Brown', 'Davis', 'Miller', 'Wilson', 'Anderson', 'Thomas', 'Jackson', 'White']
            }
            last_name = random.choice(fallback['last'])
        return {
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender
        }
    USERNAME_PATTERNS = [
        lambda f, l: f"{f}{l}",
        lambda f, l: f"{f}_{l}",
        lambda f, l: f"{f}.{l}",
        lambda f, l: f"{f}{random.randint(1,9999)}",
        lambda f, l: leetspeak(f+l),
        lambda f, l: insert_random_symbol(f+l),
        lambda f, l: f"{random.choice(ADJECTIVES)}{l}",
        lambda f, l: f"{f}{random.choice(NOUNS)}",
        lambda f, l: f"{f[:3]}{l[::-1]}",
        lambda f, l: random_case(f+l),
        lambda f, l: f"{random.choice(NOUNS)}{random.randint(100,999)}",
        lambda f, l: f"{f}_{random.choice(['op', 'pro', 'dev', 'fan', 'squad'])}",
    ]
    HANDLE_FORMATS = {
        'twitter': [
            lambda f, l: f"{f}{l}",
            lambda f, l: f"{f}_{l}",
            lambda f, l: leetspeak(f+l),
            lambda f, l: f"{random.choice(ADJECTIVES)}_{l}"
        ],
        'instagram': [
            lambda f, l: f"{f}.{random.choice(NOUNS)}",
            lambda f, l: f"{f}_{random.randint(1,99)}",
            lambda f, l: f"{random.choice(ADJECTIVES)}_{l}"
        ],
        'tiktok': [
            lambda f, l: f"{f}{l[::-1]}",
            lambda f, l: f"{random.choice(['official','real'])}{l}",
            lambda f, l: f"{l}_tv"
        ],
        'github': [
            lambda f, l: f"{f}-{l}",
            lambda f, l: f"{l}-{random.choice(['dev', 'code', 'ai'])}",
            lambda f, l: f"{random.choice(['x', 'dev'])}{l}"
        ],
        'linkedin': [
            lambda f, l: f"{f}-{l}",
            lambda f, l: f"{f}.{l}",
            lambda f, l: f"{f[0]}{l}"
        ],
        'discord': [
            lambda f, l: f"{f}{random.randint(1000,9999)}",
            lambda f, l: f"{random.choice(NOUNS)}{f}"
        ],
        'twitch': [
            lambda f, l: f"{f}_plays",
            lambda f, l: f"{f}{random.choice(['tv','live','stream'])}",
            lambda f, l: f"{random.choice(['live','gaming','streams'])}{f}"
        ]
    }
    if not first_name or not last_name or not validate_name(first_name) or not validate_name(last_name):
        person = generate_person(locale)
        first_name = person['first_name']
        last_name = person['last_name']
    def generate_username(first_name, last_name):
        pattern = random.choice(USERNAME_PATTERNS)
        return pattern(first_name.lower(), last_name.lower())
    def generate_password(min_length: int = 12, max_length: int = 18):
        length = random.randint(min_length, max_length)
        chars = string.ascii_letters + string.digits + "!@#$%^&*()[]{}<>?~"
        while True:
            password = ''.join(secrets.choice(chars) for _ in range(length))
            if (any(c.islower() for c in password) and 
                any(c.isupper() for c in password) and 
                any(c.isdigit() for c in password) and 
                any(c in "!@#$%^&*()[]{}<>?~" for c in password)):
                return password
    def generate_social_handles(first_name, last_name, platform):
        if platform not in HANDLE_FORMATS:
            platform = 'twitter'
        formatter = random.choice(HANDLE_FORMATS[platform])
        handle = formatter(first_name.lower(), last_name.lower())
        return f"@{handle}" if platform in ['twitter', 'instagram', 'tiktok'] else handle
    return {
        'username': generate_username(first_name, last_name),
        'password': generate_password(),
        'social_media': {
            'twitter': generate_social_handles(first_name, last_name, 'twitter'),
            'instagram': generate_social_handles(first_name, last_name, 'instagram'),
            'tiktok': generate_social_handles(first_name, last_name, 'tiktok'),
            'github': generate_social_handles(first_name, last_name, 'github'),
            'linkedin': generate_social_handles(first_name, last_name, 'linkedin'),
            'discord': generate_social_handles(first_name, last_name, 'discord'),
            'twitch': generate_social_handles(first_name, last_name, 'twitch')
        },
        'person': {'first_name': first_name, 'last_name': last_name}
    }