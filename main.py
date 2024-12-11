import pandas as pd
from icalendar import Calendar
import datetime
import os

# Function to process the calendar.ics file
def parse_ics_to_dataframe(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

    with open(file_path, 'r') as f:
        calendar = Calendar.from_ical(f.read())
    
    events = []
    for event in calendar.walk('VEVENT'):
        start = event.get('DTSTART').dt
        end = event.get('DTEND').dt
        summary = event.get('SUMMARY', '')
        location = event.get('LOCATION', '')
        description = event.get('DESCRIPTION', '')
        uid = event.get('UID', '')
        created = event.get('DTSTAMP').dt
        
        events.append([
            start, end, summary, location, description, created, uid
        ])

    columns = [
        "StartDate", "EndDate", "EventName", "Location", "Description", "RecordedDate", "ResponseId"
    ]
    df = pd.DataFrame(events, columns=columns)
    return df

# Function to export DataFrame to CSV
def export_to_csv(df, file_name="calendar_output.csv"):
    df.to_csv(file_name, index=False)
    print(f"Data successfully saved to {file_name}")

# Example usage
ics_file_path = "/mnt/data/calendar.ics"
try:
    df = parse_ics_to_dataframe(ics_file_path)
    export_to_csv(df)
except FileNotFoundError as e:
    print(e)
