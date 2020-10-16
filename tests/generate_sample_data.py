"""
generate_sample_data
--------------------

implements generating sample data in predefined time-sheet format.

`write_sample_file(filename: str, num_rec: int)` is the only exposed 
method. It generates a sample file of the specified size (by number of
records).

generate_sample_data can also be run as a standalone module.

Usage:

./python generate_sample_data.py [filename] [number_of_records]

Warning:

Because it is a auxiliary script, arguments validation is not 
implemented.
"""

import datetime as dt
import random
from lxml import etree as et
import sys


def _random_dt(start: dt.datetime, end: dt.datetime) -> dt.datetime:
    """Generate a random date/time object between two provided date/time
    objects.
    """
    if end < start:
        raise ValueError('End time less than start time')
    range_seconds = int((end - start).total_seconds())
    random_second = random.randint(0, range_seconds)
    return start + dt.timedelta(seconds=random_second)

def _random_name() -> dt.datetime:
    """Generate a random person name."""
    initials = 'abdefgiklmnoprstv'
    last_names = ['alekseyev', 'bobrova', 'demyanenko', 'evstigneeva',
        'fedorov', 'germanova', 'ivanov', 'klimova', 'losev', 'maksimova',
        'nikolaev', 'osina', 'petrov', 'razina', 'stepanov', 'tolstaya',
        'viktorov']
    return f'{random.choice(initials)}.{random.choice(last_names)}'

def _make_record(fname: str, start: dt.datetime, end: dt.datetime) -> str:
    """Generate a time-sheet record in a predefined format, given the 
    input data.
    """
    start_formatted = start.strftime('%d-%m-%Y %H:%M:%S')
    end_formatted = end.strftime('%d-%m-%Y %H:%M:%S')
    record = (f'\t<person full_name="{fname}">\n'
              f'\t\t<start>{start_formatted}</start>\n'
              f'\t\t<end>{end_formatted}</end>\n'
              f'\t</person>\n')
    return record

def _random_record() -> str:
    """Generate a random time-sheet record in predefined format 
    respecting the following assumptions:
    
    - all dates/times mut be in range 01/01/2000 0:00 - 31/12/2019 23:59
    - a person can clock in at any time
    - a person must clock out not later than 12 hours after clock in.
    """
    start_time = _random_dt(dt.datetime(2000, 1, 1, 0, 0, 0),
                           dt.datetime(2000, 1, 8, 23, 59, 59))
    end_time = _random_dt(start_time, start_time + dt.timedelta(hours=12))
    record = _make_record(_random_name(), start_time, end_time)
    return record

def _control_record() -> str:
    """Return a predefined record to be used as a control case for
    acceptance test scenario.
    """
    return _make_record('h.simpson', dt.datetime(2018, 12, 31, 20, 0, 0),
                        dt.datetime(2019, 1, 1, 6, 0, 0))

def _batch_of_records(num: int) -> str:
    """Generate a `num` of records and return them as a single str."""
    batch_rec = ''
    for _ in range(num):
        batch_rec += _random_record()
    return batch_rec

def write_sample_file(filename: str, num_rec: int):
    """Generate and write a file of arbitrary size.
    
    File size is specified in number of records. Each record takes
    approximately 200 bytes on average.
    """
    batch_size = 1000000
    num_batches = int(num_rec / batch_size)
    remainder = num_rec - num_batches * batch_size
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<people>\n'
    footer = '</people>'
    with open(filename, 'w') as f:
        f.write(header)
        f.write(_control_record())
        for _ in range(num_batches):
            s = _batch_of_records(batch_size)
            f.write(s)
        s = _batch_of_records(remainder)
        f.write(s)
        f.write(footer)


if __name__ == '__main__':
    filename = sys.argv[1]
    num_of_recs = int(sys.argv[2])
    print(f'Generating sample time-sheet data XML file: {filename}, '
          f'with number of records: {num_of_recs}')
    write_sample_file(filename, num_of_recs)
