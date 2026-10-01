import ipaddress
import re

import pytest

from phoney import (
    generate_domain,
    generate_hostname,
    generate_ipv4,
    generate_ipv6,
    generate_mac,
    generate_tld,
    generate_url,
)

LOCALES = [None, "en_US", "en_GB", "de_DE", "fr_FR", "ja_JP", "xx_XX"]


@pytest.mark.parametrize("locale", LOCALES)
def test_ipv4(locale):
    for _ in range(100):
        ipaddress.IPv4Address(generate_ipv4(locale=locale))


@pytest.mark.parametrize("locale", LOCALES)
def test_ipv6_global_unicast(locale):
    for _ in range(100):
        addr = ipaddress.IPv6Address(generate_ipv6(locale=locale))
        assert addr.is_global, addr


def test_ipv6_any():
    for _ in range(100):
        ipaddress.IPv6Address(generate_ipv6(global_unicast=False))


def test_mac():
    for _ in range(100):
        assert re.fullmatch(r"([0-9a-f]{2}:){5}[0-9a-f]{2}", generate_mac())


@pytest.mark.parametrize("locale", LOCALES)
def test_domain_hostname_url(locale):
    label = r"[a-z0-9]([a-z0-9-]*[a-z0-9])?"
    for _ in range(50):
        assert re.fullmatch(rf"{label}(\.{label})+", generate_domain(locale=locale))
        assert re.fullmatch(rf"{label}(\.{label})+", generate_hostname(locale=locale))
        assert re.fullmatch(r"https://\S+", generate_url(locale=locale))
        assert re.fullmatch(r"[a-z]{2,}(\.[a-z]{2,})*", generate_tld(locale=locale))


def test_domain_with_explicit_tld():
    assert generate_domain(tld="io").endswith(".io")
