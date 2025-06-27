#!/usr/bin/env python3
"""
간단한 데이터베이스 마이그레이션 스크립트
"""

from app import create_app
from app.database import db
from app.models.user import User
from app.models.lesson import Lesson
from app.models.category import Category, SubCategory
from app.models.review import Review

def create_tables():
    """테이블 생성"""
    print("테이블 생성 중...")
    with create_app().app_context():
        db.create_all()
        print("✅ 모든 테이블이 생성되었습니다.")

def add_categories():
    """카테고리 데이터 추가"""
    print("카테고리 데이터 추가 중...")
    with create_app().app_context():
        # 대분류 추가
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
        
        print("✅ 카테고리 데이터가 추가되었습니다.")

def add_sample_users():
    """샘플 사용자 추가"""
    print("샘플 사용자 추가 중...")
    with create_app().app_context():
        # 강사 1
        instructor1 = User(
            username='chef_kim',
            email='chef_kim@example.com',
            password='password123',
            name='김요리사',
            phone='010-1234-5678',
            role='instructor'
        )
        
        # 강사 2
        instructor2 = User(
            username='dev_park',
            email='dev_park@example.com',
            password='password123',
            name='박개발자',
            phone='010-2345-6789',
            role='instructor'
        )
        
        # 일반 사용자
        user1 = User(
            username='student_lee',
            email='student_lee@example.com',
            password='password123',
            name='이학생',
            phone='010-3456-7890',
            role='student'
        )
        
        db.session.add_all([instructor1, instructor2, user1])
        db.session.commit()
        
        print("✅ 샘플 사용자가 추가되었습니다.")

def add_sample_lessons():
    """샘플 수업 추가"""
    print("샘플 수업 추가 중...")
    with create_app().app_context():
        # 요리 수업들
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
            title='초밥 만들기',
            description='신선한 초밥을 만드는 방법을 배워봅시다.',
            location='서울시 마포구',
            time='오후 1시-3시',
            sub_category_id='japanese-food',
            instructor_id=1,
            image_url='https://example.com/sushi.jpg'
        )
        
        # IT 수업들
        lesson4 = Lesson(
            title='파이썬 기초',
            description='파이썬 프로그래밍의 기초를 배워봅시다.',
            location='서울시 강남구',
            time='오후 2시-4시',
            sub_category_id='programming',
            instructor_id=2,
            image_url='https://example.com/python.jpg'
        )
        
        lesson5 = Lesson(
            title='스마트폰 활용법',
            description='스마트폰의 다양한 기능을 활용하는 방법을 배워봅시다.',
            location='서울시 서초구',
            time='오후 3시-5시',
            sub_category_id='smartphone-usage',
            instructor_id=2,
            image_url='https://example.com/smartphone.jpg'
        )
        
        lesson6 = Lesson(
            title='컴퓨터 기초',
            description='컴퓨터 사용의 기초를 배워봅시다.',
            location='서울시 마포구',
            time='오후 1시-3시',
            sub_category_id='computer-usage',
            instructor_id=2,
            image_url='https://example.com/computer.jpg'
        )
        
        db.session.add_all([lesson1, lesson2, lesson3, lesson4, lesson5, lesson6])
        db.session.commit()
        
        print("✅ 샘플 수업이 추가되었습니다.")

def add_sample_reviews():
    """샘플 리뷰 추가"""
    print("샘플 리뷰 추가 중...")
    with create_app().app_context():
        # 수업 1에 대한 리뷰들
        review1 = Review(
            lesson_id=1,
            user_id=3,
            rating=5,
            comment='정말 맛있게 만들었어요!'
        )
        
        review2 = Review(
            lesson_id=1,
            user_id=1,
            rating=4,
            comment='기초부터 차근차근 가르쳐주셔서 좋았습니다.'
        )
        
        # 수업 4에 대한 리뷰들
        review3 = Review(
            lesson_id=4,
            user_id=3,
            rating=5,
            comment='파이썬 기초를 쉽게 배울 수 있었어요!'
        )
        
        review4 = Review(
            lesson_id=4,
            user_id=2,
            rating=4,
            comment='실습이 많아서 좋았습니다.'
        )
        
        db.session.add_all([review1, review2, review3, review4])
        db.session.commit()
        
        print("✅ 샘플 리뷰가 추가되었습니다.")

def main():
    """메인 실행 함수"""
    print("🚀 데이터베이스 마이그레이션을 시작합니다...")
    
    try:
        create_tables()
        add_categories()
        add_sample_users()
        add_sample_lessons()
        add_sample_reviews()
        
        print("\n🎉 모든 마이그레이션이 완료되었습니다!")
        print("이제 서버를 실행하고 API를 테스트할 수 있습니다.")
        
    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main() 