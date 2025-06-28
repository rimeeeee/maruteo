import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret-key'
    SECRET_KEY = 'super-secret-key'
    
    # CORS 설정 - 환경변수에서 origins 가져오기
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(',')