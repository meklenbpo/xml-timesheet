"""
clock_in_clock_out
------------------

includes main functionality for clock_in_clock_out module.

`query(xml_filename: str, start: str, end: str, names: bool):` is the
only exposed function - it provides the ability to query an XML file for
time-sheet data, filter and aggregate it.
"""

from datetime import datetime
from lxml import etree
import pandas as pd
import resource


def _get_mem_usage() -> float:
    """Measure current memory usage and return as decimal Mbs."""
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(mem/1024/1024, 2)

def _log_mem_usage(log_filename: str):
    """Save momentary memeory usage to a log file."""
    with open(log_filename, 'w') as log:
        timestamp = datetime.now().strftime('%D %T')
        log.write(f'{timestamp}: {_get_mem_usage()} Mb.\n')

def _schema() -> etree.XMLSchema:
    """Generate etree.XMLSchema for the predefined time-sheet format."""
    s = b'''<?xml version="1.0" encoding="UTF-8" ?>
           <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
             <xs:element name="people">
               <xs:complexType>
                 <xs:sequence>
                   <xs:element name="person" maxOccurs="unbounded">
                     <xs:complexType>
                       <xs:sequence>
                         <xs:element name="start" type="xs:string" minOccurs="1" maxOccurs="1"/>
                         <xs:element name="end" type="xs:string" minOccurs="1" maxOccurs="1"/>
                       </xs:sequence>
                       <xs:attribute name="full_name" type="xs:string" use="required"/>
                     </xs:complexType>
                   </xs:element>
                 </xs:sequence>
               </xs:complexType>
             </xs:element>
           </xs:schema>'''
    xml = etree.XML(s)
    return etree.XMLSchema(xml)

def _init_xml(xml_filename: str) -> etree.iterparse:
    """Open an XML file for iterative parsing."""
    xml = etree.iterparse(xml_filename, tag='person', schema=_schema(), 
                          events=('end',))
    return xml

def _extract_data_from_element(e: etree.Element) -> dict:
    """Extract useful data from a single XML Element."""
    return {'full_name': e.get('full_name'),
            'start': e[0].text,
            'end': e[1].text}

def _clear_element(e: etree.Element):
    """Clear XML Element and delete references to its parents."""
    e.clear()
    while e.getprevious() is not None:
        del e.getparent()[0]

def _get_batch(xml_filename: str, batch_size: int) -> tuple:
    """Read a `batch_size` of records from an XML file."""
    batch = []
    counter = 0
    for _, element in _init_xml(xml_filename):
        if counter < batch_size:
            batch.append(_extract_data_from_element(element))
            _clear_element(element)
            counter += 1
        else:
            yield batch
            batch = []
            counter = 0
    yield batch

def _time_str_diff(dt_str_1: str, dt_str_2: str) -> float:
    """Calculate the time interval between two strings representing the
    date/time object in a predefined format. Return the interval as a 
    decimal number of hours."""
    dt_format = '%d-%m-%Y %H:%M:%S'
    dt1 = datetime.strptime(dt_str_1, dt_format)
    dt2 = datetime.strptime(dt_str_2, dt_format)
    delta = dt2 - dt1
    hours = round(delta.seconds / 60 / 60, 2)
    return hours

def _add_derivative_data(source_data: pd.DataFrame) -> pd.DataFrame:
    """Take a DataFrame of source time-sheet data (full_name, start and
    end times) and calculate derivative values: `date` and `time`."""
    data = source_data.copy()
    data['date'] = data.start.str[:10]
    data['time'] = data.apply(lambda x: _time_str_diff(x.start, x.end), axis=1)
    return data

def _filter_data(dataset: pd.DataFrame, start_date: str, 
                 end_date:str) -> pd.DataFrame:
    """Filter an augmented Dataframe of time-sheet data by `date` 
    column."""
    to_filter = dataset.copy()
    cols = list(to_filter.columns)
    fmt = '%d-%m-%Y'
    to_filter['date_dt'] = to_filter.date.apply(datetime.strptime, args=(fmt,))
    start_dt = datetime.strptime(start_date, fmt)
    end_dt = datetime.strptime(end_date, fmt)
    filtered = to_filter.loc[(to_filter.date_dt >= start_dt) &
                             (to_filter.date_dt <= end_dt)]
    return filtered[cols]

def _aggregate_data(dataset: pd.DataFrame, include_names: bool) -> pd.DataFrame:
    """Aggregate an augmented DataFrame of time-sheet data on `date` and
    (optionally) `full_name` columns."""
    to_agg = dataset.copy()
    if include_names:
        return to_agg[['date', 'full_name', 'time']].\
                     groupby(['date', 'full_name']).sum().reset_index()
    else:
        return to_agg[['date', 'time']].groupby('date').sum().reset_index()

def query(xml_filename: str, start: str = '01-01-1970', end: str = '31-12-2199',
          names: bool = False) -> pd.DataFrame:
    """
    Read time-sheet data from XML file, filter and aggregate it.
    
    `query` is a wrapper function that walks through the process of:
    - iteratively parsing an XML file,
    - analyzing the source data,
    - filtering time-sheet data by date range,
    - aggregating time-sheet data by date and (optionally) by person,
    - saving the results.
    """
    results = pd.DataFrame()
    for batch in _get_batch(xml_filename, 10):
        data_df = pd.DataFrame(batch)
        augm_data = _add_derivative_data(data_df)
        filtered_data = _filter_data(augm_data, start, end)
        results = results.append(filtered_data)
        results = _aggregate_data(results, names)
        _log_mem_usage('./mem_log.log')
    return results