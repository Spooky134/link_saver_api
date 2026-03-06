from httpx import AsyncClient
from fastapi import status
import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("test@test.com", "test", status.HTTP_201_CREATED),
    ("test@test.com", "test", status.HTTP_409_CONFLICT),
    ("test@test.com", "test0", status.HTTP_409_CONFLICT),
    ("test", "test", status.HTTP_422_UNPROCESSABLE_CONTENT)
])
async def test_register(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post("v1/auth/register", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert response.json().get("message") is not None




@pytest.mark.parametrize("email, password, status_code", [
    ("john.doe@example.com", "test", status.HTTP_200_OK),
    ("JOHN.doe@example.com", "test", status.HTTP_401_UNAUTHORIZED),
    ("test@test.com", "test0", status.HTTP_401_UNAUTHORIZED),
    ("test@test.com", "", status.HTTP_401_UNAUTHORIZED),
    ("test1@test1.com", "test", status.HTTP_401_UNAUTHORIZED),
    ("test", "test", status.HTTP_422_UNPROCESSABLE_CONTENT),
])
async def test_login(email, password, status_code, async_client: AsyncClient):
    response = await async_client.post("v1/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        data = response.json()
        assert "access_token" in data

        assert "access_token" in async_client.cookies
        assert async_client.cookies["access_token"] == data["access_token"]
    else:
        assert "access_token" not in async_client.cookies


@pytest.mark.parametrize("is_authenticated, status_code", [
    (True, status.HTTP_200_OK),
    (False, status.HTTP_401_UNAUTHORIZED),
])
async def test_logout(is_authenticated: bool, status_code, async_client: AsyncClient):
    if is_authenticated:
        await async_client.post("v1/auth/login", json={
            "email": "alice.smith@example.com",
            "password": "test"
        })
        assert "access_token" in async_client.cookies
    else:
        async_client.cookies.clear()

    response = await async_client.post("v1/auth/logout")

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        assert response.json().get("message") is not None
        assert "access_token" not in async_client.cookies
