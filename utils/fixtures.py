"""Pytest fixtures shared across the api test suite."""
import pytest
import requests

from utils.helpers import BASE_API_URL


@pytest.fixture(scope="session")
def api_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()
