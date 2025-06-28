from app.database import db

class Category(db.Model):
    """대분류 모델"""
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(50), unique=True, nullable=False)  # 'cooking', 'it' 등
    name = db.Column(db.String(100), nullable=False)  # '요리', 'IT' 등
    
    # 소분류들과의 관계
    sub_categories = db.relationship('SubCategory', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, category_id=None, name=None, **kwargs):
        self.category_id = category_id
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        return {
            'id': self.category_id,
            'name': self.name,
            'sub_categories': []  # 임시로 빈 배열 반환
        }

class SubCategory(db.Model):
    """소분류 모델"""
    id = db.Column(db.Integer, primary_key=True)
    sub_category_id = db.Column(db.String(50), unique=True, nullable=False)  # 'korean-food', 'smartphone-usage' 등
    name = db.Column(db.String(100), nullable=False)  # '한식', '스마트폰 사용' 등
    category_id = db.Column(db.String(50), db.ForeignKey('category.category_id'), nullable=False)
    
    # 수업들과의 관계 (backref 제거)
    lessons = db.relationship('Lesson', lazy=True)
    
    def __init__(self, sub_category_id=None, name=None, category_id=None, **kwargs):
        self.sub_category_id = sub_category_id
        self.name = name
        self.category_id = category_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        return {
            'id': self.sub_category_id,
            'name': self.name,
            'categoryId': self.category_id
        } 