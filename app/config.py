import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret-key'
    SECRET_KEY = 'super-secret-key'