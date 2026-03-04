from typing import List

from fastapi import APIRouter, status, Query
from fastapi_versioning import VersionedFastAPI, version
from app.core.dependecies import PaginationDep
from app.link.entities import UpdateLinkEntity
from app.link.schemas import CreateLink, LinkWithCollections, Link, PatchLink
from app.link.dependencies import LinkServiceDep
from app.link.enums import LinkType
from app.auth.dependencies import CurrentUserDep
from fastapi_cache.decorator import cache



router = APIRouter(prefix="/links", tags=["links"])


@router.get("/type", response_model=List[Link])
@cache(expire=30)
async def list_by_type(
        service: LinkServiceDep,
        current_user: CurrentUserDep,
        pagination: PaginationDep,
        link_type: LinkType = Query(),
        ):
    return await service.list_by_type(
        current_user.id,
        link_type,
        pagination.skip,
        pagination.limit
    )




@router.post("", response_model=Link, status_code=status.HTTP_201_CREATED)
async def create_link(
        link: CreateLink,
        service: LinkServiceDep,
        current_user: CurrentUserDep
):
    return await service.create_link(current_user.id, str(link.url))


@router.get("", response_model=List[Link])
@cache(expire=30)
async def list_links(
        service: LinkServiceDep,
        current_user: CurrentUserDep,
        pagination: PaginationDep,
):
    return await service.list_links(current_user.id, pagination.skip, pagination.limit)


@router.get("/{link_id}", response_model=LinkWithCollections)
async def get_link(
        link_id: int,
        service: LinkServiceDep,
        current_user: CurrentUserDep
):
    return await service.get_link(current_user.id, link_id)


@router.patch("/{link_id}", response_model=Link)
async def patch_link(
        link_id: int,
        link: PatchLink,
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


# Поиск по домену
# GET /links/search?domain=github.com

# Последние добавленные
# GET /links/recent?limit=5

# Статистика
# GET /links/stats (количество по типам)
