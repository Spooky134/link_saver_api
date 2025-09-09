from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, func, select, update, delete
from sqlalchemy.orm import selectinload

from app.db.models.link import Link
from app.db.models.collection import Collection
from app.api.schemas.enums import LinkType
from app.db.models.link_collection import link_collection


#TODO collection.time_update = datetime.now() везде где изменения
class CollectionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get(self, collection_id: int) -> Optional[Collection]:
        result = await self.session.execute(select(Collection)
                                            .options(selectinload(Collection.links))  # Жадная загрузка ссылок
                                            .where(Collection.id == collection_id))
        
        return result.scalar_one_or_none()
    

    async def create(self, collection_data: dict, links: Optional[list[Link]] = None) -> Collection:
        new_collection = Collection(**collection_data)
        new_collection.links = links
        self.session.add(new_collection)
        await self.session.commit()

        return await self.get(collection_id=new_collection.id)
    

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Collection]:
        result = await self.session.execute(
            select(Collection).options(selectinload(Collection.links)).offset(skip).limit(limit))  # Жадная загрузка ссылок
        
        return result.scalars().all()


    async def update(self, collection_id: int, data: dict) -> Optional[Collection]:
        collection = self.get(collection_id=collection_id)

        for field, value in data.items():
            setattr(collection, field, value)

        collection.time_update = datetime.now()
        await self.session.commit()

        return self.get(collection_id)
    

    async def set_links_to_collection(self, collection_id: int, links: list[Link]):
        collection = await self.get(collection_id=collection_id)
        collection.links = links
        collection.time_update = datetime.now()

        await self.session.commit()


    async def add_links_to_collection(self, collection_id, links: list[Link]) -> None:
        collection = await self.get(collection_id=collection_id)

        existing_ids = {link.id for link in collection.links}
        collection.links.extend(
            link for link in links if link.id not in existing_ids
        )
        collection.time_update = datetime.now()

        await self.session.commit()


    async def delete(self, collection_id: int) -> None:
        await self.session.execute(delete(Collection).where(Collection.id==collection_id))
        await self.session.commit()


    async def exists_by_name(self, name: str) -> bool:
        return await self.session.scalar(select(exists()
                                                .where(Collection.name == name)))
    

    async def exists_by_id(self, collection_id: int) -> bool:
        return await self.session.scalar(select(exists()
                                                .where(Collection.id == collection_id)))
    

    async def get_by_ids(self, collection_ids: list[int], load_links: bool = False) -> list[Collection]:
        query = select(Collection).where(Collection.id.in_(collection_ids))

        if load_links:
            query = query.options(selectinload(Collection.links))
        
        result = await self.session.execute(query)

        return result.scalars().all()
    

    async def get_count_links(self, collection_id: int) -> int:
        count = await self.session.execute(select(func.count())
                                            .select_from(link_collection)
                                            .where(link_collection.c.collection_id == collection_id))
        
        return count or 0


    async def remove_link_from_collection(self, collection_id: int, link_id: int) -> bool:
        result = await self.session.execute(delete(link_collection)
                                            .where((link_collection.c.collection_id == collection_id) & 
                                                   (link_collection.c.link_id == link_id)))
        await self.session.commit()
        
        return result.rowcount > 0
    

    async def search_by_name(self, name_query: str, limit: int = 20) -> list[Collection]:
        result = await self.session.execute(select(Collection)
                                            .options(selectinload(Collection.links))
                                            .where(Collection.name.ilike(f"%{name_query}%"))
                                            .limit(limit))
    
        return result.scalars().all()