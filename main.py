import pandas as pd
import json
import os

# Function to process the text file into a DataFrame
def parse_text_to_dataframe(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

    records = []
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()

    record = {}
    for line in lines:
        if line.strip() == "":
            if record:
                records.append(record)
                record = {}
        else:
            key, value = map(str.strip, line.split(':', 1))
            record[key] = value.strip(' []"')
    if record:
        records.append(record)  # Append the last record if not empty

    df = pd.DataFrame(records)
    return df

# Function to export DataFrame to JSON
def export_to_json(df, file_name="output.json"):
    df.to_json(file_name, orient='records', indent=4)
    print(f"Data successfully saved to {file_name}")

text_file_path = "data.txt"
try:
    df = parse_text_to_dataframe(text_file_path)
    export_to_json(df, "output.json")
except FileNotFoundError as e:
    print(e)
