from flask import Blueprint, jsonify
from app.database import db
from app.models.user import User
from app.models.lesson import Lesson
from app.models.category import Category, SubCategory
from app.models.review import Review
import os

db_bp = Blueprint('db', __name__)

def create_sample_data():
    """샘플 데이터 생성"""
    # 카테고리 추가
    cooking = Category(category_id='cooking', name='요리')
    it = Category(category_id='it', name='IT')
    db.session.add_all([cooking, it])
    db.session.commit()
    
    # 소분류 추가
    korean_food = SubCategory(sub_category_id='korean-food', name='한식', category_id='cooking')
    western_food = SubCategory(sub_category_id='western-food', name='양식', category_id='cooking')
    programming = SubCategory(sub_category_id='programming', name='프로그래밍', category_id='it')
    smartphone = SubCategory(sub_category_id='smartphone-usage', name='스마트폰 사용', category_id='it')
    
    db.session.add_all([korean_food, western_food, programming, smartphone])
    db.session.commit()
    
    # 사용자 추가
    instructor = User(username='chef_kim', email='chef@example.com', password='password123', 
                     name='김요리사', phone='010-1234-5678', role='elder')
    student = User(username='dev_park', email='dev@example.com', password='password123', 
                  name='박개발자', phone='010-2345-6789', role='young')
    
    db.session.add_all([instructor, student])
    db.session.commit()
    
    # 수업 추가
    lesson1 = Lesson(title='김치찌개 만들기', description='맛있는 김치찌개를 만드는 방법을 배워봅시다.',
                    location='서울시 강남구', time='오후 2시-4시', sub_category_id='korean-food',
                    instructor_id=1, image_url='https://example.com/kimchi.jpg',
                    video_url='https://example.com/kimchi-video.mp4',
                    materials='["김치", "돼지고기", "두부", "양파", "대파", "고춧가루", "간장", "참기름"]',
                    unavailable={'days': ['월', '화'], 'times': ['오전 9시-11시', '오후 6시-8시']})
    
    lesson2 = Lesson(title='파이썬 기초', description='파이썬 프로그래밍의 기초를 배워봅시다.',
                    location='서울시 강남구', time='오후 2시-4시', sub_category_id='programming',
                    instructor_id=2, image_url='https://example.com/python.jpg',
                    video_url='https://example.com/python-video.mp4',
                    materials='["노트북", "파이썬 설치 파일", "개발 도구", "학습 자료"]',
                    unavailable={'days': ['토', '일'], 'times': ['오전 8시-10시']})
    
    db.session.add_all([lesson1, lesson2])
    db.session.commit()

@db_bp.route('/init-db', methods=['POST'])
def init_db():
    """데이터베이스 초기화 및 샘플 데이터 추가"""
    try:
        # 기존 데이터 삭제
        db.drop_all()
        db.create_all()
        
        # 샘플 사용자 생성
        instructor = User(username='chef_kim', email='chef@example.com', password='password123',
                         name='김요리사', phone='010-1234-5678', role='elder')
        student = User(username='dev_park', email='dev@example.com', password='password123',
                      name='박개발자', phone='010-2345-6789', role='young')
        
        db.session.add_all([instructor, student])
        db.session.commit()
        
        # 샘플 수업 생성
        lesson1 = Lesson(
            title='김치찌개 만들기', description='맛있는 김치찌개 만드는 방법을 배워보세요',
            instructor_id=1, image_url='https://example.com/kimchi.jpg',
            sub_category_id='korean-food', max_students=10, price=50000
        )
        
        lesson2 = Lesson(
            title='파이썬 기초', description='프로그래밍의 기초를 배워보세요',
            instructor_id=2, image_url='https://example.com/python.jpg',
            sub_category_id='programming', max_students=15, price=80000
        )
        
        db.session.add_all([lesson1, lesson2])
        db.session.commit()
        
        return jsonify({'message': '데이터베이스가 초기화되었습니다'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@db_bp.route('/db/recreate-tables', methods=['GET', 'POST'])
def recreate_tables():
    """테이블만 다시 생성 (파일 삭제 없이)"""
    try:
        # 모든 테이블 삭제 후 다시 생성
        db.drop_all()
        db.create_all()
        
        # 샘플 데이터 추가
        create_sample_data()
        
        return jsonify({
            'success': True,
            'message': '테이블이 다시 생성되고 샘플 데이터가 추가되었습니다.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@db_bp.route('/db/status', methods=['GET'])
def db_status():
    """데이터베이스 상태 확인"""
    try:
        user_count = User.query.count()
        lesson_count = Lesson.query.count()
        
        return jsonify({
            'success': True,
            'data': {
                'users': user_count,
                'lessons': lesson_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500 