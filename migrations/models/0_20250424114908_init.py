from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "blog_article" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS "jira_issue_type" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "name" VARCHAR(50) NOT NULL UNIQUE,
    "description" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "jira_label" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code" VARCHAR(50) NOT NULL UNIQUE,
    "description" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "auth_role" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE,
    "description" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "auth_role_permissions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "permission_id" INT NOT NULL REFERENCES "auth_permission" ("id") ON DELETE CASCADE,
    "role_id" INT NOT NULL REFERENCES "auth_role" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_auth_role_p_role_id_03dfd5" UNIQUE ("role_id", "permission_id")
);
CREATE TABLE IF NOT EXISTS "auth_user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "display_name" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True
);
CREATE TABLE IF NOT EXISTS "jira_project" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "project_key" VARCHAR(20) NOT NULL UNIQUE,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "leader_id" INT REFERENCES "auth_user" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "jira_project_user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "readonly" BOOL NOT NULL DEFAULT False,
    "project_id" INT NOT NULL REFERENCES "jira_project" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "auth_user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_jira_projec_project_81cc2d" UNIQUE ("project_id", "user_id")
);
CREATE TABLE IF NOT EXISTS "auth_role_users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "role_id" INT NOT NULL REFERENCES "auth_role" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "auth_user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_auth_role_u_user_id_6d4ba5" UNIQUE ("user_id", "role_id")
);
CREATE TABLE IF NOT EXISTS "jira_version" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "start_date" DATE NOT NULL,
    "release_date" DATE NOT NULL,
    "project_id" INT NOT NULL REFERENCES "jira_project" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "jira_workflow_status" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "name" VARCHAR(50) NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "is_initial" BOOL NOT NULL DEFAULT False
);
CREATE TABLE IF NOT EXISTS "jira_issue" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "key" VARCHAR(20) NOT NULL UNIQUE,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "priority" VARCHAR(10) NOT NULL,
    "assignee_id" INT REFERENCES "auth_user" ("id") ON DELETE SET NULL,
    "project_id" INT NOT NULL REFERENCES "jira_project" ("id") ON DELETE CASCADE,
    "reporter_id" INT REFERENCES "auth_user" ("id") ON DELETE SET NULL,
    "status_id" INT NOT NULL REFERENCES "jira_workflow_status" ("id") ON DELETE CASCADE,
    "type_id" INT NOT NULL REFERENCES "jira_issue_type" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_jira_issue_project_0414fc" ON "jira_issue" ("project_id", "status_id");
CREATE INDEX IF NOT EXISTS "idx_jira_issue_assigne_a2fd17" ON "jira_issue" ("assignee_id");
CREATE TABLE IF NOT EXISTS "jira_issue_attachments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "filename" VARCHAR(255) NOT NULL,
    "filepath" VARCHAR(255) NOT NULL,
    "issue_id" INT NOT NULL REFERENCES "jira_issue" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "auth_user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "jira_issue_commends" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ,
    "content" TEXT NOT NULL,
    "replace_count" INT NOT NULL DEFAULT 0,
    "issue_id" INT NOT NULL REFERENCES "jira_issue" ("id") ON DELETE CASCADE,
    "parent_id" INT REFERENCES "jira_issue_commends" ("id") ON DELETE CASCADE,
    "root_id" INT REFERENCES "jira_issue_commends" ("id") ON DELETE CASCADE,
    "user_id" INT REFERENCES "auth_user" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_jira_issue__root_id_b29748" ON "jira_issue_commends" ("root_id");
CREATE INDEX IF NOT EXISTS "idx_jira_issue__issue_i_f2150c" ON "jira_issue_commends" ("issue_id");
CREATE TABLE IF NOT EXISTS "jira_issue_label" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "issue_id" INT REFERENCES "jira_issue" ("id") ON DELETE SET NULL,
    "label_id" INT REFERENCES "jira_label" ("id") ON DELETE SET NULL,
    CONSTRAINT "uid_jira_issue__issue_i_10dfd1" UNIQUE ("issue_id", "label_id")
);
CREATE TABLE IF NOT EXISTS "jira_issue_version" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "issue_id" INT NOT NULL REFERENCES "jira_issue" ("id") ON DELETE CASCADE,
    "version_id" INT NOT NULL REFERENCES "jira_version" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_jira_issue__issue_i_6901ab" UNIQUE ("issue_id", "version_id")
);
CREATE TABLE IF NOT EXISTS "jira_workflow_translation" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "from_status_id" INT NOT NULL REFERENCES "jira_workflow_status" ("id") ON DELETE CASCADE,
    "project_id" INT NOT NULL REFERENCES "jira_project" ("id") ON DELETE CASCADE,
    "to_status_id" INT NOT NULL REFERENCES "jira_workflow_status" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
