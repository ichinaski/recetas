import gspread
import csv
import os
import json
from datetime import datetime

# Define column indexes
DATE_INDEX = 0
#EMAIL_INDEX = 1
AUTHOR_INDEX = 2
TITLE_INDEX = 3
CATEGORY_INDEX = 4
DIFFICULTY_INDEX = 5
TIME_INDEX = 6
SERVINGS_INDEX = 7
INGREDIENTS_INDEX = 8
PREPARATION_INDEX = 9
NOTES_INDEX = 10


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
            date_str = row[DATE_INDEX].strip()
            author = row[AUTHOR_INDEX].strip()
            title = row[TITLE_INDEX].strip()
            difficulty = row[DIFFICULTY_INDEX].strip()
            time = row[TIME_INDEX].strip()
            servings = row[SERVINGS_INDEX].strip()
            ingredients = row[INGREDIENTS_INDEX].strip()
            preparation = row[PREPARATION_INDEX].strip()
            category = row[CATEGORY_INDEX].strip() or 'Otros'  # TODO: delete me
            notes = row[NOTES_INDEX].strip()

            date = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S').isoformat()
            formatted_ingredients = format_ingredients(ingredients)
            formatted_preparation = format_preparation(preparation)

            meta_parts = [f'**Dificultad:** {difficulty}' if difficulty else None,
                          f'**Tiempo:** {time}' if time else None,
                          f'**Raciones:** {servings}' if servings else None]
            meta_line = '  |  '.join(p for p in meta_parts if p)
            section_ingredients = '### Ingredientes\n' + formatted_ingredients if formatted_ingredients else ''
            section_preparation = '### Preparación\n' + formatted_preparation if formatted_preparation else ''
            section_notes = '### Notas\n' + notes if notes else ''

            # Create Markdown content
            markdown_content = f"""+++
title = '{title}'
date = '{date}'
draft = false
categories = ['{category}']
[params]
  author = '{author}'
+++

{meta_line}

<!--more-->

{section_ingredients}

{section_preparation}

{section_notes}
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

def format_ingredients(ingredients):
    lines = [line.strip() for line in ingredients.split('\n') if line.strip()]
    return '\n'.join([f'- {line}' for line in lines])


def format_preparation(preparation):
    steps = [step.strip() for step in preparation.split('\n') if step.strip()]
    return '\n'.join([f'{i+1}. {v}' for i, v in enumerate(steps)])

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
