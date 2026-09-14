import os

# Must be set before anything imports app.db, since the connection target
# is read once at import time. Tests get an isolated in-memory database
# so they never touch a real karate.db file or interfere with each other.
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repository import reset_database


@pytest.fixture(autouse=True)
def _reset_store():
    """Every test starts from the same seed data — the database is
    mutated by requests, so it must be reset between tests."""
    reset_database()
    yield


@pytest.fixture
def client():
    return TestClient(app)
