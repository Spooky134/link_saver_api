from httpx import AsyncClient
from fastapi import status


async def test_get_me_authenticated(authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get("api/v1/users/me")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["email"] == "alice.smith@example.com"
    assert "id" in data


async def test_get_me_not_authenticated(async_client: AsyncClient):
    response = await async_client.get("api/v1/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    assert "detail" in response.json()


async def test_get_me_invalid_token(async_client: AsyncClient):
    async_client.cookies.set("access_token", "invalid.jwt.token")

    response = await async_client.get("api/v1/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED