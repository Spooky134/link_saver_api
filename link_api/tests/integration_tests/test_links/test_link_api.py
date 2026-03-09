from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize("method, url", [
    ("get", "v1/links/1"),
    ("patch", "v1/links/1"),
    ("delete", "v1/links/1"),
])
async def test_access_other_user_link(method, url, authenticated_async_client: AsyncClient):
    call = getattr(authenticated_async_client, method)
    if method == "patch":
        json_data = {"title": "hacked"}
        response = await call(url, json=json_data)
    else:
        response = await call(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.parametrize("params, expected_count", [
    ({"skip": 0, "limit": 10}, 3),
    ({"skip": 5, "limit": 10}, 0),
])
async def test_list(params, expected_count, authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get("v1/links", params=params)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert expected_count == len(response.json())


@pytest.mark.parametrize("params, expected_count, status_code", [
    ({"link_type": "article"}, 1, status.HTTP_200_OK),
    ({"link_type": "video"}, 0, status.HTTP_200_OK),
    ({"link_type": "invalid_type"}, 0, status.HTTP_422_UNPROCESSABLE_CONTENT),
    ({"link_type": "article", "skip": 0, "limit": 10}, 1, status.HTTP_200_OK),
])
async def test_list_by_type(params, status_code, expected_count, authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get("v1/links/type", params=params)

    assert response.status_code == status_code

    if response.status_code == status.HTTP_200_OK:
        assert isinstance(response.json(), list)
        assert len(response.json()) == expected_count


@pytest.mark.parametrize("link_id, status_code", [
    (4, status.HTTP_200_OK),
    (999, status.HTTP_404_NOT_FOUND),
])
async def test_get_link(link_id: int, status_code, authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get(f"v1/links/{link_id}")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert response.json()["id"] == link_id


@pytest.mark.parametrize("update_data, status_code", [
    ({
         "title": "patch_title",
         "description": "patch_description",
         "image_url": "https://example.com/image.png",
         "link_type": "website"
     }, status.HTTP_200_OK),
    ({"title": "only title updated"}, status.HTTP_200_OK),
    ({"link_type": "website"}, status.HTTP_200_OK),
    ({}, status.HTTP_200_OK),
    ({"link_type": "invalid_type"}, status.HTTP_422_UNPROCESSABLE_CONTENT),
])
async def test_patch_link(
        update_data,
        status_code,
        authenticated_async_client: AsyncClient):
    link_id = 4
    response = await authenticated_async_client.patch(
        f"v1/links/{link_id}",
        json=update_data
    )

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        result = response.json()
        assert result["id"] == link_id
        for key, value in update_data.items():
            assert result[key] == value

async def test_patch_link_with_non_existent_id(authenticated_async_client: AsyncClient):
    link_id = 999
    link_data = {}
    response = await authenticated_async_client.patch(
        f"v1/links/{link_id}",
        json=link_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("url, status_code", [
        ("https://www.youtube.com/watch?v=lBm9_pRj2UA&ab_channel=ScHoolBoyQVEVO", status.HTTP_202_ACCEPTED),
        ("https://www.youtube.com/watch?v=lBm9_pRj2UA&ab_channel=ScHoolBoyQVEVO", status.HTTP_409_CONFLICT),
        ("not-a-url", status.HTTP_422_UNPROCESSABLE_CONTENT),
    ])
async def test_create_link(
        url,
        status_code,
        mock_parse_and_update_task: AsyncMock,
        authenticated_async_client: AsyncClient
):
    json_body = {
        "url": url,
    }
    response = await authenticated_async_client.post(
        "v1/links",
        json=json_body
    )

    assert response.status_code == status_code

    if status_code == status.HTTP_202_ACCEPTED:
        result = response.json()
        assert result["url"] == url

        mock_parse_and_update_task.assert_awaited_once_with(
            user_id=result["user_id"],
            link_id=result["id"]
        )


async def test_delete_link(authenticated_async_client: AsyncClient):
    link_id = 4
    response = await authenticated_async_client.delete(
        f"v1/links/{link_id}"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await authenticated_async_client.get(f"v1/links/{link_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
