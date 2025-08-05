__all__ = ['generate_age']
# phoney/age.py
"""Age and birthdate generator."""
import random
from datetime import datetime, timedelta

def generate_age(min_age=18, max_age=80):
    """
    Generate a random age and corresponding birthdate.
    
    Args:
        min_age: Minimum age to generate
        max_age: Maximum age to generate
        
    Returns:
        tuple: (age, birthdate) where birthdate is a datetime.date object
    """
    current_date = datetime.now().date()
    birth_year = random.randint(current_date.year - max_age, current_date.year - min_age)
    birth_month = random.randint(1, 12)
    if birth_month == 2:
        max_day = 29 if (birth_year % 4 == 0 and birth_year % 100 != 0) or (birth_year % 400 == 0) else 28
    else:
        max_day = 30 if birth_month in [4, 6, 9, 11] else 31
    birth_day = random.randint(1, max_day)
    birthdate = datetime(birth_year, birth_month, birth_day).date()

    age = current_date.year - birthdate.year
    if (current_date.month, current_date.day) < (birthdate.month, birthdate.day):
        age -= 1

    return age, birthdate