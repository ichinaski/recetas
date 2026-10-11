# Recetas de Amama

"Amama" means grandma in Basque. This is a recipe book I made for my mom, who has spent decades filling notebooks with handwritten recipes: family dishes, seasonal cooking, things passed down without ever being written down properly. The site gives her a simple way to digitalize that collection, and gives our family a place to preserve and rediscover those recipes.

She adds, edits and deletes recipes in [Pages CMS](https://pagescms.org), a simple web editor. Everything else is automatic, with no technical knowledge required on her end.

Technically it is a static website built with Hugo and deployed to GitHub Pages at [recetasdeamama.es](https://recetasdeamama.es).

## Architecture

```
Pages CMS → commit to main → GitHub Actions → Hugo → GitHub Pages
```

Each recipe is a Markdown file in `content/recetas/`. Saving a recipe in Pages CMS commits that file to `main`, and every push to `main` rebuilds the site, indexes it for search with Pagefind, and deploys it to GitHub Pages.

### Key components

**`content/recetas/`** holds one file per recipe. Fields like category, difficulty, ingredients and preparation live in TOML front matter, and free-form notes go in the body.

**`.pages.yml`** configures the Pages CMS editor: which fields exist, their Spanish labels, dropdown options, and where uploaded photos go (`static/images/`).

**`layouts/`** has custom Hugo templates overriding the ananke theme. `layouts/recetas/single.html` and `layouts/partials/recipe/` render a recipe from its front matter. The rest are recipe cards, category listing, and the search page.

**`hugo.toml`** is the site configuration: Spanish locale, ananke theme, category taxonomy, main menu. Dates are read as Madrid time, matching what Pages CMS writes.

**`.github/workflows/hugo.yaml`** is the CI/CD pipeline: installs Hugo and Dart Sass, builds the site, indexes it with Pagefind, and deploys to GitHub Pages.

**`scripts/migrate_from_sheet.py`** is the one-off script that moved the recipes from the old Google Form and Sheet setup into `content/recetas/`. It's kept for reference and isn't part of the build.

## Editing recipes

Open [app.pagescms.org](https://app.pagescms.org), pick the repo and edit on `main`. Collaborators can be invited by email from Pages CMS and don't need a GitHub account. Changes are live a minute or two after saving.

## Local development

### Prerequisites

- [Hugo](https://gohugo.io/installation/) extended v0.156.0
- Node.js (for `npx pagefind`)

### Clone

```bash
git clone --recurse-submodules https://github.com/ichinaski/recetas.git
```

The `--recurse-submodules` flag is required to pull the ananke theme.

### Build and run

```bash
./scripts/build.sh   # build site and index search
./scripts/run.sh     # serve at http://localhost:1313
```

For quick previews while editing templates, `hugo server` works too (without search).
