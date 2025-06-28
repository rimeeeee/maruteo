from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # ⭐ 여기를 추가

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

with app.app_context():
    try:
        with db.engine.connect() as conn:
            conn.execute(text('SELECT 1'))  # ⭐ text()로 감싸야 함
        print("✅ DB 연결 성공!")
    except Exception as e:
        print("❌ DB 연결 실패:", e)