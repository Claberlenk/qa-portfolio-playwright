import pytest
import requests


@pytest.fixture(scope="session")
def api_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()
