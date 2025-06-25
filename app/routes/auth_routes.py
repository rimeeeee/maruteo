#회원가입/로그인 API
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User, Talent
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)  

# 회원가입 API
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # 중복 이메일 검사
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "이미 가입된 이메일입니다"}), 400

    # 비밀번호 확인 검사
    if data['password'] != data['confirm_password']:
        return jsonify({"message": "비밀번호가 일치하지 않습니다"}), 400

    # 비밀번호 해싱
    hashed_pw = generate_password_hash(data['password'])

    # 유저 생성
    user = User(
        role=data['role'],
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        birth=data['birth'],
        password=hashed_pw,
        gender=data.get('gender'),
        address=data.get('address'),
        bio=data.get('bio'),
        username=data.get('username'),
        profile_image=data.get('profile_image')
    )

    # 💡 보유 재능 등록
    have_names = data.get('have_talents', [])
    for name in have_names:
        talent = Talent.query.filter_by(name=name).first()
        if not talent:
            talent = Talent(name=name)
            db.session.add(talent)
        user.have_talents.append(talent)

    # 💡 배우고 싶은 재능 등록
    want_names = data.get('want_talents', [])
    for name in want_names:
        talent = Talent.query.filter_by(name=name).first()
        if not talent:
            talent = Talent(name=name)
            db.session.add(talent)
        user.want_talents.append(talent)

    db.session.add(user)
    db.session.commit()

    return jsonify(message='가입 성공'), 201



# 로그인 API
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify(message="이메일 또는 비밀번호가 올바르지 않습니다"), 401

    token = create_access_token(identity=str(user.id))

    user_info = {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "userType": "elder" if user.role == "어르신" else "young",
        "phone": user.phone,
        "birthDate": user.birth
    }

    return jsonify(accessToken=token, user=user_info), 200