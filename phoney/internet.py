from __future__ import annotations

import random
import string
from pathlib import Path
from typing import List, Optional, Tuple
import ipaddress

DATA_DIR = Path(__file__).parent / "data" / "internet"

DEFAULT_TLDS = [
    "com", "net", "org", "io", "dev", "app", "ai", "co", "info",
    "co.uk", "de", "fr", "es", "it", "nl", "br", "jp", "kr",
]

DEFAULT_WORDS = [
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot",
    "acme", "globex", "initech", "umbrella", "hooli", "wonka",
    "nova", "quantum", "stellar", "rocket", "fusion", "pixel",
    "lumen", "apex", "vertex", "nimbus", "atlas", "orion",
]

PREFERRED_TLDS_BY_COUNTRY = {
    "US": ["com", "net", "org"],
    "GB": ["co.uk", "uk", "com"],
    "DE": ["de", "com"],
    "FR": ["fr", "com"],
    "ES": ["es", "com"],
    "IT": ["it", "com"],
    "NL": ["nl", "com"],
    "BR": ["br", "com"],
    "JP": ["jp", "com"],
    "KR": ["kr", "com"],
}

# Minimal default IPv4 prefixes per country. Override with data files for accuracy.
DEFAULT_IPV4_PREFIXES = {
    "GB": [
        "2.24.0.0/13", "31.48.0.0/13", "51.52.0.0/14", "81.128.0.0/10",
        "82.0.0.0/11", "86.0.0.0/11", "88.96.0.0/12", "90.192.0.0/10",
        "109.144.0.0/12", "151.224.0.0/11", "188.28.0.0/14"
    ],
    "JP": [
        "1.33.0.0/16", "27.80.0.0/13", "36.8.0.0/13", "58.80.0.0/14",
        "60.32.0.0/11", "61.192.0.0/12", "106.128.0.0/10", "126.0.0.0/8",
        "133.0.0.0/8", "153.128.0.0/9", "219.96.0.0/13"
    ],
}

# Regional IPv6 /12 allocations (authoritative RIR blocks) for locale-based fallback:
# - RIPE NCC (Europe):    2a00::/12
# - APNIC (Asia/Pacific): 2400::/12
# - ARIN (North America): 2600::/12
# - LACNIC (LatAm):       2800::/12
# - AFRINIC (Africa):     2c00::/12
REGION_DEFAULT_IPV6_PREFIXES = {
    "RIPE": "2a00::/12",
    "APNIC": "2400::/12",
    "ARIN": "2600::/12",
    "LACNIC": "2800::/12",
    "AFRINIC": "2c00::/12",
}

# Minimal country -> region mapping for sane defaults
COUNTRY_TO_REGION = {
    # Europe (RIPE)
    "GB": "RIPE", "DE": "RIPE", "FR": "RIPE", "ES": "RIPE", "IT": "RIPE", "NL": "RIPE",
    "SE": "RIPE", "PL": "RIPE", "FI": "RIPE", "DK": "RIPE", "IE": "RIPE", "NO": "RIPE",
    # North America (ARIN)
    "US": "ARIN", "CA": "ARIN",
    # Asia/Pacific (APNIC)
    "JP": "APNIC", "KR": "APNIC", "CN": "APNIC", "IN": "APNIC", "AU": "APNIC", "NZ": "APNIC",
    # Latin America (LACNIC)
    "BR": "LACNIC", "AR": "LACNIC", "MX": "LACNIC", "CL": "LACNIC", "CO": "LACNIC",
    # Africa (AFRINIC)
    "ZA": "AFRINIC", "NG": "AFRINIC", "EG": "AFRINIC", "KE": "AFRINIC", "MA": "AFRINIC",
}


def _load_lines(path: Path) -> List[str]:
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    except Exception:
        pass
    return []


def _tlds() -> List[str]:
    lines = _load_lines(DATA_DIR / "tlds.txt")
    return lines if lines else DEFAULT_TLDS


def _words() -> List[str]:
    lines = _load_lines(DATA_DIR / "words.txt")
    return lines if lines else DEFAULT_WORDS

def _country_from_locale(locale: Optional[str]) -> Optional[str]:
    if not locale:
        return None
    s = locale.strip()
    if not s:
        return None
    # Support both en_GB and en-GB; also accept bare country like "GB"
    s = s.replace('-', '_')
    parts = s.split('_')
    if len(parts) == 1:
        token = parts[0]
        if 2 <= len(token) <= 3:
            return token.upper()
        return None
    # Use the last token as country/region code when present
    cc = parts[-1]
    if 2 <= len(cc) <= 3:
        return cc.upper()
    return None

def _load_prefixes(country: str) -> List[str]:
    path = DATA_DIR / f"ipv4_prefixes.{country}.txt"
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith('#')]
    except Exception:
        pass
    return DEFAULT_IPV4_PREFIXES.get(country, [])

