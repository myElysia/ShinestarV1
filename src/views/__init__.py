from fastapi import APIRouter

from src.views.jira import router as jira_router

router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
)

router.include_router(jira_router)
