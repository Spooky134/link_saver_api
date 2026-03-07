from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from redis import asyncio as aioredis
from app.config.logging import setup_logging
from app.core.database import engine
from app.config.project_config import settings



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging()

    redis = aioredis.from_url(settings.cache_url)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

    yield

    await engine.dispose()