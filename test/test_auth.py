import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from models.user import User

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_users(db_session: Session):
    db_session.query(User).delete()
    db_session.commit()
    yield
    db_session.query(User).delete()
    db_session.commit()

def test_login_success():
    response = client.post("/auth/login", json={
        "username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()



def test_register_success(db_session: Session):
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data


def test_register_existing_email(db_session: Session):
    user = User(email="duplicate@example.com", hashed_password="hashedpw")
    db_session.add(user)
    db_session.commit()

    response = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "anotherpw"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "email was registered before"


def test_register_invalid_email():
    response = client.post("/auth/register", json={
        "email": "not-an-email",
        "password": "pw123"
    })
    assert response.status_code == 422


def test_register_short_password():
    response = client.post("/auth/register", json={
        "email": "shortpw@example.com",
        "password": "12"
    })
    assert response.status_code == 422