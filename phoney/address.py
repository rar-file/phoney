# phoney/address.py
__all__ = ['generate_address']
"""Address generator with postal codes using real-world data."""

import random
import requests

_COUNTRY_DATA = None

def _get_country_data():
    """Fetch real country data (cached)"""
    global _COUNTRY_DATA
    if _COUNTRY_DATA is None:
        response = requests.get("https://restcountries.com/v3.1/all")
        _COUNTRY_DATA = response.json()
    return _COUNTRY_DATA

def generate_address(locale='en_US'):
    """Generate realistic address with postal codes"""
    countries = _get_country_data()
    country = random.choice(countries)
    
    street_num = random.randint(1, 9999)
    street_name = " ".join(random.choices([
        "Main", "Oak", "Maple", "Cedar", "Elm", "Pine", "Birch", "View", "Hill"
    ], k=2)) + " " + random.choice(["St", "Ave", "Rd", "Blvd", "Dr"])
    
    city = random.choice(country.get("capital", ["Unknown City"]))
    
    postal_format = country.get("postalCode", {}).get("format", "#####")
    postal_code = "".join([
        random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") if char == "@" 
        else random.choice("0123456789") if char == "#"
        else char for char in postal_format
    ])
    
    return {
        "street": f"{street_num} {street_name}",
        "city": city,
        "state": random.choice(list(country.get("states", {})).values()) if "states" in country else "N/A",
        "postal_code": postal_code,
        "country": country["name"]["common"],
        "country_code": country["cca2"]
    }