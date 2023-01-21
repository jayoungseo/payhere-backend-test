from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from service.core.config import settings
from service.database import get_db
from service.router.depends import get_current_user
from service.models import User
from service.schemas.user import UserCreate, UserBase
from service.schemas.token import RefreshToken
from service.crud import CRUDuser
from service.core.security import verify_password, create_access_token, create_refresh_token

import jwt

router_login = APIRouter(
    prefix="",
    tags=["login"]
)


@router_login.post("/signup", response_model=UserBase)
def create_user(
    inbound_data: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = CRUDuser.get_user_by_email(db, inbound_data)
    # 회원가입 하려는 이메일이 이미 있는 경우
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    return_data = CRUDuser.create_user(db, inbound_data)
    return return_data


@router_login.post("/login")
def login_for_access_token(
    inbound_data: UserCreate,
    db: Session = Depends(get_db)
):
    user = CRUDuser.get_user_by_email(db, inbound_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong email or password")

    is_verified = verify_password(inbound_data.password, user.password)
    if not is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong email or password")

    access_token = create_access_token(user_id=user.id)
    refresh_token = create_refresh_token(user_id=user.id)
    CRUDuser.save_refresh_token(db, inbound_data.email, refresh_token)

    return_data = {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    return return_data


@router_login.post("/token")
def get_new_access_token(
    inbound_data: RefreshToken,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(inbound_data.refresh_token, settings.SECRET_KEY, algorithms=settings.SECURITY_ALGORITHM)
        new_access_token = CRUDuser.get_new_access_token(db, inbound_data, payload['user_id'])
        return_data = {"new_access_token": new_access_token}
        return return_data

    # refresh token 시간 만료 -> 로그인 필요, 새로 
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not certified")


@router_login.post("/logout")
def logout(
    curr_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    CRUDuser.logout(db, user_id=curr_user.id)
    return 

