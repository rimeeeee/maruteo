from flask import Blueprint, jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User, Talent
from app import db

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
        'want_talents': [t.name for t in user.want_talents]
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

    # # 가진 재능 설정
    # have_names = data.get('have_talents', [])
    # user.have_talents = []
    # for name in have_names:
    #     talent = Talent.query.filter_by(name=name).first()
    #     if not talent:
    #         talent = Talent(name=name)
    #         db.session.add(talent)
    #     user.have_talents.append(talent)

    # # 배우고 싶은 재능 설정
    # want_names = data.get('want_talents', [])
    # user.want_talents = []
    # for name in want_names:
    #     talent = Talent.query.filter_by(name=name).first()
    #     if not talent:
    #         talent = Talent(name=name)
    #         db.session.add(talent)
    #     user.want_talents.append(talent)

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