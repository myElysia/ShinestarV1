from datetime import datetime, date

from pydantic import BaseModel, Field

from src.schemas.base import (
    BaseModelConfig,
    UserOut
)


class Project(BaseModel):
    project_key: str
    name: str
    description: str | None = ""
    leader: UserOut
    users: list[UserOut] = []


class ProjectOut(Project, BaseModelConfig):
    id: int


class ProjectUser(BaseModelConfig):
    project_id: int
    user_id: int
    readonly: bool


class IssueType(BaseModel):
    name: str
    description: str | None


class IssueTypeOut(IssueType, BaseModelConfig):
    id: int


class WorkflowStatus(BaseModel):
    name: str
    description: str | None


class WorkflowStatusOut(WorkflowStatus, BaseModelConfig):
    id: int


class Label(BaseModel):
    name: str
    description: str | None


class LabelOut(Label, BaseModelConfig):
    id: int


class IssueLabel(BaseModelConfig):
    id: int
    issue_id: int
    label_id: int


class Version(BaseModel):
    project: ProjectOut
    name: str
    description: str | None
    start_date: date
    release_date: date


class VersionOut(Version, BaseModelConfig):
    id: int


class IssueVersion(BaseModelConfig):
    id: int
    issue_id: int
    version_id: int


class Issue(BaseModel):
    key: str
    labels: list[LabelOut] = []
    versions: list[VersionOut] = []
    project: ProjectOut
    type: IssueTypeOut
    status: WorkflowStatusOut
    title: str
    description: str | None
    priority: str
    reporter: UserOut | None
    assignee: UserOut | None


class IssueOut(Issue, BaseModelConfig):
    id: int


class WorkFlowTranslation(BaseModel):
    from_status: WorkflowStatusOut
    to_status: WorkflowStatusOut
    project: ProjectOut


class WorkFlowTranslationOut(WorkFlowTranslation, BaseModelConfig):
    id: int


class CommentOut(BaseModelConfig):
    id: int
    issue: IssueOut
    user: UserOut
    content: str
    created_at: datetime
    replies: list["CommentOut"] = Field(default_factory=list)  # 延迟类型注解, 代表所有的回复

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }


# Pydantic V2 在所有模型定义完成后解析向前引用
CommentOut.model_rebuild()


class Attachment(BaseModel):
    issue: IssueOut
    user: UserOut
    filename: str
    filepath: str


class AttachmentOut(Attachment, BaseModelConfig):
    id: int
