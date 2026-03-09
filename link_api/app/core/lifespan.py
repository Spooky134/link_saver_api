from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from redis import asyncio as aioredis
from app.core.logging import setup_logging, get_logger
from app.core import broker
from app.core.database import engine
from app.core.config import settings

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging()

    redis = aioredis.from_url(settings.cache.url)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    if not broker.is_worker_process:
        await broker.startup()

    yield
    if not broker.is_worker_process:
        await broker.shutdown()

    await engine.dispose()