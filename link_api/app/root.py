from fastapi import APIRouter

router = APIRouter(tags=["root"])

@router.get("/root", summary="Root endpoint")
def root():
    return {
        "service": "Link storage API",
        "version": "1.0.0",
        "message": "Hello there",
        "endpoints": {
            "links": "/api/v1/links",
            "collections": "api/v1/collections",
            "auth": "/api/v1/auth"
        }
    }