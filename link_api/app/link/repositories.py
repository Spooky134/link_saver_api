from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select
from sqlalchemy.orm import selectinload
from app.link.models import LinkModel
from app.link.enums import LinkType
from app.base.repositories import BaseRepository
from app.link.entities import LinkEntity
from app.common.mappers import EntityMapper


class LinkRepository(BaseRepository[LinkModel, LinkEntity]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(
            model=LinkModel,
            entity=LinkEntity,
            async_session=async_session
        )

    def _to_entity(self, link_model: LinkModel) -> LinkEntity:
        return EntityMapper.to_link_entity(link_model)

    async def get_by_id_with_collections(self, link_id: int) -> Optional[LinkEntity]:
        query = (
            select(self.model)
            .options(selectinload(self.model.collections))
            .where(self.model.id==link_id)
        )
        res = await self.async_session.execute(query)
        res = res.scalar_one_or_none()
        return self._to_entity(res) if res else None

    async def get_all_with_collections(self, offset: int = 0, limit: int = 10) -> list[LinkEntity]:
        query = (
            select(self.model)
            .options(selectinload(self.model.collections))
            .offset(offset)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        res = [self._to_entity(m) for m in res.scalars().all()]
        return res

    async def get_all_by_type(self, link_type: LinkType = None, skip: int = 0, limit: int = 10) -> list[LinkEntity]:
        query = (
            select(self.model)
            .options(selectinload(self.model.collections))
            .where(self.model.link_type == link_type.value)
            .offset(skip)
            .limit(limit)
        )
        res = await self.async_session.execute(query)
        res = [self._to_entity(m) for m in res.scalars().all()]
        return res

    async def exists_by_url(self, url: str) -> bool:
        query = (
            select(exists().where(self.model.url == url))
        )
        result = await self.async_session.execute(query)
        return result.scalar() or False

    # TODO юзер не нужен
    async def update(self, link_id: int, link_entity: LinkEntity, _exclude: Optional[set[str]] = None) -> Optional[LinkEntity]:
        excluded_fields = {"url", "collections", "user_id"}
        if _exclude:
            excluded_fields.update(_exclude)
        link_updated = await super().update(link_id, link_entity, _exclude=excluded_fields)
        return link_updated