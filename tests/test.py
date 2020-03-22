from PeriscopeKey import *
from DBInterface import *

def test_periscope_key():
    key = PeriscopeKey()
    assert key.is_valid_key() is True

def test_db_connection():
    d = DBInterface()
    d.connect()
    pass