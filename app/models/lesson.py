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

from app import db

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    time = db.Column(db.String(100), nullable=True)
    unavailable = db.Column(db.PickleType, nullable=True)  # 문자열 배열 저장
    media_url = db.Column(db.String(500), nullable=True)
    categori_high = db.Column(db.String(100))
    categori_middle = db.Column(db.String(100))

    # 등록한 유저 정보 (청년)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instructor = db.relationship('User', backref='lessons')