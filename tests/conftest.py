import pytest

from database import db


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))

    from app import app as flask_app

    flask_app.config["TESTING"] = True
    db.init_db()
    db.seed_db()
    return flask_app
