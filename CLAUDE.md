# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
python -m venv venv
source venv/Scripts/activate      # Git Bash on Windows (PowerShell: venv\Scripts\Activate.ps1)
pip install -r requirements.txt
python app.py                     # dev server with debug reload at http://127.0.0.1:5001
pytest                            # run tests (pytest + pytest-flask)
pytest path/to/test_file.py::test_name   # run a single test
```

There is no linter or build step. No tests exist yet, and `database/db.py` (mentioned in the README) has not been created.

## Architecture

Spendly is a Flask expense tracker built step by step. Only the UI shell exists so far.

- `app.py` holds all routes. `/`, `/register`, `/login`, `/terms` and `/privacy` render templates. `/logout`, `/profile` and the `/expenses/...` routes are string-returning placeholders labelled with the build step that will implement them. Replace the placeholder rather than adding a duplicate route.
- `templates/base.html` is the layout: navbar, `{% block content %}`, footer (with the Terms/Privacy links), then `main.js` and `{% block scripts %}`. Every page extends it. Page-specific JS goes in `{% block scripts %}` (see the video modal in `landing.html`).
- `static/css/style.css` is the only stylesheet. All pages share it, including hero, mock card, legal pages and video modal. There is no `landing.css`. Styling relies on the CSS variables at the top (`--ink`, `--paper`, `--accent`, `--border`, `--radius-*`, `--font-display`, `--font-body`), so reuse them to match the theme.
- Frontend is plain HTML/CSS/vanilla JS. Do not add JS libraries or frameworks.
- The landing-page "See how it works" modal embeds a placeholder YouTube URL (`VIDEO_URL` in `landing.html`). It stops the video on close by clearing the iframe `src`.

## Conventions

- Use `url_for(...)` for links in templates, not hard-coded paths.
- The user usually scopes front-end requests narrowly ("do not touch any other part of the page"). Edit only what was asked.
- Commits use short lowercase messages prefixed with the area, e.g. `landing: add youtube modal on see how it works click`.
