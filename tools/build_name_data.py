"""Rebuild phoney/data/name_data from real, openly licensed name datasets.

Usage:
    python -m pip install "faker==40.40.0"
    python tools/build_name_data.py            # downloads sources into tools/data/names_src/
    python tools/build_name_data.py --offline  # reuse already-downloaded sources

Sources (see phoney/data/name_data/NOTICE.md for licences):
  - Faker 40.40.0 person providers (MIT)
  - sigpwned/popular-names-by-country-dataset (CC0 1.0)
  - US Social Security Administration baby names 1880-2008, via hadley/data-baby-names (public domain)
  - smashew/NameDatabases US and UK surname lists (Unlicense / public domain)
  - shuheilocale/japanese-personal-name-dataset (MIT)
  - phoney's own earlier name lists (tools/name_sources/legacy/), for locales where they were sound

Every name goes through the same filters: Unicode NFC, correct script for the
locale, no digits/punctuation, sensible length, de-duplicated case-insensitively.
Gendered-surname locales keep masculine forms only (phoney derives feminine ones).
"""
from __future__ import annotations

import argparse
import csv
import importlib
import re
import shutil
import sys
import unicodedata
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "phoney" / "data" / "name_data"
LEGACY_DIR = ROOT / "tools" / "name_sources" / "legacy"
CACHE_DIR = ROOT / "tools" / "data" / "names_src"

sys.path.insert(0, str(ROOT))
from phoney.data_loader import _capitalize_name  # noqa: E402

FAKER_VERSION = "40.40.0"
JP_DATASET = "https://raw.githubusercontent.com/shuheilocale/japanese-personal-name-dataset/main/japanese_personal_name_dataset/dataset"
# Kanji spellings kept per given-name reading (the dataset lists every attested spelling).
JP_SPELLINGS_PER_READING = 2
DOWNLOADS = {
    "sig_forenames.csv": "https://raw.githubusercontent.com/sigpwned/popular-names-by-country-dataset/main/common-forenames-by-country.csv",
    "sig_surnames.csv": "https://raw.githubusercontent.com/sigpwned/popular-names-by-country-dataset/main/common-surnames-by-country.csv",
    "ssa_baby_names.csv": "https://raw.githubusercontent.com/hadley/data-baby-names/master/baby-names.csv",
    "smashew_surnames_us.txt": "https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/surnames/us.txt",
    "smashew_surnames_uk.txt": "https://raw.githubusercontent.com/smashew/NameDatabases/master/NamesDatabases/surnames/uk.txt",
    "jp_first_male.csv": f"{JP_DATASET}/first_name_man_org.csv",
    "jp_first_female.csv": f"{JP_DATASET}/first_name_woman_org.csv",
    "jp_last.csv": f"{JP_DATASET}/last_name_org.csv",
}

REGIONS = {
    "americas": ["en_US", "en_CA", "es_MX", "es_AR", "es_CO", "es_CL", "pt_BR"],
    "european": ["en_GB", "fr_FR", "de_DE", "it_IT", "es_ES", "nl_NL", "pl_PL", "ru_RU", "tr_TR", "sv_SE",
                 "no_NO", "da_DK", "fi_FI", "el_GR", "pt_PT", "cs_CZ", "hu_HU", "ro_RO"],
    "asian": ["ja_JP", "ko_KR", "zh_CN", "zh_TW", "hi_IN", "id_ID", "th_TH", "vi_VN", "ms_MY", "fil_PH"],
    "middle_east": ["ar_SA", "ar_EG", "he_IL"],
    "africa": ["en_ZA", "sw_KE", "ha_NG"],
    "oceania": ["en_AU", "en_NZ"],
}

