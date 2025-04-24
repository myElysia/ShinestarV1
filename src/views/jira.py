from typing import List
from fastapi import APIRouter
from tortoise.transactions import atomic

from src.schemas.jira import IssueOut

router = APIRouter(
    prefix="/jira",
)


@router.get("/issues", response_model=List[IssueOut])
async def get_all_issues():
    pass


@router.get("/issues/{issue_id}", response_model=IssueOut)
async def get_one_issue(issue_id: int):
    pass


@router.post("/issues", response_model=IssueOut)
@atomic()  # 事务保护
async def create_issue(issue: IssueOut):
    pass


@router.put("/issues/{issue_id}", response_model=IssueOut)
@atomic()
async def update_issue(issue: IssueOut):
    pass


@router.delete("/issues/{issue_id}", response_model=IssueOut)
@atomic()
async def delete_issue(issue_id: int):
    pass
