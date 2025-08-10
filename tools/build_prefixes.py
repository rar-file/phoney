"""
Build per-country IPv4/IPv6 prefix lists from RIR delegated stats.

This script reads the latest delegated-*-extended files and generates:
  phoney/data/internet/ipv4_prefixes.<CC>.txt
  phoney/data/internet/ipv6_prefixes.<CC>.txt

It requires the following files downloaded into tools/data/ (no network access in this script):
- delegated-apnic-extended-latest
- delegated-arin-extended-latest
- delegated-ripencc-extended-latest
- delegated-lacnic-extended-latest
- delegated-afrinic-extended-latest

Each line format (IPv6 example):
  rir|CC|ipv6|2001:db8::|32|allocated|date|...
IPv4 example:
  rir|CC|ipv4|1.2.3.0|256|allocated|date|...

Usage (PowerShell):
  # Place the delegated files in tools/data/
  # Then run the script to generate prefix files into phoney/data/internet/
  python tools/build_prefixes.py
"""
from __future__ import annotations

import ipaddress
import os
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
INTERNET_DIR = ROOT / "phoney" / "data" / "internet"
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
INTERNET_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    "delegated-apnic-extended-latest",
    "delegated-arin-extended-latest",
    "delegated-ripencc-extended-latest",
    "delegated-lacnic-extended-latest",
    "delegated-afrinic-extended-latest",
]

def _iter_lines():
    for name in FILES:
        p = DATA_DIR / name
        if not p.exists():
            continue
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):  # comment
                    continue
                parts = line.split("|")
                if len(parts) < 7:
                    continue
                yield parts


def build():
    ipv4_by_cc: dict[str, set[str]] = defaultdict(set)
    ipv6_by_cc: dict[str, set[str]] = defaultdict(set)

    for parts in _iter_lines():
        # Example: rir|CC|ipv6|2001:db8::|32|allocated|date|...
        #          rir|CC|ipv4|1.2.3.0|256|allocated|date|...
        try:
            _, cc, addr_type, start, value, status, *_ = parts
        except ValueError:
            continue
        if status not in ("allocated", "assigned"):
            continue
        cc = cc.upper()
        if addr_type == "ipv6":
            try:
                prefix_len = int(value)
                net = ipaddress.IPv6Network(f"{start}/{prefix_len}", strict=False)
                ipv6_by_cc[cc].add(str(net))
            except Exception:
                continue
        elif addr_type == "ipv4":
            try:
                count = int(value)
                # Convert count to prefix length if it's a power of two, else aggregate to minimal CIDRs
                # delegated files use counts for IPv4, convert to CIDR blocks
                network = ipaddress.IPv4Network(f"{start}/{32}", strict=False)
                # Build a supernet from start/count by summarization
                end_int = int(ipaddress.IPv4Address(start)) + count - 1
                start_ip = ipaddress.IPv4Address(start)
                end_ip = ipaddress.IPv4Address(end_int)
                for net in ipaddress.summarize_address_range(start_ip, end_ip):
                    ipv4_by_cc[cc].add(str(net))
            except Exception:
                continue

    # Write outputs
    for cc, nets in ipv4_by_cc.items():
        out = INTERNET_DIR / f"ipv4_prefixes.{cc}.txt"
        with out.open("w", encoding="utf-8") as f:
            for cidr in sorted(nets, key=lambda x: (int(x.split("/")[1]), x)):
                f.write(cidr + "\n")
    for cc, nets in ipv6_by_cc.items():
        out = INTERNET_DIR / f"ipv6_prefixes.{cc}.txt"
        with out.open("w", encoding="utf-8") as f:
            for cidr in sorted(nets, key=lambda x: (int(x.split("/")[1]), x)):
                f.write(cidr + "\n")

    print(f"Wrote IPv4 files for {len(ipv4_by_cc)} countries and IPv6 files for {len(ipv6_by_cc)} countries to {INTERNET_DIR}")


if __name__ == "__main__":
    build()