# Each recipe lists sources merged into (male, female, last).
#   faker:<loc>      Faker person provider for <loc>
#   faker_last:<loc> only the surnames of that provider
#   sig:<CC>         sigpwned forenames + surnames for country code CC
#   legacy:<loc>     phoney's earlier lists (only those kept in tools/name_sources/legacy)
#   ssa              US SSA baby names (en_US)
#   smashew:<cc>     smashew surname list
#   faker_first:<loc> only the given names of that provider
#   jp               Japanese personal name dataset
RECIPES = {
    "en_US": ["legacy:en_US", "faker:en_US", "faker:en", "ssa", "smashew:us", "sig:US"],
    "en_GB": ["legacy:en_GB", "faker:en_GB", "smashew:uk", "sig:GB"],
    "en_CA": ["faker:en_US", "faker:en_GB", "faker:fr_CA", "sig:CA"],
    "en_AU": ["faker:en_GB", "faker:en_US", "sig:AU"],
    "en_NZ": ["faker:en_NZ", "sig:NZ"],
    "en_ZA": ["faker:zu_ZA", "faker:en_GB", "sig:ZA"],
    "fr_FR": ["legacy:fr_FR", "faker:fr_FR", "faker:fr_BE", "faker:fr_CH", "sig:FR"],
    "de_DE": ["legacy:de_DE", "faker:de_DE", "faker:de_AT", "faker:de_CH", "sig:DE", "sig:AT"],
    "it_IT": ["legacy:it_IT", "faker:it_IT", "sig:IT"],
    "es_ES": ["legacy:es_ES", "faker:es_ES", "faker:es_CA", "sig:ES"],
    "es_MX": ["faker:es_MX", "faker_last:es_ES", "sig:MX"],
    "es_AR": ["faker:es_AR", "faker_last:es_ES", "faker_last:it_IT", "sig:AR"],
    "es_CO": ["faker:es_CO", "faker_last:es_ES", "sig:CO"],
    "es_CL": ["faker:es_CL", "faker_last:es_ES", "sig:CL"],
    "pt_BR": ["legacy:pt_BR", "faker:pt_BR", "faker_last:pt_PT", "sig:BR"],
    "pt_PT": ["faker:pt_PT", "faker_last:pt_BR", "sig:PT"],
    "nl_NL": ["faker:nl_NL", "faker:nl_BE", "sig:NL"],
    "pl_PL": ["legacy:pl_PL", "faker:pl_PL", "sig:PL"],
    "cs_CZ": ["faker:cs_CZ", "sig:CZ"],
    "sv_SE": ["legacy:sv_SE", "faker:sv_SE"],
    "no_NO": ["faker:no_NO", "sig:NO"],
    "da_DK": ["legacy:da_DK", "faker:da_DK", "sig:DK"],
    "fi_FI": ["legacy:fi_FI", "faker:fi_FI", "sig:FI"],
    "el_GR": ["faker:el_GR", "sig:GR"],
    "ru_RU": ["legacy:ru_RU", "faker:ru_RU"],
    "tr_TR": ["legacy:tr_TR", "faker:tr_TR", "sig:TR"],
    "hu_HU": ["faker:hu_HU", "sig:HU"],
    "ro_RO": ["faker:ro_RO", "sig:RO"],
    "ja_JP": ["faker:ja_JP", "sig:JP", "jp"],
    "ko_KR": ["legacy:ko_KR", "faker:ko_KR", "sig:KR"],
    "zh_CN": ["legacy:zh_CN", "faker:zh_CN", "sig:CN"],
    "zh_TW": ["faker:zh_TW", "sig:TW"],
    "vi_VN": ["faker:vi_VN", "sig:VN", "vi_compose"],
    "hi_IN": ["faker:hi_IN", "sig:IN"],
    "id_ID": ["faker:id_ID"],
    "th_TH": ["faker:th_TH"],
    "ms_MY": ["sig:MY"],
    "fil_PH": ["sig:PH", "faker_first:en_US", "faker_first:es_ES", "faker_last:es_ES"],
    "ar_SA": ["faker:ar_SA", "faker:ar_AA"],
    "ar_EG": ["faker:ar_AA"],
    "he_IL": ["faker:he_IL"],
    "sw_KE": ["faker:en_KE", "faker:sw"],
    "ha_NG": ["faker:ha_NG", "faker:yo_NG", "faker:ig_NG", "faker:en_NG"],
}

SCRIPTS = {"ru": "CYRILLIC", "el": "GREEK", "ar": "ARABIC", "he": "HEBREW", "hi": "DEVANAGARI",
           "th": "THAI", "ko": "HANGUL", "zh": "CJK", "ja": "CJK"}
