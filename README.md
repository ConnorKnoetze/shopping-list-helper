# Shopping List Helper

A web app that streamlines shopping list creation and weekly menu item selection. (Under Development)

This repository contains a Flask-based single-application web project that provides user authentication, inventory management, recipe browsing, and shopping list generation/export functionality.

Currently deployed with Railway as a subdomain of my domain "connorknoetze.com". For the best free tier performance I have chosen to integrate a PostgreSQL database with Railway. Sadly moving away from Supabase but the lack of deployment region overlap forced the decision due to high transfer latency.

Repository: https://github.com/ConnorKnoetze/shopping-list-helper

## Table of contents
- Features
- Tech stack
- Quick start
- Configuration (.env)
- Running the app
- Repository modes & data population
- Project structure (high level)
- Contributing
- Troubleshooting
- Contact

## Features
- User registration and login (authentication blueprint)
- Inventory management (add/update ingredients)
- Recipe browsing and carousel UI
- Shopping list generation and download (TXT export)
- Client-side utilities: search, navigation, carousel
- Two repository modes: in-memory (fast dev) and configurable repository (via environment)

## Tech stack
- Python (Flask)
- HTML, CSS, JavaScript for the front end
- Flask-WTF / WTForms for forms and validation
- python-dotenv for environment configuration
- Simple in-memory repository for development (MemoryRepository)
- Requirements listed in `requirements.txt`

## Quick start (local development)
Prerequisites:
- Python 3.10+ (or compatible)
- pip

1. Clone the repository
   ```
   git clone https://github.com/ConnorKnoetze/shopping-list-helper.git
   cd shopping-list-helper
   ```

2. Create and activate a virtual environment
   - macOS / Linux
     ```
     python -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell)
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Add an environment file `.env` (example shown below) or set environment variables in your shell.

## Configuration (.env)
Create a `.env` file in the repository root. Example:
```env
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
TESTING=false
REPOSITORY=memory
SQLALCHEMY_DATABASE_URI=sqlite:///shopping.db
SQLALCHEMY_ECHO=false
```

Important variables:
- `SECRET_KEY` — required for session security and CSRF protection.
- `REPOSITORY` — set to `memory` to use the in-memory repository (default for quick development). If set to something else, the app expects a production repository configuration (see `config.py` for DB settings).
- `SQLALCHEMY_DATABASE_URI` — used if you configure a database-backed repository.

## Running the app
The app entry point is `wsgi.py`. To run locally:
```
python wsgi.py
```
This script loads `.env` and starts the Flask development server on `0.0.0.0:5000` by default. For production deployment, use a WSGI server (Gunicorn, uWSGI, etc.) pointing at the `app` callable.

Alternatively, you can run with the `flask` CLI after exporting `FLASK_APP=wsgi.py`:
```
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

## Repository modes & data population
- Memory mode
  - Set `REPOSITORY=memory`. The application will instantiate `MemoryRepository` at startup and populate it with sample categories and ingredients from `pantry/adapters/data/ingredients.csv` via `pantry.adapters.populate_repository.populate`.
  - Memory mode is ideal for development and testing without a database.

- Database / other mode
  - Set `REPOSITORY` to something other than `memory` and configure `SQLALCHEMY_DATABASE_URI` to use a persistent database.
  - The code reads database configuration in `config.py`. If you choose a DB-backed repository you may need to implement and wire an adapter that uses SQLAlchemy (the project provides an abstract repository interface in `pantry/adapters/repository.py`).

Data reader:
- The sample data used to populate MemoryRepository is defined in `pantry/adapters/data/ingredients.csv` and is read by `pantry/adapters/datareader/reader.py`.

## Project structure (high level)
- wsgi.py — app entry point
- config.py — configuration using environment variables
- requirements.txt — Python dependencies
- pantry/ — main application package
  - __init__.py — app factory `create_app()`, blueprint registration, and DI for repository
  - blueprints/ — blueprints (home, authentication, inventory, recipes, shopping)
  - adapters/
    - repository.py — abstract repository interface
    - memory_repository.py — in-memory repository implementation
    - populate_repository.py — helper to populate repositories with sample data
    - datareader/reader.py — reads CSV data for categories & ingredients
  - domainmodel/ — domain objects (Ingredient, Category, User, etc.)
  - templates/ — Jinja2 templates (pages, components)
  - static/
    - css/
    - js/ (nav, shopping, carousel, search)
    - downloads/ (downloaded shopping lists)
  - utilities/ — helpers such as auth utilities

## Troubleshooting
- "SECRET_KEY not set" — set `SECRET_KEY` in `.env` to avoid session/CSRF errors.
- Port conflicts — the app uses port 5000 by default.
- JS static features (download/shopping) rely on endpoints such as `/shopping/api/download` — ensure you are logged in to access protected routes.

---
