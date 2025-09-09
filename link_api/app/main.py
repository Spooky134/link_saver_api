import uvicorn
from fastapi import FastAPI, APIRouter

from app.config.project_config import settings
from app.config.migrations import lifespan
from app.api.routers import link, collection, auth, root

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


api_v1_router = APIRouter(prefix="/v1", tags=["v1"])


api_v1_router.include_router(root.router, tags=["root"])
api_v1_router.include_router(link.router, prefix="/links", tags=["links"])
api_v1_router.include_router(collection.router, prefix="/collections", tags=["collections"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])


app.include_router(api_v1_router, prefix="/api")



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)