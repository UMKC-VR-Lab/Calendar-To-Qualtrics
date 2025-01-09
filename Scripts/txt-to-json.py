import json

# Define input and output file paths
input_file = "Data/processed-calendar-data-filled-in.txt"
output_file = "Data/processed-calendar.json"

# Initialize a list to store structured events
events = []

# Read file content
with open(input_file, "r", encoding="utf-8") as file:
    content = file.read()

# Split events by "StartDate": and clean up
raw_events = content.split('"StartDate":')
raw_events = [f'"StartDate":{event.strip()}' for event in raw_events[1:] if event.strip()]

# Parse each event
for raw_event in raw_events:
    event = {}
    lines = raw_event.strip().split("\n")
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            # Clean up keys and values
            key = key.strip().strip('"')
            value = value.strip().strip(',')  # Remove trailing commas
            
            # Parse list-like values
            if value.startswith("[") and value.endswith("]"):
                try:
                    value = json.loads(value)  # Parse it as a list
                except json.JSONDecodeError:
                    value = value.strip('"')  # Keep as string if parsing fails
            else:
                value = value.strip('"')  # Remove extra quotes from strings
            
            event[key] = value  # Assign cleaned key-value pair
    if event:  # Only append if the event dictionary is not empty
        events.append(event)

# Write the cleaned events to a JSON file
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(events, json_file, indent=4)

print(f"Events successfully converted to {output_file}")
