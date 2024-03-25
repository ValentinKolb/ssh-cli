# basic test from the module with pytest

import pytest

from src.validation import is_number, is_not_empty, is_valid_hostname


def test_is_number():
    assert is_number(None, "1") == True
    with pytest.raises(Exception):
        is_number(None, "a")


def test_is_not_empty():
    assert is_not_empty(None, "a") == True
    with pytest.raises(Exception):
        is_not_empty(None, "")


def test_is_valid_hostname():
    assert is_valid_hostname(None, "example.com") == True
    with pytest.raises(Exception):
        is_valid_hostname(None, "example")
