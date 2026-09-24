def test_get_posts_requires_authentication(client):
    response = client.get("/posts/")

    assert response.status_code == 401


def test_create_post_requires_authentication(client):
    response = client.post(
        "/posts/",
        json={
            "title": "Test post",
            "content": "Test content",
            "published": True,
        },
    )

    assert response.status_code == 401
 

def test_get_latest_post_requires_authentication(client):
    response = client.get("/posts/latest")

    assert response.status_code == 401


def test_get_post_requires_authentication(client):
    response = client.get("/posts/1")

    assert response.status_code == 401


def test_get_my_posts_requires_authentication(client):
    response = client.get("/posts/me")

    assert response.status_code == 401


def test_create_post_returns_created_post(client, auth_headers):
    response = client.post(
        "/posts/",
        headers=auth_headers,
        json={
            "title": "Test post",
            "content": "Test content",
            "published": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test post"
    assert response.json()["content"] == "Test content"


def test_get_my_posts_returns_current_users_posts(client, auth_headers):
    client.post(
        "/posts/",
        headers=auth_headers,
        json={"title": "My post", "content": "Content", "published": True},
    )

    response = client.get("/posts/me", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "My post"


def test_get_latest_post_returns_latest_post(client, auth_headers):
    client.post(
        "/posts/",
        headers=auth_headers,
        json={"title": "Latest", "content": "Newest", "published": True},
    )

    response = client.get("/posts/latest", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["title"] == "Latest"
