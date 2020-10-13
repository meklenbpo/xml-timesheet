"""
Fixtures for the project's testing suite.
"""

from datetime import datetime
import pytest
import random


# Init. parameters

def random_dt(min_dt: datetime, max_dt: datetime) -> datetime:
    """Generate a random date/time object between two provided date/time
    objects."""
    return '2020-01-01'

def random_name() -> datetime:
    """Generate a random person name."""
    initials = 'abdefgiklmnoprstv'
    last_names = ['alekseyev', 'bobrova', 'demyanenko', 'evstigneeva',
        'fedorov', 'germanova', 'ivanov', 'klimova', 'losev', 'maksimova',
        'nikolaev', 'osina', 'petrov', 'razina', 'stepanov', 'tolstaya',
        'viktorov']
    return f'{random.choice(initials)}.{random.choice(last_names)}'

def random_record() -> str:
    """Generate a random timesheet record in predefined format."""
    return ''

@pytest.fixture
def sample_data_xml():
    """Generate a sample XML based on the project's requirements."""
    pass