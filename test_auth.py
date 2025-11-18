from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_success():
    response = client.post("/auth/login", json={
        "username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()