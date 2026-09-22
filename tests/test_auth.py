from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_requires_email_and_password():
    response = client.post("/auth/login", json={})

    assert response.status_code == 422


def test_login_rejects_invalid_email():
    response = client.post(
        "/auth/login",
        json={"email": "not-an-email", "password": "wrong-password"},
    )

    assert response.status_code == 422
