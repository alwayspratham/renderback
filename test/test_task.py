import pytest


def register_user(client):
    return client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })


def login_user(client):
    return client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "123456"
        }
    )


def get_token(client):
    register_user(client)
    res = login_user(client)
    return res.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ---------------- TASK TESTS ---------------- #

def test_create_task(client):
    token = get_token(client)

    response = client.post(
        "/api/v1/tasks/create",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["is_completed"] is False


def test_get_tasks(client):
    token = get_token(client)

    # create one task first
    client.post(
        "/api/v1/tasks/create",
        json={
            "title": "Task 1",
            "description": "Desc"
        },
        headers=auth_headers(token)
    )

    response = client.get(
        "/api/v1/tasks/",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_single_task(client):
    token = get_token(client)

    create_res = client.post(
        "/api/v1/tasks/create",
        json={
            "title": "Single Task",
            "description": "Desc"
        },
        headers=auth_headers(token)
    )

    task_id = create_res.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_update_task(client):
    token = get_token(client)

    create_res = client.post(
        "/api/v1/tasks/create",
        json={
            "title": "Old",
            "description": "Old desc"
        },
        headers=auth_headers(token)
    )

    task_id = create_res.json()["id"]

    response = client.put(
        f"/api/v1/tasks/update/{task_id}",
        json={
            "title": "Updated"
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_delete_task(client):
    token = get_token(client)

    create_res = client.post(
        "/api/v1/tasks/create",
        json={
            "title": "Delete Me",
            "description": "Temp"
        },
        headers=auth_headers(token)
    )

    task_id = create_res.json()["id"]

    response = client.delete(
        f"/api/v1/tasks/delete/{task_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"{task_id} is deleted"