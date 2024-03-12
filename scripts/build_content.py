import gspread
import csv
import os
import json

# Define column indexes
TITLE_INDEX = 2
DIFFICULTY_INDEX = 3
TIME_INDEX = 4
SERVINGS_INDEX = 5
INGREDIENTS_INDEX = 6
PREPARATION_INDEX = 7
NOTES_INDEX = 8


def open_sheet(sheet_id, service_account_data):
    credentials = json.loads(service_account_data)
    gc = gspread.service_account_from_dict(credentials)
    return gc.open_by_key(sheet_id)

def download_csv(sheet, destination_file="spreadsheet.csv"):
    # Get all values from the sheet and write to CSV file
    values = sheet.sheet1.get_all_values()
    with open(destination_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(values)

def create_markdown_files(csv_file):
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        # Skip header row
        next(csvreader)

        for row in csvreader:
            title = row[TITLE_INDEX]
            difficulty = row[DIFFICULTY_INDEX]
            time = row[TIME_INDEX]
            servings = row[SERVINGS_INDEX]
            ingredients = row[INGREDIENTS_INDEX]
            preparation = row[PREPARATION_INDEX]
            notes = row[NOTES_INDEX]

            # Create Markdown content
            markdown_content = f"""+++
title = '{title}'
date = 2024-03-12T15:46:56+01:00
draft = false
+++

## {title}

**Dificultad:** {difficulty}  
**Tiempo:** {time} minutos
**Raciones:** {servings}  

### Ingredientes:
{ingredients}

### Preparación:
{preparation}

#### Notas:
{notes}
"""

            # Replace spaces in title with underscores for filename
            filename = f"{title.replace(' ', '_')}.md"

            # Create a separate Markdown file for each row
            output_file = f"content/recetas/{filename}.md"
            with open(output_file, 'w') as md_file:
                md_file.write(markdown_content)

if __name__ == "__main__":
    sheet_id = os.getenv("SHEET_ID")
    service_account_data = os.getenv("GSPREAD_SERVICE_ACCOUNT")
    print("sheet_id: ", sheet_id)
    csv_file = "spreadsheet.csv"

    # Open the public spreadsheet
    sheet = open_sheet(sheet_id, service_account_data)

    # Download the spreadsheet as a CSV file
    download_csv(sheet, csv_file)

    # Create Markdown files for each row
    create_markdown_files(csv_file)

    # Optional: Remove the downloaded CSV file
    os.remove(csv_file)
