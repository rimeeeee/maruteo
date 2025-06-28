import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    # 로컬 테스트용 SQLite 설정
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/app.db'
    
    # PostgreSQL 설정 (주석 처리)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret-key'
    SECRET_KEY = 'super-secret-key'
    # templates 디렉토리 설정
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')