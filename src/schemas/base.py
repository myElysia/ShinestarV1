from pydantic import (
    BaseModel,
    field_validator,
    SecretStr, EmailStr
)

from src.config.mail import (
    SELF_DOMAINS,
    MAIL_DOMAINS,
)
from src.utils.security import validate_password

mail_domains = MAIL_DOMAINS + SELF_DOMAINS
TOKEN_TYPE = 'Bearer'


class BaseModelConfig(BaseModel):
    class Config:
        from_attributes = True  # Pydantic v2 新语法, 允许转换orm


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = TOKEN_TYPE


class UserLogin(BaseModel):
    email: EmailStr | None
    username: str
    password: str


class UserWriten(BaseModelConfig):
    id: int | None
    username: str
    email: EmailStr
    password: SecretStr  # 安全封装密码
    display_name: str

    @field_validator('email')
    def validate_email(cls, value: str):
        mail_name, mail_domain = value.rsplit('@', 1)
        if mail_domain.lower() not in mail_domains:
            raise ValueError('Invalid email address')
        return value

    @field_validator('password')
    def validate_password(cls, value: SecretStr):
        password = value.get_secret_value()
        validate_password(password)
        return value


class User(BaseModel):
    username: str
    email: str
    display_name: str


class Role(BaseModel):
    name: str
    description: str | None = ""


class UserRole(BaseModelConfig):
    user_id: int
    role_id: int


class Permission(BaseModel):
    name: str
    description: str | None = ""


class RolePermission(BaseModelConfig):
    role_id: int
    permission_id: int


class PermissionOut(Permission, BaseModelConfig):
    id: int


class RoleOut(Role, BaseModelConfig):
    id: int
    permissions: list[PermissionOut] = []  # 嵌套权限层


class UserOut(User, BaseModelConfig):
    id: int
    roles: list[RoleOut] = []
