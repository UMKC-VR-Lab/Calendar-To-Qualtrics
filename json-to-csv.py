import json
import pandas as pd

# Load JSON data from a file
input_file = "Data/processed-calendar.json"
with open(input_file, "r") as file:
    json_data = json.load(file)

# Flatten the JSON data for CSV
flattened_data = []
for event in json_data:
    flattened_event = {key: value[0] if isinstance(value, list) and value else "" for key, value in event.items()}
    flattened_event["Name"] = f"{flattened_event.get('RecipientFirstName', '')} {flattened_event.get('RecipientLastName', '')}".strip()
    flattened_data.append(flattened_event)

# Convert to DataFrame
df = pd.DataFrame(flattened_data)

# Rearrange columns to match Qualtrics format
columns_order = [
    "Date", "Progress", "Name", "RecipientEmail", 
    "What is your primary purpose for visiting the Innovation Studio today?", "Name of Your Organization", 
    "Email", "Estimated Group Size", "Type of Visit", "Brief Description of the Project"
]

# Ensure Date exists and add default if missing
if "Date" not in df.columns:
    df["Date"] = ""

df = df[columns_order]

# Save to CSV
output_file = "calendar_events.csv"
df.to_csv(output_file, index=False)

print(f"CSV file created: {output_file}")