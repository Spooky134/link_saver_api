import uvicorn
from fastapi import FastAPI, APIRouter
from sqladmin import Admin

from app.admin.views import LinkAdmin, CollectionAdmin
from app.core.database import engine

from app.config.project_config import settings
from app.core.lifespan import lifespan
from app.link.router import router as link_router
from app.collection.router import router as collection_router
from app.root import router as root_router

app = FastAPI(title=settings.SERVICE_NAME, lifespan=lifespan)


api_v1_router = APIRouter(prefix="/v1", tags=["v1"])


api_v1_router.include_router(root_router, tags=["root"])
api_v1_router.include_router(link_router)
api_v1_router.include_router(collection_router)
# api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])


app.include_router(api_v1_router, prefix="/api")

admin = Admin(app, engine)
admin.add_view(LinkAdmin)
admin.add_view(CollectionAdmin)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)