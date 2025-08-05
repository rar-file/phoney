__all__ = ['generate_phone']
# phoney/phone.py
import random
import re
import os
import json
from collections import defaultdict

COUNTRY_CODES = {
    'en_US':'1','en_CA':'1','es_MX':'52','en_GB':'44','fr_FR':'33',
    'de_DE':'49','it_IT':'39','es_ES':'34','nl_NL':'31','pl_PL':'48',
    'ru_RU':'7','tr_TR':'90','sv_SE':'46','no_NO':'47','da_DK':'45',
    'fi_FI':'358','el_GR':'30','pt_PT':'351','cs_CZ':'420','hu_HU':'36',
    'ro_RO':'40','ja_JP':'81','ko_KR':'82','zh_CN':'86','zh_TW':'886',
    'hi_IN':'91','id_ID':'62','th_TH':'66','vi_VN':'84','ms_MY':'60',
    'fil_PH':'63','ar_SA':'966','he_IL':'972','en_AU':'61','en_NZ':'64',
    'en_ZA':'27','sw_KE':'254','ar_EG':'20','ha_NG':'234','pt_BR':'55',
    'es_AR':'54','es_CO':'57','es_CL':'56'
}

VALIDATORS = {
    # North America
    'en_US': re.compile(r'^(?!(?:555))[2-9]\d{2}[2-9](?!11)\d{6}$'),
    'en_CA': re.compile(r'^(?!(?:555))[2-9]\d{2}[2-9](?!11)\d{6}$'),
    'es_MX': re.compile(r'^[1-9]\d{9}$'),
    
    # Europe
    'en_GB': re.compile(r'^7\d{9}$'),  # UK numbers start with 7
    'fr_FR': re.compile(r'^[1-9]\d{8}$'),  # 9-digit numbers
    'de_DE': re.compile(r'^[1-9]\d{2,11}$'),
    'it_IT': re.compile(r'^[13]\d{8,9}$'),
    'es_ES': re.compile(r'^[689]\d{8}$'),
    'nl_NL': re.compile(r'^[1-9]\d{8}$'),
    'pl_PL': re.compile(r'^[1-9]\d{8}$'),
    'ru_RU': re.compile(r'^[3489]\d{9}$'),
    'cs_CZ': re.compile(r'^[1-9]\d{8}$'),
    'hu_HU': re.compile(r'^[1-9]\d{8}$'),
    'ro_RO': re.compile(r'^[1-9]\d{8}$'),
    'fi_FI': re.compile(r'^[1-9]\d{4,10}$'),
    'sv_SE': re.compile(r'^[1-9]\d{6,9}$'),
    'no_NO': re.compile(r'^[1-9]\d{7}$'),
    'da_DK': re.compile(r'^[1-9]\d{7}$'),
    'el_GR': re.compile(r'^[1-9]\d{9}$'),
    'pt_PT': re.compile(r'^[1-9]\d{8}$'),
    
    # Asia
    'ja_JP': re.compile(r'^[1-9]\d{8,9}$'),
    'ko_KR': re.compile(r'^[1-9]\d{7,9}$'),
    'zh_CN': re.compile(r'^[1-9]\d{10}$'),
    'zh_TW': re.compile(r'^[1-9]\d{8}$'),
    'hi_IN': re.compile(r'^[1-9]\d{9}$'),
    'id_ID': re.compile(r'^8\d{10}$'),  # Fixed: 11 digits starting with 8
    'th_TH': re.compile(r'^[1-9]\d{8}$'),
    'vi_VN': re.compile(r'^[1-9]\d{8,9}$'),
    'ms_MY': re.compile(r'^[1-9]\d{7,9}$'),
    'fil_PH': re.compile(r'^[1-9]\d{9}$'),
    'tr_TR': re.compile(r'^[1-9]\d{9}$'),
    
    # Middle East/Africa
    'ar_SA': re.compile(r'^[1-9]\d{8}$'),
    'he_IL': re.compile(r'^[1-9]\d{8}$'),
    'ar_EG': re.compile(r'^[1-9]\d{9}$'),
    'en_ZA': re.compile(r'^[1-9]\d{8}$'),
    'sw_KE': re.compile(r'^[1-9]\d{8}$'),
    'ha_NG': re.compile(r'^[1-9]\d{9}$'),
    
    # Oceania
    'en_AU': re.compile(r'^[1-9]\d{8}$'),
    'en_NZ': re.compile(r'^[1-9]\d{8,9}$'),
    
    # South America
    'pt_BR': re.compile(r'^[1-9]\d{9}$'),
    'es_AR': re.compile(r'^[1-9]\d{9}$'),
    'es_CO': re.compile(r'^[1-9]\d{9}$'),
    'es_CL': re.compile(r'^[1-9]\d{8}$')
}

