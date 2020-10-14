"""
Fixtures for the project's testing suite.
"""

import datetime as dt
import os
import pytest
import random
import xml.etree.ElementTree as et


# XML generating fixture and functions that it requires
def random_dt(start: dt.datetime, end: dt.datetime) -> dt.datetime:
    """Generate a random date/time object between two provided date/time
    objects."""
    if end < start:
        raise ValueError('End time less than start time')
    range_seconds = int((end - start).total_seconds())
    random_second = random.randint(0, range_seconds)
    return start + dt.timedelta(seconds=random_second)

def random_name() -> dt.datetime:
    """Generate a random person name."""
    initials = 'abdefgiklmnoprstv'
    last_names = ['alekseyev', 'bobrova', 'demyanenko', 'evstigneeva',
        'fedorov', 'germanova', 'ivanov', 'klimova', 'losev', 'maksimova',
        'nikolaev', 'osina', 'petrov', 'razina', 'stepanov', 'tolstaya',
        'viktorov']
    return f'{random.choice(initials)}.{random.choice(last_names)}'

def make_record(fname: str, start: dt.datetime, end: dt.datetime) -> str:
    """Generate a timesheet record in a predefined format, given the 
    input data."""
    start_formatted = start.strftime('%Y-%m-%d %H:%M:%S')
    end_formatted = end.strftime('%Y-%m-%d %H:%M:%S')
    record = (f'\t<person full_name="{fname}">\n'
              f'\t\t<start>{start_formatted}</start>\n'
              f'\t\t<end>{end_formatted}</end>\n'
              f'\t</person>\n')
    return record

def random_record() -> str:
    """Generate a random timesheet record in predefined format 
    respecting the following assumptions:
    
    - all dates/times mut be in range 01 Jan 2000 0:00 - 31 Dec 2019 23:59
    - a person can clock in at any time
    - a person must clock out not later than 12 hours after clock in.
    """
    start_time = random_dt(dt.datetime(2000, 1, 1, 0, 0, 0),
                           dt.datetime(2000, 1, 8, 23, 59, 59))
    end_time = random_dt(start_time, start_time + dt.timedelta(hours=12))
    record = make_record(random_name(), start_time, end_time)
    return record

def control_record() -> str:
    """Return a predefined record to be used as a control case for
    acceptance test scenario."""
    return make_record('h.simpson', dt.datetime(2018, 12, 31, 20, 0, 0),
                        dt.datetime(2019, 1, 1, 6, 0, 0))

def batch_of_records(num: int) -> str:
    """Generate a `num` of records and return them as a single str."""
    batch_rec = ''
    for _ in range(num):
        batch_rec += random_record()
    return batch_rec

def write_file(filename: str, num_rec: int):
    """Generate and write a file of arbitrary size."""
    batch_size = 1000000
    num_batches = int(num_rec / batch_size)
    remainder = num_rec - num_batches * batch_size
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<people>\n'
    footer = '</people>'
    with open(filename, 'w') as f:
        f.write(header)
        f.write(control_record())
        for _ in range(num_batches):
            s = batch_of_records(batch_size)
            f.write(s)
        s = batch_of_records(remainder)
        f.write(s)
        f.write(footer)

@pytest.fixture
def small_xml():
    """A pytest fixture that generates a small sample XML dataset."""
    filename = './sample_data.xml'
    write_file(filename, 50)
    yield filename
    os.remove(filename)