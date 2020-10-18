"""
A test suite to cover main clock_in_clock_out module with unit tests.
"""

from lxml import etree
import pytest

import clock_in_clock_out.clock_in_clock_out as cc


def test_schema():
    """Test if _schema function returns a proper XMLSchema object."""
    assert isinstance(cc._schema(), etree.XMLSchema)

def test_extract_data(sample_xml_element):
    """Test extraction of data from XML element."""
    expected = {
        'full_name':'h.simpson',
        'start':'31-12-2018 20:00:00',
        'end':'01-01-2019 06:00:00'
    }
    assert cc._extract_data_from_element(sample_xml_element) == expected

def test_time_diff():
    """Test time difference from strings."""
    assert cc._time_str_diff('01-01-2000 10:00:00', '01-01-2000 11:00:00') == 1

def test_time_diff_over_midnight():
    """Test if time_diff function return correct values when the
    interval crosses the 0:00 line.
    """
    assert cc._time_str_diff('07-01-2018 23:00:00', '08-01-2018 02:00:00') == 3

def test_derivative_data_date(sample_source_df):
    """Test how dervative data (date column) is calculated."""
    der_data = cc._add_derivative_data(sample_source_df)
    assert list(der_data['date']) == ['02-01-2000', '12-09-2000', 
                                      '30-07-2009', '02-01-2000']

def test_filter_data(sample_derivate_df):
    """Test how data is filtered on start and end dates."""
    f_data = cc._filter_data(sample_derivate_df, '02-01-2000', '02-01-2000')
    assert len(f_data) == 2

def test_agg_data_names(sample_derivate_df):
    """Test how data is aggregated if names flag is True."""
    agg_data = cc._aggregate_data(sample_derivate_df, include_names=True)
    assert len(agg_data) == 4

def test_agg_data_names_off(sample_derivate_df):
    """Test how data is aggregated if names flag is False."""
    agg_data = cc._aggregate_data(sample_derivate_df, include_names=False)
    assert len(agg_data) == 3