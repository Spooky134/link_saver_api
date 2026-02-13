from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select, update, delete
from sqlalchemy.orm import selectinload
from app.link.model import LinkModel
from app.collection.model import CollectionModel
from app.link.enum import LinkType


class LinkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, link_id: int) -> Optional[LinkModel]:
        query = (
            select(LinkModel)
            .options(selectinload(LinkModel.collections))
            .where(LinkModel.id==link_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, link_data: dict) -> LinkModel:
        new_link = LinkModel(**link_data)
        new_link.collections = []
        self.session.add(new_link)
        await self.session.commit()

        return await self.get(new_link.id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[LinkModel]:
        result = await self.session.execute(
            select(LinkModel).options(selectinload(LinkModel.collections)).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, link_id: int, data: dict, collections: Optional[list[CollectionModel]] = None) -> Optional[LinkModel]:
        link = await self.get(link_id=link_id)

        if collections is not None:
            link.collections = collections

        for field, value in data.items():
            setattr(link, field, value)

        link.time_update = datetime.now()
        await self.session.commit()

        return await self.get(link_id)

    async def delete(self, link_id: int) -> None:
        await self.session.execute(delete(LinkModel).where(LinkModel.id == link_id))
        await self.session.commit()

    async def exists_by_url(self, url: str) -> bool:
        return await self.session.scalar(select(exists()
                                                .where(LinkModel.url == url)))

    async def exists_by_id(self, link_id: int) -> bool:
        return await self.session.scalar(select(exists()
                                                .where(LinkModel.id == link_id)))

    async def get_by_type(self, link_type: Optional[LinkType] = None) -> list[LinkModel]:
        query = select(LinkModel).options(selectinload(LinkModel.collections))

        if link_type:
            query = query.where(LinkModel.link_type == link_type.value)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_by_ids(self, link_ids: list[int], load_collection: bool = False) -> list[LinkModel]:
        query = select(LinkModel).where(LinkModel.id.in_(link_ids))

        if load_collection:
            query = query.options(selectinload(LinkModel.collections))

        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_by_collection_id(self, collection_id: int, skip: int = 0, limit: int = 100) -> list[LinkModel]:
        result = await self.session.execute(
            select(LinkModel)
            .join(LinkModel.collections)
            .options(
                selectinload(LinkModel.collections)  # Жадная загрузка коллекций
            )
            .where(CollectionModel.id == collection_id)
            .offset(skip)
            .limit(limit)
        )

        return result.scalars().all()

    async def exists(self, *, url: Optional[str] = None, id: Optional[int] = None) -> bool:
        pass

    async def filter(self):
        pass