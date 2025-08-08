__all__ = ['generate_agent']
# phoney/agent.py
"""User agent generator for web scraping and testing."""
import random

_USER_AGENTS = {
    "desktop": [
        # Chrome Windows
        "Mozilla/5.0 (Windows NT {win_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36",
        # Chrome macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36",
        # Chrome Linux
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36",
        # Firefox Windows
        "Mozilla/5.0 (Windows NT {win_ver}; Win64; x64; rv:{firefox_ver}) Gecko/20100101 Firefox/{firefox_ver}",
        # Firefox macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}; rv:{firefox_ver}) Gecko/20100101 Firefox/{firefox_ver}",
        # Firefox Linux
        "Mozilla/5.0 (X11; Linux x86_64; rv:{firefox_ver}) Gecko/20100101 Firefox/{firefox_ver}",
        # Safari macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari_ver} Safari/605.1.15",
        # Edge Windows
        "Mozilla/5.0 (Windows NT {win_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36 Edg/{edge_ver}",
        # Edge macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X {mac_ver}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36 Edg/{edge_ver}",
        # Opera Windows
        "Mozilla/5.0 (Windows NT {win_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36 OPR/{opera_ver}",
    ],
    "mobile": [
        # Android Chrome
        "Mozilla/5.0 (Linux; Android {android_ver}; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36",
        # Android Firefox
        "Mozilla/5.0 (Android {android_ver}; Mobile; rv:{firefox_ver}) Gecko/{firefox_ver} Firefox/{firefox_ver}",
        # iOS Safari (iPhone)
        "Mozilla/5.0 (iPhone; CPU iPhone OS {ios_ver} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari_ver} Mobile/15E148 Safari/604.1",
        # iOS Safari (iPad)
        "Mozilla/5.0 (iPad; CPU OS {ios_ver} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari_ver} Mobile/15E148 Safari/604.1",
        # Android Edge
        "Mozilla/5.0 (Linux; Android {android_ver}; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36 EdgA/{edge_ver}",
        # iOS Edge
        "Mozilla/5.0 (iPhone; CPU iPhone OS {ios_ver} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari_ver} EdgiOS/{edge_ver} Mobile/15E148 Safari/605.1.15",
        # Android Opera
        "Mozilla/5.0 (Linux; Android {android_ver}; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Mobile Safari/537.36 OPR/{opera_ver}",
    ]
}

_VERSION_RANGES = {
    "chrome": (100, 125),
    "firefox": (115, 125),
    "safari": (15, 17),
    "edge": (100, 125),
    "opera": (80, 100),
    "android": (10, 14),
    "ios": (15, 17),
}

_OS_VERSIONS = {
    "win": ["10.0", "6.3", "6.2", "6.1"],
    "mac": ["10_15_7", "11_0_0", "12_0_0", "13_0_0", "14_0_0"],
}

def generate_user_agent(device_type="desktop"):
    templates = _USER_AGENTS.get(device_type, _USER_AGENTS["desktop"])
    template = random.choice(templates)
    
    replacements = {
        "chrome_ver": str(random.randint(*_VERSION_RANGES["chrome"])),
        "firefox_ver": str(random.randint(*_VERSION_RANGES["firefox"])),
        "safari_ver": str(random.randint(*_VERSION_RANGES["safari"])),
        "edge_ver": str(random.randint(*_VERSION_RANGES["edge"])),
        "opera_ver": str(random.randint(*_VERSION_RANGES["opera"])),
    }
    
    replacements.update({
        "win_ver": random.choice(_OS_VERSIONS["win"]),
        "mac_ver": random.choice(_OS_VERSIONS["mac"]),
        "android_ver": str(random.randint(*_VERSION_RANGES["android"])),
        "ios_ver": str(random.randint(*_VERSION_RANGES["ios"])),
    })
    
    for placeholder, value in replacements.items():
        template = template.replace("{" + placeholder + "}", value)
    
    return template
