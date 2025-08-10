from __future__ import annotations

import argparse
import ipaddress
from pathlib import Path
from collections import defaultdict

DEFAULT_FILES = [
    "delegated-apnic-extended-latest",
    "delegated-arin-extended-latest",
    "delegated-ripencc-extended-latest",
    "delegated-lacnic-extended-latest",
    "delegated-afrinic-extended-latest",
]


def _iter_lines(data_dir: Path, files: list[str]):
    for name in files:
        p = data_dir / name
        if not p.exists():
            continue
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) < 7:
                    continue
                yield parts


def main() -> None:
    parser = argparse.ArgumentParser(description="Build per-country IPv4/IPv6 prefix files from RIR delegated datasets.")
    parser.add_argument("--input-dir", type=Path, default=Path(__file__).resolve().parent / "data", help="Directory containing delegated-* files")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[2] / "phoney" / "data" / "internet", help="Directory to write prefix files into")
    args = parser.parse_args()

    data_dir: Path = args.input_dir
    out_dir: Path = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    ipv4_by_cc: dict[str, set[str]] = defaultdict(set)
    ipv6_by_cc: dict[str, set[str]] = defaultdict(set)

    for parts in _iter_lines(data_dir, DEFAULT_FILES):
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
                end_int = int(ipaddress.IPv4Address(start)) + count - 1
                start_ip = ipaddress.IPv4Address(start)
                end_ip = ipaddress.IPv4Address(end_int)
                for net in ipaddress.summarize_address_range(start_ip, end_ip):
                    ipv4_by_cc[cc].add(str(net))
            except Exception:
                continue

    for cc, nets in ipv4_by_cc.items():
        out = out_dir / f"ipv4_prefixes.{cc}.txt"
        with out.open("w", encoding="utf-8") as f:
            for cidr in sorted(nets, key=lambda x: (int(x.split("/")[1]), x)):
                f.write(cidr + "\n")
    for cc, nets in ipv6_by_cc.items():
        out = out_dir / f"ipv6_prefixes.{cc}.txt"
        with out.open("w", encoding="utf-8") as f:
            for cidr in sorted(nets, key=lambda x: (int(x.split("/")[1]), x)):
                f.write(cidr + "\n")

    print(f"Wrote IPv4 files for {len(ipv4_by_cc)} countries and IPv6 files for {len(ipv6_by_cc)} countries to {out_dir}")


if __name__ == "__main__":
    main()
