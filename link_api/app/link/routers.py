from fastapi import APIRouter, status, Query
from app.link.entities import LinkEntity, UpdateLinkEntity
from app.link.schemas import CreateLink, LinkWithCollections, Link, UpdateLink
from app.link.dependencies import LinkServiceDep
from app.link.enums import LinkType
from app.auth.dependencies import CurrentUserDep



router = APIRouter(prefix="/links", tags=["links"])


@router.get("/type", response_model=list[Link])
async def get_links_by_type(
        service: LinkServiceDep,
        current_user: CurrentUserDep,
        link_type: LinkType = Query(), skip: int = 0, limit: int = 10):
    return await service.get_links_by_type(current_user.id, link_type, skip, limit)


@router.post("/", response_model=Link, status_code=status.HTTP_201_CREATED)
async def create_link(
        link: CreateLink,
        service: LinkServiceDep,
        current_user: CurrentUserDep
):
    return await service.create_link(current_user.id, str(link.url))


@router.get("/", response_model=list[Link])
async def get_all_links(
        service: LinkServiceDep,
        current_user: CurrentUserDep,
        skip: int = 0, limit: int = 10
):
    return await service.get_all_links(current_user.id, skip, limit)


@router.get("/{link_id}", response_model=LinkWithCollections)
async def get_link(
        link_id: int,
        service: LinkServiceDep,
        current_user: CurrentUserDep
):
    return await service.get_link(current_user.id, link_id)


@router.patch("/{link_id}", response_model=Link)
async def update_link_partial(
        link_id: int,
        link: UpdateLink,
        service: LinkServiceDep,
        current_user: CurrentUserDep
):
    update_link = UpdateLinkEntity(**link.model_dump(exclude_unset=True))
    return await service.update_link(current_user.id, link_id, update_link)


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
        link_id: int,
        service: LinkServiceDep,
        current_user: CurrentUserDep
):
    await service.delete_link(current_user.id, link_id)


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