from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers import link, collection
from fastapi import FastAPI, Depends, HTTPException
from app.db.database import Base, engine
import asyncio
from contextlib import asynccontextmanager

 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Приложение работает
    # (опционально) Очистка при завершении
    # await engine.dispose()


app = FastAPI(title="Link saver API", lifespan=lifespan)



app.include_router(link.router, prefix="/links", tags=["links"])
app.include_router(collection.router, prefix="/collections", tags=["collections"])


@app.get("/", summary="Root endpoint")
def root():
    return {
        "message": "Hello there",
        "endpoints": {
            "links": "/links",
            "collections": "/collections"
        }
    }