GENDERED_SURNAMES = {"ru", "el", "pl", "cs"}
# Feminine surname endings to drop from masculine-only lists.
FEMININE_ENDINGS = {
    "ru": ("ова", "ева", "ёва", "ина", "ына", "ская", "цкая", "ая"),
    "pl": ("ska", "cka", "dzka"),
    "cs": ("ová", "á"),
    "el": ("ου", "ού", "η", "ή", "α", "ά"),
}
# Vietnamese full given names are "middle + given"; Faker lists only the final given name.
VI_MIDDLE = {"male": ["Văn", "Đức", "Minh", "Quang", "Hữu", "Công", "Thanh", "Hoàng"],
             "female": ["Thị", "Ngọc", "Thu", "Thanh", "Kim", "Minh", "Phương", "Bích"]}
ZH_COMPOUND = {"欧阳", "司马", "上官", "诸葛", "东方", "皇甫", "尉迟", "公孙", "慕容", "令狐", "夏侯",
               "长孙", "宇文", "司徒", "申屠", "轩辕", "端木", "澹台", "南宫", "呼延", "欧陽", "諸葛"}
KO_COMPOUND = {"남궁", "황보", "제갈", "선우", "독고", "사공", "서문"}
BAD = re.compile(r"[\d()\[\],;:/\\|*#•@?!_=+<>\"]|\s{2,}")


def download(offline: bool) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in DOWNLOADS.items():
        dest = CACHE_DIR / name
        if dest.exists() or offline:
            continue
        print(f"downloading {url}")
        with urllib.request.urlopen(url, timeout=60) as resp:
            dest.write_bytes(resp.read())


def char_ok(ch: str, script: str | None) -> bool:
    if ch in " -'’" or unicodedata.category(ch).startswith("M"):
        return True
    name = unicodedata.name(ch, "")
    if script == "CJK":
        return "CJK" in name or "HIRAGANA" in name or "KATAKANA" in name or ch in "々ヶ"
    if script:
        return name.startswith(script)
    return name.startswith("LATIN")


def clean(name: str, locale: str) -> str | None:
    name = unicodedata.normalize("NFC", name.strip().replace("’", "'"))
    name = re.sub(r"'\s+", "'", name)
    lang = locale.split("_")[0]
    if not name or BAD.search(name) or len(name) > 30:
        return None
    if not all(char_ok(c, SCRIPTS.get(lang)) for c in name):
        return None
    if SCRIPTS.get(lang) is None and len(name) < 2:
        return None
    return _capitalize_name(name, locale)


# ----------------------------------------------------------------- sources

def faker_lists(loc: str) -> dict[str, list[str]]:
    import faker
    if faker.VERSION != FAKER_VERSION:
        raise SystemExit(f"need faker=={FAKER_VERSION}, found {faker.VERSION}")
    prov = importlib.import_module(f"faker.providers.person.{loc}").Provider
    own = vars(prov)

    def get(attr):
        v = own.get(attr)
        return list(v) if isinstance(v, (dict, list, tuple)) else []

    last = get("last_names_male") or get("last_names")
    return {"male": get("first_names_male"), "female": get("first_names_female"), "last": last}


