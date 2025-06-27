from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.attendance import LessonAttendance
from app import db

mypage_bp = Blueprint('mypage', __name__)

# 출석 및 약속 이행률 계산
@mypage_bp.route('/mypage/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    user_id = get_jwt_identity()

    records = LessonAttendance.query.filter_by(user_id=user_id).all()
    total = len(records)

    if total == 0:
        return jsonify({
            'attendance_rate': 0,
            'fulfillment_rate': 0
        }), 200

    attended = sum([1 for r in records if r.attended])
    fulfilled = sum([1 for r in records if r.fulfilled])

    return jsonify({
        'attendance_rate': round(attended / total * 100, 2),
        'fulfillment_rate': round(fulfilled / total * 100, 2)
    }), 200


#뱃지 계산
from datetime import datetime, timedelta
from app.models.lesson import Lesson
from app.models.attendance import LessonAttendance
from app.models.user import User

@mypage_bp.route('/mypage/badges', methods=['GET'])
@jwt_required()
def get_badges():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    badges = {
        '찜 10회 이상': False,
        '수업 진행 10회 이상': False,
        '활동 기간 1년 이상': False,
        '출석 및 약속 이행률 90% 이상': False
    }

    # 1) 수업 찜 횟수 (찜 기능이 구현되어 있어야 함. 현재는 예시로 0 처리)
    total_likes = 0  # TODO: 찜 모델 만들어서 count 넣기
    if total_likes >= 10:
        badges['찜 10회 이상'] = True

    # 2) 수업 진행 횟수
    lesson_count = Lesson.query.filter_by(instructor_id=user_id).count()
    if lesson_count >= 10:
        badges['수업 진행 10회 이상'] = True

    # 3) 활동 기간 1년 이상
    joined_at = user.created_at or datetime.utcnow()  # created_at 필드가 없으면 지금 시간
    if (datetime.utcnow() - joined_at) >= timedelta(days=365):
        badges['활동 기간 1년 이상'] = True

    # 4) 출석/이행률 90% 이상
    records = LessonAttendance.query.filter_by(user_id=user_id).all()
    total = len(records)
    if total > 0:
        attended = sum([1 for r in records if r.attended])
        fulfilled = sum([1 for r in records if r.fulfilled])
        attendance_rate = attended / total
        fulfillment_rate = fulfilled / total

        if attendance_rate >= 0.9 and fulfillment_rate >= 0.9:
            badges['출석 및 약속 이행률 90% 이상'] = True

    return jsonify({'badges': badges}), 200