import pytest
import uuid

def unique_email():
    return f"test_{uuid.uuid4()}@example.com"

def test_register(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login(client):
    # First ensure user exists
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
def get_token(client):
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })

    res = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "123456"
        }
    )

    return res.json()["access_token"]