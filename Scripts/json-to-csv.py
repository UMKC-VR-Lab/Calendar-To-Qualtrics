import json
import pandas as pd

# Load JSON data from a file
input_file = "Data/processed-calendar.json"
with open(input_file, "r") as file:
    json_data = json.load(file)

# Define mapping from event keys to Qualtrics columns
mapping = {
    "Date": "StartDate",
    "Progress": "Progress",
    "RecipientLastName": "RecipientLastName",
    "RecipientFirstName": "RecipientFirstName",
    "RecipientEmail": "RecipientEmail",
    "What is your primary purpose for visiting the Innovation Studio today?": "QID20",
    "Name of Your Organization": "QID19",
    "Email": "QID21",
    "Estimated Group Size": "QID24",
    "Type of Visit": "QID25",
    "Brief Description of the Project": "QID28"
}

# Define full list of required Qualtrics columns
qualtrics_columns = [
    "StartDate", "EndDate", "Status", "IPAddress", "Progress", "Duration (in seconds)", "Finished", "RecordedDate", "ResponseId",
    "RecipientLastName", "RecipientFirstName", "RecipientEmail", "ExternalReference", "LocationLatitude", "LocationLongitude",
    "DistributionChannel", "UserLanguage", "Q_RecaptchaScore", "QID3", "QID16", "QID20", "QID19", "QID21", "QID24",
    "QID25", "QID27", "QID26", "QID28"
]

# Define friendly names for the second row of the header
friendly_names = [
    "Start Date", "End Date", "Response Type", "IP Address", "Progress", "Duration (in seconds)", "Finished", "Recorded Date", "Response ID",
    "Recipient Last Name", "Recipient First Name", "Recipient Email", "External Data Reference", "Location Latitude", "Location Longitude",
    "Distribution Channel", "User Language", "Q_RecaptchaScore", "First and Last Name", "Affiliation: What is your primary role? (Choose one)",
    "What is your primary purpose for visiting the Innovation Studio today? (Choose one)", "Name of Your Organization", "Email",
    "(Office use only) Estimated Group Size", "Type of Visit", "Spaces Toured", "Equipment Used", "Brief Description of the Project"
]

# Define ImportId row data
import_id_row = {
    "StartDate": "{\"ImportId\":\"startDate\",\"timeZone\":\"America/Denver\"}",
    "EndDate": "{\"ImportId\":\"endDate\",\"timeZone\":\"America/Denver\"}",
    "Status": "{\"ImportId\":\"status\"}",
    "IPAddress": "{\"ImportId\":\"ipAddress\"}",
    "Progress": "{\"ImportId\":\"progress\"}",
    "Duration (in seconds)": "{\"ImportId\":\"duration\"}",
    "Finished": "{\"ImportId\":\"finished\"}",
    "RecordedDate": "{\"ImportId\":\"recordedDate\",\"timeZone\":\"America/Denver\"}",
    "ResponseId": "{\"ImportId\":\"_recordId\"}",
    "RecipientLastName": "{\"ImportId\":\"recipientLastName\"}",
    "RecipientFirstName": "{\"ImportId\":\"recipientFirstName\"}",
    "RecipientEmail": "{\"ImportId\":\"recipientEmail\"}",
    "ExternalReference": "{\"ImportId\":\"externalDataReference\"}",
    "LocationLatitude": "{\"ImportId\":\"locationLatitude\"}",
    "LocationLongitude": "{\"ImportId\":\"locationLongitude\"}",
    "DistributionChannel": "{\"ImportId\":\"distributionChannel\"}",
    "UserLanguage": "{\"ImportId\":\"userLanguage\"}",
    "Q_RecaptchaScore": "{\"ImportId\":\"Q_RecaptchaScore\"}",
    "QID3": "{\"ImportId\":\"QID3_TEXT\"}",
    "QID16": "{\"ImportId\":\"QID16\"}",
    "QID20": "{\"ImportId\":\"QID20\"}",
    "QID19": "{\"ImportId\":\"QID19_TEXT\"}",
    "QID21": "{\"ImportId\":\"QID21_TEXT\"}",
    "QID24": "{\"ImportId\":\"QID24_TEXT\"}",
    "QID25": "{\"ImportId\":\"QID25\"}",
    "QID27": "{\"ImportId\":\"QID27\"}",
    "QID26": "{\"ImportId\":\"QID26\"}",
    "QID28": "{\"ImportId\":\"QID28_TEXT\"}"
}

# Flatten the JSON data for CSV
flattened_data = []
for event in json_data:
    flattened_event = {qualtrics_key: event.get(event_key, [""])[0] if isinstance(event.get(event_key), list) else event.get(event_key, "") for event_key, qualtrics_key in mapping.items()}
    flattened_event.update({key: "" for key in qualtrics_columns if key not in flattened_event})
    flattened_data.append(flattened_event)

# Convert to DataFrame
df = pd.DataFrame(flattened_data)

# Ensure columns are ordered correctly
df = df[qualtrics_columns]

# Create a new DataFrame for the header rows
header_rows = pd.DataFrame([qualtrics_columns, friendly_names, list(import_id_row.values())])

# Concatenate headers and data
final_df = pd.concat([header_rows, df], ignore_index=True)

# Ensure empty fields are just commas
final_df.fillna("", inplace=True)

# Remove special characters from text columns
final_df.replace(r'[^\x00-\x7F]+', '', regex=True, inplace=True)

# Save to CSV with UTF-8 encoding
output_file = "calendar_events.csv"
final_df.to_csv(output_file, index=False, encoding='utf-8', header=False)

print(f"CSV file created: {output_file}")
