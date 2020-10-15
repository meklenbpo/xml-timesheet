"""
clock_in_clock_out
------------------

includes main functionality for clock_in_clock_out module.
"""

from datetime import datetime
from lxml import etree
import pandas as pd


def _schema() -> etree.XMLSchema:
    """Prepare a predefined XML Schema and return it as etree.XMLSchema
    object."""
    s = b'''<?xml version="1.0" encoding="UTF-8" ?>
           <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
             <xs:element name="people">
               <xs:complexType>
                 <xs:sequence>
                   <xs:element name="person" maxOccurs="unbounded">
                     <xs:complexType>
                       <xs:sequence>
                         <xs:element name="start" type="xs:string" minOccurs="0" maxOccurs="1"/>
                         <xs:element name="end" type="xs:string" minOccurs="0" maxOccurs="1"/>
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
    """Open and XML file with predefined settings and return it as an 
    etree.iterparse object."""
    xml = etree.iterparse(xml_filename, tag='person', schema=_schema(), 
                          events=('end',))
    return xml

def _extract_data_from_element(e: etree.Element) -> dict:
    """Extract useful data from XML Element and return it via a
    dictionary."""
    return {'full_name': e.get('full_name'),
            'start': e[0].text,
            'end': e[1].text}

def _clear_element(e: etree.Element):
    """Clear XML Element and delete references to its parents."""
    e.clear()
    while e.getprevious() is not None:
        del e.getparent()[0]

def _get_batch(xml_filename: str, batch_size: int) -> tuple:
    """Read a `batch_size` of records from an XML file and yield it as
    a list of etree.Elements."""
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
    """Take two strings representing the date/time object in predefined
    format and calculate the time interval between them. Return the
    interval as a decimal number of hours."""
    dt_format = '%d-%m-%Y %H:%M:%S'
    dt1 = datetime.strptime(dt_str_1, dt_format)
    dt2 = datetime.strptime(dt_str_2, dt_format)
    delta = dt2 - dt1
    hours = round(delta.seconds / 60 / 60, 2)
    return hours

def _add_derivative_data(source_data: pd.DataFrame) -> pd.DataFrame:
    """Take a DataFrame of source data (full_name, start and end times)
    and calculate derivative values: `date` and `time`."""
    data = source_data.copy()
    data['date'] = data.start.str[:10]
    data['time'] = data.apply(lambda x: _time_str_diff(x.start, x.end), axis=1)
    return data

def _filter_data(dataset: pd.DataFrame, start_date: str, 
                 end_date:str) -> pd.DataFrame:
    """Take a Dataframe of predefined structure and filter it by `date`
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
    """Take a DataFrame of predefined structure and aggregate it on `date` and
    (optionally) `full_name` columns. Return as a pandas DataFrame."""
    to_agg = dataset.copy()
    if include_names:
        return to_agg[['date', 'full_name', 'time']].\
                     groupby(['date', 'full_name']).sum().reset_index()
    else:
        return to_agg[['date', 'time']].groupby('date').sum().reset_index()

def query(xml_filename: str, start: str = '01-01-1970', end: str = '31-12-2199',
          names: bool = False) -> pd.DataFrame:
    """Extract working time data from XML file chunk by chunk."""
    results = pd.DataFrame()
    for batch in _get_batch(xml_filename, 10):
        data_df = pd.DataFrame(batch)
        augm_data = _add_derivative_data(data_df)
        filtered_data = _filter_data(augm_data, start, end)
        results = results.append(filtered_data)
        results = _aggregate_data(results, names)
    return results