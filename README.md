# Clock In Clock Out

Clock-In-Clock-Out is a Python module and an application that enables reading time-sheet data from XML files of pre-defined format (see Source Format below), analyzing it, filtering it by date range and aggregating by date and (optionally) person.

Clock-In-Clock-Out is also available as a CLI tool (see CLI Usage below).

## Features

- Read time-sheet data from an XML file
- Calculate total working time per date
- Filter data by date range
- Group data by person (optional)
- Memory usage doesn't depend on source file size

## Usage

Clock-In-Clock-Out module can be used in three principal ways:
1. as a Docker container packaged app
2. as a Python standalone script
3. as a Python library
Please see details below:

### Docker usage

Clock-In-Clock-Out Docker container is available from Docker hub at:
```
$ docker run meklenbpo/xml_timesheet
```
The app has a help system implemented and available at:
```
$ docker run meklenbpo/xml_timesheet -h
```
The app has 1 positional (required) argument - `xml_filename` - i.e. name of the file to be analyzed and 3 optional arguments:
- `-s, --start DD-MM-YYY` - start date filter, if specified, the dates before start date will not be taken into account
- `-e, --end DD-MM-YYYY` - end date filter, if specified, the dates after end date will not be taken into account
- `-n, --names` - names flag, if specified the app will break down daily totals by person

Docker container includes a sample dataset for testing purposes `sample_data.xml`.

```
$ docker run meklenbpo/xml_timesheet sample_data.xml
         date   time
0  01-01-2000  15.24
1  02-01-2000  51.80
2  03-01-2000  19.07
3  04-01-2000  27.86
4  05-01-2000  29.78
5  06-01-2000  35.61
6  07-01-2000  36.24
7  08-01-2000  43.88

$ docker run meklenbpo/xml_timesheet sample_data.xml -s04-01-2000
         date   time
0  04-01-2000  27.86
1  05-01-2000  29.78
2  06-01-2000  35.61
3  07-01-2000  36.24
4  08-01-2000  43.88

$ docker run meklenbpo/xml_timesheet sample_data.xml -e01-01-2000 -n
         date    full_name  time
0  01-01-2000    a.bobrova  1.81
1  01-01-2000   b.viktorov  3.24
2  01-01-2000  f.alekseyev  0.36
3  01-01-2000     n.razina  9.83
```

In order to process one's own timesheet data, one will need to mount a
local directory into the docker container. For example to query a local file */path/to/local/file/timesheet.xml* one will need to run the following command:

```
$ docker run -v /path/to/local/file/:/app/data meklenbpo/xml_timesheet data/timesheet.xml
```

Any other arguments can be applied to mounted data files as well:
```
$ docker run -v /path/to/local/file/:/app/data meklenbpo/xml_timesheet data/timesheet.xml -s01-01-2000 --end 04-01-2000 --names
```


### Python library

Once all the dependencies (lxml and pandas, see requirements.txt for more details) are in place Clock-In-Clock-Out library can be used by simply importing main module. See the examples below:

#### Basic query, no filtering, no break down by person:

```python
import clock_in_clock_out as cc
cc.query('./sample_data.xml')
```

results in:
```
         date   time
0  01-01-2000  32.93
1  02-01-2000  28.06
2  03-01-2000  29.73
3  04-01-2000  18.42
4  05-01-2000  33.49
5  06-01-2000  53.07
6  07-01-2000  28.50
7  08-01-2000  23.43
8  31-12-2018  10.00
```

#### Filtering by date range

To enable filtering by date range one of the two arguments must be
provided:

`start: str` - starting date in `%d-%m-%Y` format. If provided, only
records starting on or later than specified date will be taken into
account.

`end: str` - ending date in `%d-%m-%Y` format. If provided, only records
ending before or on the specified date will be taken into account.

```python
import clock_in_clock_out as cc
cc.query('./sample_data.xml', start='01-01-2000', end='04-01-2000')
```

results in:
```
         date   time
0  01-01-2000  53.95
1  02-01-2000  65.84
2  03-01-2000  91.91
3  04-01-2000  51.05
```

#### Break down by employee is enabled:

To enable break down by person optional `names` argument must be set to
`True` (is `False` by default):

```python
import clock_in_clock_out as cc
cc.query('./sample_data.xml', names=True)
```

results in:
```
          date    full_name   time
0   01-01-2000  d.maksimova   3.98
1   01-01-2000      e.osina   5.07
2   01-01-2000   f.stepanov   3.58
3   01-01-2000   i.nikolaev   2.58
4   01-01-2000  k.germanova  10.91
..         ...          ...    ...
84  08-01-2000     s.ivanov   0.12
85  08-01-2000    t.fedorov   6.07
86  08-01-2000   t.tolstaya   6.76
87  08-01-2000     v.petrov   1.21
88  31-12-2018    h.simpson  10.00
```

### CLI Usage

Clock-In-Clock-Out can also be run via a Command Line Interface. The standalone script to run is `app.py`. Please see the examples below:

```
$ python app.py -h

usage: app.py [-h] [-s START] [-e END] [-n] xml_filename

Clock-In-Clock-Out: time-sheet analysis

positional arguments:
  xml_filename          source time-sheet file (.XML)

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        starting date filter in DD-MM-YYYY format
  -e END, --end END     ending date filter in DD-MM-YYYY format
  -n, --names           a flag that provides data break down by person
```

Examples:

```
$ python app.py sample_data.xml
...

$ python app.py sample_data.xml --names
...

$ python app.py sample_data.xml --start 01-01-2000 --end 02-01-2000
...

$ python app.py sample_data.xml -s01-01-2000 -e31-12-2008 -n
...
```

## Testing

The app's acceptance test suite is located at: `tests/test_acceptance.py` and features all important use cases of the code base.

The unit tests are located in:
- `tests/test_unit_clock_in_clock_out.py`
- `tests/test_unit_generate_xml.py`

## Additional information

### Source data format

An example of source time-sheet XML file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<people>
    <person full_name="i.ivanov">
        <start>21-12-2011 10:54:47</start>
        <end>21-12-2011 19:43:02</end>
    </person>
    <person full_name="a.stepanova">
        <start>21-12-2011 09:40:10</start>
        <end>21-12-2011 17:59:15</end>
    </person>
...
</people>
```

### Time-sheet XML Schema:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
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
</xs:schema>
```

