from fastapi import APIRouter, status, Query
from app.link.entities import LinkEntity
from app.link.schemas import LinkCreate, LinkResponse, LinkUpdate
from app.link.dependencies import LinkServiceDep
from app.auth.dependencies import get_current_user
from app.user.models import UserModel
from app.link.enums import LinkType


router = APIRouter(prefix="/links", tags=["links"])


@router.get("/type", response_model=list[LinkResponse])
async def get_links_by_type(service: LinkServiceDep, link_type: LinkType = Query(), skip: int = 0, limit: int = 10):
    return await service.get_links_by_type(link_type, skip, limit)


@router.post("/", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link(link_create: LinkCreate, service: LinkServiceDep):
    new_link = LinkEntity(**link_create.model_dump())
    return await service.create_link(new_link)


@router.get("/", response_model=list[LinkResponse])
async def get_all_links(service: LinkServiceDep, skip: int = 0, limit: int = 10):
    return await service.get_all_links(skip, limit)


@router.get("/{link_id}", response_model=LinkResponse)
async def get_link(link_id: int, service: LinkServiceDep): #, user: UserModel = Depends(get_current_user)):
    # print(user, type(user), user.email)
    return await service.get_link(link_id=link_id)


@router.patch("/{link_id}", response_model=LinkResponse)
async def partial_update_link(link_id: int, link_patch: LinkUpdate, service: LinkServiceDep):
    update_link = LinkEntity(**link_patch.model_dump())
    return await service.update_link(link_id, update_link)


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(link_id: int, service: LinkServiceDep):
    await service.delete_link(link_id)


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