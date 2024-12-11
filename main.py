import pandas as pd
from icalendar import Calendar
import datetime
import os

# Function to process the calendar.ics file
def parse_ics_to_dataframe(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

    with open(file_path, 'rb') as f:
        calendar = Calendar.from_ical(f.read())
    
    events = []
    for event in calendar.walk('VEVENT'):
        start = event.get('DTSTART').dt
        end = event.get('DTEND').dt
        summary = event.get('SUMMARY', '')
        location = event.get('LOCATION', '')
        description = event.get('DESCRIPTION', '').replace("\n", " ").replace(",", " ")
        uid = event.get('UID', '')
        created = event.get('DTSTAMP').dt

        # Adding placeholder fields for Qualtrics-specific requirements
        status = ""
        ip_address = ""
        progress = 100
        duration = ""
        finished = True
        location_latitude = ""
        location_longitude = ""
        distribution_channel = ""
        user_language = ""

        events.append([
            start, end, status, ip_address, progress, duration, finished, created, uid, "", "", "", "", location_latitude, location_longitude, distribution_channel, user_language, "", summary, "", "", description, location
        ])

    columns = [
        "StartDate", "EndDate", "Status", "IPAddress", "Progress", "Duration (in seconds)", "Finished", "RecordedDate", "ResponseId", 
        "RecipientLastName", "RecipientFirstName", "RecipientEmail", "ExternalReference", "LocationLatitude", "LocationLongitude", 
        "DistributionChannel", "UserLanguage", "Q_RecaptchaScore", "EventName", "QID16", "QID20", "QID19", "Location"
    ]
    df = pd.DataFrame(events, columns=columns)
    return df

# Function to export DataFrame to CSV
def export_to_csv(df, file_name="calendar_output.csv"):
    df.to_csv(file_name, index=False)
    print(f"Data successfully saved to {file_name}")

ics_file_path = "calendar.ics"
try:
    df = parse_ics_to_dataframe(ics_file_path)
    export_to_csv(df)
except FileNotFoundError as e:
    print(e)
