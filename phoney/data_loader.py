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

import os
import random
import json
from collections import defaultdict

BASE_DIR = os.path.join(os.path.dirname(__file__), 'data', 'name_data')

def get_available_locales():
    """Get all available locales from the name_data directory."""
    locales = []
    try:
        for region in os.listdir(BASE_DIR):
            region_path = os.path.join(BASE_DIR, region)
            if os.path.isdir(region_path):
                for locale in os.listdir(region_path):
                    locale_path = os.path.join(region_path, locale)
                    if os.path.isdir(locale_path):
                        locales.append(locale)
    except FileNotFoundError:
        pass
    return locales

def load_names(locale):
    """Load names for a specific locale."""
    names = {'male': [], 'female': [], 'last': []}
    try:
        for region in os.listdir(BASE_DIR):
            locale_path = os.path.join(BASE_DIR, region, locale)
            if os.path.exists(locale_path):
                for gender in names.keys():
                    file_path = os.path.join(locale_path, f"{gender}.txt")
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            names[gender] = [line.strip() for line in f if line.strip()]
                break
    except FileNotFoundError:
        pass
    return names

def load_phone_formats():
    """Load phone number formats from JSON file."""
    formats_path = os.path.join(os.path.dirname(__file__), 'data', 'phone_formats.json')
    try:
        with open(formats_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_email_domains():
    """Load email domains from JSON file."""
    domains_path = os.path.join(os.path.dirname(__file__), 'data', 'email_domains.json')
    try:
        with open(domains_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}