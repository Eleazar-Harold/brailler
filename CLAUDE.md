# CLAUDE.md — AI Assistant Guide for Brailler

## Project Overview

**Brailler** is a Django web application that converts between English text and Grade 1 Braille (and back). It supports Braille Unicode rendering, PDF export, and handles contractions, capital indicators, and number indicators per Braille conventions.

Live deployment: https://brailler.herokuapp.com/

---

## Repository Structure

```
brailler/
├── brl/                          # Single Django application (all logic lives here)
│   ├── settings/
│   │   ├── __init__.py           # Loads base, overrides with production if available
│   │   ├── base.py               # Development settings (DEBUG=True, SQLite)
│   │   └── production.py         # Production settings (PostgreSQL, WhiteNoise, HTTPS)
│   ├── AlphaBrailleMapper.py     # English → Braille Unicode character maps
│   ├── BrailleAlphaMapper.py     # Braille Unicode → English character maps (inverse)
│   ├── textTobraille.py          # Core text-to-Braille conversion engine
│   ├── brailleTotext.py          # Core Braille-to-text conversion engine
│   ├── app_conv.py               # BrCnvx wrapper class around conversion functions
│   ├── Printer.py                # Debug utility to print mapping tables
│   ├── forms.py                  # Django forms (T2BForm, B2TForm)
│   ├── views.py                  # Function-based views and PDF generation
│   ├── urls.py                   # URL routing
│   └── wsgi.py                   # WSGI entry point
├── templates/
│   ├── base.html                 # Base layout with Bootstrap navbar
│   └── pages/
│       ├── ttob.html             # Text-to-Braille page
│       └── btot.html             # Braille-to-Text page
├── staticfiles/                  # Collected static assets (do not edit directly)
├── scripts/
│   ├── format.sh                 # Auto-format code (black, isort, autoflake)
│   └── linter.sh                 # Lint/type-check without modifying files
├── manage.py
├── requirements.txt
├── Procfile                      # Heroku: runs gunicorn brl.wsgi
└── README.md
```

---

## URL Routes

| URL | View | Purpose |
|-----|------|---------|
| `/` | `ttob_page` | Text → Braille (main page) |
| `/btt/` | `btot_page` | Braille → Text |
| `/pdf_brl/` | `t2b_print` | Download Text→Braille result as PDF |
| `/pdf_txt/` | `b2t_print` | Download Braille→Text result as PDF |

---

## Key Components and How They Work

### Braille Conversion Pipeline

**Text → Braille** (`textTobraille.py`):
1. Split input into words
2. For each word: strip punctuation, check contractions, convert char-by-char
3. Handle special cases:
   - Numbers: prefix sequence with `⠼` (chr(10300), number indicator)
   - Capitals: prefix letter with `⠠` (chr(10272), capital indicator)
   - Smart quotes: tracked via `open_quotes` global to distinguish open/close
4. Reassemble punctuation around converted word

**Braille → Text** (`brailleTotext.py`):
1. Split Braille input into words
2. Decode each word character by character via `BrailleAlphaMapper`
3. Handle indicator prefixes (number indicator, capital indicator)
4. Run `fix_exceptions()` to disambiguate symbols that map to multiple characters (e.g., brackets, quotes)

### Character Maps (`AlphaBrailleMapper.py` / `BrailleAlphaMapper.py`)

Four mapping dictionaries in each direction:
- **letters**: a–z → Braille Unicode
- **contractions**: Common English words/abbreviations → single Braille symbol
- **punctuation**: `.`, `,`, `?`, `!`, etc. → Braille Unicode
- **numbers**: 0–9 → Braille Unicode (same cells as a–j, distinguished by number indicator)

### BrCnvx Wrapper (`app_conv.py`)

```python
cnv = BrCnvx()
cnv.user_braille()  # Returns session braille string
cnv.user_text()     # Returns session text string
cnv.open_braille()  # Opens braille output (PDF context)
cnv.open_text()     # Opens text output (PDF context)
```

Note: The methods are defined as `@classmethod` but are called on instances — this is a known inconsistency.

### Views and Session Flow

Views use Django sessions to pass conversion results between the form POST and the PDF download GET:
```python
# POST: store result
request.session['braille'] = BrCnvx.user_braille(string)

# Later GET (PDF download): retrieve result
string = request.session.get('braille', '')
```

