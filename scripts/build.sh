#!/bin/bash
set -e

if [ -z "$SHEET_ID" ]; then
  echo "Error: SHEET_ID is not set"
  exit 1
fi

if [ -z "$GSPREAD_SERVICE_ACCOUNT" ]; then
  echo "Error: GSPREAD_SERVICE_ACCOUNT is not set"
  exit 1
fi

python3 scripts/build_content.py
hugo
npx pagefind --site public --glob "recetas/*/index.html" --exclude-selectors "nav,header,footer"

echo "Done. Serve with: ./scripts/run.sh"
