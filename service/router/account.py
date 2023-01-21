from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from service.database import get_db
from service.router.depends import get_current_user
from service.models import User
from service.schemas.account import *
from service.crud import CRUDaccount, CRUDurl
from service.core.config import settings

router_account = APIRouter(
    prefix="/account-book",
    tags=["account-book"]
)


# 가계부 모든 내역 보기
@router_account.get("", response_model=List[AccountDataInDB])
def get_all_account_data(
    curr_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return_data = CRUDaccount.get_all_data(db, user_id=curr_user.id)
    return return_data


# 한개의 세부 내역 보기
@router_account.get("/{id}", response_model=AccountDataInDB)
def get_one_account_data(
    id: int,
    curr_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return_data = CRUDaccount.get_one_data(db, acc_id=id)
    return return_data


# 세부 내역 공유
@router_account.get("/{id}/share-url")
def get_shorten_url(
    id: int,
    curr_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    shorten_code = CRUDurl.get_shorten_url_code(db, acc_id=id)
    share_url = f'http://{settings.API_DOMAIN_ADDRESS}/url/{shorten_code}'

    return share_url


# 세부 내역 작성
@router_account.post("", response_model=AccountReturnData)
def write_account_book_contents(
    inbound_data: AccountPostDTO,
    curr_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return_data = CRUDaccount.create_contetns(db, inbound_data, user_id=curr_user.id)
    return return_data


# 세부 내역 업데이트
@router_account.post("/{id}/update", response_model=AccountReturnData)
def update_account_book_contetns(
    id: int,
    inbound_data: AccountUpdateDTO,
    curr_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):

    return_data = CRUDaccount.update_contents(db, inbound_data, acc_id=id)
    return return_data


# 세부 내역 복제
@router_account.post("/{id}/copy", response_model=AccountReturnData)
def copy_account_book_contetns(
    id: int,
    curr_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return_data = CRUDaccount.copy_contents(db, acc_id=id)
    return return_data


# 세부 내역 삭제
@router_account.post("/{id}/delete")
def update_account_book_contetns(
    id: int,
    curr_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):

    return_data = CRUDaccount.delete_contents(db, acc_id=id)
    return return_data