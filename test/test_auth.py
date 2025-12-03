import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from db.session import Base, get_db
from main import app
from models.token import RefreshToken
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


### logout


SQLALCHEMY_DATABASE_URL = "postgresql://test_user:test_password@localhost:5432/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db_session():
    """Фікстура для роботи з тестовою БД"""
    session = TestingSessionLocal()
    yield session
    session.close()


def test_logout_success(db_session):

    token = RefreshToken(token="valid_token", revoked=False)
    db_session.add(token)
    db_session.commit()

    response = client.post("/logout", json={"refreshed_token": "valid_token"})
    assert response.status_code == 200
    assert response.json() == {"message": "successfully logout!!!"}

    refreshed = db_session.query(RefreshToken).filter_by(token="valid_token").first()
    assert refreshed.revoked is True


def test_logout_invalid_token(db_session):
    response = client.post("/logout", json={"refreshed_token": "wrong_token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "invalid refresh token"