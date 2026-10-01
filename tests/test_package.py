import re

import phoney
from phoney import Phoney


def test_version_is_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", phoney.__version__)


def test_everything_in_all_is_importable():
    for name in phoney.__all__:
        assert hasattr(phoney, name), name


def test_generate_functions_are_callable_on_instance():
    p = Phoney()
    for name in phoney.__all__:
        if name.startswith("generate_"):
            assert callable(getattr(p, name)), name


def test_unknown_attribute_raises():
    p = Phoney()
    try:
        p.does_not_exist
    except AttributeError:
        pass
    else:
        raise AssertionError("expected AttributeError")


def test_name_locales_are_discovered():
    locales = phoney.get_available_locales()
    for expected in ("en_US", "en_GB", "de_DE", "fr_FR", "ja_JP", "zh_CN"):
        assert expected in locales


def test_bundled_data_files_are_loadable():
    assert phoney.load_email_domains()
    from phoney.data_loader import load_phone_formats

    assert load_phone_formats()
