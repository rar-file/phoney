__all__ = ['generate_phone']
# phoney/phone.py
import random
from .data_loader import load_phone_formats
from collections import defaultdict

LOCALES = [
    'en_US', 'en_CA', 'es_MX', 'en_GB', 'fr_FR', 'de_DE',
    'it_IT', 'es_ES', 'nl_NL', 'pl_PL', 'ru_RU', 'tr_TR',
    'sv_SE', 'no_NO', 'da_DK', 'fi_FI', 'el_GR', 'pt_PT',
    'cs_CZ', 'hu_HU', 'ro_RO', 'ja_JP', 'ko_KR', 'zh_CN',
    'zh_TW', 'hi_IN', 'id_ID', 'th_TH', 'vi_VN', 'ms_MY',
    'fil_PH', 'ar_SA', 'he_IL', 'en_AU', 'en_NZ', 'en_ZA',
    'sw_KE', 'ar_EG', 'ha_NG', 'pt_BR', 'es_AR', 'es_CO',
    'es_CL',
]

def generate_phone(locale=None):
    locale = locale if locale in LOCALES else random.choice(LOCALES)
    fmt = load_phone_formats()[locale]
    digits = [random.choice('0123456789') if char == "#" else char for char in fmt]
    return "".join(digits)