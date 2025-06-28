from app import create_app, db
from app.models.user import User, Talent
from app.models.lesson import Lesson, wishlist
from app.models.application import Application
from app.models.category import Category, SubCategory
from app.models.review import Review
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # 데이터베이스 테이블 생성
    db.create_all()
    print("데이터베이스 테이블이 성공적으로 생성되었습니다.")
    
    # 분류 데이터 추가
    categories_data = [
        {
            'id': 'cooking',
            'name': '요리',
            'sub_categories': [
                {'id': 'korean-food', 'name': '한식'},
                {'id': 'chinese-food', 'name': '중식'},
                {'id': 'japanese-food', 'name': '일식'},
                {'id': 'western-food', 'name': '양식'},
                {'id': 'cooking-etc', 'name': '기타'},
            ]
        },
        {
            'id': 'it',
            'name': 'IT',
            'sub_categories': [
                {'id': 'smartphone-usage', 'name': '스마트폰 사용'},
                {'id': 'delivery-app-usage', 'name': '배달앱 사용'},
                {'id': 'internet-banking', 'name': '인터넷 뱅킹'},
                {'id': 'kiosk-usage', 'name': '키오스크 사용법'},
                {'id': 'voice-phishing', 'name': '보이스 피싱'},
                {'id': 'it-etc', 'name': '기타'},
            ]
        },
        {
            'id': 'instrument',
            'name': '악기',
            'sub_categories': [
                {'id': 'piano', 'name': '피아노'},
                {'id': 'guitar', 'name': '기타'},
                {'id': 'drums', 'name': '드럼'},
                {'id': 'ukulele', 'name': '우쿨렐레'},
                {'id': 'instrument-etc', 'name': '기타'},
            ]
        },
        {
            'id': 'exercise',
            'name': '운동',
            'sub_categories': [
                {'id': 'fitness', 'name': '헬스'},
                {'id': 'yoga', 'name': '요가'},
                {'id': 'walking', 'name': '걷기'},
                {'id': 'pingpong', 'name': '탁구'},
                {'id': 'exercise-etc', 'name': '기타'},
            ]
        },
        {
            'id': 'writing',
            'name': '글쓰기',
            'sub_categories': [
                {'id': 'diary', 'name': '일기'},
                {'id': 'letter', 'name': '편지'},
                {'id': 'poem', 'name': '시'},
                {'id': 'essay', 'name': '수필'},
                {'id': 'writing-etc', 'name': '기타'},
            ]
        },
        {
            'id': 'art',
            'name': '미술',
            'sub_categories': [
                {'id': 'drawing', 'name': '수채화'},
                {'id': 'painting', 'name': '색연필화'},
                {'id': 'calligraphy', 'name': '캘리그라피'},
                {'id': 'paper-craft', 'name': '종이접기'},
                {'id': 'art-etc', 'name': '기타'},
            ]
        },
        {
            'id': 'farming',
            'name': '농업',
            'sub_categories': [
                {'id': 'gardening', 'name': '텃밭 가꾸기'},
                {'id': 'farming-basic', 'name': '화분 관리'},
                {'id': 'farming-basic', 'name': '작물 재배'},
                {'id': 'farming-etc', 'name': '기타'},
            ]
        }
    ]
    
    # 분류 데이터 추가
    for category_data in categories_data:
        # 대분류가 이미 존재하는지 확인
        existing_category = Category.query.filter_by(category_id=category_data['id']).first()
        if not existing_category:
            category = Category()
            category.category_id = category_data['id']
            category.name = category_data['name']
            db.session.add(category)
            db.session.flush()  # ID 생성을 위해 flush
            
            # 소분류들 추가
            for sub_data in category_data['sub_categories']:
                existing_sub = SubCategory.query.filter_by(sub_category_id=sub_data['id']).first()
                if not existing_sub:
                    sub_category = SubCategory()
                    sub_category.sub_category_id = sub_data['id']
                    sub_category.name = sub_data['name']
                    sub_category.category_id = category.category_id
                    db.session.add(sub_category)
    
    db.session.commit()
    print("분류 데이터가 성공적으로 추가되었습니다.")
    
    # 샘플 데이터 추가 (선택사항)
    print("샘플 데이터를 추가하시겠습니까? (y/n): ", end="")
    # 실제로는 사용자 입력을 받지만, 여기서는 자동으로 추가
    add_sample_data = True
    
    if add_sample_data:
        # 샘플 사용자 추가
        sample_instructors = [
            {
                'name': '김요리사',
                'email': 'chef@example.com',
                'role': 'elder',
                'password': generate_password_hash('password123')
            },
            {
                'name': '박개발자',
                'email': 'dev@example.com',
                'role': 'young',
                'password': generate_password_hash('password123')
            }
        ]
        
        for instructor_data in sample_instructors:
            existing_user = User.query.filter_by(email=instructor_data['email']).first()
            if not existing_user:
                user = User()
                user.name = instructor_data['name']
                user.email = instructor_data['email']
                user.role = instructor_data['role']
                user.password = instructor_data['password']  # 실제로는 해시화해야 함
                db.session.add(user)
        
        db.session.commit()
        print("샘플 강사 데이터가 추가되었습니다.")
    
    print("마이그레이션이 완료되었습니다.") 