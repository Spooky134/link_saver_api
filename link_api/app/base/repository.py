from sqlalchemy import insert

from app.core.database import async_session_maker


class BaseRepository:
    model = None

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            obj = cls.model(**data)
            session.add(obj)
            await session.commit()


