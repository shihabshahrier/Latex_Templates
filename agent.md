# LaTeX Templates Agent Guide

Central registry for the 66 LaTeX templates powering [letx.app](https://letx.app).

## Repository Structure

```
Latex_Templates/
  assignments/       (6 templates)
  books/             (4 templates)
  cv-resume/         (7 templates)
  journal-articles/  (5 templates)
  letters/           (5 templates)
  miscellaneous/     (6 templates)
  posters/           (4 templates)
  presentations/     (6 templates)
  theses/            (23 templates)
```

Each template has `main.tex`, `metadata.json`, and optional `.cls`/`.sty`/`.bib` files.

## Compiler Requirements

| Compiler | Count | Templates |
|----------|-------|-----------|
| pdfLaTeX | 59 | Most templates |
| XeLaTeX | 5 | altacv, awesome-cv, banking-cv, classic-cv, deedy-resume |
| LuaLaTeX | 2 | moderncv, hipstercv (workspace only) |

### Known Issues (Fixed 2026-05-28)

- **madrid-beamer**: Unescaped `&` in `\subtitle` — fixed
- **syllabus-template**: Unescaped `&` in `\title` — fixed
- **ruet-thesis**: Missing `imgs/ruetlogo.pdf` — placeholder added
- **oxford-thesis**: Missing `figures/beltcrest.pdf` and `figures/newlogo.pdf` — placeholders added
- **acmart**: Missing `sampleteaser.pdf` and `sample-franklin.pdf` — placeholders added
- **mit-thesis**: fontspec references in comments trigger false xelatex detection — fixed in letx.app backend
- **math-homework**: Minor undefined control sequences — compiles with `-f` flag

### XeLaTeX Font Issues

Templates using `\usepackage{fontspec}` need system fonts visible to fontconfig. On macOS with TeX Live:

```bash
export FONTCONFIG_PATH=/usr/local/texlive/2025/texmf-dist/fonts
```

Without this, XeLaTeX will fail with "Latin Modern Roman cannot be found".

## Creating New Templates

1. Pick the right category directory
2. Create `template-name/main.tex` with `\documentclass` at top
3. Add `metadata.json`:
   ```json
   {
     "name": "Display Name",
     "compiler": "pdflatex",
     "description": "One-line description.",
     "author": "Author Name",
     "license": "Open Source",
     "category": "category-slug"
   }
   ```
4. Test: `latexmk -pdf main.tex` (or appropriate engine)
5. Clean: `latexmk -C` — no build artifacts in repo

## Integration with letx.app

Templates are zipped per-directory and uploaded to prod via:
- `POST /api/v1/admin/upload` (multipart file + type=zip/thumbnail/preview)
- `POST /api/v1/admin/templates` (JSON metadata)

Auto-detection in letx.app scans for `.xtx` files or `\usepackage{fontspec}` (uncommented) to set the project compiler. The `metadata.json` compiler field should match what letx.app auto-detects.

## Categories in letx.app

| Category Slug | Category Name |
|--------------|---------------|
| universities | Universities |
| cvs-resumes | CVs and Resumes |
| journal-articles | Journal Articles |
| presentations | Presentations |
| assignments | Assignments |
| formal-letters | Formal Letters |
| books | Books |
| posters | Posters |
| miscellaneous | Miscellaneous |
| conferences | Conferences |
