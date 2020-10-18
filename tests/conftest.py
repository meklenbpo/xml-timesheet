"""
Fixtures for the project's testing suite.
"""

import os
import pytest

from generate_sample_data import write_sample_file


@pytest.fixture
def small_xml():
    """A pytest fixture that generates a small sample XML dataset."""
    filename = './sample_data.xml'
    write_sample_file(filename, 50)
    yield filename
    os.remove(filename)