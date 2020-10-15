"""
Clock In Clock Out
==================

- Reads time sheet data from a formatted XML file (see data/time_data.xsd
for XML schema),
- Aggregates data by date and (optionally) person,
- Reports aggregated results as a pandas DataFrame.
"""

from datetime import datetime
from lxml import etree
import pandas as pd


def schema() -> etree.XMLSchema:
    """Load an XML validation schema from a predefined file and return
    it as an lxml object that can be used for parsing."""
    schema_filename = './data/time_data.xsd'
    schema_doc = etree.parse(schema_filename)
    return etree.XMLSchema(schema_doc)

def init_xml(xml_filename: str) -> etree.iterparse:
    """Open and XML file with predefined settings and return it as an 
    etree.iterparse object."""
    xml = etree.iterparse(xml_filename, tag='person', schema=schema(), 
                          events=('end',))
    return xml

def extract_data_from_element(e: etree.Element) -> dict:
    """Extract useful data from XML Element and return it via a
    dictionary."""
    return {'full_name': e.get('full_name'),
            'start': e[0].text,
            'end': e[1].text}

def clear_element(e: etree.Element):
    """Clear XML Element and delete references to its parents."""
    e.clear()
    while e.getprevious() is not None:
        del e.getparent()[0]

def get_batch(xml_filename: str, batch_size: int) -> tuple:
    """Read a `batch_size` of records from an XML file and yield it as
    a list of etree.Elements."""
    batch = []
    counter = 0
    for _, element in init_xml(xml_filename):
        if counter < batch_size:
            batch.append(extract_data_from_element(element))
            clear_element(element)
            counter += 1
        else:
            yield batch
            batch = []
            counter = 0
    yield batch

def time_str_diff(dt_str_1: str, dt_str_2: str) -> float:
    """Take two strings representing the date/time object in predefined
    format and calculate the time interval between them. Return the
    interval as a decimal number of hours."""
    dt_format = '%d-%m-%Y %H:%M:%S'
    dt1 = datetime.strptime(dt_str_1, dt_format)
    dt2 = datetime.strptime(dt_str_2, dt_format)
    delta = dt2 - dt1
    hours = round(delta.seconds / 60 / 60, 2)
    return hours

def add_derivative_data(source_data: pd.DataFrame) -> pd.DataFrame:
    """Take a DataFrame of source data (full_name, start and end times)
    and calculate derivative values: `date` and `time`."""
    data = source_data.copy()
    data['date'] = data.start.str[:10]
    data['time'] = data.apply(lambda x: time_str_diff(x.start, x.end), axis=1)
    return data

def filter_data(dataset: pd.DataFrame, start_date: str, 
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

def aggregate_data(dataset: pd.DataFrame, include_names: bool) -> pd.DataFrame:
    """Take a DataFrame of predefined structure and aggregate it on `date` and
    (optionally) `full_name` columns. Return as a pandas DataFrame."""
    to_agg = dataset.copy()
    if include_names:
        return to_agg[['date', 'full_name', 'time']].\
                     groupby(['date', 'full_name']).sum().reset_index()
    else:
        return to_agg[['date', 'time']].groupby('date').sum().reset_index()

def query(xml_filename: str, start_date: str = '01-01-1970',
          end_date: str = '31-12-2199', incl_names: bool = False) -> pd.DataFrame:
    """Extract working time data from XML file chunk by chunk."""
    results = pd.DataFrame()
    for batch in get_batch(xml_filename, 10):
        data_df = pd.DataFrame(batch)
        augm_data = add_derivative_data(data_df)
        filtered_data = filter_data(augm_data, start_date, end_date)
        results = results.append(filtered_data)
        results = aggregate_data(results, incl_names)
    return results