def _load_ipv6_prefixes(country: str) -> List[str]:
    """Load IPv6 CIDR prefixes for a given country from data files.
    File format: one CIDR per line, e.g., "2400:cb00::/32". Lines starting with # are ignored.
    """
    path = DATA_DIR / f"ipv6_prefixes.{country}.txt"
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith('#')]
    except Exception:
        pass
    # No hard-coded defaults to avoid inaccurate country claims; fallback handled by generator.
    return []

def _ip_to_int(ip: str) -> int:
    a, b, c, d = (int(x) for x in ip.split('.'))
    return (a << 24) | (b << 16) | (c << 8) | d

def _int_to_ip(n: int) -> str:
    return f"{(n >> 24) & 0xFF}.{(n >> 16) & 0xFF}.{(n >> 8) & 0xFF}.{n & 0xFF}"

def _cidr_range(cidr: str) -> Tuple[int, int]:
    base, prefix = cidr.split('/')
    prefix = int(prefix)
    base_int = _ip_to_int(base)
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    network = base_int & mask
    size = 1 << (32 - prefix)
    first = network
    last = network + size - 1
    return first, last

def _random_ip_in_cidr(cidr: str) -> str:
    first, last = _cidr_range(cidr)
    if last - first >= 3:
        n = random.randint(first + 1, last - 1)
    else:
        n = random.randint(first, last)
    return _int_to_ip(n)


def _slug(n: int = 6) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


def generate_tld(locale: Optional[str] = None) -> str:
    if locale:
        cc = _country_from_locale(locale)
        if cc:
            prefs = PREFERRED_TLDS_BY_COUNTRY.get(cc, [])
            if prefs:
                available = _tlds()
                for t in prefs:
                    if t in available:
                        return t
                return random.choice(prefs)
    return random.choice(_tlds())


def generate_domain(tld: str | None = None, locale: Optional[str] = None) -> str:
    tld = tld or generate_tld(locale=locale)
    name = random.choice(_words()) + "-" + _slug(4)
    return f"{name}.{tld}"


def generate_hostname(domain: str | None = None, locale: Optional[str] = None) -> str:
    host = random.choice(["host", "app", "api", "web", "srv", "db", "cache"]) + "-" + _slug(3)
    dom = domain or generate_domain(locale=locale)
    return f"{host}.{dom}"


def generate_url(
    scheme: str = "https",
    domain: str | None = None,
    path_segments: list[str] | None = None,
    query_params: dict[str, str] | None = None,
    locale: Optional[str] = None,
) -> str:
    dom = domain or generate_domain(locale=locale)
    segs = path_segments or [random.choice(["api", "v1", "users", "search", "docs"]), _slug(5)]
    path = "/" + "/".join(segs)
    if query_params is None:
        query_params = {"q": random.choice(_words()), "page": str(random.randint(1, 9))}
    query = "&".join(f"{k}={v}" for k, v in query_params.items()) if query_params else ""
    return f"{scheme}://{dom}{path}" + (f"?{query}" if query else "")


def generate_ipv4(country: Optional[str] = None, locale: Optional[str] = None) -> str:
    def ok(o1: int, o2: int) -> bool:
        if o1 == 0 or o1 == 127 or o1 >= 224:
            return False
        if o1 == 10:
            return False
        if o1 == 169 and o2 == 254:
            return False
        if o1 == 172 and 16 <= o2 <= 31:
            return False
        if o1 == 192 and o2 == 168:
            return False
        return True

    cc = (country or _country_from_locale(locale))
    if cc:
        prefixes = _load_prefixes(cc)
        if prefixes:
            for _ in range(5):
                ip = _random_ip_in_cidr(random.choice(prefixes))
                o1, o2 = (int(x) for x in ip.split('.')[:2])
                if ok(o1, o2):
                    return ip
            return _random_ip_in_cidr(random.choice(prefixes))
        # Region fallback when no country-specific prefixes
        region = COUNTRY_TO_REGION.get(cc)
        if region:
            # Pick a typical public block within the RIR space for realism
            region_blocks = {
                "RIPE": ["2.16.0.0/13", "5.0.0.0/8", "31.0.0.0/8", "81.0.0.0/8", "82.0.0.0/8"],
                "APNIC": ["27.0.0.0/8", "36.0.0.0/8", "49.0.0.0/8", "58.0.0.0/8", "59.0.0.0/8", "60.0.0.0/8"],
                "ARIN": ["3.0.0.0/8", "13.0.0.0/8", "23.0.0.0/8", "34.0.0.0/8", "44.0.0.0/8", "63.0.0.0/8"],
                "LACNIC": ["177.0.0.0/8", "179.0.0.0/8", "186.0.0.0/8", "187.0.0.0/8", "189.0.0.0/8"],
                "AFRINIC": ["41.0.0.0/8", "102.0.0.0/8", "105.0.0.0/8"],
            }
            blocks = region_blocks.get(region, [])
            if blocks:
                for _ in range(5):
                    ip = _random_ip_in_cidr(random.choice(blocks))
                    o1, o2 = (int(x) for x in ip.split('.')[:2])
                    if ok(o1, o2):
                        return ip
                return _random_ip_in_cidr(random.choice(blocks))

    while True:
        o1 = random.randint(1, 223)
        o2 = random.randint(0, 255)
        if not ok(o1, o2):
            continue
        o3 = random.randint(0, 255)
        o4 = random.randint(1, 254)
        return f"{o1}.{o2}.{o3}.{o4}"


