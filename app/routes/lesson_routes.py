from flask import Blueprint, request, jsonify
from app import db
from app.models.lesson import Lesson
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

lesson_bp = Blueprint('lesson', __name__)

#수업 등록
# @lesson_bp.route('/lesson', methods=['POST'])
# @jwt_required()
# def create_lesson():
#     current_user = get_jwt_identity()
#     data = request.get_json()

#     lesson = Lesson(
#         title=data['title'],
#         description=data['description'],
#         location=data['location'],
#         date=data['date'],
#         instructor_id=int(get_jwt_identity())
#     )

#     db.session.add(lesson)
#     db.session.commit()

#     return jsonify(message='수업 등록 완료'), 201



#수업등록
@lesson_bp.route('/lesson', methods=['POST'])
@jwt_required()
def create_lesson():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    lesson = Lesson(
        title=data.get('title'),
        description=data.get('description'),
        location=data.get('location'),
        time=data.get('time'),
        unavailable=data.get('unavailable', []),
        media_url=data.get('media_url'),
        instructor_id=user.id
    )

    db.session.add(lesson)
    db.session.commit()

    return jsonify({'msg': 'Lesson created successfully'}), 201

# #수업 목록 조회
# @lesson_bp.route('/lesson', methods=['GET'])
# def get_lessons():
#     lessons = Lesson.query.all()
#     return jsonify([lesson.to_dict() for lesson in lessons])

# 수업 목록 조회 (내가 등록한 수업만 보기)
@lesson_bp.route('/lesson', methods=['GET'])
@jwt_required()
def get_lessons():
    user_id = get_jwt_identity()
    lessons = Lesson.query.filter_by(instructor_id=user_id).all()

    lesson_list = []
    for lesson in lessons:
        lesson_list.append({
            'id': lesson.id,
            'title': lesson.title,
            'description': lesson.description,
            'location': lesson.location,
            'time': lesson.time,
            'unavailable': lesson.unavailable,
            'media_url': lesson.media_url
        })

    return jsonify(lesson_list), 200


# 내 수업 삭제
@lesson_bp.route('/lesson/<int:lesson_id>', methods=['DELETE'])
@jwt_required()
def delete_lesson(lesson_id):
    user_id = get_jwt_identity()
    lesson = Lesson.query.filter_by(id=lesson_id, instructor_id=user_id).first()

    if not lesson:
        return jsonify({'msg': '수업을 찾을 수 없거나 삭제 권한이 없습니다'}), 404

    db.session.delete(lesson)
    db.session.commit()

    return jsonify({'msg': '수업이 삭제되었습니다'}), 200