from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Приложение работает
    # (опционально) Очистка при завершении
    # await engine.dispose()