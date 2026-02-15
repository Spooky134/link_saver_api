from fastapi import Depends, APIRouter, HTTPException, status, Query
from app.link.entity import LinkEntity
from app.link.schema import LinkCreate, LinkResponse, LinkUpdate
from app.link.service import LinkService
from app.dependencies import service_factory
from app.exceptions import ValidationError, NotFoundError
from app.auth.dependencie import get_current_user
from app.user.model import UserModel
from app.link.enum import LinkType



router = APIRouter(prefix="/links", tags=["links"])


@router.get("/type", response_model=list[LinkResponse])
async def get_links_by_type(link_type: LinkType = Query(None),
                            service: LinkService = Depends(service_factory(LinkService))):
    return await service.get_links_by_type(link_type)

@router.post("/", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link(link_create: LinkCreate,
                      service: LinkService = Depends(service_factory(LinkService))):
    try:
        new_link = LinkEntity(**link_create.model_dump())
        return await service.create_link(new_link)
    except ValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=list[LinkResponse])
async def get_all_links(service: LinkService = Depends(service_factory(LinkService))):
    return await service.get_all_links()


@router.get("/{link_id}", response_model=LinkResponse)
async def get_link(link_id: int, service: LinkService = Depends(service_factory(LinkService))): #, user: UserModel = Depends(get_current_user)):
    try:
        # print(user, type(user), user.email)
        return await service.get_link(link_id=link_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.patch("/{link_id}", response_model=LinkResponse)
async def partial_update_link(
        link_id:int,
        link_patch: LinkUpdate,
        service: LinkService = Depends(service_factory(LinkService))):
    try:
        update_link = LinkEntity(**link_patch.model_dump())
        return await service.update_link(link_id, update_link)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
        link_id: int,
        service: LinkService = Depends(service_factory(LinkService))):
    try:
        await service.delete_link(link_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


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