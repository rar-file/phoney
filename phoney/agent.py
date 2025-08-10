# phoney/agent.py
__all__ = ['generate_user_agent']
"""User agent generator for web scraping and testing."""
import random

_USER_AGENTS = {
    "desktop": [
        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
        # Firefox
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{version}) Gecko/20100101 Firefox/{version}",
        # Safari
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Safari/605.1.15",
    ],
    "mobile": [
        # Android
        "Mozilla/5.0 (Linux; Android {android_version}; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Mobile Safari/537.36",
        # iOS
        "Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{version} Mobile/15E148 Safari/604.1"
    ]
}

_VERSION_RANGES = {
    "chrome": (100, 125),
    "firefox": (115, 125),
    "safari": (15, 17),
    "android": (10, 14),
    "ios": (15, 17)
}

def generate_user_agent(device_type="desktop"):
    """Generate realistic user agent string"""
    templates = _USER_AGENTS.get(device_type, _USER_AGENTS["desktop"])
    template = random.choice(templates)
    
    if "Chrome" in template:
        version = random.randint(*_VERSION_RANGES["chrome"])
    elif "Firefox" in template:
        version = random.randint(*_VERSION_RANGES["firefox"])
    else:
        version = random.randint(*_VERSION_RANGES["safari"])
    
    if "{android_version}" in template:
        template = template.replace("{android_version}", str(random.randint(10, 14)))
    if "{ios_version}" in template:
        template = template.replace("{ios_version}", str(random.randint(15, 17)))
    
    return template.replace("{version}", str(version))