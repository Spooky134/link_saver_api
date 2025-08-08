from fastapi import APIRouter, HTTPException, status
from app.api.schemas.collection import CollectionResponse, CollectionCreate, CollectionUpdate, CollectionUpdateFull, CollectionLinkRequest
from fastapi import Depends, Query
from app.api.schemas.link import LinkResponse
from app.exceptions.exceptions import ValidationError, NotFoundError
from app.services.collection_service import CollectionService
from app.api.dependencies import service_factory


router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("/search/", response_model=list[CollectionResponse])
async def search_collection(name: str = Query(..., min_length=1, example="String"),
                            service: CollectionService = Depends(service_factory(CollectionService))):
    return await service.search_by_name(query_string=name)


@router.get("/{collection_id}/count",response_model=dict)
async def get_links_count(collection_id: int,
                          service: CollectionService = Depends(service_factory(CollectionService))):
    try:
        return await service.links_count(collection_id=collection_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{collection_id}/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_link_from_collection(collection_id: int,
                                      link_id: int,
                                      service: CollectionService = Depends(service_factory(CollectionService))):
    try:
        return await service.remove_link(collection_id=collection_id, link_id=link_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/{collection_id}/links", response_model=list[LinkResponse])
async def get_collection_links(collection_id: int,
                               service: CollectionService = Depends(service_factory(CollectionService))):
    try:
        return await service.get_links(collection_id=collection_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/{collection_id}/links", response_model=list[LinkResponse])
async def add_links_to_collection(collection_id: int,
                                  request: CollectionLinkRequest,
                                  service: CollectionService = Depends(service_factory(CollectionService))):
    try:
        return await service.add_links(collection_id=collection_id, data=request)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/{collection_id}", response_model=CollectionResponse)
async def read_collection(collection_id: int,
                          service: CollectionService = Depends(service_factory(CollectionService))):
    try:
        return await service.get_collection(collection_id=collection_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.status_code)
    

@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(collection_id: int,
                            service: CollectionService = Depends(service_factory(CollectionService))):
    try:
        await service.delete_collection(collection_id=collection_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.patch("/{collection_id}", response_model=CollectionResponse)
async def update_collection(collection_id: int,
                            collection_update: CollectionUpdate,
                            service: CollectionService = Depends(service_factory(CollectionService))):
    try:
        return await service.update_collection(collection_id=collection_id,
                                               data=collection_update)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/{collection_id}", response_model=CollectionResponse)
async def update_collection(collection_id: int,
                            collection_update: CollectionUpdateFull,
                            service: CollectionService = Depends(service_factory(CollectionService))):
    try:
        return await service.update_collection(collection_id=collection_id, data=collection_update, replace=True)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    

@router.get("/", response_model=list[CollectionResponse])
async def read_collections(service: CollectionService = Depends(service_factory(CollectionService))):
    
    return await service.get_collections()


@router.post("/", response_model=CollectionResponse, status_code=201)
async def create_collection(collection: CollectionCreate,
                            service: CollectionService = Depends(service_factory(CollectionService))):
    try:
        return await service.create_collection(data=collection)
    except ValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)