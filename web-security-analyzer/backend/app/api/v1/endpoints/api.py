from fastapi import APIRouter
from app.api.v1 import scan

api_router = APIRouter()

# Incluir rotas de scan
api_router.include_router(scan.router, prefix="/scan", tags=["scan"])

@api_router.get("/")
async def api_info():
    return {
        "message": "Web Security Analyzer API v1",
        "endpoints": {
            "scan": "/scan",
            "health": "/health"
        }
    }