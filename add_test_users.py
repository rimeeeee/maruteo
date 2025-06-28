from app import db, create_app
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # 청년 계정 생성
    if not User.query.filter_by(username='youth_user').first():
        youth = User(
            username='youth_user',
            password=generate_password_hash('password123'),
            name='테스트청년',
            role='student',
            email='youth_user@test.com',
            profile_image='',
            bio='테스트용 청년 계정'
        )
        db.session.add(youth)
        print('청년 계정 생성 완료')
    else:
        print('청년 계정 이미 존재')

    # 어르신 계정 생성
    if not User.query.filter_by(username='instructor_user').first():
        instructor = User(
            username='instructor_user',
            password=generate_password_hash('password123'),
            name='테스트어르신',
            role='instructor',
            email='instructor_user@test.com',
            profile_image='',
            bio='테스트용 어르신 계정'
        )
        db.session.add(instructor)
        print('어르신 계정 생성 완료')
    else:
        print('어르신 계정 이미 존재')

    db.session.commit()
    print('DB 커밋 완료') 