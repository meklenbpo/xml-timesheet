"""
Fixtures for the project's testing suite.
"""

from lxml import etree
import os
import pandas as pd
import pytest


@pytest.fixture
def sample_xml_element():
    """A fixture to generate a dummy xml Element."""
    el_s = ('<person full_name="h.simpson">'
            '<start>31-12-2018 20:00:00</start>'
            '<end>01-01-2019 06:00:00</end>'
            '</person>')
    return etree.fromstring(el_s)

@pytest.fixture
def sample_source_df():
    """A fixture to emulate a source data parsed dataframe."""
    data = [{'full_name':'a.bc', 'start':'02-01-2000 10:00:00', 
             'end':'02-01-2000 19:00:00'},
            {'full_name':'d.ef', 'start':'12-09-2000 10:00:00', 
             'end':'12-09-2000 19:00:00'},
            {'full_name':'g.hi', 'start':'30-07-2009 10:00:00', 
             'end':'30-07-2009 19:00:00'},
            {'full_name':'j.kl', 'start':'02-01-2000 10:00:00', 
             'end':'02-01-2000 19:00:00'}]
    data_df = pd.DataFrame(data)
    return data_df

@pytest.fixture
def sample_derivate_df():
    """A fixture to emulate a dataframe with derivative fields in 
    place."""
    data = [{'full_name':'a.bc', 'start':'02-01-2000 10:00:00', 
             'end':'02-01-2000 19:00:00', 'date':'02-01-2000', 'time':9},
            {'full_name':'a.bc', 'start':'12-09-2000 10:00:00', 
             'end':'12-09-2000 19:00:00', 'date':'12-09-2000', 'time':9},
            {'full_name':'g.hi', 'start':'30-07-2009 10:00:00', 
             'end':'30-07-2009 19:00:00', 'date':'30-07-2009', 'time':9},
            {'full_name':'j.kl', 'start':'02-01-2000 10:00:00', 
             'end':'02-01-2000 19:00:00', 'date':'02-01-2000', 'time':9}]
    data_df = pd.DataFrame(data)
    return data_df