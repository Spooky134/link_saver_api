import os

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


os.environ["MODE"] = "TEST"

import asyncio
import json

import pytest
from sqlalchemy import insert, text

from app.core.database import Base, async_session_maker, engine
from app.config.project_config import settings
from app.link.models import LinkModel, link_collection
from app.collection.models import CollectionModel
from app.user.models import UserModel

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport, Cookies
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
def init_cache():
    FastAPICache.init(InMemoryBackend(), prefix="test-cache")
    yield
    FastAPICache.reset()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    assert "test" in engine.url.database.lower()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mock_data/mock_{model}.json", encoding="utf-8") as f:
            return json.load(f)

    users = open_mock_json("users")
    links = open_mock_json("links")
    collections = open_mock_json("collections")
    link_coll = open_mock_json("link_collection")

    from datetime import datetime
    from typing import Iterable

    DATETIME_FIELDS = {"created_at", "updated_at"}

    def convert_datetime_fields(items: Iterable[dict]) -> list[dict]:
        converted = []
        for item in items:
            new_item = item.copy()
            for field in DATETIME_FIELDS:
                value = new_item.get(field)
                if isinstance(value, str):
                    new_item[field] = datetime.fromisoformat(value)

            converted.append(new_item)
        return converted

    users = convert_datetime_fields(users)
    collections = convert_datetime_fields(collections)
    links = convert_datetime_fields(links)

    async with async_session_maker() as session:
        add_users = insert(UserModel).values(users)
        add_links = insert(LinkModel).values(links)
        add_collections = insert(CollectionModel).values(collections)
        add_link_collection = insert(link_collection).values(link_coll)

        await session.execute(add_users)
        await session.execute(add_links)
        await session.execute(add_collections)
        await session.execute(add_link_collection)

        tables = ["user", "link", "collection"]

        for table in tables:
            result = await session.execute(
                text(f'SELECT COALESCE(MAX(id), 0) FROM "{table}"')
            )
            max_id = result.scalar()

            await session.execute(
                text(f"SELECT setval('{table}_id_seq', {max_id})")
            )

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def authenticated_async_client():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        await ac.post("/v1/auth/login", json={
            "email": "alice.smith@example.com", "password": "test"
        })
        assert ac.cookies["access_token"]
        yield ac

@pytest.fixture(scope="function")
async def db_session():
    async with async_session_maker() as session:
        yield session