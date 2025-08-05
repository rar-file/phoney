__all__ = ['generate_profile']
# phoney/profile.py
"""Complete profile generator."""
import random
from .person import generate_person
from .phone import generate_phone
from .emailgen import generate_email
from .age import generate_age

def generate_profile(locale=None, gender=None):
    """
    Generate a complete personal profile.
    
    Args:
        locale: Locale to use for generation (random if not specified)
        gender: Gender to use for generation (random if not specified)
        
    Returns:
        dict: Complete profile dictionary
    """
    if locale is None:
        from .data_loader import get_available_locales
        locale = random.choice(get_available_locales())
    
    person = generate_person(locale, gender)
    first_name = person['first_name']
    last_name = person['last_name']
    gender = person['gender']

    age, birthdate = generate_age()
    birth_year = birthdate.year

    phone = generate_phone(locale)
    email = generate_email(first_name, last_name, locale)

    return {
        'first_name': first_name,
        'last_name': last_name,
        'full_name': f"{first_name} {last_name}",
        'gender': gender,
        'age': age,
        'birthdate': birthdate.isoformat(),
        'email': email,
        'phone': phone,
        'locale': locale
    }