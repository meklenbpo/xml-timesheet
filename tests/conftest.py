"""
Fixtures for the project's testing suite.
"""

from datetime import datetime
import pytest
import random


# Init. parameters

def random_dt(min_dt: datetime, max_dt: datetime) -> str:
    """Generate a random date/time object between two date/time 
    objects."""
    return '2020-01-01'

def random_record() -> tuple:
    """Generate a random timesheet record in predefined format, based on
    predefined initialization values."""
    initials = 'abdefgiklmnoprstv'
    last_names = ['alekseyev', 'bobrova', 'demyanenko', 'evstigneeva',
        'fedorov', 'germanova', 'ivanov', 'klimova', 'losev', 'maksimova',
        'nikolaev', 'osina', 'petrov', 'razina', 'stepanov', 'tolstaya',
        'viktorov']
    earliest_date = '2010-01-01'
    latest_date = '2019-12-31'
    pass

@pytest.fixture
def sample_data_xml():
    """Generate a sample XML based on the project's requirements."""
    pass