"""
Basic testing scenario to act as an acceptance test.
"""

import pytest

import clock_in_clock_out


def test_scenario_1(small_xml):
    """
    Basic testing scenario:
    1. Load data from sample_data.xml
    2. Query the dataset with predefined parameters.
    """
    data_table = clock_in_clock_out.Storage()
    data_table.load_xml(small_xml)
    clock = data_table.query('h.simpson', '2018-12-31', '2019-01-01')
    assert clock == 10