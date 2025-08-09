__all__ = ['generate_profile']

import random
import uuid
from datetime import datetime

from .person import generate_person
from .phone import generate_phone
from .emailgen import generate_email
from .age import generate_age
from .agent import generate_user_agent
from .data_loader import get_available_locales
from .username import generate_username
from .finacial import FinancialDataGenerator

def generate_profile(locale=None, gender=None, domain=None, uuid_version=4):
    if locale is None:
        locale = random.choice(get_available_locales())
    
    person = generate_person(locale, gender)
    first_name = person['first_name']
    last_name = person['last_name']
    gender = person['gender']

    age, birthdate = generate_age()
    birth_year = birthdate.year

    phone = generate_phone(locale)
    email = generate_email(first_name, last_name, locale, domain=domain)
    
    user_agent = generate_user_agent()
    
    if uuid_version in (3, 5):
        namespace = uuid.NAMESPACE_DNS
        name = f"{first_name}.{last_name}@{domain if domain else 'example.com'}"
        profile_uuid = str(uuid.uuid3(namespace, name)) if uuid_version == 3 else str(uuid.uuid5(namespace, name))
    elif uuid_version == 1:
        profile_uuid = str(uuid.uuid1())
    else:
        profile_uuid = str(uuid.uuid4())
    
    created_at = datetime.now().isoformat()

    username = generate_username(first_name, last_name, locale)
    credit_card_info = FinancialDataGenerator(locale).generate()['credit_card']

    return {
        'uuid': profile_uuid,
        'first_name': first_name,
        'last_name': last_name,
        'full_name': f"{first_name} {last_name}",
        'gender': gender,
        'age': age,
        'birthdate': birthdate.isoformat(),
        'birth_year': birth_year,
        'email': email,
        'phone': phone,
        'user_agent': user_agent,
        'username': username,
        'credit_card': credit_card_info,
        'locale': locale,
        'created_at': created_at
    }