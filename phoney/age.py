__all__ = ['generate_age']
# phoney/age.py
"""Age and birthdate generator."""
import random
from datetime import datetime, timedelta

def _years_before(day, years):
    """Return the same calendar day `years` earlier (Feb 29 becomes Feb 28)."""
    try:
        return day.replace(year=day.year - years)
    except ValueError:
        return day.replace(year=day.year - years, day=28)

def generate_age(min_age=18, max_age=80):
    """
    Generate a random age and corresponding birthdate.
    
    Args:
        min_age: Minimum age to generate
        max_age: Maximum age to generate
        
    Returns:
        tuple: (age, birthdate) where birthdate is a datetime.date object
    """
    if min_age > max_age:
        raise ValueError("min_age must not be greater than max_age")
    current_date = datetime.now().date()
    # Anyone born in (today - (max_age + 1) years, today - min_age years] is
    # currently between min_age and max_age, so pick a birthdate in that window.
    latest = _years_before(current_date, min_age)
    earliest = _years_before(current_date, max_age + 1) + timedelta(days=1)
    birthdate = earliest + timedelta(days=random.randint(0, (latest - earliest).days))

    age = current_date.year - birthdate.year
    if (current_date.month, current_date.day) < (birthdate.month, birthdate.day):
        age -= 1

    return age, birthdate