# Spec: Profile Page Design

## Overview

Replace the `/profile` placeholder with a real, logged-in page that shows who the user is and a read-only snapshot of their spending. The page has three parts: a header card with the user's name, email and member-since date; a row of summary stats (total spent, number of expenses, top category); and a table of their most recent expenses plus a per-category breakdown. This is the first logged-in page. It builds on the session introduced in Step 3 and gives later expense steps (add, edit, delete) a place to link back to.

## Depends on

- Step 1 — Database setup (`users` and `expenses` tables, `get_db()`, seeded demo user with expenses)
- Step 2 — Registration (users can be created)
- Step 3 — Login and logout (`session["user_id"]` is set on login and the navbar links to `url_for('profile')`)

## Routes

- `GET /profile` — render the profile page for the signed-in user; if there is no `user_id` in the session, redirect to `url_for('login')` — logged-in. Replaces the existing placeholder in `app.py`

Do not add a second `/profile` route. The `/expenses/...` placeholders are not touched.

## Database changes

No database changes. The page reads from the existing tables:

- `users` — `id`, `name`, `email`, `created_at`
- `expenses` — `user_id`, `amount`, `category`, `date`, `description`

All expense queries must be scoped with `WHERE user_id = ?` using the session's `user_id`.

## Templates

- **Create:**
  - `templates/profile.html` — extends `base.html`; sets `{% block title %}`; renders the header card, stats row, category breakdown and recent expenses table
- **Modify:** none. The navbar in `base.html` already links to `url_for('profile')` for signed-in users.

## Files to change

- `app.py` — replace the `profile()` placeholder with the real view (session guard, three queries, `render_template`)
- `static/css/style.css` — append profile page styles (new classes prefixed `profile-`); do not alter existing rules

## Files to create

- `templates/profile.html`
- `tests/test_profile.py` — pytest-flask tests for the redirect when logged out and for the data shown when logged in (reuse fixtures from `tests/` if they exist)

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (this page never reads or displays `password_hash`)
- Use CSS variables — never hardcode hex values (`--ink`, `--paper`, `--accent`, `--border`, `--radius-*`, `--font-display`, `--font-body`)
- All templates extend `base.html`
- Use `url_for(...)` for links and redirects, not hard-coded paths
- Replace the existing `profile` view; do not add a second route
- Guard with `session.get("user_id")`; when missing, `redirect(url_for("login"))`
- Fetch the user by `session["user_id"]`, never by an id from the URL or query string. If the user row no longer exists, `session.clear()` and redirect to `url_for("login")`
- Open every connection with `contextlib.closing(get_db())`, matching the other views
- Do the aggregation in SQL (`SUM`, `COUNT`, `GROUP BY category`), not in Jinja
- Recent expenses: latest 10 ordered by `date DESC, id DESC`
- Category breakdown: ordered by total descending; the top category in the stats row is the first row of this result
- Format amounts with the ₹ symbol and two decimals; format dates as stored (`YYYY-MM-DD`)
- Rely on Jinja autoescaping for `name`, `email` and `description`; do not use `|safe`
- Empty state: a user with no expenses sees "No expenses yet" in place of the table and breakdown, and the stats show `₹0.00`, `0` and `—`
- Plain HTML/CSS only; no JS libraries and no new JS
- Responsive: stats and layout stack to a single column at the existing mobile breakpoint
- Only touch `app.py`'s `profile()` view and the styles needed for this page; do not change the other pages or placeholder routes

## Definition of done

- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Logging in as `demo@spendly.com` / `demo123` and clicking Profile in the navbar opens the profile page
- [ ] The header card shows the demo user's name, email and member-since date
- [ ] The stats row shows total spent, expense count (8) and top category for the seeded data, and the figures match the database
- [ ] The category breakdown lists each category with its total, highest first
- [ ] The recent expenses table shows at most 10 rows, newest first, with date, category, description and amount
- [ ] A newly registered user with no expenses sees "No expenses yet" and `₹0.00` / `0` / `—` in the stats
- [ ] One user never sees another user's expenses (verified with two accounts)
- [ ] A name or description containing `<script>` renders as text, not as markup
- [ ] The page uses the existing theme (fonts, colours, spacing) with no hardcoded hex values in new CSS
- [ ] At phone width the layout stacks cleanly with no horizontal scroll
- [ ] `pytest tests/test_profile.py` passes
- [ ] App starts without errors and no other page changes
