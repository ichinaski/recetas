#!/bin/bash
set -e

cd "$(dirname "$0")/.."

hugo
npx pagefind --site public --glob "recetas/*/index.html" --root-selector "article"

echo "Done. Serve with: ./scripts/run.sh"
