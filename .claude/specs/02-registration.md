# Spec: Registration

## Overview

Make the existing `/register` page functional. Today the route only renders the form; this step accepts the form submission, validates it, stores a new user with a hashed password in the `users` table, and On Suceessfly register the user is shown with a sucess message and sends the user on to the login page. It is the first feature built on the Step 1 data layer and is required before login/logout (Step 3) can authenticate anyone.

## Depends on

- Step 1 — Database setup (`users` table, `get_db()`, `init_db()`)

## Routes

- `GET /register` — render the empty registration form — public (already exists, unchanged)
- `POST /register` — validate form, create user, redirect to `/login` on success or re-render the form with an error — public

Both methods are handled by the single existing `register()` view in `app.py`. Do not add a duplicate route.

## Database changes

No database changes. The `users` table in `database/db.py` already has `name`, `email` (UNIQUE, NOT NULL), `password_hash` and `created_at`.

## Templates

- **Create:** none
- **Modify:** `templates/register.html`
  - Change the form `action` from the hard-coded `/register` to `{{ url_for('register') }}`
  - Re-populate the `name` and `email` inputs with the submitted values after a failed submit (never the password)
  - Keep the existing `{% if error %}` block for showing errors
  - Add `minlength="8"` to the password input

## Files to change

- `app.py` — accept `GET` and `POST` on `/register`, add validation and insert logic, import `request`, `redirect`, `url_for`, `sqlite3`, and `generate_password_hash`
- `templates/register.html` — as described above

## Files to create

- `tests/test_registration.py` — pytest-flask tests for the registration flow (the `tests/` directory does not exist yet)

## New dependencies

No new dependencies. Uses `sqlite3` (stdlib) and `werkzeug.security`, both already available.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`); never store or log the plain password
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for(...)` for links and redirects, not hard-coded paths
- Replace the existing `register` view; do not add a second `/register` route
- Edit only `app.py` and `templates/register.html` for the feature itself; do not touch other pages or `static/css/style.css` (the `.auth-error` style already exists)
- Server-side validation (the HTML `required` attributes are not enough):
  - `name`, `email` and `password` must be present; strip whitespace from `name` and `email`
  - `email` must contain a single `@` with text on both sides; store it lowercased
  - `password` must be at least 8 characters
  - Show one clear error message at a time via the `error` template variable
- Handle duplicate emails by catching `sqlite3.IntegrityError` from the insert (UNIQUE constraint), not by a separate check-then-insert, and show "An account with that email already exists"
- Always close the connection (use `contextlib.closing`, matching `database/db.py`) and commit after the insert
- On success, redirect to `url_for('login')`. Do not log the user in; sessions belong to Step 3
- Do not add `secret_key`, sessions or `flash`; they are not needed in this step
- Failed validation returns the form with HTTP 200 and the error shown

## Definition of done

- [ ] `GET /register` still renders the form with name, email and password fields
- [ ] Submitting valid details creates a row in `users` and redirects to `/login`
- [ ] The stored `password_hash` is a werkzeug hash, not the plain password
- [ ] The stored email is lowercased and trimmed
- [ ] Submitting with an empty name, email or password shows an error and creates no row
- [ ] An email without a valid `@` format shows an error and creates no row
- [ ] A password shorter than 8 characters shows an error and creates no row
- [ ] Registering `demo@spendly.com` (the seeded user) shows "An account with that email already exists" and the app does not crash
- [ ] Registering the same email in a different case (e.g. `Demo@Spendly.com`) is also rejected as a duplicate
- [ ] After a failed submit, name and email are pre-filled and the password field is empty
- [ ] The form posts via `url_for('register')`, with no hard-coded path
- [ ] `pytest tests/test_registration.py` passes
- [ ] App starts without errors and no other page changes
