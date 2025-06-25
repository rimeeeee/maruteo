from app import db

class LessonAttendance(db.Model):
    __tablename__ = 'lesson_attendance'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)

    attended = db.Column(db.Boolean, default=False)  # 출석 여부
    fulfilled = db.Column(db.Boolean, default=False)  # 약속 이행 여부

    user = db.relationship('User', backref='attendances')
    lesson = db.relationship('Lesson', backref='attendances')