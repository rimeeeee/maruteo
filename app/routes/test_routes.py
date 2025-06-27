from flask import Blueprint, jsonify
from app.database import db
from app.models.user import User
from app.models.lesson import Lesson
from app.models.category import Category, SubCategory
from app.models.review import Review
import os

test_bp = Blueprint('test', __name__)

@test_bp.route('/test/reset-db', methods=['GET', 'POST'])
def reset_database():
    """데이터베이스 초기화"""
    try:
        # 데이터베이스 파일 삭제
        db_path = 'instance/app.db'
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print("✅ 기존 데이터베이스 파일이 삭제되었습니다.")
            except PermissionError:
                print("⚠️ 데이터베이스 파일이 사용 중입니다. 테이블만 다시 생성합니다.")
        
        # 테이블 생성
        db.create_all()
        print("✅ 모든 테이블이 생성되었습니다.")
        
        return jsonify({
            'success': True,
            'message': '데이터베이스가 초기화되었습니다.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@test_bp.route('/test/recreate-tables', methods=['GET'])
def recreate_tables():
    """테이블만 다시 생성 (파일 삭제 없이)"""
    try:
        # 모든 테이블 삭제 후 다시 생성
        db.drop_all()
        db.create_all()
        
        return jsonify({
            'success': True,
            'message': '테이블이 다시 생성되었습니다.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@test_bp.route('/test/add-sample-data', methods=['GET', 'POST'])
def add_sample_data():
    """샘플 데이터 추가"""
    try:
        # 카테고리 추가
        cooking = Category(category_id='cooking', name='요리')
        it = Category(category_id='it', name='IT')
        
        db.session.add(cooking)
        db.session.add(it)
        db.session.commit()
        
        # 소분류 추가
        korean_food = SubCategory(sub_category_id='korean-food', name='한식', category_id='cooking')
        western_food = SubCategory(sub_category_id='western-food', name='양식', category_id='cooking')
        japanese_food = SubCategory(sub_category_id='japanese-food', name='일식', category_id='cooking')
        
        programming = SubCategory(sub_category_id='programming', name='프로그래밍', category_id='it')
        smartphone = SubCategory(sub_category_id='smartphone-usage', name='스마트폰 사용', category_id='it')
        computer = SubCategory(sub_category_id='computer-usage', name='컴퓨터 사용', category_id='it')
        
        db.session.add_all([korean_food, western_food, japanese_food, programming, smartphone, computer])
        db.session.commit()
        
        # 사용자 추가
        elder_instructor = User(
            username='chef_kim',
            email='chef_kim@example.com',
            password='password123',
            name='김요리사',
            phone='010-1234-5678',
            role='instructor'  # 어르신
        )
        
        young_instructor = User(
            username='dev_park',
            email='dev_park@example.com',
            password='password123',
            name='박개발자',
            phone='010-2345-6789',
            role='student'  # 청년
        )
        
        young_student = User(
            username='student_lee',
            email='student_lee@example.com',
            password='password123',
            name='이학생',
            phone='010-3456-7890',
            role='student'  # 청년
        )
        
        db.session.add_all([elder_instructor, young_instructor, young_student])
        db.session.commit()
        
        # 수업 추가
        lesson1 = Lesson(
            title='김치찌개 만들기',
            description='맛있는 김치찌개를 만드는 방법을 배워봅시다.',
            location='서울시 강남구',
            time='오후 2시-4시',
            sub_category_id='korean-food',
            instructor_id=1,
            image_url='https://example.com/kimchi.jpg'
        )
        
        lesson2 = Lesson(
            title='파스타 만들기',
            description='이탈리안 파스타의 정석을 배워봅시다.',
            location='서울시 서초구',
            time='오후 3시-5시',
            sub_category_id='western-food',
            instructor_id=1,
            image_url='https://example.com/pasta.jpg'
        )
        
        lesson3 = Lesson(
            title='파이썬 기초',
            description='파이썬 프로그래밍의 기초를 배워봅시다.',
            location='서울시 강남구',
            time='오후 2시-4시',
            sub_category_id='programming',
            instructor_id=2,
            image_url='https://example.com/python.jpg'
        )
        
        lesson4 = Lesson(
            title='스마트폰 활용법',
            description='스마트폰의 다양한 기능을 활용하는 방법을 배워봅시다.',
            location='서울시 서초구',
            time='오후 3시-5시',
            sub_category_id='smartphone-usage',
            instructor_id=2,
            image_url='https://example.com/smartphone.jpg'
        )
        
        db.session.add_all([lesson1, lesson2, lesson3, lesson4])
        db.session.commit()
        
        # 리뷰 추가
        review1 = Review(
            lesson_id=1,
            user_id=3,
            rating=5,
            comment='정말 맛있게 만들었어요!'
        )
        
        review2 = Review(
            lesson_id=1,
            user_id=2,
            rating=4,
            comment='기초부터 차근차근 가르쳐주셔서 좋았습니다.'
        )
        
        review3 = Review(
            lesson_id=3,
            user_id=1,
            rating=5,
            comment='파이썬 기초를 쉽게 배울 수 있었어요!'
        )
        
        review4 = Review(
            lesson_id=3,
            user_id=3,
            rating=4,
            comment='실습이 많아서 좋았습니다.'
        )
        
        db.session.add_all([review1, review2, review3, review4])
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '샘플 데이터가 추가되었습니다.'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@test_bp.route('/test/status', methods=['GET'])
def test_status():
    """테스트 상태 확인"""
    try:
        # 각 테이블의 데이터 수 확인
        user_count = User.query.count()
        category_count = Category.query.count()
        subcategory_count = SubCategory.query.count()
        lesson_count = Lesson.query.count()
        review_count = Review.query.count()
        
        return jsonify({
            'success': True,
            'data': {
                'users': user_count,
                'categories': category_count,
                'subcategories': subcategory_count,
                'lessons': lesson_count,
                'reviews': review_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@test_bp.route('/test/setup', methods=['GET'])
def setup_database():
    """데이터베이스 초기화 + 샘플 데이터 추가 (한번에)"""
    try:
        # 1단계: 테이블 다시 생성
        db.drop_all()
        db.create_all()
        
        # 2단계: 샘플 데이터 추가
        # 카테고리 추가
        cooking = Category(category_id='cooking', name='요리')
        it = Category(category_id='it', name='IT')
        
        db.session.add(cooking)
        db.session.add(it)
        db.session.commit()
        
        # 소분류 추가
        korean_food = SubCategory(sub_category_id='korean-food', name='한식', category_id='cooking')
        western_food = SubCategory(sub_category_id='western-food', name='양식', category_id='cooking')
        japanese_food = SubCategory(sub_category_id='japanese-food', name='일식', category_id='cooking')
        
        programming = SubCategory(sub_category_id='programming', name='프로그래밍', category_id='it')
        smartphone = SubCategory(sub_category_id='smartphone-usage', name='스마트폰 사용', category_id='it')
        computer = SubCategory(sub_category_id='computer-usage', name='컴퓨터 사용', category_id='it')
        
        db.session.add_all([korean_food, western_food, japanese_food, programming, smartphone, computer])
        db.session.commit()
        
        # 사용자 추가
        elder_instructor = User(
            username='chef_kim',
            email='chef_kim@example.com',
            password='password123',
            name='김요리사',
            phone='010-1234-5678',
            role='instructor'  # 어르신
        )
        
        young_instructor = User(
            username='dev_park',
            email='dev_park@example.com',
            password='password123',
            name='박개발자',
            phone='010-2345-6789',
            role='student'  # 청년
        )
        
        young_student = User(
            username='student_lee',
            email='student_lee@example.com',
            password='password123',
            name='이학생',
            phone='010-3456-7890',
            role='student'  # 청년
        )
        
        db.session.add_all([elder_instructor, young_instructor, young_student])
        db.session.commit()
        
        # 수업 추가
        lesson1 = Lesson(
            title='김치찌개 만들기',
            description='맛있는 김치찌개를 만드는 방법을 배워봅시다.',
            location='서울시 강남구',
            time='오후 2시-4시',
            sub_category_id='korean-food',
            instructor_id=1,
            image_url='https://example.com/kimchi.jpg'
        )
        
        lesson2 = Lesson(
            title='파스타 만들기',
            description='이탈리안 파스타의 정석을 배워봅시다.',
            location='서울시 서초구',
            time='오후 3시-5시',
            sub_category_id='western-food',
            instructor_id=1,
            image_url='https://example.com/pasta.jpg'
        )
        
        lesson3 = Lesson(
            title='파이썬 기초',
            description='파이썬 프로그래밍의 기초를 배워봅시다.',
            location='서울시 강남구',
            time='오후 2시-4시',
            sub_category_id='programming',
            instructor_id=2,
            image_url='https://example.com/python.jpg'
        )
        
        lesson4 = Lesson(
            title='스마트폰 활용법',
            description='스마트폰의 다양한 기능을 활용하는 방법을 배워봅시다.',
            location='서울시 서초구',
            time='오후 3시-5시',
            sub_category_id='smartphone-usage',
            instructor_id=2,
            image_url='https://example.com/smartphone.jpg'
        )
        
        db.session.add_all([lesson1, lesson2, lesson3, lesson4])
        db.session.commit()
        
        # 리뷰 추가
        review1 = Review(
            lesson_id=1,
            user_id=3,
            rating=5,
            comment='정말 맛있게 만들었어요!'
        )
        
        review2 = Review(
            lesson_id=1,
            user_id=2,
            rating=4,
            comment='기초부터 차근차근 가르쳐주셔서 좋았습니다.'
        )
        
        review3 = Review(
            lesson_id=3,
            user_id=1,
            rating=5,
            comment='파이썬 기초를 쉽게 배울 수 있었어요!'
        )
        
        review4 = Review(
            lesson_id=3,
            user_id=3,
            rating=4,
            comment='실습이 많아서 좋았습니다.'
        )
        
        db.session.add_all([review1, review2, review3, review4])
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '데이터베이스 초기화 및 샘플 데이터 추가가 완료되었습니다.'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500