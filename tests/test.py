from PeriscopeKey import *

def test_periscope_key(capsys):
    key = PeriscopeKey()
    assert key.is_valid_key() is True

def test_two():
    pass