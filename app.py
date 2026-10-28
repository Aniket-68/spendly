import os
import sqlite3
from contextlib import closing
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-secret-change-me")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    def fail(error):
        return render_template("register.html", error=error, name=name, email=email)

    if not name or not email or not password:
        return fail("All fields are required")

    local, _, domain = email.partition("@")
    if not local or not domain or "@" in domain:
        return fail("Enter a valid email address")

    if len(password) < 8:
        return fail("Password must be at least 8 characters")

    try:
        with closing(get_db()) as conn:
            conn.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, generate_password_hash(password)),
            )
            conn.commit()
    except sqlite3.IntegrityError:
        return fail("An account with that email already exists")

    return render_template("register.html", success=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    def fail(error):
        return render_template("login.html", error=error, email=email)

    if not email or not password:
        return fail("All fields are required")

    with closing(get_db()) as conn:
        user = conn.execute(
            "SELECT id, name, password_hash FROM users WHERE email = ?",
            (email,),
        ).fetchone()

    if user is None or not check_password_hash(user["password_hash"], password):
        return fail("Invalid email or password")

    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("landing"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    with closing(get_db()) as conn:
        user = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        categories = conn.execute(
            "SELECT category, SUM(amount) AS total, COUNT(*) AS n "
            "FROM expenses WHERE user_id = ? GROUP BY category ORDER BY total DESC",
            (user_id,),
        ).fetchall()
        recent = conn.execute(
            "SELECT date, category, description, amount "
            "FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT 10",
            (user_id,),
        ).fetchall()

    if user is None:
        session.clear()
        return redirect(url_for("login"))

    total = sum(c["total"] for c in categories)
    stats = {
        "total": total,
        "count": sum(c["n"] for c in categories),
        "top_category": categories[0]["category"] if categories else None,
    }
    breakdown = [
        {
            "category": c["category"],
            "total": c["total"],
            "n": c["n"],
            "pct": round(c["total"] / total * 100) if total else 0,
        }
        for c in categories
    ]
    member_since = datetime.strptime(user["created_at"][:10], "%Y-%m-%d").strftime("%d %b %Y")

    return render_template(
        "profile.html",
        user=user,
        member_since=member_since,
        stats=stats,
        categories=breakdown,
        recent=recent,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
