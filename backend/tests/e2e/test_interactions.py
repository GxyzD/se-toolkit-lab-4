import httpx
import pytest
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TOKEN = os.getenv("API_TOKEN", "secretkey1")

@pytest.fixture
def client():
    """Создает HTTPX клиент с заголовками авторизации"""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    with httpx.Client(base_url=API_BASE_URL, headers=headers, timeout=10.0) as client:
        yield client


def test_get_interactions_returns_200(client: httpx.Client) -> None:
    """Test that GET /interactions/ returns 200 OK"""
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_response_is_a_list(client: httpx.Client) -> None:
    """Test that GET /interactions/ returns a JSON array"""
    response = client.get("/interactions/")
    data = response.json()
    assert isinstance(data, list)
