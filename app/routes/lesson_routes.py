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

# 수업 목록 조회 (역할에 따른 필터링)
@lesson_bp.route('/lesson', methods=['GET'])
@jwt_required()
def get_lessons():
    user_id = get_jwt_identity()
    current_user = User.query.get(int(user_id))
    
    if not current_user:
        return jsonify({'msg': 'User not found'}), 404
    
    # 사용자 역할에 따른 필터링
    if current_user.role == 'young':  # 청년인 경우
        # 어르신이 등록한 수업만 조회
        lessons = Lesson.query.join(User).filter(
            User.role == 'elder'
        ).all()
    elif current_user.role == 'elder':  # 어르신인 경우
        # 청년이 등록한 수업만 조회
        lessons = Lesson.query.join(User).filter(
            User.role == 'young'
        ).all()
    else:
        # 기본적으로 모든 수업 조회 (관리자 등)
        lessons = Lesson.query.all()

    lesson_list = []
    for lesson in lessons:
        # 강사 정보 가져오기
        instructor = User.query.get(lesson.instructor_id)
        
        lesson_list.append({
            'id': lesson.id,
            'title': lesson.title,
            'description': lesson.description,
            'location': lesson.location,
            'time': lesson.time,
            'unavailable': lesson.unavailable,
            'media_url': lesson.media_url,
            'instructor_name': instructor.name if instructor else None,
            'instructor_role': instructor.role if instructor else None
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

@lesson_bp.route('/lessons/<int:lesson_id>/apply-form', methods=['GET'])
def get_lesson_apply_form(lesson_id):
    """수업 신청 폼 정보를 가져옴"""
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
        
        # 찜수 계산
        wish_count = len(lesson.wished_by)
        
        # 평균 별점 계산
        reviews = Review.query.filter_by(lesson_id=lesson.id).all()
        avg_rating = 0
        review_count = 0
        if reviews:
            avg_rating = sum(review.rating for review in reviews) / len(reviews)
            review_count = len(reviews)
        
        # 신청수 계산
        application_count = Application.query.filter_by(lesson_id=lesson.id).count()
        
        # 수업 신청 폼 정보 구성
        apply_form = {
            'lesson': {
                'id': lesson.id,
                'title': lesson.title,  # 2. 수업명
                'image_url': lesson.image_url,  # 1. 수업 사진
                'location': lesson.location,  # 6. 수업 장소(주소지)
                'time': lesson.time,  # 수업 시간
                'description': lesson.description,
                'avg_rating': round(avg_rating, 1),  # 3. 별점
                'review_count': review_count,
                'wish_count': wish_count,  # 4. 찜수
                'application_count': application_count,  # 7. 인원수 (신청수)
                'unavailable': lesson.unavailable  # 안되는 요일, 시간대
            },
            
            'instructor': {
                'id': instructor.id if instructor else None,
                'name': instructor.name if instructor else None,
                'profile_image': instructor.profile_image if instructor else None,
                'role': instructor.role if instructor else None
            },
            
            'category': {
                'name': category_name,
                'sub_category_name': sub_category_name
            }
        }
        
        return jsonify({
            'success': True,
            'data': apply_form
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@lesson_bp.route('/lessons/<int:lesson_id>/apply', methods=['POST'])
def apply_lesson(lesson_id):
    """수업 신청"""
    try:
        data = request.get_json()
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
        
        # 신청 데이터 추출
        selected_date = data.get('selected_date')  # 5. 수업 날짜
        selected_time = data.get('selected_time')  # 선택한 시간대
        
        # 안되는 요일/시간대 체크
        if lesson.unavailable:
            unavailable_days = lesson.unavailable.get('days', [])
            unavailable_times = lesson.unavailable.get('times', [])
            
            # 요일 체크 (예: '월', '화', '수' 등)
            import datetime
            if selected_date:
                date_obj = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
                day_name = ['월', '화', '수', '목', '금', '토', '일'][date_obj.weekday()]
                
                if day_name in unavailable_days:
                    return jsonify({
                        'success': False,
                        'message': f'{day_name}요일은 수업이 불가능합니다.'
                    }), 400
            
            # 시간대 체크
            if selected_time and selected_time in unavailable_times:
                return jsonify({
                    'success': False,
                    'message': f'{selected_time} 시간대는 수업이 불가능합니다.'
                }), 400
        
        # 새로운 신청 생성
        application = Application(
            lesson_id=lesson_id,
            user_id=current_user.id,
            status='pending',  # 대기중 상태
            selected_date=selected_date,
            selected_time=selected_time
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

# 역할별 수업 목록 조회 (청년은 어르신 수업만, 어르신은 청년 수업만)
@lesson_bp.route('/lessons/filtered', methods=['GET'])
@jwt_required()
def get_filtered_lessons():
    user_id = get_jwt_identity()
    current_user = User.query.get(int(user_id))
    
    if not current_user:
        return jsonify({'msg': 'User not found'}), 404
    
    # 사용자 역할에 따른 필터링
    if current_user.role == 'young':  # 청년인 경우
        # 어르신이 등록한 수업만 조회
        lessons = Lesson.query.join(User).filter(
            User.role == 'elder'
        ).all()
    elif current_user.role == 'elder':  # 어르신인 경우
        # 청년이 등록한 수업만 조회
        lessons = Lesson.query.join(User).filter(
            User.role == 'young'
        ).all()
    else:
        # 기본적으로 모든 수업 조회 (관리자 등)
        lessons = Lesson.query.all()

    lesson_list = []
    for lesson in lessons:
        # 강사 정보 가져오기
        instructor = User.query.get(lesson.instructor_id)
        
        # 신청수 계산
        application_count = Application.query.filter_by(lesson_id=lesson.id).count()
        
        # 찜수 계산
        wish_count = len(lesson.wished_by)
        
        # 평균 별점 계산
        reviews = Review.query.filter_by(lesson_id=lesson.id).all()
        avg_rating = 0
        review_count = 0
        if reviews:
            avg_rating = sum(review.rating for review in reviews) / len(reviews)
            review_count = len(reviews)
        
        lesson_list.append({
            'id': lesson.id,
            'title': lesson.title,
            'description': lesson.description,
            'location': lesson.location,
            'time': lesson.time,
            'unavailable': lesson.unavailable,
            'media_url': lesson.media_url,
            'image_url': lesson.image_url,
            'instructor_name': instructor.name if instructor else None,
            'instructor_role': instructor.role if instructor else None,
            'instructor_profile_image': instructor.profile_image if instructor else None,
            'application_count': application_count,
            'wish_count': wish_count,
            'avg_rating': round(avg_rating, 1),
            'review_count': review_count,
            'created_at': lesson.created_at.strftime('%Y-%m-%d %H:%M') if lesson.created_at else None
        })

    return jsonify({
        'success': True,
        'data': lesson_list
    }), 200

# 프론트엔드 요청에 맞는 수업 목록 조회 API
@lesson_bp.route('/lessons', methods=['GET'])
@jwt_required()
def get_lessons_with_filters():
    """쿼리 파라미터를 지원하는 수업 목록 조회 API"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(int(user_id))
        
        if not current_user:
            return jsonify({'msg': 'User not found'}), 404
        
        # 쿼리 파라미터 가져오기
        category = request.args.get('category')  # 예: korean-food
        instructor_role = request.args.get('instructor_role')  # 예: elder, young
        sort = request.args.get('sort', 'latest')  # 예: latest, popular, rating
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # 기본 쿼리 시작 (User와 JOIN)
        query = Lesson.query.join(User, Lesson.instructor_id == User.id)
        
        # 역할에 따른 필터링 (기본 필터)
        if current_user.role == 'young':  # 청년인 경우
            # 어르신이 등록한 수업만 조회
            query = query.filter(User.role == 'elder')
        elif current_user.role == 'elder':  # 어르신인 경우
            # 청년이 등록한 수업만 조회
            query = query.filter(User.role == 'young')
        
        # 추가 필터링
        if category:
            # 카테고리 필터링 (sub_category_id로)
            query = query.filter(Lesson.sub_category_id == category)
        
        if instructor_role:
            # 강사 역할 필터링 (이미 JOIN된 User 테이블 사용)
            if instructor_role == 'elder':
                query = query.filter(User.role == 'elder')
            elif instructor_role == 'young':
                query = query.filter(User.role == 'young')
        
        # 정렬
        if sort == 'latest':
            query = query.order_by(Lesson.created_at.desc())
        elif sort == 'popular':
            # 신청수 기준 정렬 (복잡하므로 간단하게)
            query = query.order_by(Lesson.created_at.desc())
        elif sort == 'rating':
            # 별점 기준 정렬 (복잡하므로 간단하게)
            query = query.order_by(Lesson.created_at.desc())
        
        # 페이지네이션
        offset = (page - 1) * limit
        lessons = query.offset(offset).limit(limit).all()
        
        # 전체 개수 계산 (페이지네이션용)
        total_count = query.count()
        
        # 결과 데이터 구성
        lesson_list = []
        for lesson in lessons:
            # 강사 정보 가져오기
            instructor = User.query.get(lesson.instructor_id)
            
            # 신청수 계산
            application_count = Application.query.filter_by(lesson_id=lesson.id).count()
            
            # 찜수 계산
            wish_count = len(lesson.wished_by)
            
            # 평균 별점 계산
            reviews = Review.query.filter_by(lesson_id=lesson.id).all()
            avg_rating = 0
            review_count = 0
            if reviews:
                avg_rating = sum(review.rating for review in reviews) / len(reviews)
                review_count = len(reviews)
            
            lesson_data = {
                'id': lesson.id,
                'title': lesson.title,
                'description': lesson.description,
                'location': lesson.location,
                'time': lesson.time,
                'unavailable': lesson.unavailable,
                'media_url': lesson.media_url,
                'image_url': lesson.image_url,
                'video_url': lesson.video_url,
                'sub_category_id': lesson.sub_category_id,
                'max_students': lesson.max_students,
                'price': lesson.price,
                'instructor_name': instructor.name if instructor else None,
                'instructor_role': instructor.role if instructor else None,
                'instructor_profile_image': instructor.profile_image if instructor else None,
                'application_count': application_count,
                'wish_count': wish_count,
                'avg_rating': round(avg_rating, 1),
                'review_count': review_count,
                'created_at': lesson.created_at.strftime('%Y-%m-%d %H:%M') if lesson.created_at else None
            }
            lesson_list.append(lesson_data)
        
        return jsonify({
            'success': True,
            'data': lesson_list,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'total_pages': (total_count + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500