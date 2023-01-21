from service.models import Account
from service.schemas.account import *

from datetime import date, datetime


def get_all_data(db, user_id: int):
    db_data = db.query(Account).filter(
        Account.user_id == user_id,
        Account.is_deleted == 0 # 삭제된 데이터 제외
    ).all()
    return db_data


def get_one_data(db, acc_id: int):
    db_data = db.query(Account).filter(
        Account.id == acc_id,
        Account.is_deleted == 0 # 삭제된 데이터 제외
    ).first()
    return db_data


def create_contetns(db, inbound_data: AccountPostDTO, user_id: int):
    obj = Account(
        user_id = user_id,
        use_date = date.today(), # 돈 사용한 날짜
        amount = inbound_data.amount,
        memo   = inbound_data.memo,
        created_at = datetime.today() # 가계부 작성 날찌/시간
    )
    db.add(obj)
    return obj


def update_contents(db, inbound_data: AccountUpdateDTO, acc_id: int):
    db_data = db.query(Account).filter(Account.id == acc_id).first()

    update_data = inbound_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_data, key, value)
    
    db_data.updated_at = datetime.today()
    db.add(db_data)
    return db_data


def delete_contents(db, acc_id: int):
    db_data = db.query(Account).filter(Account.id == acc_id).update(
        values = {
            Account.is_deleted : 1
        }
    )
    return True


def copy_contents(db, acc_id: int):
    obj = db.query(Account).filter(Account.id == acc_id).first()

    add_data = AccountPostDTO(
        amount = obj.amount,
        memo = obj.memo
    )
    copy_obj = create_contetns(db, inbound_data=add_data, user_id=obj.user_id)
    return copy_obj

