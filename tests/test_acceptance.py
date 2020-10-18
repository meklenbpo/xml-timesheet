"""

Acceptance test suite:
======================

Tests that demonstarte the usage of the clock_in_clock_out module for
the most important use-cases.
"""

import os
import pandas as pd
import pytest

import clock_in_clock_out as cc

@pytest.fixture
def mock_xml():
    """Create a small test XML that covers basic scenarios."""
    filename = './mock_data.xml'
    xml_content = ('<?xml version="1.0" encoding="UTF-8"?>'
                   '<people>'
                   '  <person full_name="h.simpson">'
                   '    <start>01-01-2020 10:00:00</start>'
                   '    <end>01-01-2020 19:00:00</end>'
                   '  </person>'
                   '  <person full_name="d.vader">'
                   '    <start>01-01-2020 11:00:00</start>'
                   '    <end>01-01-2020 17:00:00</end>'
                   '  </person>'
                   '  <person full_name="h.simpson">'
                   '    <start>02-01-2020 10:00:00</start>'
                   '    <end>02-01-2020 18:00:00</end>'
                   '  </person>'
                   '  <person full_name="h.simpson">'
                   '    <start>03-01-2020 10:00:00</start>'
                   '    <end>03-01-2020 19:00:00</end>'
                   '  </person>'
                   '  <person full_name="h.simpson">'
                   '    <start>04-01-2020 20:00:00</start>'
                   '    <end>05-01-2020 02:00:00</end>'
                   '  </person>'
                   '</people>')
    with open(filename, 'w') as f:
        f.write(xml_content)
    yield filename
    os.remove(filename)


def test_scenario_1(mock_xml):
    """Testing the most basic usage scenario - working time by date, no
    filters by date, no breakdown by person."""
    results = cc.query(mock_xml)
    expected = pd.DataFrame([{'date':'01-01-2020', 'time':15.0},
                             {'date':'02-01-2020', 'time':8.0},
                             {'date':'03-01-2020', 'time':9.0},
                             {'date':'04-01-2020', 'time':6.0}],
                             index=[0,1,2,3])
    pd.testing.assert_frame_equal(results, expected)

def test_scenario_2(mock_xml):
    """Testing filtering by date - working time by date, limited by
    start date only, no breakdown by person."""
    results = cc.query(mock_xml, start='03-01-2020')
    expected = pd.DataFrame([{'date':'03-01-2020', 'time':9.0},
                             {'date':'04-01-2020', 'time':6.0}],
                             index=[0,1])
    pd.testing.assert_frame_equal(results, expected)

def test_scenario_3(mock_xml):
    """Testing filtering by date - working time by date, limited by
    end date only, no breakdown by person."""
    results = cc.query(mock_xml, end='02-01-2020')
    expected = pd.DataFrame([{'date':'01-01-2020', 'time':15.0},
                             {'date':'02-01-2020', 'time':8.0}],
                             index=[0,1])
    pd.testing.assert_frame_equal(results, expected)

def test_scenario_4(mock_xml):
    """Testing filtering by date - working time by date, limited by
    both start and end dates, no breakdown by person."""
    results = cc.query(mock_xml, start='02-01-2020', end='02-01-2020')
    expected = pd.DataFrame([{'date':'02-01-2020', 'time':8.0}], index=[0])
    pd.testing.assert_frame_equal(results, expected)

def test_scenario_5(mock_xml):
    """Testing break down by person - working time by date, limited by
    both start and end dates, break down by person = True."""
    results = cc.query(mock_xml, start='01-01-2020', end='01-01-2020',
                       names=True)
    expected = pd.DataFrame([
        {'date':'01-01-2020', 'full_name':'d.vader', 'time':6.0},
        {'date':'01-01-2020', 'full_name':'h.simpson', 'time':9.0}],
        index=[0, 1])
    pd.testing.assert_frame_equal(results, expected)