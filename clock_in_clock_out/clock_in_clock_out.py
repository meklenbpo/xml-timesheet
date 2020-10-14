"""
Clock In Clock Out module
=========================

A module that implements basic functionality for the project:
- reads data from source XML file
- organizes the data within the table as necessary
- queries table for total timesheet values (per person/date range).
"""

import datetime as dt
from lxml import etree
import os
import pandas as pd

def validate_xml_by_schema(filename: str):
    """Validate input XML file by predefined schema. Raise an exception
    if the tested file is not valid."""
    pass

def query(filename: str, start: str = '1970-01-01', end: str = '9999-12-31', 
          incl_persons: bool = False) -> pd.DataFrame:
    """Sequentially read through an XML file (`source_filename`) and
    calculate total working time per date and (optionally) per person on
    the fly. The results are saved to a `target_filename` as CSV.
    """
    validate_xml_by_schema(filename)
    xml = etree.iterparse(filename, tag='person', events=['end'])
    query_df = pd.DataFrame()
    buffer_size = 10
    counter = 0
    buffer_rows = []
    for _, element in xml:
        if counter < buffer_size:
            # Extract source values
            f_name = element.get('full_name')
            st_time = dt.datetime.strptime(element[0].text, '%Y-%m-%d %H:%M:%S')
            en_time = dt.datetime.strptime(element[1].text, '%Y-%m-%d %H:%M:%S')
            element.clear()
            # Calculate and filter output values
            st_date = st_time.strftime('%Y-%m-%d')
            if start <= st_date <= end:
                duration = round((en_time - st_time).seconds/60/60, 2)
                row = {'person': f_name if incl_persons else '', 
                       'date': st_date, 
                       'time': duration}
                buffer_rows.append(row)
                counter += 1
            else: # date out of range
                pass 
        else: # buffer filled
            query_df = query_df.append(pd.DataFrame(buffer_rows))
            query_df = query_df.groupby(['date', 'person']).sum().reset_index()
            buffer_rows = []
            counter = 0
    # XML file exhausted, process unflushed buffer
    query_df = query_df.append(pd.DataFrame(buffer_rows))
    query_df = query_df.groupby(['date', 'person']).sum().reset_index()
    # Export
    if incl_persons:
        return query_df
    else:
        return query_df[['date', 'time']]

query('./sample_data.xml', incl_persons=True)