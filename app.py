"""
A script that provides command-line interface to the 
Clock-In-Clock-Out module.

Usage:
./python app.py [-h] [--file SAMPLE.XML] [--start 01-01-2000]
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
from lxml import etree
import pandas as pd
import sys

import clock_in_clock_out as cc


def _validate_arg_date(date_str):
    """Check if the argument string is in %d-%m-%Y format and raise
    argparse.ArgumentTypeError if it isn't."""
    try:
        _dt = datetime.strptime(date_str, '%d-%m-%Y')
        return date_str
    except ValueError:
        raise argparse.ArgumentTypeError(f'{date_str} is not a valid '
                                         'date in DD-MM-YYYY format.')

def _parse_arguments():
    """Parse command-line arguments and return them as a dict that can
    be used to run the query function."""
    description = 'Clock-In-Clock-Out: time-sheet analysis'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('xml_filename', type=str,
                        help='source time-sheet file (.XML)')
    parser.add_argument('-s', '--start', type=_validate_arg_date,
                        help='starting date filter in DD-MM-YYYY format')
    parser.add_argument('-e', '--end', type=_validate_arg_date,
                        help='ending date filter in DD-MM-YYYY format')
    parser.add_argument('-n', '--names', action='store_true',
                        help='a flag that provides data break down by person')
    args = parser.parse_args()
    return vars(args)

def main():
    """Top-level runner function.
    
    Parse the command-line arguments into analysis function compatible
    arguments dictionary, run the analysis function and display the 
    results.
    """
    args = _parse_arguments()
    try:
        results = cc.query(**args)
    # Gracefully process fatal errors
    except FileNotFoundError:
        print(f'Error. File {args["xml_filename"]} not found.')
        sys.exit(1)
    except etree.XMLSyntaxError:
        print(f'Error. Invalid XML (schema validation fails)')
        sys.exit(1)
    pd.set_option('display.max_rows', None)
    print(results)

if __name__ == "__main__":
    main()
