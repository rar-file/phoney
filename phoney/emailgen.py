__all__ = ['generate_email']
"""Email address generator."""
import random
import re
from datetime import datetime
from .data_loader import load_email_domains

def generate_email(first_name, last_name, locale):
    """
    Generate a realistic email address based on name and locale.
    Args:
        first_name: First name of the person
        last_name: Last name of the person
        locale: Locale to determine email domain
    Returns:
        str: Generated email address
    """
    clean_first = re.sub(r'[^a-zA-Z]', '', first_name).lower() or "user"
    clean_last = re.sub(r'[^a-zA-Z]', '', last_name).lower() or "name"

    nickname = clean_first[:random.randint(3, min(5, len(clean_first)))] if len(clean_first) > 3 else clean_first
    initials = clean_first[0] + clean_last[0]

    if random.random() < 0.2 and clean_first.endswith(('y', 'ie')):
        nickname = clean_first.rstrip('yie') + 'ey'

    domain = random.choice(load_email_domains().get(locale, ["gmail.com"]))
    sep_choices = ['', '.', '_']
    sep = random.choices(sep_choices, weights=[2, 5, 3], k=1)[0]

    import inspect
    frame = inspect.currentframe().f_back
    age = frame.f_locals.get('age', None)
    birth_year = frame.f_locals.get('birth_year', None)
    current_year = datetime.now().year
    if age is None:
        age = random.randint(13, 65)
    if birth_year is None:
        birth_year = current_year - age

    suffix_type = random.choice(['year', 'age', 'number', 'none'])
    if suffix_type == 'year':
        suffix = str(birth_year) if random.random() < 0.5 else str(birth_year)[-2:]
    elif suffix_type == 'age':
        suffix = str(age)
    elif suffix_type == 'number':
        suffix = str(random.randint(1, 19999))
    else:
        suffix = ''

    patterns = []
    patterns.append(f"{clean_first}{sep}{clean_last}{suffix}@{domain}")
    patterns.append(f"{clean_first[0]}{sep}{clean_last}{suffix}@{domain}")
    patterns.append(f"{clean_first}{clean_last}{suffix}@{domain}")
    patterns.append(f"{clean_first[0]}{clean_last}{suffix}@{domain}")
    patterns.append(f"{clean_first}{sep}{clean_last}@{domain}")
    patterns.append(f"{clean_first}{clean_last}@{domain}")
    patterns.append(f"{clean_first[0]}{sep}{clean_last}@{domain}")
    patterns.append(f"{clean_first}{clean_last[0]}@{domain}")
    patterns.append(f"{initials}{suffix}@{domain}")
    patterns.append(f"{nickname}{sep}{clean_last}{suffix}@{domain}")
    patterns.append(f"{clean_last}{sep}{clean_first}{suffix}@{domain}")
    patterns.append(f"{clean_first}{suffix}@{domain}")
    patterns.append(f"{nickname}{sep}{clean_last}@{domain}")
    patterns.append(f"{clean_last}{sep}{clean_first}@{domain}")

    random.shuffle(patterns)
    email = random.choice(patterns)
    return email
