from fastapi import APIRouter, HTTPException

from backend.src.views import register_router

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# 注册路由到总路由中
register_router(router)
