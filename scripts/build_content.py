import gspread
import csv
import os
import json
from datetime import datetime

# Define column indexes
DATE_INDEX = 0
AUTHOR_INDEX = 1
TITLE_INDEX = 2
DIFFICULTY_INDEX = 3
TIME_INDEX = 4
SERVINGS_INDEX = 5
INGREDIENTS_INDEX = 6
PREPARATION_INDEX = 7
NOTES_INDEX = 8
CATEGORY_INDEX = 9


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

        n = 0
        for row in csvreader:
            date_str = row[DATE_INDEX]
            author = row[AUTHOR_INDEX]
            title = row[TITLE_INDEX]
            difficulty = row[DIFFICULTY_INDEX]
            time = row[TIME_INDEX]
            servings = row[SERVINGS_INDEX]
            ingredients = row[INGREDIENTS_INDEX]
            preparation = row[PREPARATION_INDEX]
            notes = row[NOTES_INDEX]
            category = row[CATEGORY_INDEX] or 'Otros'  # TODO: delete me

            date = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S').isoformat()

            # Create an itemized list for ingredients
            ingredients_lines = ingredients.split('\n') if ingredients else []
            formatted_ingredients = '\n'.join([f'- {ingredient}' for ingredient in ingredients_lines])

            author = author.split('@')[0] if author and '@' in author else ''

            # Create Markdown content
            markdown_content = f"""+++
title = '{title}'
date = '{date}'
draft = false
categories = ['{category}']
[params]
  author = '{author}'
+++

**Dificultad:** {difficulty}  |  **Tiempo:** {time}  |  **Raciones:** {servings}

<!--more-->

### Ingredientes
{formatted_ingredients}

### Preparación
{preparation}

#### Notas
{notes}
"""

            # Replace spaces in title with underscores for filename
            filename = f"content/recetas/{title.replace(' ', '_')}_{n}.md"
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Create a separate Markdown file for each row
            with open(filename, 'w') as md_file:
                md_file.write(markdown_content)

            n = n+1

if __name__ == "__main__":
    sheet_id = os.getenv("SHEET_ID")
    service_account_data = os.getenv("GSPREAD_SERVICE_ACCOUNT", "")
    csv_file = "spreadsheet.csv"

    # Open the public spreadsheet
    sheet = open_sheet(sheet_id, service_account_data)

    # Download the spreadsheet as a CSV file
    download_csv(sheet, csv_file)

    # Create Markdown files for each row
    create_markdown_files(csv_file)

    # Optional: Remove the downloaded CSV file
    os.remove(csv_file)
