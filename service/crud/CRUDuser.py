from service.models import User
from service.schemas.user import UserCreate
from service.schemas.token import RefreshToken
from service.core.security import *

from datetime import datetime


def get_user_by_email(db, inbound_data: UserCreate):
    db_data = db.query(User).filter(User.email == inbound_data.email).first()
    return db_data


def get_user_by_id(db, user_id: int):
    db_data = db.query(User).filter(User.id == user_id).first()
    return db_data


def create_user(db, inbound_data: UserCreate):
    obj = User(
        email    = inbound_data.email,
        password = get_hashed_password(inbound_data.password),
        created_at = datetime.today()
    )
    db.add(obj)
    return obj


def save_refresh_token(db, user_email: int, refresh_token: str):
    db_data = db.query(User).filter(User.email == user_email).update(
        values = {
            User.refresh_token : refresh_token
        }
    )
    return


def get_new_access_token(db, inbound_data: RefreshToken, user_id: int):
    user_obj = get_user_by_id(db, user_id)

    if inbound_data.refresh_token == user_obj.refresh_token:
        access_token = create_access_token(user_id=user_obj.id)
        return access_token
    else:
        return None


def logout(db, user_id: int):
    db_data = db.query(User).filter(User.id == user_id).update(
        values = {
            User.refresh_token : 0
        }
    )
    return