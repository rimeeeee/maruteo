from app.database import db
from datetime import datetime

class Review(db.Model):
    """수업 리뷰 모델"""
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 리뷰 작성자
    rating = db.Column(db.Integer, nullable=False)  # 별점 (1-5)
    comment = db.Column(db.Text, nullable=True)  # 리뷰 내용
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 관계 설정 (backref 제거)
    lesson = db.relationship('Lesson')
    user = db.relationship('User', backref='reviews')
    
    def __init__(self, lesson_id=None, user_id=None, rating=None, comment=None, **kwargs):
        self.lesson_id = lesson_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        } 