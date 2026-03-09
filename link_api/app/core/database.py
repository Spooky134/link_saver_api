from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from app.core.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.test_database.url
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.database.url
    DATABASE_PARAMS = {}



engine = create_async_engine(
    DATABASE_URL,
    # echo=True
    **DATABASE_PARAMS
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} ({', '.join(cols)})>"


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as db:
        yield db
