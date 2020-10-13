"""
A test sub-suite to test XML generating fixture functionality.
"""

import datetime as dt
import pytest

import conftest


def test_random_dt_attribute_types_1():
    """Test that random_dt parameter 1 must be a datetime object, not
    string."""
    with pytest.raises(ValueError):
        conftest.random_dt('2010-01-01', dt.datetime(2010, 1, 1))

def test_random_dt_attribute_types_2():
    """Test that random_dt parameter 2 must be a datetime object, not
    string."""
    with pytest.raises(ValueError):
        conftest.random_dt(dt.datetime(2010, 1, 1), '2020-01-01')

def test_random_dt_max_greater_min():
    """Test if random_dt function raises an exception when dt_max 
    parameter is less than dt_min parameter."""
    with pytest.raises(ValueError):
        conftest.random_dt(dt.datetime(2020, 12, 28), dt.datetime(2010, 12, 1))

def test_random_dt_output_greater_than():
    """Test that random_dt output is greater than parameter 1."""
    rd = conftest.random_dt(dt.datetime(2010, 1, 1), dt.datetime(2012, 1, 1))
    assert rd > dt.datetime(2010, 1, 1, 0, 0, 0)

def test_random_dt_output_less_than():
    """Test that random_dt output is less than parameter 2."""
    rd = conftest.random_dt(dt.datetime(2012, 2, 1), dt.datetime(2014, 7, 5))
    assert rd <= dt.datetime(2014, 7, 5, 23, 59, 59)


