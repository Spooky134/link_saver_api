from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api.routers import link, collection
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
# import asyncio
from contextlib import asynccontextmanager
from config.database import Base, engine, get_db
from config.project_config import settings

 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Приложение работает
    # (опционально) Очистка при завершении
    # await engine.dispose()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)



app.include_router(link.router, prefix="/v1")
app.include_router(collection.router, prefix="/v1")


@app.get("/v1", summary="Root endpoint")
def root():
    return {
        "service": "Link storage",
        "version": "1.0.0",
        "message": "Hello there",
        "endpoints": {
            "links": "/links",
            "collections": "/collections"
        }
    }


@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT 1")
    return {"status": "OK", "data": result.scalar()}