# User테이블 정의
from app import db

# 보유 재능
user_have_talents = db.Table('user_have_talents',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('talent_id', db.Integer, db.ForeignKey('talent.id'))
)

# 배우고 싶은 재능
user_want_talents = db.Table('user_want_talents',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('talent_id', db.Integer, db.ForeignKey('talent.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20))       # '청년', '어르신'
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    birth = db.Column(db.String(20))      # 'YYYY-MM-DD' 형식
    password = db.Column(db.String(255), nullable=False)

    #프로필 필드
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.String(200), nullable=True)       # 한 줄 소개
    username = db.Column(db.String(50), unique=True, nullable=True) #로그인용 아니고 공개 닉네임?아이디
    profile_image = db.Column(db.String(200), nullable=True)  # 이미지 경로
    have_talents = db.relationship('Talent', secondary=user_have_talents, backref='owners')
    want_talents = db.relationship('Talent', secondary=user_want_talents, backref='learners')


class Talent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)