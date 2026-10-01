import random

import pytest


@pytest.fixture(autouse=True)
def _seed_random():
    """Make every test reproducible: phoney draws from the global `random` module."""
    random.seed(1234)
    yield
