#수업테이블정의
# from app import db

# class Lesson(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100))
#     description = db.Column(db.Text)
#     location = db.Column(db.String(100))
#     date = db.Column(db.String(50))  # 날짜는 문자열로 우선 처리
    
#     #instructor_id는 User 테이블의 ID와 연결
#     instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 강사 (청년)

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "description": self.description,
#             "location": self.location,
#             "date": self.date,
#             "instructor_id": self.instructor_id
#         }

from app.database import db
from datetime import datetime

# 찜한 수업 테이블
wishlist = db.Table('wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id'))
)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    time = db.Column(db.String(100), nullable=True)
    unavailable = db.Column(db.PickleType, nullable=True)  # 문자열 배열 저장
    media_url = db.Column(db.String(500), nullable=True)
    
    # 새로운 분류 시스템
    sub_category_id = db.Column(db.String(50), db.ForeignKey('sub_category.sub_category_id'), nullable=True)
    
    # 클라우디너리 이미지 URL
    image_url = db.Column(db.String(500), nullable=True)
    
    # 생성일
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 등록한 유저 정보 (청년)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instructor = db.relationship('User', backref='lessons')
    
    # 찜한 사용자들
    wished_by = db.relationship('User', secondary=wishlist, backref='wished_lessons')
    
    # 리뷰 관계
    reviews = db.relationship('Review', backref='lesson_ref', lazy=True)
    
    def __init__(self, title=None, description=None, location=None, time=None, sub_category_id=None, instructor_id=None, image_url=None, **kwargs):
        self.title = title
        self.description = description
        self.location = location
        self.time = time
        self.sub_category_id = sub_category_id
        self.instructor_id = instructor_id
        self.image_url = image_url
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        # 분류 정보 안전하게 가져오기 (직접 쿼리)
        sub_category_name = None
        category_id = None
        category_name = None
        
        if self.sub_category_id:
            from app.models.category import SubCategory
            sub_category = SubCategory.query.filter_by(sub_category_id=self.sub_category_id).first()
            if sub_category:
                sub_category_name = sub_category.name
                if sub_category.category:
                    category_id = sub_category.category_id
                    category_name = sub_category.category.name
        
        # 평균 별점 계산
        avg_rating = 0
        review_count = 0
        # reviews는 실제 쿼리에서 계산하므로 여기서는 기본값 사용
        
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "time": self.time,
            "media_url": self.media_url,
            "image_url": self.image_url,  # 클라우디너리 이미지 URL
            "sub_category_id": self.sub_category_id,
            "sub_category_name": sub_category_name,
            "category_id": category_id,
            "category_name": category_name,
            "instructor_id": self.instructor_id,
            "instructor_name": self.instructor.name if self.instructor else None,
            "wish_count": 0,  # 임시로 0으로 설정, 실제로는 쿼리에서 계산
            "avg_rating": avg_rating,
            "review_count": review_count,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }