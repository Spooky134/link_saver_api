from typing import List

from fastapi import APIRouter, Query, status
from fastapi_cache.decorator import cache

from app.auth.dependencies import CurrentUserDep
from app.collection.dependencies import CollectionServiceDep
from app.collection.entities import CreateCollectionEntity, UpdateCollectionEntity
from app.collection.schemas import (
    Collection,
    CollectionCreate,
    CollectionPatch,
    CollectionUpdate,
    CountLinkInCollection,
    PatchLinksInCollection,
)
from app.core.dependecies import PaginationDep
from app.link.schemas import Link

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("/search", response_model=List[Collection])
@cache(expire=30)
async def search_collection(
    service: CollectionServiceDep,
    current_user: CurrentUserDep,
    pagination: PaginationDep,
    name: str = Query(..., min_length=1, examples=["String"]),
):
    return await service.search_by_name(
        current_user.id, name, skip=pagination.skip, limit=pagination.limit
    )


@router.post("", response_model=Collection, status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection_create: CollectionCreate,
    service: CollectionServiceDep,
    current_user: CurrentUserDep,
):
    new_collection = CreateCollectionEntity(**collection_create.model_dump())
    return await service.create_collection(current_user.id, new_collection)


@router.get("", response_model=List[Collection])
@cache(expire=30)
async def list_collections(
    service: CollectionServiceDep,
    current_user: CurrentUserDep,
    pagination: PaginationDep,
):
    return await service.list_collections(
        current_user.id, pagination.skip, pagination.limit
    )


@router.get("/{collection_id}", response_model=Collection)
async def get_collection(
    collection_id: int,
    service: CollectionServiceDep,
    current_user: CurrentUserDep,
):
    return await service.get_collection(current_user.id, collection_id)


@router.put("/{collection_id}", response_model=Collection)
async def update_collection(
    collection_id: int,
    collection_update: CollectionUpdate,
    service: CollectionServiceDep,
    current_user: CurrentUserDep,
):
    collection_update = UpdateCollectionEntity(**collection_update.model_dump())
    return await service.update_collection(
        current_user.id, collection_id, collection_update
    )


@router.patch("/{collection_id}", response_model=Collection)
async def patch_collection(
    collection_id: int,
    collection_update: CollectionPatch,
    service: CollectionServiceDep,
    current_user: CurrentUserDep,
):
    collection_update = UpdateCollectionEntity(
        **collection_update.model_dump(exclude_unset=True)
    )
    return await service.update_collection(
        current_user.id, collection_id, collection_update
    )


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
    collection_id: int, service: CollectionServiceDep, current_user: CurrentUserDep
):
    await service.delete_collection(current_user.id, collection_id)


@router.get("/{collection_id}/links/count", response_model=CountLinkInCollection)
@cache(expire=30)
async def get_collection_links_count(
    collection_id: int, service: CollectionServiceDep, current_user: CurrentUserDep
):
    count = await service.links_count(current_user.id, collection_id)
    return {"count": count}


@router.get("/{collection_id}/links", response_model=List[Link])
@cache(expire=30)
async def get_collection_list_links(
    collection_id: int,
    service: CollectionServiceDep,
    current_user: CurrentUserDep,
    pagination: PaginationDep,
):
    return await service.list_links(
        current_user.id, collection_id, pagination.skip, pagination.limit
    )


@router.patch("/{collection_id}/links", status_code=status.HTTP_204_NO_CONTENT)
async def patch_links_in_collection(
    collection_id: int,
    patch_links: PatchLinksInCollection,
    service: CollectionServiceDep,
    current_user: CurrentUserDep,
):
    await service.update_links(
        current_user.id, collection_id, patch_links.add_ids, patch_links.remove_ids
    )