PDF files are generated into `/tmp/` via ReportLab and served as `FileResponse`.

---

## Development Setup

### Prerequisites
- Python 3.x
- pip

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run locally
```bash
python manage.py runserver
```

The app uses SQLite in development (no database setup required — the app has no models, so no migrations are needed).

### Format code
```bash
bash scripts/format.sh
```
Runs: `isort` → `autoflake` → `black` → `isort` (double-pass for consistency)

### Lint/type-check (read-only)
```bash
bash scripts/linter.sh
```
Runs: `mypy`, `black --check`, `isort --check-only`, `flake8`

Line length limit: **88 characters** (black/flake8 configured)

---

## Key Conventions

### Code Style
- **Formatter**: `black` (line length 88)
- **Import sorter**: `isort` (force single-line, alphabetical within sections)
- **Linter**: `flake8` (max-line-length 88)
- **Type checker**: `mypy` (configured but type hints are sparse in current code)
- Run `scripts/format.sh` before committing

### Django Patterns
- **Function-based views** only (no class-based views)
- **No models** — this is a stateless application; sessions hold transient data
- **Template inheritance**: all pages extend `templates/base.html`
- URL patterns use deprecated `url()` (Django 1.x style) — prefer `path()` for any new routes

### Braille Special Characters (Unicode)
| Symbol | chr() | Meaning |
|--------|-------|---------|
| `⠠` | chr(10272) | Capital indicator (prefix) |
| `⠼` | chr(10300) | Number indicator (prefix) |
| Braille cells | chr(10241)–chr(10303) | Standard Braille Unicode block |

### Known Issues to Be Aware Of
1. **Global mutable state**: `open_quotes` in `textTobraille.py` is not thread-safe — concurrent requests could interfere with each other
2. **classmethod inconsistency**: `BrCnvx` methods are `@classmethod` but called on instances
3. **Deprecated syntax**: `len(x) is not 0` should be `len(x) != 0`
4. **Bare except**: `brl/settings/__init__.py` uses `except:` without specifying exception type
5. **No tests**: The repository has no test suite

### What NOT to Do
- Do not add models — the application is intentionally stateless
- Do not edit files under `staticfiles/` directly; these are auto-generated by `collectstatic`
- Do not push secrets or environment variables; `SECRET_KEY` and `DATABASE_URL` are environment variables in production

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.28 | Web framework |
| gunicorn | 19.7.1 | WSGI server (production) |
| whitenoise | 3.3.1 | Static file serving (production) |
| psycopg2 | 2.7.3.2 | PostgreSQL adapter (production) |
| dj-database-url | 0.4.2 | Parse DATABASE_URL env var |
| reportlab | 3.6.13 | PDF generation |
| Pillow | 10.2.0 | Image processing (reportlab dep) |
| django-crispy-forms | 1.7.0 | Installed but currently unused |

Frontend (CDN, not in requirements.txt):
- Bootstrap 4.0.0-beta.2
- jQuery 3.2.1
- Font Awesome 4.7.0

---

## Deployment (Heroku)

The `Procfile` defines the web process:
```
web: gunicorn brl.wsgi
```

Production settings are loaded automatically when `brl.settings.production` is importable. Required environment variables:
- `SECRET_KEY` — Django secret key
- `DATABASE_URL` — PostgreSQL connection string

Production features enabled:
- `DEBUG = False`
- WhiteNoise middleware for compressed static files
- HTTPS redirect (`SECURE_SSL_REDIRECT = True`)
- HSTS headers
- Secure session and CSRF cookies

---

## Adding Features — Guidance for AI Assistants

- **New conversion rules**: Add entries to `AlphaBrailleMapper.py` and the corresponding inverse in `BrailleAlphaMapper.py`
- **New URL**: Add to `brl/urls.py` using `path()` (not the legacy `url()`)
- **New view**: Add as a function-based view in `brl/views.py`; follow the existing POST→session→GET pattern for multi-step flows
- **Tests**: There are none — adding a `tests.py` or `tests/` directory with Django `TestCase` classes is strongly encouraged before making logic changes
- **Thread safety**: If touching `open_quotes` global in `textTobraille.py`, consider refactoring to pass state as a parameter instead
