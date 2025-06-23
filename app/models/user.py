# User테이블 정의
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20))       # '청년', '어르신'
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    birth = db.Column(db.String(20))      # 'YYYY-MM-DD' 형식
    password = db.Column(db.String(255))