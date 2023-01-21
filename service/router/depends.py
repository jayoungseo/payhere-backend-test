from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from service.database import get_db
from service.core.config import settings
from service.crud import CRUDuser

import jwt

"""
########### 나중에 리드미 작성하기
docs에서 인증하기 위해서 username, password 입력하는 것 중 username에 특수문자가 들어간 이메일을 넣을수 없음
-> 그러나 제대로 작동 되는 코드임, curl 통신으로 토큰 넣어서 테스트 하면 테스트 잘 됨
###########
"""



oauth2 = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.SECURITY_ALGORITHM)
    # 토큰 시간 만료
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Expired access token")
    # 그 외 토큰 에러
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not certified")

    user = CRUDuser.get_user_by_id(db, user_id=payload['user_id'])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 로그아웃 상태
    if user.refresh_token == '0':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")

    return user