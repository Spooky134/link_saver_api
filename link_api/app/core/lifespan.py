from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.core import broker
from app.core.config import settings
from app.core.database import engine
from app.core.logging import get_logger, setup_logging

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
