from fastapi import FastAPI
from sqlalchemy.orm import Session

# from .database import SessionLocal, engine, Base
from service import models
from service.database import SessionLocal, engine
from service.router.login import router_login
from service.router.account import router_account
from service.router.url import router_url

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router_login)
app.include_router(router_account)
app.include_router(router_url)

