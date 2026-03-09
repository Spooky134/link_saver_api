import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from sqladmin import Admin
from app.admin.auth import authentication_backend
from app.auth.routers import router as auth_router
from app.collection.admin import CollectionAdmin
from app.collection.routers import router as collection_router
from app.core.config import settings
from app.core.database import engine
from app.core.lifespan import lifespan
from app.link.admin import LinkAdmin
from app.link.routers import router as link_router
from app.root import router as root_router
from app.user.admin import UserAdmin
from app.core.exceptions import BaseAppException
from app.user.routers import router as user_router
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title=settings.service.name,
    lifespan=lifespan,
    root_path="/api"
)


@app.exception_handler(BaseAppException)
async def app_exception_handler(_, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


v1_router = APIRouter(prefix="/v1")

v1_router.include_router(root_router)
v1_router.include_router(auth_router)
v1_router.include_router(user_router)
v1_router.include_router(link_router)
v1_router.include_router(collection_router)

app.include_router(v1_router)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(LinkAdmin)
admin.add_view(CollectionAdmin)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics", "^/v1/root$"]
)
instrumentator.instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
