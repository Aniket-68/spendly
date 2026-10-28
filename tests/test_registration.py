from contextlib import closing

import pytest
from werkzeug.security import check_password_hash

from database.db import get_db

VALID = {"name": "Asha Rao", "email": "asha@example.com", "password": "longenough1"}


def user_count():
    with closing(get_db()) as conn:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]


def test_get_shows_form(client):
    resp = client.get("/register")
    assert resp.status_code == 200
    for field in (b'name="name"', b'name="email"', b'name="password"'):
        assert field in resp.data


def test_valid_registration(client):
    before = user_count()
    resp = client.post("/register", data={**VALID, "name": "  Asha Rao ", "email": "  Asha@Example.com "})
    assert resp.status_code == 200
    assert b"Account created" in resp.data
    assert user_count() == before + 1
    with closing(get_db()) as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", ("asha@example.com",)).fetchone()
    assert row["name"] == "Asha Rao"
    assert row["password_hash"] != VALID["password"]
    assert check_password_hash(row["password_hash"], VALID["password"])


@pytest.mark.parametrize("field", ["name", "email", "password"])
def test_missing_field(client, field):
    before = user_count()
    resp = client.post("/register", data={**VALID, field: ""})
    assert resp.status_code == 200
    assert b"All fields are required" in resp.data
    assert user_count() == before


@pytest.mark.parametrize("email", ["abc", "a@", "@b.com", "a@@b.com"])
def test_bad_email(client, email):
    before = user_count()
    resp = client.post("/register", data={**VALID, "email": email})
    assert resp.status_code == 200
    assert b"valid email" in resp.data
    assert user_count() == before


def test_short_password(client):
    before = user_count()
    resp = client.post("/register", data={**VALID, "password": "1234567"})
    assert b"at least 8 characters" in resp.data
    assert user_count() == before


@pytest.mark.parametrize("email", ["demo@spendly.com", "Demo@Spendly.com"])
def test_duplicate_email(client, email):
    before = user_count()
    resp = client.post("/register", data={**VALID, "email": email})
    assert resp.status_code == 200
    assert b"An account with that email already exists" in resp.data
    assert user_count() == before


def test_failed_submit_prefills_but_not_password(client):
    resp = client.post("/register", data={**VALID, "password": "short"})
    assert b'value="Asha Rao"' in resp.data
    assert b'value="asha@example.com"' in resp.data
    assert b"short" not in resp.data.replace(b"Password must be at least 8 characters", b"")
