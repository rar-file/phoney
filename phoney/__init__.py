__all__ = [
    'Phoney', 'phoney',
    'generate_person', 'generate_phone', 'generate_email', 'generate_age',
    'generate_profile', 'generate_user_agent', 'generate_uuid',
    'generate_financial_data', 'generate_online_presence', 'generate_username',
    'generate_password', 'generate_social_handles',
    # Resume
    'generate_resume',
    # Career
    'generate_job_title', 'generate_salary', 'generate_employment_history', 'generate_skills', 'experience_level_from_years',
    # Internet
    'generate_tld', 'generate_domain', 'generate_hostname', 'generate_url', 'generate_ipv4', 'generate_ipv6', 'generate_mac',
    # Identifiers
    'generate_imei', 'generate_vin', 'generate_ean13', 'generate_upca', 'generate_isbn13'
]

import sys
from .person import generate_person
from .phone import generate_phone
from .emailgen import generate_email
from .data_loader import load_email_domains, get_available_locales
from .age import generate_age
from .create_profile import generate_profile
from .agent import generate_user_agent
from .uuidgen import generate_uuid
from .financial import generate_financial_data
from .username import (
    generate_online_presence,
    generate_username,
    generate_password,
    generate_social_handles
)
from .resume import generate_resume
from .career import (
    generate_job_title,
    generate_salary,
    generate_employment_history,
    generate_skills,
    experience_level_from_years,
)
from .internet import (
    generate_tld,
    generate_domain,
    generate_hostname,
    generate_url,
    generate_ipv4,
    generate_ipv6,
    generate_mac,
)
from .imei import generate_imei
from .vin import generate_vin
from .barcode import generate_ean13, generate_upca, generate_isbn13

