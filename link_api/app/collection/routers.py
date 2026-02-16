from fastapi import Query, APIRouter, status

from app.collection.entities import CollectionEntity
from app.collection.schemas import (
    CollectionResponse,
    CollectionCreate,
    CollectionUpdatePUT,
    CollectionUpdatePATCH,
    CollectionLinkRequest
)
from app.link.schemas import LinkResponse
from app.collection.dependencies import CollectionServiceDep

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("/search/", response_model=list[CollectionResponse])
async def search_collection(
        service: CollectionServiceDep,
        name: str = Query(..., min_length=1, example="String"),
        skip: int = 0, limit: int = 10
):
    return await service.search_by_name(name, skip=skip, limit=limit)


@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
async def create_collection(collection_create: CollectionCreate, service: CollectionServiceDep):
    new_collection = CollectionEntity(**collection_create.model_dump())
    return await service.create_collection(new_collection)


@router.get("/", response_model=list[CollectionResponse])
async def get_all_collections(service: CollectionServiceDep, skip: int = 0, limit: int = 10):
    return await service.get_all_collections(skip, limit)


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(collection_id: int, service: CollectionServiceDep):
    return await service.get_collection(collection_id)


@router.put("/{collection_id}", response_model=CollectionResponse)
async def update_collection_full(
        collection_id: int,
        collection_update: CollectionUpdatePUT,
        service: CollectionServiceDep
):
    collection_update = CollectionEntity(**collection_update.model_dump())
    return await service.update_collection(collection_id, collection_update)


@router.patch("/{collection_id}", response_model=CollectionResponse)
async def update_collection_partial(
        collection_id: int,
        collection_update: CollectionUpdatePATCH,
        service: CollectionServiceDep
):
    collection_update = CollectionEntity(**collection_update.model_dump())
    return await service.update_collection(collection_id, collection_update)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(collection_id: int, service: CollectionServiceDep):
    await service.delete_collection(collection_id)


@router.get("/{collection_id}/count", response_model=dict)
async def get_links_count(
        collection_id: int,
        service: CollectionServiceDep
):
    return await service.links_count(collection_id)


@router.post("/{collection_id}/links", response_model=list[LinkResponse])
async def add_links_to_collection(
        collection_id: int,
        request: CollectionLinkRequest,
        service: CollectionServiceDep
):
    return await service.add_links(collection_id=collection_id, data=request)


@router.get("/{collection_id}/links", response_model=list[LinkResponse])
async def get_collection_links(collection_id: int, service: CollectionServiceDep):
    return await service.get_links(collection_id=collection_id)


@router.delete("/{collection_id}/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_link_from_collection(
        collection_id: int,
        link_id: int,
        service: CollectionServiceDep
):
    return await service.remove_link(collection_id, link_id)
