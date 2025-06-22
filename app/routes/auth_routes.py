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
    hashed_pw = generate_password_hash(data['password'])
    user = User(name=data['name'], email=data['email'], password=hashed_pw, role=data['role'])
    db.session.add(user)
    db.session.commit()
    return jsonify(message='가입 성공'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(token=token)
    return jsonify(message='로그인 실패'), 401