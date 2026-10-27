# Spendly

Spendly is a personal expense tracker built with Flask and SQLite. It helps you log expenses, see where your money goes, and stay on top of your spending — one transaction at a time.

## Features

- **Log expenses** — record the amount, category, date and description in one simple form
- **Understand your patterns** — category breakdowns and monthly summaries
- **Filter by time period** — view spending for last week, last month or a custom date range
- **User accounts** — register, log in and manage your profile

> Spendly is being built step by step. The landing, register and login pages are in place; database setup, authentication, profiles and expense add/edit/delete are still to come.

## Tech stack

- Python 3.12, Flask 3.1
- SQLite
- Jinja2 templates, plain HTML/CSS/JavaScript
- pytest + pytest-flask for tests

## Getting started

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
# source venv/Scripts/activate   # Git Bash on Windows
# source venv/bin/activate       # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open http://127.0.0.1:5001 in your browser.

## Running tests

```bash
pytest
```

## Project structure

```
expense-tracker/
├── app.py              # Flask app and routes
├── database/
│   └── db.py           # SQLite connection, schema and seed data
├── templates/          # Jinja2 templates (base, landing, login, register)
├── static/
│   ├── css/style.css
│   └── js/main.js
└── requirements.txt
```
