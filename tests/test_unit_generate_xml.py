"""
A test sub-suite to test XML generating fixture functionality.
"""

import datetime as dt
import pytest
from lxml import etree as et

from clock_in_clock_out import generate_sample_data as gsd


def test_random_dt_attribute_types_1():
    """Test that random_dt parameter 1 must be a datetime object, not
    string."""
    with pytest.raises(TypeError):
        gsd._random_dt('2010-01-01', dt.datetime(2010, 1, 1))

def test_random_dt_attribute_types_2():
    """Test that random_dt parameter 2 must be a datetime object, not
    string."""
    with pytest.raises(TypeError):
        gsd._random_dt(dt.datetime(2010, 1, 1), '2020-01-01')

def test_random_dt_max_greater_min():
    """Test if random_dt function raises an exception when dt_max 
    parameter is less than dt_min parameter."""
    with pytest.raises(ValueError):
        gsd._random_dt(dt.datetime(2020, 12, 28), dt.datetime(2010, 12, 1))

def test_random_dt_output_greater_than():
    """Test that random_dt output is greater than parameter 1."""
    rd = gsd._random_dt(dt.datetime(2010, 1, 1), dt.datetime(2012, 1, 1))
    assert rd > dt.datetime(2010, 1, 1, 0, 0, 0)

def test_random_dt_output_less_than():
    """Test that random_dt output is less than parameter 2."""
    rd = gsd._random_dt(dt.datetime(2012, 2, 1), dt.datetime(2014, 7, 5))
    assert rd <= dt.datetime(2014, 7, 5, 23, 59, 59)

def test_random_name_type():
    """Test for type of random_name output."""
    name = gsd._random_name()
    assert isinstance(name, str)

def test_make_record_output_type():
    """Test if random_record outputs a string."""
    rec = gsd._make_record('h.simpson', dt.datetime(2010,1,1,10,14,0), 
                               dt.datetime(2010,1,1,16,0,0))
    assert isinstance(rec, str)

def test_make_record_valid_xml():
    """Test if random_record output produces valid XML"""
    rec = gsd._make_record('h.simpson', dt.datetime(2010,1,1,10,14,0), 
                               dt.datetime(2010,1,1,16,0,0))
    xml = et.fromstring(rec)

def test_make_record_root():
    """Test if random record root is a <person> tag."""
    rec = gsd._make_record('h.simpson', dt.datetime(2010,1,1,10,14,0), 
                               dt.datetime(2010,1,1,16,0,0))
    xml = et.fromstring(rec)
    assert xml.tag == 'person'

@pytest.mark.parametrize("tag", ['start', 'end'])
def test_make_record_has_tag(tag):
    """Test if generated random record has the predefined XML tags."""
    rec = gsd._make_record('h.simpson', dt.datetime(2010,1,1,10,14,0), 
                               dt.datetime(2010,1,1,16,0,0))
    xml = et.fromstring(rec)
    assert xml.find(tag) is not None

def test_batch_length():
    """Test if batch string length is at least 100 times greater than 
    amount of it's components (avg. length of a record is 111 chars).
    """
    batch_s = gsd._batch_of_records(1000)
    assert len(batch_s) > 100000


