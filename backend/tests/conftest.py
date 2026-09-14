import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import reset_store


@pytest.fixture(autouse=True)
def _reset_store():
    """Every test starts from the same seed data — the mock store is
    in-memory and mutated by requests, so it must be reset between tests."""
    reset_store()
    yield


@pytest.fixture
def client():
    return TestClient(app)
