from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User, Talent
from app import db
from datetime import datetime

profile_bp = Blueprint('profile_routes', __name__)



#프로필 조회
@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'role': user.role,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'birth': user.birth,
        'gender': user.gender,
        'address': user.address,
        'bio': user.bio,
        'username': user.username,
        'profile_image': user.profile_image,
        'have_talents': [t.name for t in user.have_talents],
        'want_talents': [t.name for t in user.want_talents],
        'badges': get_user_badges(user)
    }), 200

#프로필 수정
@profile_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    data = request.get_json()

    user.gender = data.get('gender', user.gender)
    user.address = data.get('address', user.address)
    user.bio = data.get('bio', user.bio)
    user.username = data.get('username', user.username)
    user.profile_image = data.get('profile_image', user.profile_image)

    # 가진 재능 설정
    have_names = data.get('have_talents', [])
    user.have_talents.clear()
    for name in have_names:
        talent = Talent.query.filter_by(name=name).first()
        if not talent:
            talent = Talent(name=name)
            db.session.add(talent)
        user.have_talents.append(talent)

    # 배우고 싶은 재능 설정
    want_names = data.get('want_talents', [])
    user.want_talents.clear()
    for name in want_names:
        talent = Talent.query.filter_by(name=name).first()
        if not talent:
            talent = Talent(name=name)
            db.session.add(talent)
        user.want_talents.append(talent)

    db.session.commit()
    return jsonify({'msg': 'Profile updated successfully'}), 200


# 프로핗 뱃지 로직
def get_user_badges(user):
    badges = []

    # 1. 찜 10회 이상
    if hasattr(user, 'liked_lessons') and len(user.liked_lessons) >= 10:
        badges.append("찜 10회 이상")

    # 2. 수업 10회 이상
    if hasattr(user, 'lessons') and len(user.lessons) >= 10:
        badges.append("수업 진행 10회 이상")

    # 3. 활동 기간 1년 이상
    if user.created_at and (datetime.utcnow() - user.created_at).days >= 365:
        badges.append("활동 1년 이상")

    # 4. 출석/약속 이행률 90% 이상
    if hasattr(user, 'attendance_rate') and user.attendance_rate >= 0.9:
        badges.append("출석 90% 이상")

    return badges