import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.parametrize("params, expected_count, status_code", [
    ({"name": "Reading"}, 1, status.HTTP_200_OK),
    ({"name": "None existed collection"}, 0, status.HTTP_200_OK),
    ({"name": "Reading", "skip": 0, "limit": 10}, 1, status.HTTP_200_OK),
    ({"name": "", "skip": 0, "limit": 10}, 0, status.HTTP_422_UNPROCESSABLE_CONTENT),
    ({"name": "Reading", "skip": -1, "limit": 100}, 0, status.HTTP_422_UNPROCESSABLE_CONTENT),
])
async def test_search_collection(params, expected_count, status_code, authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get("v1/collections/search", params=params)

    assert response.status_code == status_code

    if response.status_code == status.HTTP_200_OK:
        assert isinstance(response.json(), list)
        assert len(response.json()) == expected_count


@pytest.mark.parametrize("params, expected_count", [
    ({"skip": 0, "limit": 10}, 2),
    ({"skip": 5, "limit": 10}, 0),
])
async def test_list_collection(params, expected_count, authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get("v1/collections", params=params)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert expected_count == len(response.json())


@pytest.mark.parametrize("collection_id, status_code", [
    (4, status.HTTP_200_OK),
    (999, status.HTTP_404_NOT_FOUND),
])
async def test_get_collection(collection_id, status_code, authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get(f"v1/collections/{collection_id}")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert response.json()["id"] == collection_id


@pytest.mark.parametrize("collection_id, links_count, status_code", [
    (4, 2, status.HTTP_200_OK),
    (999, 0, status.HTTP_404_NOT_FOUND),
])
async def test_get_collection_links_count(
        collection_id,
        links_count,
        status_code,
        authenticated_async_client: AsyncClient
):
    response = await authenticated_async_client.get(f"v1/collections/{collection_id}/links/count")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert isinstance(response.json()["count"], int)
        assert response.json()["count"] == links_count

@pytest.mark.parametrize("collection_id, links_count, status_code", [
    (4, 2, status.HTTP_200_OK),
    (999, 0, status.HTTP_404_NOT_FOUND),
])
async def test_get_collection_list_links(
        collection_id,
        links_count,
        status_code,
        authenticated_async_client: AsyncClient
):
    response = await authenticated_async_client.get(f"v1/collections/{collection_id}/links")

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert isinstance(response.json(), list)
        assert len(response.json()) == links_count


@pytest.mark.parametrize("update_data, status_code", [
    ({
         "name": "name update",
         "description": "description update ",
     }, status.HTTP_200_OK),
    ({"name": "only name update"}, status.HTTP_422_UNPROCESSABLE_CONTENT),
    ({"description": "only description update"}, status.HTTP_422_UNPROCESSABLE_CONTENT),
    ({}, status.HTTP_422_UNPROCESSABLE_CONTENT),
])
async def test_update_collection(
        update_data,
        status_code,
        authenticated_async_client: AsyncClient):
    collection_id = 4
    response = await authenticated_async_client.put(
        f"v1/collections/{collection_id}",
        json=update_data
    )

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        result = response.json()
        assert result["id"] == collection_id
        for key, value in update_data.items():
            assert result[key] == value


@pytest.mark.parametrize("patch_data, status_code", [
    ({
         "name": "name patch",
         "description": "description patch",
     }, status.HTTP_200_OK),
    ({"name": "only name patch"}, status.HTTP_200_OK),
    ({"description": "only description patch"}, status.HTTP_200_OK),
    ({}, status.HTTP_200_OK),
    ({"name": ""}, status.HTTP_422_UNPROCESSABLE_CONTENT),
])
async def test_patch_collection(
        patch_data,
        status_code,
        authenticated_async_client: AsyncClient):
    collection_id = 4
    response = await authenticated_async_client.patch(
        f"v1/collections/{collection_id}",
        json=patch_data
    )

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        result = response.json()
        assert result["id"] == collection_id
        for key, value in patch_data.items():
            assert result[key] == value


@pytest.mark.parametrize("collection_id, json_data, status_code", [
    (999, {"add_ids": [4, 6]}, status.HTTP_404_NOT_FOUND),
    (4, {"add_ids": [8]}, status.HTTP_204_NO_CONTENT),
    (4, {"remove_ids": [1]} , status.HTTP_204_NO_CONTENT),
])
async def test_patch_links_in_collection_negative(
        collection_id,
        json_data,
        status_code,
        authenticated_async_client: AsyncClient
):

    response = await authenticated_async_client.patch(
        f"v1/collections/{collection_id}/links",
        json=json_data
    )

    assert response.status_code == status_code

    if response.status_code == status.HTTP_204_NO_CONTENT:
        get_response = await authenticated_async_client.get(
            f"v1/collections/{collection_id}/links",
            params={"skip": 0, "limit": 10}
        )
        collection_data = get_response.json()
        current_links = {link["id"] for link in collection_data}

        for link_id in json_data.get("remove_ids", []):
            assert link_id not in current_links
        for link_id in json_data.get("add_ids", []):
            assert link_id not in current_links


@pytest.mark.parametrize("collection_id, json_data, status_code", [
    (4, {"add_ids": [4, 6]}, status.HTTP_204_NO_CONTENT),
    (4, {"add_ids": [4, 6]}, status.HTTP_204_NO_CONTENT),
    (4, {"add_ids": [5], "remove_ids": [4]}, status.HTTP_204_NO_CONTENT),
    (1, {"add_ids": [4, 6]}, status.HTTP_404_NOT_FOUND),
    (4, {"add_ids": ["abc"]}, status.HTTP_422_UNPROCESSABLE_CONTENT),
])
async def test_patch_links_in_collection(
        collection_id,
        json_data,
        status_code,
        authenticated_async_client: AsyncClient
):

    response = await authenticated_async_client.patch(
        f"v1/collections/{collection_id}/links",
        json=json_data
    )

    assert response.status_code == status_code

    get_response = await authenticated_async_client.get(
        f"v1/collections/{collection_id}/links",
        params={"skip": 0, "limit": 10}
    )

    if get_response.status_code == status.HTTP_204_NO_CONTENT:
        collection_data = get_response.json()

        current_links = {link["id"] for link in collection_data}

        for link_id in json_data.get("remove_ids", []):
            assert link_id not in current_links

        for link_id in json_data.get("add_ids", []):
            assert link_id in current_links


@pytest.mark.parametrize("create_data, status_code", [
        ({"name":"name create",
          "description": "description create"
          }, status.HTTP_201_CREATED,),
        ({"name":"name create",
          "description": "description create"
          }, status.HTTP_409_CONFLICT),
        ({}, status.HTTP_422_UNPROCESSABLE_CONTENT),
    ])
async def test_create_collection(create_data, status_code, authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.post(
        "v1/collections",
        json=create_data
    )
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        result = response.json()
        for key, value in create_data.items():
            assert result[key] == value

        response = await authenticated_async_client.get(
            f"v1/collections/{result['id']}"
        )
        assert response.status_code == status.HTTP_200_OK


async def test_delete_collection(authenticated_async_client: AsyncClient):
    collection_id = 4
    response = await authenticated_async_client.delete(
        f"v1/collections/{collection_id}"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await authenticated_async_client.get(f"v1/collections/{collection_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
