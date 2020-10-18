"""
Clock In Clock Out
==================

Clock-In-Clock-Out is a Python module for reading and analyzing time
sheet data in a predefined XML format.

It can:
- Read time sheet data from an XML file of predefined format,
- Filter time sheet data by start and end date,
- Aggregate data by date and (optionally) person,
- Report the results as a pandas DataFrame.
- Generate random sample data in time-sheet format

Usage:

>>> import clock_in_clock_out as cc
>>> cc.query('sample.xml', start='01-01-2019', end='02-01-2019', names=False)
date        time
01-01-2019  12.1
02-01-2019  4.8

Breaking down by person:

>>> cc.query('sample.xml', start='01-01-2019', end='01-01-2019', names=True)
date        person      time
01-01-2019  i.ivanov    6.1
01-01-2019  s.tolstaya  6.0

Generating random sample data (50 time-sheet records):

>>> cc.write_file('sample.xml', 50)

"""

from .clock_in_clock_out import query
from .generate_sample_data import write_sample_file