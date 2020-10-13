"""
A test sub-suite to test XML generating fixture functionality.
"""

import datetime as dt
import pytest
import xml.etree.ElementTree as ET

import conftest

# conftest.random_dt tests
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

#conftest.random_name
def test_random_name_type():
    """Test for type of random_name output."""
    name = conftest.random_name()
    assert isinstance(name, str)

#conftest.random_record
def test_random_record_output_type():
    """Test if random_record outputs a string."""
    rec = conftest.random_record()
    assert isinstance(rec, str)

def test_random_record_valid_xml():
    """Test if random_record output produces valid XML"""
    rec = conftest.random_record()
    xml = ET.fromstring(rec)

def test_random_record_root():
    """Test if random record root is a <person> tag."""
    rec = conftest.random_record()
    xml = ET.fromstring(rec)
    assert xml.tag == 'person'

@pytest.mark.parametrize("tag", ['start', 'end'])
def test_random_record_has_tag(tag):
    """Test if generated random record has the predefined XML tags."""
    rec = conftest.random_record()
    xml = ET.fromstring(rec)
    assert xml.find(tag) is not None
