from tortoise import fields
from src.models import WithTimeBase, Base

MODEL_NAME = "jira"
MAX_DEPTH = 3


class Project(WithTimeBase):
    project_key = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField()
    leader = fields.ForeignKeyField("models.User", related_name="lea_projects", on_delete=fields.SET_NULL, null=True)

    class Meta:
        table = f"{MODEL_NAME}_project"


class ProjectUser(Base):
    project = fields.ForeignKeyField("models.Project", related_name="users", on_delete=fields.CASCADE)
    user = fields.ForeignKeyField("models.User", related_name="projects", on_delete=fields.CASCADE)
    readonly = fields.BooleanField(default=False)

    class Meta:
        table = f"{MODEL_NAME}_project_user"
        unique_together = ("project_id", "user_id")


class IssueType(WithTimeBase):
    # 问题类型表
    name = fields.CharField(max_length=50, unique=True)
    description = fields.TextField()

    class Meta:
        table = f"{MODEL_NAME}_issue_type"


class WorkflowStatus(WithTimeBase):
    # 工作流状态
    name = fields.CharField(max_length=50, unique=True)
    description = fields.TextField()
    is_initial = fields.BooleanField(default=False)

    class Meta:
        table = f"{MODEL_NAME}_workflow_status"


class Issue(WithTimeBase):
    # 问题表
    key = fields.CharField(max_length=20, unique=True)
    project = fields.ForeignKeyField("models.Project", related_name="issues", on_delete=fields.CASCADE)
    type = fields.ForeignKeyField("models.IssueType", related_name="issues", on_delete=fields.CASCADE)
    status = fields.ForeignKeyField("models.WorkflowStatus", related_name="issues", on_delete=fields.CASCADE)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    priority = fields.CharField(max_length=10, choices=["Low", "Medium", "High", "Critical"])
    # 谁提的, 允许为空，人走单还在
    reporter = fields.ForeignKeyField("models.User", related_name="reporter_issues", on_delete=fields.SET_NULL,
                                      null=True)
    # 给谁的, 允许为空
    assignee = fields.ForeignKeyField("models.User", related_name="assignee_issues", on_delete=fields.SET_NULL,
                                      null=True)

    class Meta:
        table = f"{MODEL_NAME}_issue"
        # 联合索引
        indexes = [
            ('project_id', 'status'),
            ('assignee_id',),
        ]


class WorkFlowTranslation(Base):
    from_status = fields.ForeignKeyField("models.WorkflowStatus", related_name="outgoing_translations",
                                         on_delete=fields.CASCADE)
    to_status = fields.ForeignKeyField("models.WorkflowStatus", related_name="incoming_translations",
                                       on_delete=fields.CASCADE)
    project = fields.ForeignKeyField("models.Project", related_name="workflow_translations", on_delete=fields.CASCADE)

    # required_permission = fields.CharField(max_length=50) # 精细化操作权限，本次不需要

    class Meta:
        table = f"{MODEL_NAME}_workflow_translation"


class Comment(WithTimeBase):
    # 评论表
    issue = fields.ForeignKeyField("models.Issue", related_name="comments", on_delete=fields.CASCADE)
    user = fields.ForeignKeyField("models.User", related_name="comments", on_delete=fields.SET_NULL, null=True)
    # 评论支持嵌套回复, 类似B站的嵌套类型, 一个顶层以及多个子层
    root = fields.ForeignKeyField("models.Comment", related_name="descendants", on_delete=fields.CASCADE, null=True)
    parent = fields.ForeignKeyField("models.Comment", related_name="replies", on_delete=fields.CASCADE, null=True)
    content = fields.TextField()
    replace_count = fields.IntField(default=0)

    class Meta:
        table = f"{MODEL_NAME}_issue_commends"
        # 加速顶层评论和按Issue查询
        indexes = [
            ('root_id',),
            ('issue_id',),
        ]


class Attachment(WithTimeBase):
    # 附件表，用于问题本身
    issue = fields.ForeignKeyField("models.Issue", related_name="attachments", on_delete=fields.CASCADE)
    user = fields.ForeignKeyField("models.User", related_name="attachments", on_delete=fields.CASCADE)
    filename = fields.CharField(max_length=255)
    filepath = fields.CharField(max_length=255)

    class Meta:
        table = f"{MODEL_NAME}_issue_attachments"


class Label(Base):
    name = fields.CharField(max_length=100)
    description = fields.TextField()

    class Meta:
        table = f"{MODEL_NAME}_label"


class IssueLabel(Base):
    # 问题和标签的关联表
    issue = fields.ForeignKeyField("models.Issue", related_name="labels", on_delete=fields.SET_NULL, null=True)
    label = fields.ForeignKeyField("models.Label", related_name='issues', on_delete=fields.SET_NULL, null=True)

    class Meta:
        table = f"{MODEL_NAME}_issue_label"
        unique_together = (("issue_id", "label_id"),)


class Version(Base):
    project = fields.ForeignKeyField("models.Project", related_name="versions", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=100)
    description = fields.TextField()
    start_date = fields.DateField()
    release_date = fields.DateField()

    class Meta:
        table = f"{MODEL_NAME}_version"


class IssueVersion(Base):
    issue = fields.ForeignKeyField("models.Issue", related_name="versions", on_delete=fields.CASCADE)
    version = fields.ForeignKeyField("models.Version", related_name="issues", on_delete=fields.CASCADE)

    class Meta:
        table = f"{MODEL_NAME}_issue_version"
        unique_together = (("issue_id", "version_id"),)
