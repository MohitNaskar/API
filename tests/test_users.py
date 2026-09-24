def test_create_user_rejects_invalid_email(client):
    response = client.post(
        "/users/",
        json={"email": "not-an-email", "password": "strong-password"},
    )

    assert response.status_code == 422


def test_create_user_requires_password(client):
    response = client.post(
        "/users/",
        json={"email": "test@example.com"},
    )

    assert response.status_code == 422


def test_create_user_requires_email(client):
    response = client.post(
        "/users/",
        json={"password": "strong-password"},
    )

    assert response.status_code == 422


def test_get_user_requires_integer_id(client):
    response = client.get("/users/not-an-id")

    assert response.status_code == 422


def test_create_user_returns_public_fields(client, user_payload):
    response = client.post("/users/", json=user_payload)

    assert response.status_code == 201
    assert response.json()["email"] == user_payload["email"]
    assert "password" not in response.json()
    assert "created_at" in response.json()


def test_create_user_rejects_duplicate_email(client, user_payload):
    first_response = client.post("/users/", json=user_payload)
    second_response = client.post("/users/", json=user_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 500


def test_get_user_returns_created_user(client, registered_user):
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["email"] == registered_user["email"]


def test_get_missing_user_returns_not_found(client):
    response = client.get("/users/999")

    assert response.status_code == 404
