from app import db, create_app
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # 기존 테스트 계정 삭제
    existing_youth = User.query.filter_by(email='young@test.com').first()
    if existing_youth:
        db.session.delete(existing_youth)
        print('기존 청년 계정 삭제')
    
    existing_elder = User.query.filter_by(email='elder@test.com').first()
    if existing_elder:
        db.session.delete(existing_elder)
        print('기존 어르신 계정 삭제')
    
    db.session.commit()

    # 청년 계정 생성
    youth = User(
        username='김철수',
        password=generate_password_hash('password123'),
        name='테스트청년',
        role='young',
        email='young@test.com',
        profile_image='',
        bio='테스트용 청년 계정'
    )
    db.session.add(youth)
    print('청년 계정 생성 완료')

    # 어르신 계정 생성
    instructor = User(
        username='박어르신',
        password=generate_password_hash('password123'),
        name='테스트어르신',
        role='elder',
        email='elder@test.com',
        profile_image='',
        bio='테스트용 어르신 계정'
    )
    db.session.add(instructor)
    print('어르신 계정 생성 완료')

    db.session.commit()
    print('DB 커밋 완료')
    
    # 생성된 계정 확인
    youth_check = User.query.filter_by(email='young@test.com').first()
    elder_check = User.query.filter_by(email='elder@test.com').first()
    
    if youth_check:
        print(f'청년 계정 확인: {youth_check.email} - {youth_check.role}')
    if elder_check:
        print(f'어르신 계정 확인: {elder_check.email} - {elder_check.role}') 