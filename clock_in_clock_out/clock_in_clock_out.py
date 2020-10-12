"""
Clock In Clock Out module
=========================

A module that implements basic functionality for the project:
- reads data from source XML file
- organizes the data within the table as necessary
- queries table for total timesheet values (per person/date range).
"""

class Storage:
    
    """The timesheet data table."""
    
    def __init__(self):
        pass

    def load_xml(self, filename):
        """Read the data from XML file."""
        pass

    def query(self, person, start_date, end_date) -> float:
        """
        Query the table for clock in / clock out values, aggregate
        them by date and return the value as a decimal number of hours.
        """
        return 0.0