#!/usr/bin/env python3
"""
샘플 데이터 추가 스크립트
"""

from app import create_app
from app.database import db
from app.models.user import User
from app.models.lesson import Lesson
from app.models.category import Category, SubCategory
from app.models.review import Review

def add_sample_data():
    """샘플 데이터 추가"""
    print("📝 샘플 데이터 추가 중...")
    
    with create_app().app_context():
        # 카테고리 추가
        print("1. 카테고리 추가 중...")
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
        print("✅ 카테고리 추가 완료")
        
        # 사용자 추가
        print("2. 사용자 추가 중...")
        # 어르신 강사 (청년이 배울 수 있는)
        elder_instructor = User(
            username='chef_kim',
            email='chef_kim@example.com',
            password='password123',
            name='김요리사',
            phone='010-1234-5678',
            role='instructor'  # 어르신
        )
        
        # 청년 강사 (어르신이 배울 수 있는)
        young_instructor = User(
            username='dev_park',
            email='dev_park@example.com',
            password='password123',
            name='박개발자',
            phone='010-2345-6789',
            role='student'  # 청년
        )
        
        # 청년 학생
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
        print("✅ 사용자 추가 완료")
        
        # 수업 추가
        print("3. 수업 추가 중...")
        # 어르신이 만든 수업 (청년이 배울 수 있는)
        lesson1 = Lesson(
            title='김치찌개 만들기',
            description='맛있는 김치찌개를 만드는 방법을 배워봅시다.',
            location='서울시 강남구',
            time='오후 2시-4시',
            sub_category_id='korean-food',
            instructor_id=1,  # 어르신 강사
            image_url='https://example.com/kimchi.jpg'
        )
        
        lesson2 = Lesson(
            title='파스타 만들기',
            description='이탈리안 파스타의 정석을 배워봅시다.',
            location='서울시 서초구',
            time='오후 3시-5시',
            sub_category_id='western-food',
            instructor_id=1,  # 어르신 강사
            image_url='https://example.com/pasta.jpg'
        )
        
        # 청년이 만든 수업 (어르신이 배울 수 있는)
        lesson3 = Lesson(
            title='파이썬 기초',
            description='파이썬 프로그래밍의 기초를 배워봅시다.',
            location='서울시 강남구',
            time='오후 2시-4시',
            sub_category_id='programming',
            instructor_id=2,  # 청년 강사
            image_url='https://example.com/python.jpg'
        )
        
        lesson4 = Lesson(
            title='스마트폰 활용법',
            description='스마트폰의 다양한 기능을 활용하는 방법을 배워봅시다.',
            location='서울시 서초구',
            time='오후 3시-5시',
            sub_category_id='smartphone-usage',
            instructor_id=2,  # 청년 강사
            image_url='https://example.com/smartphone.jpg'
        )
        
        db.session.add_all([lesson1, lesson2, lesson3, lesson4])
        db.session.commit()
        print("✅ 수업 추가 완료")
        
        # 리뷰 추가
        print("4. 리뷰 추가 중...")
        review1 = Review(
            lesson_id=1,
            user_id=3,  # 청년 학생
            rating=5,
            comment='정말 맛있게 만들었어요!'
        )
        
        review2 = Review(
            lesson_id=1,
            user_id=2,  # 청년 강사
            rating=4,
            comment='기초부터 차근차근 가르쳐주셔서 좋았습니다.'
        )
        
        review3 = Review(
            lesson_id=3,
            user_id=1,  # 어르신 강사
            rating=5,
            comment='파이썬 기초를 쉽게 배울 수 있었어요!'
        )
        
        review4 = Review(
            lesson_id=3,
            user_id=3,  # 청년 학생
            rating=4,
            comment='실습이 많아서 좋았습니다.'
        )
        
        db.session.add_all([review1, review2, review3, review4])
        db.session.commit()
        print("✅ 리뷰 추가 완료")
        
        print("\n🎉 모든 샘플 데이터가 추가되었습니다!")
        print("이제 API를 테스트할 수 있습니다.")

if __name__ == '__main__':
    add_sample_data() 