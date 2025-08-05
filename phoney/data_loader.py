# phoney/data_loader.py
"""Data loader for locale-specific information."""
import os
import random
import json
from collections import defaultdict

BASE_DIR = os.path.join(os.path.dirname(__file__), 'data', 'name_data')

def get_available_locales():
    """Get all available locales from the name_data directory."""
    locales = []
    for region in os.listdir(BASE_DIR):
        region_path = os.path.join(BASE_DIR, region)
        if os.path.isdir(region_path):
            for locale in os.listdir(region_path):
                locale_path = os.path.join(region_path, locale)
                if os.path.isdir(locale_path):
                    locales.append(locale)
    return locales

def load_names(locale):
    """Load names for a specific locale."""
    names = {'male': [], 'female': [], 'last': []}
    
    for region in os.listdir(BASE_DIR):
        locale_path = os.path.join(BASE_DIR, region, locale)
        if os.path.exists(locale_path):
            for gender in names.keys():
                file_path = os.path.join(locale_path, f"{gender}.txt")
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        names[gender] = [line.strip() for line in f if line.strip()]
            break
    
    return names

def load_phone_formats():
    """Load phone number formats from JSON file."""
    formats_path = os.path.join(os.path.dirname(__file__), 'data', 'phone_formats.json')
    with open(formats_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_email_domains():
    """Load email domains from JSON file."""
    domains_path = os.path.join(os.path.dirname(__file__), 'data', 'email_domains.json')
    with open(domains_path, 'r', encoding='utf-8') as f:
        return json.load(f)