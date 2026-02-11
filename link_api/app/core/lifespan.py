from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.logging import setup_logging
from app.core.database import Base, engine
from app.link.model import Link, link_collection
from app.collection.model import Collection

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()