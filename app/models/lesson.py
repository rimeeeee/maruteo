from app import db

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    date = db.Column(db.String(50))  # 날짜는 문자열로 우선 처리
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 강사 (청년)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "date": self.date,
            "instructor_id": self.instructor_id
        }