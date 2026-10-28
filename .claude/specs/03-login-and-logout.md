# Spec: Login and Logout

## Overview

Make the existing `/login` page functional and replace the `/logout` placeholder. Login verifies the submitted email and password against the `users` table, stores the user's id in the Flask session, and redirects to the home page. Signed-in users are also kept off `/register` and the landing page hides its "Create free account" buttons. Logout clears the session and returns the user to the landing page. The navbar switches between "Sign in / Get started" and "Profile / Sign out" depending on session state. This is the step that introduces sessions, which Registration (Step 2) deliberately left out, and it is required before any logged-in page (profile, expenses) can be built.

## Depends on

- Step 1 — Database setup (`users` table, `get_db()`, seeded demo user)
- Step 2 — Registration (users with werkzeug-hashed passwords can be created)

## Routes

- `GET /login` — render the sign-in form; if already logged in, redirect to `url_for('landing')` — public (already exists, extended)
- `POST /login` — validate credentials, start a session, redirect to `url_for('landing')`, or re-render the form with an error — public
- `GET /logout` — clear the session and redirect to `url_for('landing')` — logged-in (harmless if not logged in; still redirects to landing). Replaces the existing placeholder in `app.py`

`login()` handles both methods in the single existing view. Do not add duplicate routes. `/profile` stays a placeholder (Step 4); it is only reachable from the navbar.

## Database changes

No database changes. The `users` table already has `id`, `email` (UNIQUE) and `password_hash`.

## Templates

- **Create:** none
- **Modify:**
  - `templates/login.html`
    - Change the form `action` from the hard-coded `/login` to `{{ url_for('login') }}`
    - Re-populate the `email` input with the submitted value after a failed submit (never the password)
    - Keep the existing `{% if error %}` block
  - `templates/base.html`
    - In the navbar, show "Sign in" and "Get started" when `session.get('user_id')` is not set
    - When it is set, show a link to `url_for('profile')` and a "Sign out" link to `url_for('logout')` instead

## Files to change

- `app.py` — add `secret_key`, import `session`, `redirect`, `url_for`, `check_password_hash`; implement `login()` POST handling; replace the `logout()` placeholder
- `templates/login.html` — as described above
- `templates/base.html` — conditional navbar links

## Files to create

- `tests/test_login_logout.py` — pytest-flask tests for the login and logout flow (reuse any fixtures from `tests/` created in Step 2 if they exist)

## New dependencies

No new dependencies. Uses Flask's built-in `session` and `werkzeug.security.check_password_hash`.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords verified with werkzeug (`check_password_hash`); never compare, store or log the plain password
- Use CSS variables — never hardcode hex values (no new CSS is expected; reuse existing `.auth-*` and nav classes)
- All templates extend `base.html`
- Use `url_for(...)` for links and redirects, not hard-coded paths
- Replace the existing `login` and `logout` views; do not add second routes
- Set `app.secret_key` from the `SECRET_KEY` environment variable with a clearly named development fallback; do not hardcode a production secret
- Store only `user_id` (and optionally `user_name` for display) in the session; never the email hash or password
- Normalise the email the same way as registration: strip whitespace and lowercase before the lookup
- Use a single generic error, "Invalid email or password", for both an unknown email and a wrong password, so the form does not reveal which accounts exist
- Missing email or password shows "All fields are required" and does not query the database
- Always close the connection with `contextlib.closing` and fetch the user with `SELECT ... WHERE email = ?`
- Call `session.clear()` before setting `user_id` on login to avoid session fixation, and `session.clear()` on logout
- Failed login returns the form with HTTP 200 and the error shown; success is a 302 redirect to `url_for('landing')`
- Do not add `flash`, Flask-Login, or any auth library
- Do not touch the other placeholder routes (`/profile`, `/expenses/...`) or any other page

## Definition of done

- [ ] `GET /login` renders the form with email and password fields
- [ ] Logging in as `demo@spendly.com` / `demo123` redirects to the home page (`/`)
- [ ] Email is matched case-insensitively and ignoring surrounding whitespace (e.g. ` Demo@Spendly.com `)
- [ ] A wrong password shows "Invalid email or password" and no session is created
- [ ] An unknown email shows the same "Invalid email or password" message
- [ ] Submitting with an empty email or password shows "All fields are required"
- [ ] After a failed submit, the email is pre-filled and the password field is empty
- [ ] The login form posts via `url_for('login')`, with no hard-coded path
- [ ] After login, the navbar shows Profile and Sign out instead of Sign in and Get started
- [ ] Visiting `/login` while logged in redirects to the home page (`/`)
- [ ] Visiting `/logout` clears the session, redirects to the landing page, and the navbar shows Sign in and Get started again
- [ ] A user registered through `/register` can immediately log in with the same credentials
- [ ] `pytest tests/test_login_logout.py` passes
- [ ] App starts without errors and no other page changes
