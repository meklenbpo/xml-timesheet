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
No filtering, no aggregation by person:

```python
import clock_in_clock_out as cc
cc.query('./sample_data.xml')
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
cc.query('./sample_data.xml', start='01-01-2019', end='31-01-2019')
```

### Break down by employee is enabled:

To enable break down by person optional `names` argument must be set to
`True` (is `False` by default):

```python
import clock_in_clock_out as cc
cc.query('./sample_data.xml', names=True)
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

