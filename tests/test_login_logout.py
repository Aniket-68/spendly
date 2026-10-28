DEMO = {"email": "demo@spendly.com", "password": "demo123"}


def test_get_shows_form(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b'name="email"' in resp.data
    assert b'name="password"' in resp.data
    assert b'action="/login"' in resp.data


def test_valid_login_redirects_to_home(client):
    resp = client.post("/login", data=DEMO)
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
    assert not resp.headers["Location"].endswith("/profile")
    with client.session_transaction() as sess:
        assert sess["user_id"]


def test_email_is_trimmed_and_case_insensitive(client):
    resp = client.post("/login", data={**DEMO, "email": "  Demo@Spendly.com "})
    assert resp.status_code == 302


def test_wrong_password(client):
    resp = client.post("/login", data={**DEMO, "password": "wrongpass"})
    assert resp.status_code == 200
    assert b"Invalid email or password" in resp.data
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_unknown_email_same_error(client):
    resp = client.post("/login", data={"email": "nobody@example.com", "password": "demo123"})
    assert resp.status_code == 200
    assert b"Invalid email or password" in resp.data


def test_missing_fields(client):
    for data in ({"email": "", "password": "x"}, {"email": "demo@spendly.com", "password": ""}):
        resp = client.post("/login", data=data)
        assert resp.status_code == 200
        assert b"All fields are required" in resp.data


def test_failed_submit_prefills_email_not_password(client):
    resp = client.post("/login", data={"email": "demo@spendly.com", "password": "wrongpass"})
    assert b'value="demo@spendly.com"' in resp.data
    assert b"wrongpass" not in resp.data


def test_login_page_redirects_when_logged_in(client):
    client.post("/login", data=DEMO)
    resp = client.get("/login")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
    assert not resp.headers["Location"].endswith("/profile")


def test_register_redirects_when_logged_in(client):
    from contextlib import closing

    from database.db import get_db

    def user_count():
        with closing(get_db()) as conn:
            return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    client.post("/login", data=DEMO)
    before = user_count()

    resp = client.get("/register")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")

    resp = client.post(
        "/register",
        data={"name": "Asha Rao", "email": "asha@example.com", "password": "longenough1"},
    )
    assert resp.status_code == 302
    assert user_count() == before


def test_landing_register_cta_hidden_when_logged_in(client):
    assert b"Create free account" in client.get("/").data
    client.post("/login", data=DEMO)
    assert b"Create free account" not in client.get("/").data


def test_logout_clears_session_and_navbar(client):
    client.post("/login", data=DEMO)
    assert b"Sign out" in client.get("/").data

    resp = client.get("/logout")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
    with client.session_transaction() as sess:
        assert "user_id" not in sess

    page = client.get("/").data
    assert b"Sign in" in page
    assert b"Sign out" not in page


def test_registered_user_can_login(client):
    creds = {"name": "Asha Rao", "email": "asha@example.com", "password": "longenough1"}
    client.post("/register", data=creds)
    resp = client.post("/login", data={"email": creds["email"], "password": creds["password"]})
    assert resp.status_code == 302
