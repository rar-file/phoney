__all__ = ['generate_email']
"""Email address generator."""
import random
import re
from datetime import datetime
from .data_loader import load_email_domains

def generate_email(first_name=None, last_name=None, locale='en_US', age=None, birth_year=None, domain=None):
    if not first_name or not last_name:
        from .person import generate_person
        person = generate_person(locale)
        first_name = person['first_name']
        last_name = person['last_name']

    clean_first = re.sub(r'[^a-zA-Z]', '', first_name).lower() or "user"
    clean_last = re.sub(r'[^a-zA-Z]', '', last_name).lower() or "name"
    
    nickname = clean_first[:random.randint(3, min(5, len(clean_first)))] if len(clean_first) > 3 else clean_first
    if random.random() < 0.2 and clean_first.endswith(('y', 'ie')):
        nickname = clean_first.rstrip('yie') + 'ey'
    initials = clean_first[0] + clean_last[0]

    if not domain:
        try:
            domains = load_email_domains().get(locale, ["gmail.com"])
        except:
            domains = ["gmail.com"]
        domain = random.choice(domains)

    sep = random.choices(['', '.', '_'], weights=[2, 5, 3], k=1)[0]

    current_year = datetime.now().year
    if age is None and birth_year is not None:
        age = current_year - birth_year
    elif age is None:
        age = random.randint(13, 65)
    if birth_year is None:
        birth_year = current_year - age

    suffix_type = random.choice(['year', 'age', 'number', 'none', 'alphanum'])
    if suffix_type == 'year':
        suffix = str(birth_year) if random.random() < 0.5 else str(birth_year)[-2:]
    elif suffix_type == 'age':
        suffix = str(age)
    elif suffix_type == 'number':
        suffix = str(random.randint(1, 19999))
    elif suffix_type == 'alphanum':
        suffix = random.choice(['', 
                              f"{random.choice(['', '.', '_'])}{random.randint(10, 999)}",
                              f"{random.choice(['', '.', '_'])}{random.choice('abcdefghjkmnpqrstuvwxyz')}{random.randint(1, 99)}"])
    else:
        suffix = ''

    patterns = [
        f"{clean_first}{sep}{clean_last}{suffix}@{domain}",
        f"{clean_first[0]}{sep}{clean_last}{suffix}@{domain}",
        f"{clean_first}{clean_last}{suffix}@{domain}",
        f"{clean_first[0]}{clean_last}{suffix}@{domain}",
        f"{clean_first}{sep}{clean_last}@{domain}",
        f"{clean_first[0]}{sep}{clean_last}@{domain}",
        f"{nickname}{sep}{clean_last}{suffix}@{domain}",
        f"{clean_last}{sep}{clean_first}{suffix}@{domain}",
        f"{nickname}{sep}{clean_last}{random.randint(1,100)}@{domain}",
    ]

    if random.random() < 0.15:
        non_name_patterns = [
            f"{clean_first[0]}{clean_last}{random.randint(10,9999)}@{domain}",
            f"{nickname}{random.randint(1980, current_year)}@{domain}",
            f"{clean_last[:4]}{clean_first[:2]}{random.randint(1,999)}@{domain}",
            f"{random.choice(['user','mail','contact'])}{random.randint(1000,9999)}@{domain}",
            f"{clean_first[:3]}.{random.randint(1,99)}@{domain}"
        ]
        patterns.extend(non_name_patterns)

    valid_emails = [email for email in patterns if len(email.split('@')[0]) >= 5]
    
    if not valid_emails:
        fallback_local = (
            f"{clean_first}{clean_last}{random.randint(100,999)}" 
            if clean_first and clean_last else
            f"user{random.randint(10000,99999)}"
        )
        valid_emails = [f"{fallback_local}@{domain}"]

    return random.choice(valid_emails)