DEMO = {"email": "demo@spendly.com", "password": "demo123"}


def register_and_login(client, name, email, password="password123"):
    client.post("/register", data={"name": name, "email": email, "password": password})
    client.post("/login", data={"email": email, "password": password})


def test_logged_out_redirects_to_login(client):
    resp = client.get("/profile")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/login")


def test_shows_user_and_stats(client):
    client.post("/login", data=DEMO)
    resp = client.get("/profile")
    assert resp.status_code == 200
    assert b"Demo User" in resp.data
    assert b"demo@spendly.com" in resp.data
    assert "₹6,814.74".encode() in resp.data
    assert b"Shopping" in resp.data
    assert resp.data.count(b"<tr>") == 9  # header row + 8 expenses


def test_category_breakdown_highest_first(client):
    client.post("/login", data=DEMO)
    html = client.get("/profile").data.decode()
    breakdown = html.split("By category")[1].split("Recent expenses")[0]
    assert breakdown.index("Shopping") < breakdown.index("Food")


def test_new_user_sees_empty_state(client):
    register_and_login(client, "Fresh User", "fresh@example.com")
    html = client.get("/profile").data.decode()
    assert "No expenses yet" in html
    assert "₹0.00" in html


def test_users_only_see_their_own_expenses(client):
    register_and_login(client, "Other User", "other@example.com")
    html = client.get("/profile").data.decode()
    assert "Groceries" not in html
    assert "Demo User" not in html


def test_name_is_escaped(client):
    register_and_login(client, "<script>alert(1)</script>", "xss@example.com")
    html = client.get("/profile").data.decode()
    assert "&lt;script&gt;" in html
    assert "<script>alert(1)</script>" not in html


def test_deleted_user_session_is_cleared(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 9999
    resp = client.get("/profile")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/login")
    with client.session_transaction() as sess:
        assert "user_id" not in sess
