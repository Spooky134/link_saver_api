from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers import links
 
app = FastAPI(title="Link saver API")

app.include_router(links.router, prefix="/links", tags=["links"])
 
@app.get("/", summary="Root endpoint")
def root():
    return {
        "message": "Hello there",
        "endpoints": {
            "links": "/links",
        }
    }