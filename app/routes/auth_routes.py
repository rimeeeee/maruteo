#회원가입/로그인 API
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)  

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # 비밀번호 확인 검사
    if data['password'] != data['password_check']:
        return jsonify(message='비밀번호가 일치하지 않습니다'), 400
    
    # 중복 이메일 검사
    if User.query.filter_by(email=data['email']).first():
        return jsonify(message='이미 등록된 이메일입니다'), 409

    hashed_pw = generate_password_hash(data['password'])

    user = User(
        role=data['role'],
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        birth=data['birth'],
        password=hashed_pw
    )
    
    db.session.add(user)
    db.session.commit()
    return jsonify(message='가입 성공'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify(token=token)
    return jsonify(message='로그인 실패'), 401