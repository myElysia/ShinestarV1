from tortoise import fields
from tortoise.models import Model


class Base(Model):
    id = fields.IntField(pk=True)

    # 抽象类，不生成表数据
    class Meta:
        abstract = True


class WithTimeBase(Base):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        abstract = True


class User(WithTimeBase):
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255)
    display_name = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)

    def __str__(self):
        return self.username

    class Meta:
        table = "auth_user"

    class PydanticMeta:
        exclude = ("password",)

    def to_dict(self, use_password=False):
        data = {i: getattr(self, i) for i in self.__dict__ if not i.startswith('_')}
        if not use_password:
            del data['password']
        return data


class Role(Base):
    name = fields.CharField(max_length=50, unique=True)
    description = fields.CharField(max_length=255)

    class Meta:
        table = "auth_role"


class Permission(Base):
    code = fields.CharField(max_length=50, unique=True)
    description = fields.CharField(max_length=255)

    class Meta:
        table = "auth_permission"


class RolePermission(Base):
    role = fields.ForeignKeyField("models.Role", on_delete=fields.CASCADE, related_name="permissions")
    permission = fields.ForeignKeyField("models.Permission", on_delete=fields.CASCADE, related_name="roles")

    class Meta:
        table = "auth_role_permissions"
        unique_together = ("role_id", "permission_id")


class UserRole(Base):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, related_name="roles")
    role = fields.ForeignKeyField("models.Role", on_delete=fields.CASCADE, related_name="users")

    class Meta:
        table = "auth_role_users"
        unique_together = ("user_id", "role_id")
