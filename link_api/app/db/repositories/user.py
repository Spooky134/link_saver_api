from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select, update, delete
from sqlalchemy.orm import selectinload

from app.db.models.user import User
from app.db.models.collection import Collection
from app.api.schemas.enums import LinkType


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id))
        
        return result.scalar_one_or_none()
    
    
    async def create(self, user_data: dict) -> User:
        new_user = User(email=user_data["email"],
                        hashed_password=user_data["hashed_password"])
    
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user
    
    async def exists_by_email(self, email: str) -> bool:
        return await self.session.scalar(select(exists()
                                                .where(User.email == email)))


    # async def update(self, link_id: int, data: dict, collections: Optional[list[Collection]] = None) -> Link | None:
    #     link = await self.get(link_id=link_id)
    
    #     if collections is not None:
    #         link.collections = collections

    #     for field, value in data.items():
    #         setattr(link, field, value)

    #     link.time_update = datetime.now()
    #     await self.session.commit()

    #     return await self.get(link_id)


    # async def delete(self, link_id: int) -> None:
    #     await self.session.execute(delete(Link).where(Link.id==link_id))
    #     await self.session.commit()
    

    