def sig_lists(cc: str, locale: str) -> dict[str, list[str]]:
    out = defaultdict(list)

    def pick(row):
        for key in ("Localized Name", "Romanized Name"):
            for part in row[key].split("/"):
                if part and clean(part, locale):
                    return part
        return None

    with open(CACHE_DIR / "sig_forenames.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["Country"] == cc and (name := pick(row)):
                out["male" if row["Gender"] == "M" else "female"].append(name)
    with open(CACHE_DIR / "sig_surnames.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["Country"] == cc and (name := pick(row)):
                out["last"].append(name)
    return out


def ssa_lists() -> dict[str, list[str]]:
    out = defaultdict(list)
    with open(CACHE_DIR / "ssa_baby_names.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out["male" if row["sex"] == "boy" else "female"].append(row["name"])
    return out


def smashew_lists(cc: str) -> dict[str, list[str]]:
    text = (CACHE_DIR / f"smashew_surnames_{cc}.txt").read_text(encoding="utf-8", errors="replace")
    return {"last": text.splitlines()}


def legacy_lists(loc: str) -> dict[str, list[str]]:
    out = {}
    for kind in ("male", "female", "last"):
        path = LEGACY_DIR / loc / f"{kind}.txt"
        if path.exists():
            out[kind] = path.read_text(encoding="utf-8").splitlines()
    # Old zh/ko lists hold full names: split off the family name. The old zh
    # given names were identical for both genders, so only its surnames are used.
    if loc in ("zh_CN", "ko_KR"):
        compounds = ZH_COMPOUND if loc == "zh_CN" else KO_COMPOUND
        split = defaultdict(list)
        for kind in ("male", "female"):
            for full in out.get(kind, []):
                full = full.strip()
                n = 2 if full[:2] in compounds else 1
                if len(full) > n:
                    split["last"].append(full[:n])
                    if loc == "ko_KR":
                        split[kind].append(full[n:])
        out = split
    return out


def jp_lists() -> dict[str, list[str]]:
    out = defaultdict(list)
    for kind, fname in (("male", "jp_first_male.csv"), ("female", "jp_first_female.csv")):
        with open(CACHE_DIR / fname, encoding="utf-8") as f:
            for row in csv.reader(f):
                out[kind].extend(row[2:2 + JP_SPELLINGS_PER_READING])
    with open(CACHE_DIR / "jp_last.csv", encoding="utf-8") as f:
        out["last"] = [row[0] for row in csv.reader(f) if row]
    return out


def vi_compose(male: list[str], female: list[str]) -> dict[str, list[str]]:
    singles = {k: [n for n in v if " " not in n] for k, v in (("male", male), ("female", female))}
    return {k: [f"{m} {g}" for m in VI_MIDDLE[k] for g in singles[k] if m != g] for k in singles}


# ----------------------------------------------------------------- build

def build_locale(loc: str) -> dict[str, list[str]]:
    lang = loc.split("_")[0]
    raw = defaultdict(list)
    for src in RECIPES[loc]:
        kind, _, arg = src.partition(":")
        if kind == "faker":
            lists = faker_lists(arg)
        elif kind == "faker_last":
            lists = {"last": faker_lists(arg)["last"]}
        elif kind == "faker_first":
            lists = {k: v for k, v in faker_lists(arg).items() if k != "last"}
        elif kind == "jp":
            lists = jp_lists()
        elif kind == "sig":
            lists = sig_lists(arg, loc)
        elif kind == "legacy":
            lists = legacy_lists(arg)
        elif kind == "ssa":
            lists = ssa_lists()
        elif kind == "smashew":
            lists = smashew_lists(arg)
        elif kind == "vi_compose":
            lists = vi_compose(raw["male"], raw["female"])
        else:
            raise ValueError(src)
        for k, names in lists.items():
            raw[k].extend(names)

    result = {}
    for k in ("male", "female", "last"):
        seen, names = set(), []
        for n in raw[k]:
            c = clean(n, loc)
            if not c or c.casefold() in seen:
                continue
            if k == "last" and lang in GENDERED_SURNAMES and c.endswith(FEMININE_ENDINGS.get(lang, ())):
                continue
            seen.add(c.casefold())
            names.append(c)
        result[k] = sorted(names, key=str.casefold)
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--offline", action="store_true", help="do not download; use cached sources")
    args = ap.parse_args()
    download(args.offline)

    built = {loc: build_locale(loc) for locs in REGIONS.values() for loc in locs}
    shutil.rmtree(OUT_DIR, ignore_errors=True)
    print(f"{'locale':7} {'male':>7} {'female':>7} {'last':>7}")
    for region, locs in REGIONS.items():
        for loc in locs:
            d = OUT_DIR / region / loc
            d.mkdir(parents=True)
            for k, names in built[loc].items():
                (d / f"{k}.txt").write_text("".join(n + "\n" for n in names), encoding="utf-8")
            print(f"{loc:7} {len(built[loc]['male']):7} {len(built[loc]['female']):7} {len(built[loc]['last']):7}")
    shutil.copy(ROOT / "tools" / "name_sources" / "NOTICE.md", OUT_DIR / "NOTICE.md")


if __name__ == "__main__":
    main()