class Phoney:
    """
    Main class for generating fake data.

    Usage:
        from phoney import Phoney
        phoney = Phoney()
        
        # Basic information
        phoney.first_name(gender="male", locale="en_GB")
        phoney.last_name(locale="fr_FR")
        phoney.phone(locale="en_US")
        phoney.email(first_name="jim", last_name="cooley", locale="en_US")
        
        # Online presence
        phoney.username("John", "Smith")
        phoney.password()
        phoney.social_handle("John", "Smith", "twitter")
        phoney.online_presence("John", "Smith")
        
    # Complete profiles
        phoney.profile(locale="de_DE")
    """
    def __init__(self):
        # Expose all generate_* functions directly on the instance for convenience
        for _name, _fn in list(globals().items()):
            if isinstance(_name, str) and _name.startswith("generate_") and callable(_fn):
                # Instance attribute; avoids binding 'self' like methods do
                try:
                    setattr(self, _name, _fn)
                except Exception:
                    pass
    def first_name(self, gender=None, locale='en_US'):
        """
        Generate a first name.
        Args:
            gender (str): 'male' or 'female'. If None, random.
            locale (str): Locale code (e.g. 'en_US').
        Returns:
            str: First name.
        """
        return generate_person(locale, gender)['first_name']

    def last_name(self, gender=None, locale='en_US'):
        """
        Generate a last name.
        Args:
            gender (str): 'male' or 'female'. If None, random.
            locale (str): Locale code.
        Returns:
            str: Last name.
        """
        return generate_person(locale, gender)['last_name']

    def full_name(self, gender=None, locale='en_US'):
        """
        Generate a full name.
        Args:
            gender (str): 'male' or 'female'. If None, random.
            locale (str): Locale code.
        Returns:
            str: Full name.
        """
        p = generate_person(locale, gender)
        return f"{p['first_name']} {p['last_name']}"

    def gender(self, locale='en_US'):
        """
        Generate a gender value.
        Args:
            locale (str): Locale code.
        Returns:
            str: Gender ('male' or 'female').
        """
        return generate_person(locale)['gender']

    def phone(self, locale='en_US'):
        """
        Generate a phone number for the given locale.
        Args:
            locale (str): Locale code.
        Returns:
            str: Phone number.
        """
        return generate_phone(locale)

    def email(self, first_name=None, last_name=None, locale='en_US', age=None, birth_year=None):
        """
        Generate a realistic email address.
        Args:
            first_name (str): First name. If None, random.
            last_name (str): Last name. If None, random.
            locale (str): Locale code.
            age (int): Age (optional).
            birth_year (int): Birth year (optional).
        Returns:
            str: Email address.
        """
        if not first_name or not last_name:
            p = generate_person(locale)
            first_name = p['first_name']
            last_name = p['last_name']
        return generate_email(first_name, last_name, locale, age=age, birth_year=birth_year)

    def age(self, min_age=18, max_age=80):
        """
        Generate a random age.
        Args:
            min_age (int): Minimum age.
            max_age (int): Maximum age.
        Returns:
            int: Age.
        """
        return generate_age(min_age, max_age)[0]

    def birthdate(self, min_age=18, max_age=80):
        """
        Generate a random birthdate.
        Args:
            min_age (int): Minimum age.
            max_age (int): Maximum age.
        Returns:
            datetime.date: Birthdate.
        """
        return generate_age(min_age, max_age)[1]

    def profile(self, locale='en_US', gender=None):
        """
        Generate a complete fake profile.
        Args:
            locale (str): Locale code.
            gender (str): 'male' or 'female'. If None, random.
        Returns:
            dict: Profile with name, gender, age, birthdate, email, phone, locale.
        """
        return generate_profile(locale, gender)

    def resume(self, locale: str | None = None, family: str | None = None, years: int = 8, format: str = 'dict'):
        """Generate a resume/CV. format in {'dict','text'}."""
        return generate_resume(locale=locale, family=family, years=years, format=format)

    def user_agent(self, device_type="desktop"):
        """
        Generate browser user agent string
        Args:
            device_type: 'desktop' or 'mobile'
        Returns:
            str: User agent string
        """
        return generate_user_agent(device_type)
    
    def uuid(self, version=4):
        """
        Generate UUID
        Args:
            version: UUID version (1,3,4,5)
        Returns:
            str: UUID string
        """
        return generate_uuid(version)
    
    def username(self, first_name=None, last_name=None, locale='en_US'):
        """
        Generate a username based on name components.
        Args:
            first_name (str): First name. If None, generates random.
            last_name (str): Last name. If None, generates random.
            locale (str): Locale for random name generation if needed.
        Returns:
            str: Generated username
        """
        if not first_name or not last_name:
            p = generate_person(locale)
            first_name = p['first_name']
            last_name = p['last_name']
        return generate_username(first_name, last_name)

    def password(self, length=12):
        """
        Generate a secure password.
        Args:
            length (int): Length of password
        Returns:
            str: Generated password
        """
        return generate_password(length)

    def social_handle(self, first_name=None, last_name=None, platform='twitter', locale='en_US'):
        """
        Generate social media handle for specific platform.
        Args:
            first_name (str): First name. If None, generates random.
            last_name (str): Last name. If None, generates random.
            platform (str): Social platform ('twitter', 'instagram', 'tiktok', 'github')
            locale (str): Locale for random name generation if needed.
        Returns:
            str: Social media handle
        """
        if not first_name or not last_name:
            p = generate_person(locale)
            first_name = p['first_name']
            last_name = p['last_name']
        return generate_social_handles(first_name, last_name, platform)

    def online_presence(self, first_name=None, last_name=None, locale='en_US'):
        """
        Generate complete online presence including username and social handles.
        Args:
            first_name (str): First name. If None, generates random.
            last_name (str): Last name. If None, generates random.
            locale (str): Locale for random name generation if needed.
        Returns:
            dict: Online presence data including username, password, and social media handles
        """
        if not first_name or not last_name:
            p = generate_person(locale)
            first_name = p['first_name']
            last_name = p['last_name']
        return generate_online_presence(first_name, last_name)

    # Career
    def job_title(self, family=None, level=None, locale='en_US'):
        return generate_job_title(locale=locale, family=family, level=level)

    def salary(self, family=None, level=None, title=None, locale='en_US'):
        return generate_salary(locale=locale, family=family, level=level, title=title)

    def employment_history(self, years=10, locale='en_US', family=None, min_jobs=1, max_jobs=5):
        return generate_employment_history(years=years, locale=locale, family=family, min_jobs=min_jobs, max_jobs=max_jobs)

    def skills(self, family, level=None, count=None):
        return generate_skills(family=family, level=level, count=count)

    def experience_level(self, years):
        return experience_level_from_years(years)

    # Internet
    def tld(self, locale=None):
        return generate_tld(locale=locale)

    def domain(self, tld=None, locale=None):
        return generate_domain(tld=tld, locale=locale)

    def hostname(self, domain=None, locale=None):
        return generate_hostname(domain=domain, locale=locale)

    def url(self, scheme='https', domain=None, path_segments=None, query_params=None, locale=None):
        return generate_url(scheme=scheme, domain=domain, path_segments=path_segments, query_params=query_params, locale=locale)

    def ipv4(self, country=None, locale=None):
        return generate_ipv4(country=country, locale=locale)

    def ipv6(self, global_unicast=True, country=None, locale=None):
        return generate_ipv6(global_unicast=global_unicast, country=country, locale=locale)

    def mac(self):
        return generate_mac()

    # Other identifiers
    def imei(self, tac=None):
        return generate_imei(tac=tac)

    def vin(self):
        return generate_vin()

    def ean13(self, prefix=""):
        return generate_ean13(prefix=prefix)

    def upca(self, prefix=""):
        return generate_upca(prefix=prefix)

    def isbn13(self, group_prefix="978"):
        return generate_isbn13(group_prefix=group_prefix)

    # Dynamic aliasing for simplicity: allow p.generate_* to call module functions directly.
    def __getattr__(self, name):
        # If someone calls p.generate_imei(...) or any generate_* API,
        # return the top-level function with the same name using the module object.
        if name.startswith("generate_"):
            mod = sys.modules.get(__name__)
            if mod is not None:
                fn = getattr(mod, name, None)
                if callable(fn):
                    return fn
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    # Explicit generate_* wrappers for identifiers for maximum compatibility
    def generate_imei(self, tac=None):
        return generate_imei(tac=tac)

    def generate_vin(self):
        return generate_vin()

    def generate_ean13(self, prefix=""):
        return generate_ean13(prefix=prefix)

    def generate_upca(self, prefix=""):
        return generate_upca(prefix=prefix)

    def generate_isbn13(self, group_prefix="978"):
        return generate_isbn13(group_prefix=group_prefix)

phoney = Phoney()