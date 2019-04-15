import json

import pytest

from src import my_module


def test_my_function():
    assert isinstance(my_module.my_function(), float)
