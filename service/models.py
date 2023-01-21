from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, BigInteger, String, Date, DateTime, Boolean

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    email = Column(String(255), unique=True, index=True, nullable=False) # 이메일
    password = Column(String(255), nullable=False) # 비밀번호
    created_at = Column(DateTime, nullable=False) # 계정 생성 날짜/시간
    refresh_token = Column(String(255), nullable=False, default=0) # refresh token


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False) # 유저 고유의 id
    use_date = Column(Date, nullable=False) # 돈 사용 날짜
    amount = Column(Integer, nullable=False) # 사용한 돈
    memo = Column(String(255), nullable=True) # 관련 메모
    created_at = Column(DateTime, nullable=False) # 가계부 작성 날짜/시간
    updated_at = Column(DateTime, nullable=True) # 가계부 내용 수정 날짜/시간
    is_deleted = Column(Boolean, nullable=False, default=0) # 삭제 여부 (1:삭제)


class Url(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    shorten_code = Column(String(255), unique=True, index=True, nullable=False) # base62 코드
    acc_id = Column(Integer, ForeignKey('account.id'), nullable=False) # 가계부 내역의 고유 id
    expired_at = Column(DateTime, nullable=False) # 공유 만료 날짜/시간
    