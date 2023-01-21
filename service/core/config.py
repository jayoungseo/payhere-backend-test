from pydantic import BaseSettings
from dotenv import load_dotenv

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../../.env"))

class Settings(BaseSettings):
    # DB 연결 정보 
    USER = os.environ['MYSQL_USER']
    PASSWORD = os.environ['MYSQL_PASSWORD']
    HOST = os.environ['DB_HOST']
    PORT = os.environ['DB_PORT']
    DATABASE = os.environ['MYSQL_DATABASE']
    DB_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"

    # token 관련
    ACCESS_TOKEN_EXPIRATION: int = 60 * 60 # 1시간
    REFRESH_TOKEN_EXPIRATION: int = 60 * 60 * 24 * 14 # 
    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_ALGORITHM = 'HS256'

    # 단축 url 관련
    URL_SHARE_EXPIRATION: int = 60 * 10 # 10분
    API_DOMAIN_ADDRESS = os.environ['API_DOMAIN_ADDRESS']

settings = Settings()