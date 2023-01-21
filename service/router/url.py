from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from service.database import get_db
from service.router.depends import get_current_user
from service.models import User
from service.schemas.account import *
from service.crud import CRUDaccount, CRUDurl

router_url = APIRouter(
    prefix="/url",
    tags=["url"]
)


@router_url.get("/{code}", response_model=AccountReturnData)
def redirect_original_url(
    code: str,
    db: Session = Depends(get_db)
):
    return_data = CRUDurl.get_account_share_contents(db, code)
    if not return_data:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return return_data