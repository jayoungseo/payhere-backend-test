from service.models import Url, Account
from service.core.config import settings

from datetime import date, datetime, timedelta

import string
import random
import time



def get_base62_code():
    curr_time = time.time() * 100000
    char_list = list(string.digits + string.ascii_letters)
    random.shuffle(char_list)

    s_code = ""
    # Convert Base-62
    while curr_time > 0:
        p = curr_time % 62
        s_code += char_list[int(p)]
        curr_time = curr_time // 62

    return s_code


def get_shorten_url_code(db, acc_id: int):
    expired_dt = datetime.today()+timedelta(seconds=settings.URL_SHARE_EXPIRATION) # 공유 만료 시간

    shorten_code = get_base62_code()
    print(expired_dt, shorten_code)
    obj = Url(
        shorten_code = shorten_code,
        acc_id = acc_id,
        expired_at = expired_dt
    )
    db.add(obj)

    return shorten_code


def get_account_share_contents(db, code: str):
    url_obj = db.query(Url).filter(Url.shorten_code == code).first()

    curr_dt = datetime.today()
    # 공유 시간이 만료되지 않았을때
    if curr_dt < url_obj.expired_at:
        acc_obj = db.query(Account).filter(Account.id == url_obj.acc_id).first()
        return acc_obj
    # 공유 시간이 만료되었을때
    else:
        return None

    


