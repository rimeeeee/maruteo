import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class Config:
    # PostgreSQL 연결 정보 (환경변수에서 가져옴)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'maruteo')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # 개발 환경에서는 SQLite, 프로덕션에서는 PostgreSQL 사용
    if os.getenv('FLASK_ENV') == 'production' or os.getenv('DB_HOST'):
        # PostgreSQL 연결 문자열
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # 개발 환경에서는 SQLite 사용
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    
    # SSL 설정 (GCP Cloud SQL에서 필요한 경우)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
    }
    
    # GCP Cloud SQL에서 SSL 연결이 필요한 경우
    if os.getenv('DB_SSL_MODE') == 'require':
        SQLALCHEMY_ENGINE_OPTIONS['connect_args'] = {'sslmode': 'require'}