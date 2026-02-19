from fastapi import Query, APIRouter, status

from app.collection.entities import CollectionEntity
from app.collection.schemas import (
    Collection,
    CollectionWithLinks,
    CollectionCreate,
    CollectionUpdateFull,
    CollectionUpdate,
    CountLinkInCollection,
    AddLinksToCollection,
    RemoveLinksFromCollection
)
from app.link.schemas import Link
from app.collection.dependencies import CollectionServiceDep
from app.auth.dependencies import CurrentUserDep

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("/search", response_model=list[Collection])
async def search_collection(
        service: CollectionServiceDep,
        current_user: CurrentUserDep,
        name: str = Query(..., min_length=1, example="String"),
        skip: int = 0, limit: int = 10
):
    return await service.search_by_name(current_user.id, name, skip=skip, limit=limit)


@router.post("/", response_model=Collection, status_code=status.HTTP_201_CREATED)
async def create_collection(
        collection_create: CollectionCreate,
        service: CollectionServiceDep,
        current_user: CurrentUserDep
):
    new_collection = CollectionEntity(**collection_create.model_dump())
    return await service.create_collection(current_user.id, new_collection)


@router.get("/", response_model=list[Collection])
async def get_all_collections(
        service: CollectionServiceDep,
        current_user: CurrentUserDep,
        skip: int = 0,
        limit: int = 10
):
    return await service.get_all_collections(current_user.id, skip, limit)


@router.get("/{collection_id}", response_model=CollectionWithLinks)
async def get_collection(
        collection_id: int,
        service: CollectionServiceDep,
        current_user: CurrentUserDep,
        skip: int = 0,
        limit: int = 10
):
    return await service.get_collection(current_user.id, collection_id, skip, limit)


@router.put("/{collection_id}", response_model=Collection)
async def update_collection_full(
        collection_id: int,
        collection_update: CollectionUpdateFull,
        service: CollectionServiceDep,
        current_user: CurrentUserDep
):
    collection_update = CollectionEntity(**collection_update.model_dump())
    return await service.update_collection(current_user.id, collection_id, collection_update)


@router.patch("/{collection_id}", response_model=Collection)
async def update_collection_partial(
        collection_id: int,
        collection_update: CollectionUpdate,
        service: CollectionServiceDep,
        current_user: CurrentUserDep
):
    collection_update = CollectionEntity(**collection_update.model_dump(exclude_unset=True))
    return await service.update_collection(current_user.id, collection_id, collection_update)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(
        collection_id: int,
        service: CollectionServiceDep,
        current_user: CurrentUserDep
):
    await service.delete_collection(current_user.id, collection_id)


@router.get("/{collection_id}/links/count", response_model=CountLinkInCollection)
async def get_collection_links_count(
        collection_id: int,
        service: CollectionServiceDep,
        current_user: CurrentUserDep
):
    count = await service.get_links_count(current_user.id, collection_id)
    return {"count": count}

@router.get("/{collection_id}/links", response_model=list[Link])
async def get_collection_links(
        collection_id: int,
        service: CollectionServiceDep,
        current_user: CurrentUserDep,
        skip: int = 0,
        limit: int = 10
):
    return await service.get_links(current_user.id, collection_id, skip, limit)


@router.post("/{collection_id}/links", response_model=list[Link])
async def add_links_to_collection(
        collection_id: int,
        add_links_to_col: AddLinksToCollection,
        service: CollectionServiceDep,
        current_user: CurrentUserDep
):
    return await service.add_links(current_user.id, collection_id, add_links_to_col.link_ids)


@router.delete("/{collection_id}/links", status_code=status.HTTP_204_NO_CONTENT)
async def remove_links_from_collection(
        collection_id: int,
        remove_links_from_col: RemoveLinksFromCollection,
        service: CollectionServiceDep,
        current_user: CurrentUserDep
):
    return await service.remove_links(current_user.id, collection_id, remove_links_from_col.link_ids)
