#수업 신청 모델

from app import db
from datetime import datetime

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 신청자 (어르신)
    status = db.Column(db.String(20), default='신청됨')  # 추후 승인 구조로 확장 가능
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "lesson_id": self.lesson_id,
            "user_id": self.user_id,
            "status": self.status,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M')
        }