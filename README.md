# Recetas de Amama

"Amama" means grandma in Basque. This is a recipe book I made for my mom, who has spent decades filling notebooks with handwritten recipes — family dishes, seasonal cooking, things passed down without ever being written down properly. The site gives her a simple way to digitalize that collection, and gives our family a place to preserve and rediscover those recipes.

She submits recipes through a Google Form. Everything else is automatic — no accounts, no dashboards, no technical knowledge required on her end.

Technically it is a static website built with Hugo and deployed to GitHub Pages. Recipes are submitted via Google Forms, stored in a Google Sheet, and automatically published on every form submission — no manual intervention needed.

## Architecture

```
Google Form → Google Sheet → GitHub Actions → Hugo → GitHub Pages
```

Recipes live entirely in a Google Sheet. When someone submits a form, a Google Apps Script fires a webhook to GitHub, which triggers a build. The build fetches all rows from the sheet, converts each one to a Hugo Markdown file, builds the static site, indexes it for search with Pagefind, and deploys to GitHub Pages.

Nothing is committed to the repository — recipe content and the built site are both generated fresh on every build.

### Key components

**`scripts/build_content.py`** — downloads the Google Sheet as CSV and generates one Markdown file per recipe under `content/recetas/`. Handles author extraction, date formatting, and ingredient/preparation formatting.

**`hugo.toml`** — site configuration: Spanish locale, ananke theme, category taxonomy, main menu.

**`layouts/`** — custom Hugo templates overriding the theme: recipe cards, category listing, and the search page.

**`.github/workflows/hugo.yaml`** — the full CI/CD pipeline: installs Hugo and Dart Sass, fetches content from Google Sheets, builds the site, indexes with Pagefind, and deploys to GitHub Pages.

**`scripts/trigger_workflow.js`** — Google Apps Script installed on the spreadsheet. Fires a `repository_dispatch` event to GitHub on every form submission to trigger a rebuild.

## Local development

### Prerequisites

- [Hugo](https://gohugo.io/installation/) extended v0.156.0
- Python 3 with `pip install -r scripts/requirements.txt`
- Node.js (for `npx pagefind`)

### Credentials

You need the two secrets from the GitHub repo (Settings → Secrets and variables → Actions):

```bash
export SHEET_ID="your-sheet-id"
export GSPREAD_SERVICE_ACCOUNT='{ ...service account json... }'
```

### Clone

```bash
git clone --recurse-submodules https://github.com/ichinaski/recetas-revamp.git
```

The `--recurse-submodules` flag is required to pull the ananke theme.

### Build and run

```bash
./scripts/build.sh   # fetch recipes, build site, index search
./scripts/run.sh     # serve at http://localhost:1313
```
