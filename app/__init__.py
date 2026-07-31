from fastapi import APIRouter
from app.routes import router

apps_router = APIRouter(prefix="/api/v1")

apps_router.include_router(router)