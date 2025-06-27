from flask import Blueprint, request, jsonify
from app import db
from app.models.lesson import Lesson
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.review import Review
from app.models.application import Application
from app.models.category import SubCategory
from flask_login import current_user
import json

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

@lesson_bp.route('/lessons/<int:lesson_id>/detail', methods=['GET'])
def get_lesson_detail(lesson_id):
    """수업 상세 정보를 가져옴"""
    try:
        # 수업 정보 가져오기
        lesson = Lesson.query.get_or_404(lesson_id)
        
        # 강사 정보 가져오기
        instructor = User.query.get(lesson.instructor_id)
        
        # 분류 정보 가져오기
        sub_category_name = None
        category_name = None
        if lesson.sub_category_id:
            sub_category = SubCategory.query.filter_by(sub_category_id=lesson.sub_category_id).first()
            if sub_category:
                sub_category_name = sub_category.name
                if sub_category.category:
                    category_name = sub_category.category.name
        
        # 신청수 계산
        application_count = Application.query.filter_by(lesson_id=lesson.id).count()
        
        # 찜수 계산
        wish_count = len(lesson.wished_by)
        
        # 현재 사용자가 찜했는지 확인
        is_wished = False
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            is_wished = lesson in current_user.wished_lessons
        
        # 평균 별점 계산
        reviews = Review.query.filter_by(lesson_id=lesson.id).all()
        avg_rating = 0
        review_count = 0
        if reviews:
            avg_rating = sum(review.rating for review in reviews) / len(reviews)
            review_count = len(reviews)
        
        # 준비물 리스트 파싱
        materials_list = []
        if lesson.materials:
            try:
                materials_list = json.loads(lesson.materials)
            except:
                materials_list = []
        
        # 수업 상세 정보 구성
        lesson_detail = {
            'id': lesson.id,
            'title': lesson.title,  # 3. 수업 명칭
            'description': lesson.description,  # 8. 수업 소개
            'location': lesson.location,
            'time': lesson.time,  # 9. 수업진행시간
            'image_url': lesson.image_url,  # 2. 사진
            'video_url': lesson.video_url,  # 2. 동영상
            'materials': materials_list,  # 10. 준비물 리스트
            
            # 강사 정보
            'instructor': {
                'id': instructor.id if instructor else None,
                'name': instructor.name if instructor else None,  # 5. 재능기부자 이름
                'profile_image': instructor.profile_image if instructor else None,  # 4. 재능기부자 사진
                'bio': instructor.bio if instructor else None,
                'role': instructor.role if instructor else None
            },
            
            # 카테고리 정보
            'category': {
                'name': category_name,  # 6. 어떤 카테고리 재능기부자인지
                'sub_category_name': sub_category_name
            },
            
            # 통계 정보
            'stats': {
                'application_count': application_count,
                'wish_count': wish_count,  # 1. 찜기능 - 누르면 +1
                'avg_rating': round(avg_rating, 1),
                'review_count': review_count
            },
            
            # 현재 사용자 관련
            'user_info': {
                'is_wished': is_wished,  # 현재 사용자가 찜했는지
                'can_apply': True  # 신청 가능 여부 (추후 로직 추가 가능)
            },
            
            'created_at': lesson.created_at.strftime('%Y-%m-%d %H:%M') if lesson.created_at else None
        }
        
        return jsonify({
            'success': True,
            'data': lesson_detail
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@lesson_bp.route('/lessons/<int:lesson_id>/wish', methods=['POST'])
def toggle_lesson_wish(lesson_id):
    """수업 찜하기/찜해제"""
    try:
        lesson = Lesson.query.get_or_404(lesson_id)
        
        if lesson in current_user.wished_lessons:
            # 이미 찜한 경우 찜해제
            current_user.wished_lessons.remove(lesson)
            action = 'removed'
        else:
            # 찜하지 않은 경우 찜하기
            current_user.wished_lessons.append(lesson)
            action = 'added'
        
        db.session.commit()
        
        # 업데이트된 찜수 반환
        wish_count = len(lesson.wished_by)
        
        return jsonify({
            'success': True,
            'action': action,
            'wish_count': wish_count,
            'message': f'찜하기가 {action}되었습니다.'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@lesson_bp.route('/lessons/<int:lesson_id>/apply', methods=['POST'])
def apply_lesson(lesson_id):
    """수업 신청"""
    try:
        lesson = Lesson.query.get_or_404(lesson_id)
        
        # 이미 신청했는지 확인
        existing_application = Application.query.filter_by(
            lesson_id=lesson_id,
            user_id=current_user.id
        ).first()
        
        if existing_application:
            return jsonify({
                'success': False,
                'message': '이미 신청한 수업입니다.'
            }), 400
        
        # 새로운 신청 생성
        application = Application(
            lesson_id=lesson_id,
            user_id=current_user.id,
            status='pending'  # 대기중 상태
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '수업 신청이 완료되었습니다.'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500