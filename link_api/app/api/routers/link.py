from fastapi import Depends, APIRouter, HTTPException, status, Query
from typing import Optional

from app.api.schemas.link import LinkCreate, LinkResponse, LinkUpdate
from app.services.link import LinkService
from app.api.dependencies import service_factory
from app.exceptions.exceptions import ValidationError, NotFoundError


router = APIRouter(prefix="/links", tags=["links"])


@router.get("/{link_id}", response_model=LinkResponse)
async def read_link(link_id: int, service: LinkService = Depends(service_factory(LinkService))):
    try:
        return await service.get_link(link_id=link_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.patch("/{link_id}", response_model=LinkResponse)
async def partial_update_link(link_id:int,
                      link_patch: LinkUpdate,
                      service: LinkService = Depends(service_factory(LinkService))):
    try:
        return await service.update_link(link_id=link_id, data=link_patch)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(link_id: int,
                      service: LinkService = Depends(service_factory(LinkService))):
    try:
        await service.delete_link(link_id=link_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/", response_model=list[LinkResponse])
async def get_links_by_type(link_type: Optional[str] = Query(None),
                            service: LinkService = Depends(service_factory(LinkService))):
    return await service.get_filtered_links(type_str=link_type) 


@router.get("/", response_model=list[LinkResponse])
async def read_links(service: LinkService = Depends(service_factory(LinkService))):
    return await service.get_links()


@router.post("/", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link(link_create: LinkCreate,
                      service: LinkService = Depends(service_factory(LinkService))):
    try:
        return await service.create_link(link_data=link_create)
    except ValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



# Для ссылок:
# Фильтрация по типу
# GET /links?type=article

# Поиск по домену
# GET /links/search?domain=github.com

# Последние добавленные
# GET /links/recent?limit=5

# Статистика
# GET /links/stats (количество по типам)

# Общие:
# Массовое удаление
# POST /batch-delete (тело: {"ids": [1,2,3]})

# Проверка существования URL
# GET /links/exists?url=...