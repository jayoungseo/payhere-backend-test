from datetime import datetime, timedelta
from passlib.context import CryptContext

from .config import settings

import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: int):
    expires = datetime.today() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRATION)
    payload = {"exp": expires, "user_id": user_id}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: str):
    expires = datetime.today() + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRATION)
    payload = {"exp": expires, "user_id": str(user_id)}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def get_hashed_password(password: str):
    return pwd_context.hash(password)