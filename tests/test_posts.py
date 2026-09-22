from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_posts_requires_authentication():
    response = client.get("/posts/")

    assert response.status_code == 401


def test_create_post_requires_authentication():
    response = client.post(
        "/posts/",
        json={
            "title": "Test post",
            "content": "Test content",
            "published": True,
        },
    )

    assert response.status_code == 401
