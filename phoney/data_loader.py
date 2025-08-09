def load_countries():
    """Load country codes and names. Fallback to common countries if data is missing."""
    # You can later load from a file if you want
    return {
        'US': 'United States',
        'GB': 'United Kingdom',
        'FR': 'France',
        'DE': 'Germany',
        'IT': 'Italy',
        'ES': 'Spain',
        'JP': 'Japan',
        'CN': 'China',
        'RU': 'Russia',
        'BR': 'Brazil',
    }

def load_streets():
    """Load street names for locales. Fallback to generic names."""
    return {
        'en_US': ['Main Street', 'Broadway', 'Elm St', 'Maple Ave'],
        'de_DE': ['Hauptstraße', 'Bahnhofstraße', 'Gartenweg'],
        'fr_FR': ['Rue de Paris', 'Avenue Victor Hugo'],
        'default': ['Main Street']
    }

def load_cities():
    """Load city names for locales. Fallback to generic names."""
    return {
        'en_US': ['New York', 'Los Angeles', 'Chicago'],
        'de_DE': ['Berlin', 'Munich', 'Hamburg'],
        'fr_FR': ['Paris', 'Lyon', 'Marseille'],
        'default': ['Metropolis']
    }

def load_states():
    """Load state names for locales. Fallback to generic names."""
    return {
        'en_US': ['CA', 'NY', 'TX'],
        'de_DE': ['Bayern', 'Berlin'],
        'fr_FR': ['Île-de-France', 'Provence'],
        'default': ['State']
    }
    
import random
import json
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

def get_available_locales():
    """Get all available locales from the name_data directory."""
    locales = [locale_dir.name for region_dir in (DATA_DIR / "name_data").iterdir() for locale_dir in region_dir.iterdir()]
    
    return locales

def load_names(locale):
    """Load names for a specific locale."""
    names = {}
    
    for region_dir in (DATA_DIR / "name_data").iterdir():
        locale_dir = region_dir / locale
        if locale_dir.exists():
            for gender_file in locale_dir.iterdir():
                with gender_file.open() as f:
                    names[gender_file.stem] = [line.strip() for line in f if line.strip()]
            break
    return names
    
def load_phone_formats():
    """Load phone number formats from JSON file."""
    with (DATA_DIR / "phone_formats.json").open() as f:
        return json.load(f)

def load_email_domains():
    """Load email domains from JSON file."""
    with (DATA_DIR / "email_domains.json").open() as f:
        return json.load(f)