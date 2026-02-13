import uvicorn
from fastapi import APIRouter, FastAPI
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.auth.router import router as auth_router
from app.collection.admin import CollectionAdmin
from app.collection.router import router as collection_router
from app.config.project_config import settings
from app.core.database import async_session_maker, engine
from app.core.lifespan import lifespan
from app.link.admin import LinkAdmin
from app.link.router import router as link_router
from app.root import router as root_router
from app.user.admin import UserAdmin

app = FastAPI(title=settings.SERVICE_NAME, lifespan=lifespan)

api_v1_router = APIRouter(prefix="/v1", tags=["v1"])

api_v1_router.include_router(root_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(link_router)
api_v1_router.include_router(collection_router)

app.include_router(api_v1_router, prefix="/api")

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(LinkAdmin)
admin.add_view(CollectionAdmin)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
