def test_login_requires_email_and_password(client):
    response = client.post("/auth/login", json={})

    assert response.status_code == 422


def test_login_rejects_invalid_email(client):
    response = client.post(
        "/auth/login",
        json={"email": "not-an-email", "password": "wrong-password"},
    )

    assert response.status_code == 422


def test_login_requires_password(client):
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com"},
    )

    assert response.status_code == 422


def test_login_returns_access_token(client, user_payload, registered_user):
    response = client.post("/auth/login", json=user_payload)

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_rejects_wrong_password(client, user_payload, registered_user):
    response = client.post(
        "/auth/login",
        json={"email": user_payload["email"], "password": "wrong-password"},
    )

    assert response.status_code == 401
