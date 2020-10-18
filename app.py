#!/usr/bin/env python3

"""
A script that provides command-line interface to the 
Clock-In-Clock-Out module.

Usage:
./python runner.py [-h] [--file SAMPLE.XML] [--start 01-01-2000]
                   [--end 01-01-2000] [--names]

Required parameters:

file: - name of the source time-sheet file to query,

Optional parameters:

--start:  - a starting date filter. Dates before specified date will not
            be taken into account.

--end:    - an ending date filter. Dates after the specified date will 
            not be taken into account.

--names:  - if provided the time-records will be broken down by person.
"""

import argparse
from datetime import datetime
import pandas as pd

import clock_in_clock_out as cc


def validate_date(date_str):
    """Check if the argument string is in %d-%m-%Y format and raise
    argparse.ArgumentTypeError if it isn't."""
    try:
        _dt = datetime.strptime(date_str, '%d-%m-%Y')
        return date_str
    except ValueError:
        raise argparse.ArgumentTypeError(f'{date_str} is not a valid '
                                         'date in DD-MM-YYYY format.')


if __name__ == '__main__':
    
    # Greeting
    print('\n'
          '==================\n'
          'Clock-In-Clock-Out\n'
          '==================\n'
          '\n'
          'Time-sheet analysis software\n'
          '----------------------------')

    # Parse CLI arguments
    cc_description = 'Clock-In-Clock-Out: time-sheet analysis'
    parser = argparse.ArgumentParser(description=cc_description)
    parser.add_argument('xml_filename', type=str,
                        help='source time-sheet file (.XML)')
    parser.add_argument('-s', '--start', type=validate_date,
                        help='starting date filter in DD-MM-YYYY format')
    parser.add_argument('-e', '--end', type=validate_date,
                        help='ending date filter in DD-MM-YYYY format')
    parser.add_argument('-n', '--names', action='store_true',
                        help='a flag that provides data break down by person')
    args = parser.parse_args()
    query_args = vars(args)

    # Run analysis
    print(f'Processing {args.xml_filename}:\n')
    pd.set_option('display.max_rows', None)
    print(cc.query(**query_args))
    print('\nCompleted successfully.\n')