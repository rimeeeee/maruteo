from flask import Blueprint, request, jsonify
from app import db
from app.models.lesson import Lesson
from flask_jwt_extended import jwt_required, get_jwt_identity

lesson_bp = Blueprint('lesson', __name__)

#수업 등록록
@lesson_bp.route('/lesson', methods=['POST'])
@jwt_required()
def create_lesson():
    current_user = get_jwt_identity()
    data = request.get_json()

    lesson = Lesson(
        title=data['title'],
        description=data['description'],
        location=data['location'],
        date=data['date'],
        instructor_id=int(get_jwt_identity())
    )

    db.session.add(lesson)
    db.session.commit()

    return jsonify(message='수업 등록 완료'), 201


#수업 목록 조회
@lesson_bp.route('/lesson', methods=['GET'])
def get_lessons():
    lessons = Lesson.query.all()
    return jsonify([lesson.to_dict() for lesson in lessons])

