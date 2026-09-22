from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_user_rejects_invalid_email():
    response = client.post(
        "/users/",
        json={"email": "not-an-email", "password": "strong-password"},
    )

    assert response.status_code == 422


def test_create_user_requires_password():
    response = client.post(
        "/users/",
        json={"email": "test@example.com"},
    )

    assert response.status_code == 422
