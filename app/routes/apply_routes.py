#수업 신청 라우터
from flask import Blueprint, request, jsonify
from app import db
from app.models.application import Application
from flask_jwt_extended import jwt_required, get_jwt_identity

apply_bp = Blueprint('apply', __name__)

@apply_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_lesson():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    lesson_id = data.get('lesson_id')
    if not lesson_id:
        return jsonify(message="lesson_id is required"), 400

    application = Application(user_id=user_id, lesson_id=lesson_id)
    db.session.add(application)
    db.session.commit()

    return jsonify(message="수업 신청 완료"), 201

@apply_bp.route('/apply', methods=['GET'])
@jwt_required()
def get_my_applications():
    user_id = int(get_jwt_identity())
    applications = Application.query.filter_by(user_id=user_id).all()
    return jsonify([a.to_dict() for a in applications])