DEFAULT_FORMATS = {
    'en_US': '(###) ###-####',
    'en_CA': '(###) ###-####',
    'es_MX': '## #### ####',
    'en_GB': '#### ######',  # UK format
    'fr_FR': '### ### ###',   # 9-digit format
    'de_DE': '#### ########',
    'it_IT': '### #######',
    'es_ES': '### ### ###',
    'nl_NL': '### ######',
    'pl_PL': '### ### ###',
    'ru_RU': '### ###-##-##',
    'tr_TR': '### ### ####',
    'sv_SE': '### ### ## ##',
    'no_NO': '### ## ###',
    'da_DK': '## ## ## ##',
    'fi_FI': '### ######',
    'el_GR': '### #######',
    'pt_PT': '### ### ###',
    'cs_CZ': '### ### ###',
    'hu_HU': '### ### ###',
    'ro_RO': '### ### ###',
    'ja_JP': '## #### ####',
    'ko_KR': '## #### ####',
    'zh_CN': '### #### ####',
    'zh_TW': '#### ######',
    'hi_IN': '#### ### ###',
    'id_ID': '8## #### #####',  # Fixed: 11-digit mobile format
    'th_TH': '### ### ###',
    'vi_VN': '### #######',
    'ms_MY': '### ### ###',
    'fil_PH': '#### ### ####',
    'ar_SA': '## ### ####',
    'he_IL': '## ### ####',
    'en_AU': '#### ######',
    'en_NZ': '#### ######',
    'en_ZA': '## ### ####',
    'sw_KE': '### ######',
    'ar_EG': '### #######',
    'ha_NG': '### ### ####',
    'pt_BR': '(##) ####-####',
    'es_AR': '## ####-####',
    'es_CO': '### #######',
    'es_CL': '## #######'
}

def load_phone_formats():
    """Load phone number formats from JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    formats_path = os.path.join(current_dir, 'data', 'phone_formats.json')
    
    try:
        with open(formats_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_FORMATS

def generate_phone(locale=None, max_attempts=500):
    fmts = load_phone_formats()
    if not locale or locale not in COUNTRY_CODES:
        locale = random.choice(list(COUNTRY_CODES))
    
    fmt = DEFAULT_FORMATS.get(locale, fmts.get(locale, '(###) ###-####'))
    needed = fmt.count('#')
    country_code = COUNTRY_CODES[locale]
    validator = VALIDATORS.get(locale)

    for _ in range(max_attempts):
        if locale == 'id_ID':
            digits = ['8'] + [random.choice('0123456789') for _ in range(10)]
            clean = ''.join(digits)
            formatted = ''
            digit_idx = 0
            for char in fmt:
                if char == '#':
                    formatted += clean[digit_idx]
                    digit_idx += 1
                else:
                    formatted += char
            number_str = formatted
        elif locale == 'en_GB':
            digits = ['7'] + [random.choice('0123456789') for _ in range(9)]
            clean = ''.join(digits)
            formatted = ''
            digit_idx = 0
            for char in fmt:
                if char == '#':
                    formatted += clean[digit_idx]
                    digit_idx += 1
                else:
                    formatted += char
            number_str = formatted
        else:
            digits = []
            for char in fmt:
                if char == '#':
                    digits.append(random.choice('0123456789'))
                else:
                    digits.append(char)
            number_str = ''.join(digits)
            clean = re.sub(r'[^\d]', '', number_str)

        if len(clean) != needed:
            continue

        if validator and not validator.fullmatch(clean):
            continue

        return f"+{country_code} {number_str}"

    print(f"DEBUG: Failed to generate valid number for {locale}. Format: {fmt}, Needed: {needed}, Attempts: {max_attempts}")
    raise ValueError(f"Failed to generate valid number for {locale} after {max_attempts} attempts")