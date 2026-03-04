from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from redis import asyncio as aioredis
from app.config.logging import setup_logging
from app.core.database import Base, engine
from app.config.project_config import settings
from app.link.models import LinkModel, link_collection
from app.collection.models import CollectionModel
from app.user.models import UserModel



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging()

    redis = aioredis.from_url(settings.cache_url)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()