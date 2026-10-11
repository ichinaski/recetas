"""One-off migration: export recipes from the Google Sheet into content/recetas/*.md.

Usage:
    SHEET_ID=... GSPREAD_SERVICE_ACCOUNT='{...}' python3 scripts/migrate_from_sheet.py
"""
import json
import os
import re
import unicodedata
from datetime import datetime

import gspread

DATE, EMAIL, AUTHOR, TITLE, CATEGORY, DIFFICULTY, TIME, SERVINGS, INGREDIENTS, PREPARATION, NOTES = range(11)
OUT_DIR = "content/recetas"


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def lines(text):
    return [l.strip() for l in text.split("\n") if l.strip()]


def toml_value(value):
    # JSON strings/arrays of strings are valid TOML basic strings/arrays.
    if isinstance(value, list):
        if not value:
            return "[]"
        return "[\n" + "".join(f"  {json.dumps(v, ensure_ascii=False)},\n" for v in value) + "]"
    return json.dumps(value, ensure_ascii=False)


def render(row):
    fields = {
        "title": row[TITLE].strip(),
        "date": datetime.strptime(row[DATE].strip(), "%m/%d/%Y %H:%M:%S").isoformat(),
        "categories": [row[CATEGORY].strip() or "Otros"],
        "author": row[AUTHOR].strip(),
        "difficulty": row[DIFFICULTY].strip(),
        "time": row[TIME].strip(),
        "servings": row[SERVINGS].strip(),
        "ingredients": lines(row[INGREDIENTS]),
        "steps": lines(row[PREPARATION]),
    }
    front = "".join(f"{k} = {toml_value(v)}\n" for k, v in fields.items() if v)
    notes = row[NOTES].strip()
    return f"+++\n{front}+++\n" + (f"\n{notes}\n" if notes else "")


def main():
    credentials = json.loads(os.environ["GSPREAD_SERVICE_ACCOUNT"])
    sheet = gspread.service_account_from_dict(credentials).open_by_key(os.environ["SHEET_ID"])
    rows = sheet.sheet1.get_all_values()[1:]

    os.makedirs(OUT_DIR, exist_ok=True)
    used = set()
    for row in rows:
        base = slugify(row[TITLE].strip())
        slug, n = base, 2
        while slug in used:
            slug, n = f"{base}-{n}", n + 1
        used.add(slug)
        with open(f"{OUT_DIR}/{slug}.md", "w") as f:
            f.write(render(row))

    print(f"Wrote {len(used)} recipes to {OUT_DIR}/")


if __name__ == "__main__":
    main()
