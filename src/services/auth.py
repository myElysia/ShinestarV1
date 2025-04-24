import os
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt

from src.models import User
from src.schemas.base import UserOut

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=30)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def create_access_token(data: dict) -> str:
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(username: str, password: str) -> UserOut | None:
    user = await User.get_or_none(username=username)
    if not user or not verify_password(password, user.password):
        return None
    return UserOut.model_validate(user)
