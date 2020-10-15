# Clock In Clock Out

Clock-In-Clock-Out is a Python module that enables reading time-sheet
data from XML files of pre-defined format (see Source Format below),
analyzing it, filtering it by date range and aggregating by date and
(optionally) person.

## Features

- Read time-sheet data from an XML file
- Calculate total working time per date
- Filter data by date range
- Group data by person (optional)
- Memory usage doesn't depend on source file size

## Usage

### Basic usage

Query time-sheet data for aggregated totals of work time by date. 
No filtering, no break down by person:

```python
import clock_in_clock_out as cc
cc.query('./sample_data.xml')
```

results in:
```
         date   time
0  01-01-2000  53.95
1  02-01-2000  65.84
2  03-01-2000  91.91
3  04-01-2000  51.05
4  05-01-2000  56.09
5  06-01-2000  84.83
6  07-01-2000  92.99
```


### Filtering by date range

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

### Break down by employee is enabled:

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

## Source Format

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

