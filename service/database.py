from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

from .core.config import settings

import os


DB_URL = settings.DB_URL

engine = create_engine(DB_URL, encoding='utf-8')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
        print("commit")
    finally:
        db.close()