# LaTeX Templates for LetX

Production template library for [letx.app](https://letx.app). Each template becomes a one-click project on the platform.

## Repo Structure

```
Latex_Templates/
├── journal-articles/
│   ├── ieee-conference/
│   │   ├── main.tex
│   │   ├── *.cls / *.sty / *.bst (bundled if not in TexLive)
│   │   └── figures/
│   ├── acm-sigconf/
│   └── ...
├── cv-resume/
├── thesis-dissertation/
├── presentations/
├── letters-formal/
├── books/
├── posters/
├── assignments-homework/
└── README.md
```

Each template = a directory that zips into a working LaTeX project.

---

## Categories & Priority Templates

Priority is based on Google search volume and Overleaf gallery popularity. **Create high-search templates first.**

### 1. Journal Articles (Highest Search Volume)

Most searched academic templates globally. Publishers require exact formatting.

| Template | Search Signal | Compiler | Notes |
|----------|--------------|----------|-------|
| IEEE Conference (IEEEtran) | ~50K monthly | pdflatex | Most popular LaTeX template worldwide |
| IEEE Journal | ~20K | pdflatex | Two-column journal variant |
| ACM SIGCONF | ~15K | pdflatex | `acmart.cls` — conference proceedings |
| ACM Journal (acmsmall/acmlarge) | ~8K | pdflatex | Different from sigconf layout |
| Elsevier (elsarticle) | ~12K | pdflatex | Single/double column variants |
| Elsevier CAS (cas-dc, cas-sc) | ~5K | pdflatex | Newer Elsevier format |
| Springer LNCS | ~10K | pdflatex | `llncs.cls` — CS conferences |
| Springer Nature | ~8K | pdflatex | Nature-branded journals |
| APS Physical Review (REVTeX) | ~6K | pdflatex | Physics journals |
| MDPI (multidisciplinary) | ~4K | pdflatex | Open access journals |
| PLoS ONE | ~3K | pdflatex | Biology/medicine |
| arXiv Preprint (clean) | ~5K | pdflatex | Minimal, no publisher lock-in |
| SIAM Journal | ~2K | pdflatex | Applied math |
| AMS Journal (amsart) | ~3K | pdflatex | Pure math |
| Royal Society | ~1K | pdflatex | UK science journals |

### 2. CV & Resume (Second Highest)

People search "[template name] latex" constantly. CV templates drive signups.

| Template | Search Signal | Compiler | Notes |
|----------|--------------|----------|-------|
| Jake's Resume | ~15K | pdflatex | #1 CS resume on Reddit/GitHub |
| Awesome-CV Resume | ~10K | xelatex | Custom fonts, fontspec |
| Awesome-CV Cover Letter | ~5K | xelatex | Matching cover letter |
| Deedy Resume (OpenFonts) | ~8K | xelatex | .xtx file, bundled fonts |
| AltaCV (Infographic) | ~6K | xelatex/lualatex | Two-column infographic style |
| moderncv (all styles) | ~10K | pdflatex | banking/casual/classic/fancy/oldstyle |
| EuropassCV | ~4K | pdflatex | EU standard CV format |
| sb2nov Resume | ~3K | pdflatex | Clean single-page |
| HipsterCV | ~2K | pdflatex | Creative sidebar layout |
| Friggeri CV | ~3K | xelatex | Colorful sidebar, custom fonts |
| Academic CV (long-form) | ~5K | pdflatex | Multi-page for professors |
| Two-Column Resume (generic) | ~4K | pdflatex | Simple, no custom cls |

### 3. Thesis & Dissertation

Universities often mandate specific templates. High retention — users spend weeks on these.

| Template | Search Signal | Compiler | Notes |
|----------|--------------|----------|-------|
| MIT Thesis | ~5K | pdflatex | Classic US thesis |
| Stanford PhD Thesis | ~3K | pdflatex | |
| Oxford Thesis | ~3K | pdflatex | UK format |
| Cambridge Thesis | ~2K | pdflatex | |
| Clean Thesis (generic) | ~4K | pdflatex | No university branding |
| BUET UG Thesis | regional | pdflatex | Bangladesh — our user base |
| BUET PG Thesis | regional | pdflatex | |
| RUET Thesis | regional | pdflatex | |
| IIT Bombay Thesis | ~2K | pdflatex | India — large LaTeX user base |
| IIT Madras Thesis | ~1K | pdflatex | |
| NUS Thesis | ~1K | pdflatex | Singapore |
| TU Delft Thesis | ~1K | pdflatex | Netherlands |
| ETH Zurich Thesis | ~1K | pdflatex | Switzerland |
| Generic PhD Thesis | ~3K | pdflatex | Customizable, no branding |

### 4. Presentations (Beamer)

| Template | Search Signal | Compiler | Notes |
|----------|--------------|----------|-------|
| Metropolis | ~8K | pdflatex | Most popular modern Beamer theme |
| Madrid (default) | ~3K | pdflatex | Built-in Beamer theme |
| Focus | ~2K | pdflatex | Minimalist |
| Moloch | ~1K | pdflatex | Metropolis successor |
| Academic Presentation | ~3K | pdflatex | Generic with bibliography |
| PhD Defense | ~2K | pdflatex | Defense-specific structure |
| Conference Talk (15min) | ~1K | pdflatex | Pre-structured timing |

### 5. Letters & Formal Documents

| Template | Search Signal | Compiler | Notes |
|----------|--------------|----------|-------|
| KOMA-Script Letter (scrlttr2) | ~3K | pdflatex | German-style formal letter |
| Business Letter (generic) | ~2K | pdflatex | US format |
| Cover Letter (standalone) | ~4K | pdflatex | Job application |
| Recommendation Letter | ~1K | pdflatex | Academic reference |
| Resignation Letter | ~1K | pdflatex | Professional template |

### 6. Books

| Template | Search Signal | Compiler | Notes |
|----------|--------------|----------|-------|
| Tufte-Book | ~3K | pdflatex | Side-margin notes, elegant |
| Tufte-Handout | ~2K | pdflatex | Short-form Tufte |
| Memoir Class Book | ~2K | pdflatex | Flexible book class |
| Textbook (generic) | ~1K | pdflatex | With exercises, solutions |
| Novel / Fiction | ~500 | pdflatex | Simple prose layout |

### 7. Posters

| Template | Search Signal | Compiler | Notes |
|----------|--------------|----------|-------|
| tikzposter | ~3K | pdflatex | Most popular poster package |
| baposter | ~2K | pdflatex | Flexible column layout |
| Gemini (Beamerposter) | ~1K | pdflatex | Modern look |
| a0poster (simple) | ~1K | pdflatex | Minimal setup |

### 8. Assignments & Homework

| Template | Search Signal | Compiler | Notes |
|----------|--------------|----------|-------|
| jdavis Homework | ~3K | pdflatex | Most forked homework template |
| Problem Set (generic) | ~2K | pdflatex | Numbered problems with solutions |
| Lab Report | ~2K | pdflatex | Science lab format |
| Math Homework | ~2K | pdflatex | AMS math heavy |
| Exam Paper | ~1K | pdflatex | With answer key option |

### 9. Miscellaneous

| Template | Search Signal | Compiler | Notes |
|----------|--------------|----------|-------|
| Cheatsheet (multi-column) | ~3K | pdflatex | 2-4 column reference card |
| Meeting Minutes | ~500 | pdflatex | |
| Invoice | ~1K | pdflatex | Freelancer invoice |
| Recipe Book | ~500 | pdflatex | |
| Concert Program | ~200 | pdflatex | |

---

## How to Create a Template

### Requirements

Every template directory MUST contain:

1. **`main.tex`** (or clearly named driver file) — the file that gets compiled
2. **All required `.cls` and `.sty` files** — if not available in TexLive 2025
3. **Sample content** — not lorem ipsum, realistic placeholder text
4. **No pre-compiled PDFs** — we compile fresh
5. **No unnecessary files** — no `.aux`, `.log`, `.synctex.gz`, `.git/`

### Template Quality Checklist

- [ ] Compiles cleanly with no errors (warnings OK)
- [ ] Correct compiler specified (pdflatex/xelatex/lualatex)
- [ ] All custom fonts bundled in `fonts/` if using fontspec
- [ ] All images/figures included (use placeholder if needed)
- [ ] `.bib` file included if template uses bibliography
- [ ] No absolute paths — all paths relative
- [ ] No `\usepackage{fontspec}` in pdflatex templates
- [ ] Total zip size < 2MB (ideally < 500KB)
- [ ] `\documentclass` and `\begin{document}` in main file

### Compiler Rules

| Compiler | When to Use |
|----------|------------|
| `pdflatex` | Default. Use unless template needs custom fonts or Unicode |
| `xelatex` | Templates with `\usepackage{fontspec}`, custom `.ttf/.otf` fonts, `.xtx` files |
| `lualatex` | Templates explicitly requiring LuaLaTeX features (rare) |

**Auto-detection**: LetX auto-detects xelatex when it finds `.xtx` files or `\usepackage{fontspec}` in any `.tex/.cls/.sty` file.

### Naming Convention

```
category-name/
  template-slug/          # lowercase, hyphens, matches URL slug
    main.tex              # or descriptive name like resume.tex
    custom-class.cls      # only if not in TexLive
    references.bib        # if needed
    figures/              # images dir
    fonts/                # only for fontspec templates
```

### Using the LaTeX Engineer Skill

Use `/latex-engineer` to generate templates. Example prompts:

```
/latex-engineer Create a complete IEEE conference paper template using IEEEtran class 
with realistic CS paper content about machine learning. Include abstract, 
introduction, related work, methodology, results, conclusion sections. 
Add a references.bib with 5 sample entries.
```

```
/latex-engineer Create a Beamer presentation using the Metropolis theme with 
15 slides covering a CS research talk. Include title slide, outline, 
methodology, results with TikZ figures, and conclusion.
```

```
/latex-engineer Create a professional CV using moderncv with banking style. 
Include education, work experience, publications, skills, and languages sections. 
Use realistic placeholder content for a software engineer.
```

### Inspiration Sources

1. **Overleaf Gallery** — browse by category, note which have most views
2. **LaTeX Templates (.com)** — curated collection with previews
3. **GitHub search** — `latex template` sorted by stars
4. **CTAN** — official package docs often include example documents
5. **University websites** — thesis/dissertation template pages
6. **Publisher author guidelines** — IEEE, ACM, Springer, Elsevier all provide official templates

### Search-Driven Priority

Create templates that people actually search for. Check:

1. Google Trends: compare "ieee latex template" vs "springer latex template"
2. Overleaf gallery: sort by "Most Popular"
3. GitHub: sort template repos by stars
4. Reddit r/LaTeX: frequently requested templates

**Rule: If a template has >5K monthly searches, it's a must-have.**

---

## Upload to LetX

After creating templates, upload to letx.app via admin API:

1. Zip the template directory
2. Generate a thumbnail (compile → screenshot first page → crop to 3:4)
3. Generate a preview PDF (compile the template)
4. Upload assets via `/api/v1/admin/upload`
5. Create template entry via `/api/v1/admin/templates`

Detailed upload script will be added later.

---

## Phase Plan

### Phase 1: Core Templates (Week 1)
- All journal article templates (IEEE, ACM, Elsevier, Springer)
- Top 5 CV/Resume templates
- 3 thesis templates (MIT, Clean, BUET)

### Phase 2: Extended Library (Week 2)
- Remaining CVs and resumes
- All presentation/Beamer templates
- Assignment and homework templates
- Poster templates

### Phase 3: Regional & Niche (Week 3)
- Indian university templates (IIT Bombay, IIT Madras, IISc)
- Pakistani university templates (LUMS, NUST, FAST)
- Other Asian universities (NUS, NTU, KAIST)
- Niche templates (cheatsheets, invoices, lab reports)

### Phase 4: SEO & Optimization
- SEO metadata for every template
- Category landing pages
- Template comparison guides
- "How to use [template]" content