def generate_ipv6(
    global_unicast: bool = True,
    country: Optional[str] = None,
    locale: Optional[str] = None,
) -> str:
    """Generate an IPv6 address.

    - If a country (or locale) is provided and corresponding IPv6 prefixes exist in data files,
      a random address from one of those prefixes will be generated.
    - Otherwise, if global_unicast is True, the address will be in 2000::/3.
    - Else, a random valid IPv6 address will be generated and returned in canonical compressed form.
    """
    # Try country/locale-aware generation first via data files
    cc = (country or _country_from_locale(locale))
    if cc:
        prefixes6 = _load_ipv6_prefixes(cc)
        if prefixes6:
            # Pick a prefix and generate a random address within it using ipaddress
            cidr = random.choice(prefixes6)
            try:
                net = ipaddress.IPv6Network(cidr, strict=False)
                # Avoid network and broadcast concepts (not applicable in IPv6 the same way),
                # but skip all-zero interface identifier when possible by picking from full range.
                # Choose a random integer within the network range
                # net.num_addresses can be huge; sample a random 64-bit host part when prefix <= 64 for efficiency
                if net.prefixlen <= 64:
                    # Keep the first 64 bits fixed, randomize the lower 64 bits
                    network_int = int(net.network_address)
                    host_max = (1 << (128 - net.prefixlen)) - 1
                    # Sample within the available host space
                    host = random.randint(1, min(host_max, (1 << 64) - 1))
                    addr_int = (network_int & (~host_max)) | host
                else:
                    # Smaller host space; sample uniformly
                    first = int(net.network_address)
                    last = int(net.broadcast_address)
                    if last - first >= 2:
                        addr_int = random.randint(first + 1, last - 1)
                    else:
                        addr_int = random.randint(first, last)
                addr = ipaddress.IPv6Address(addr_int)
                return addr.compressed
            except Exception:
                # If CIDR is malformed, fall through to global-unicast generation
                pass

        # No country-specific prefixes available: try region fallback
        region = COUNTRY_TO_REGION.get(cc)
        if region:
            cidr = REGION_DEFAULT_IPV6_PREFIXES.get(region)
            try:
                net = ipaddress.IPv6Network(cidr, strict=False)
                if net.prefixlen <= 64:
                    network_int = int(net.network_address)
                    host_max = (1 << (128 - net.prefixlen)) - 1
                    host = random.randint(1, min(host_max, (1 << 64) - 1))
                    addr_int = (network_int & (~host_max)) | host
                else:
                    first = int(net.network_address)
                    last = int(net.broadcast_address)
                    if last - first >= 2:
                        addr_int = random.randint(first + 1, last - 1)
                    else:
                        addr_int = random.randint(first, last)
                addr = ipaddress.IPv6Address(addr_int)
                return addr.compressed
            except Exception:
                pass

    if global_unicast:
        # 2000::/3 => first group between 0x2000 and 0x3FFF
        first_group = random.randint(0x2000, 0x3FFF)
        groups = [first_group] + [random.randint(0, 0xFFFF) for _ in range(7)]
        addr = ipaddress.IPv6Address(":".join(f"{g:04x}" for g in groups))
        return addr.compressed
    # fallback: random 8 groups
    groups = [random.randint(0, 0xFFFF) for _ in range(8)]
    addr = ipaddress.IPv6Address(":".join(f"{g:04x}" for g in groups))
    return addr.compressed


def generate_mac() -> str:
    first = random.randint(0x00, 0xFF)
    first = (first | 0x02) & 0xFE
    octets = [first] + [random.randint(0x00, 0xFF) for _ in range(5)]
    return ":".join(f"{b:02x}" for b in octets)


def _is_global_unicast_ipv6(addr: str) -> bool:
    try:
        ip = ipaddress.IPv6Address(addr)
        return ip.is_global and not (ip.is_multicast or ip.is_link_local or ip.is_private)
    except Exception:
        return False


__all__ = [
    "generate_tld",
    "generate_domain",
    "generate_hostname",
    "generate_url",
    "generate_ipv4",
    "generate_ipv6",
    "generate_mac",
]
