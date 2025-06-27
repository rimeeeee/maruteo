from flask import Blueprint, jsonify, request
from app.database import db
from app.models.category import Category, SubCategory
from app.models.lesson import Lesson
from app.models.user import User
from app.models.review import Review
from app.models.application import Application
from sqlalchemy import func, desc, asc
from flask_login import current_user

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    """모든 분류 정보를 가져옴"""
    try:
        categories = Category.query.all()
        
        categories_data = []
        for category in categories:
            category_dict = {
                'id': category.category_id,
                'name': category.name,
                'sub_categories': []
            }
            
            for sub_category in category.sub_categories:
                sub_category_dict = {
                    'id': sub_category.sub_category_id,
                    'name': sub_category.name,
                    'categoryId': sub_category.category_id
                }
                category_dict['sub_categories'].append(sub_category_dict)
            
            categories_data.append(category_dict)
        
        return jsonify({
            'success': True,
            'data': categories_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@category_bp.route('/categories/<category_id>/subcategories', methods=['GET'])
def get_subcategories(category_id):
    """특정 대분류의 소분류들을 가져옴"""
    try:
        category = Category.query.filter_by(category_id=category_id).first()
        
        if not category:
            return jsonify({
                'success': False,
                'message': '분류를 찾을 수 없습니다.'
            }), 404
        
        sub_categories_data = []
        for sub_category in category.sub_categories:
            sub_category_dict = {
                'id': sub_category.sub_category_id,
                'name': sub_category.name,
                'categoryId': sub_category.category_id
            }
            sub_categories_data.append(sub_category_dict)
        
        return jsonify({
            'success': True,
            'data': sub_categories_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@category_bp.route('/talent-exploration/<sub_category_id>/instructors', methods=['GET'])
def get_instructors_by_subcategory(sub_category_id):
    """특정 소분류의 강사 목록을 가져옴 (재능탐색 페이지)"""
    try:
        # 쿼리 파라미터 가져오기
        sort_by = request.args.get('sort', 'latest')  # latest, popular, wish_count, rating
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # 현재 로그인한 사용자의 역할 확인
        user_role = None
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            user_role = current_user.role
        
        # 해당 소분류의 수업들을 가져옴
        lessons_query = Lesson.query.filter_by(sub_category_id=sub_category_id)
        
        # 역할에 따른 필터링
        if user_role == 'student':  # 청년이 로그인한 경우
            # 어르신이 만든 수업만 보여줌
            lessons_query = lessons_query.join(User).filter(User.role == 'instructor')
        elif user_role == 'instructor':  # 어르신이 로그인한 경우
            # 청년이 만든 수업만 보여줌
            lessons_query = lessons_query.join(User).filter(User.role == 'student')
        
        lessons = lessons_query.all()
        
        # 강사별로 데이터 집계
        instructor_data = {}
        
        for lesson in lessons:
            instructor_id = lesson.instructor_id
            
            if instructor_id not in instructor_data:
                # 강사 정보 가져오기
                instructor = User.query.get(instructor_id)
                if not instructor:
                    continue
                
                # 해당 강사의 모든 수업들
                instructor_lessons = Lesson.query.filter_by(instructor_id=instructor_id).all()
                
                # 평균 별점 계산
                total_rating = 0
                review_count = 0
                for l in instructor_lessons:
                    reviews = Review.query.filter_by(lesson_id=l.id).all()
                    for review in reviews:
                        total_rating += review.rating
                        review_count += 1
                
                avg_rating = total_rating / review_count if review_count > 0 else 0
                
                # 총 찜수 계산
                total_wish_count = 0
                for l in instructor_lessons:
                    wish_count = len(l.wished_by)
                    total_wish_count += wish_count
                
                # 총 신청수 계산
                total_application_count = 0
                for l in instructor_lessons:
                    app_count = Application.query.filter_by(lesson_id=l.id).count()
                    total_application_count += app_count
                
                instructor_data[instructor_id] = {
                    'id': instructor.id,
                    'name': instructor.name,
                    'username': instructor.username,
                    'profile_image': instructor.profile_image,
                    'bio': instructor.bio,
                    'avg_rating': round(avg_rating, 1),
                    'review_count': review_count,
                    'total_wish_count': total_wish_count,
                    'total_application_count': total_application_count,
                    'lesson_count': len(instructor_lessons),
                    'latest_lesson_date': max([l.created_at for l in instructor_lessons]) if instructor_lessons else None
                }
        
        # 정렬
        instructors_list = list(instructor_data.values())
        
        if sort_by == 'latest':
            # 최신순 (최근 수업 등록일 기준)
            instructors_list.sort(key=lambda x: x['latest_lesson_date'] or '', reverse=True)
        elif sort_by == 'popular':
            # 인기순 (신청수 기준)
            instructors_list.sort(key=lambda x: x['total_application_count'], reverse=True)
        elif sort_by == 'wish_count':
            # 찜많은순
            instructors_list.sort(key=lambda x: x['total_wish_count'], reverse=True)
        elif sort_by == 'rating':
            # 별점높은순
            instructors_list.sort(key=lambda x: x['avg_rating'], reverse=True)
        
        # 페이징
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_instructors = instructors_list[start_idx:end_idx]
        
        return jsonify({
            'success': True,
            'data': {
                'instructors': paginated_instructors,
                'total_count': len(instructors_list),
                'page': page,
                'per_page': per_page,
                'total_pages': (len(instructors_list) + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@category_bp.route('/talent-exploration/instructors/<int:instructor_id>/detail', methods=['GET'])
def get_instructor_detail(instructor_id):
    """강사 상세 정보를 가져옴"""
    try:
        # 강사 정보 가져오기
        instructor = User.query.get_or_404(instructor_id)
        
        # 해당 강사의 모든 수업들
        instructor_lessons = Lesson.query.filter_by(instructor_id=instructor_id).all()
        
        # 평균 별점 및 신뢰도 계산
        total_rating = 0
        review_count = 0
        all_reviews = []
        
        for lesson in instructor_lessons:
            reviews = Review.query.filter_by(lesson_id=lesson.id).all()
            for review in reviews:
                total_rating += review.rating
                review_count += 1
                all_reviews.append(review)
        
        avg_rating = total_rating / review_count if review_count > 0 else 0
        
        # 신뢰도 계산 (별점 + 리뷰수 + 수업수 기준)
        trust_score = 0
        if avg_rating >= 4.5:
            trust_score += 30
        elif avg_rating >= 4.0:
            trust_score += 20
        elif avg_rating >= 3.5:
            trust_score += 10
        
        if review_count >= 10:
            trust_score += 30
        elif review_count >= 5:
            trust_score += 20
        elif review_count >= 1:
            trust_score += 10
        
        if len(instructor_lessons) >= 5:
            trust_score += 40
        elif len(instructor_lessons) >= 3:
            trust_score += 30
        elif len(instructor_lessons) >= 1:
            trust_score += 20
        
        # 강사가 가진 카테고리들 수집
        categories = set()
        for lesson in instructor_lessons:
            if lesson.sub_category_id:
                sub_category = SubCategory.query.filter_by(sub_category_id=lesson.sub_category_id).first()
                if sub_category and sub_category.category:
                    categories.add(sub_category.category.name)
        
        # 진행중인 수업 목록 (현재는 모든 수업을 진행중으로 간주)
        active_lessons = []
        for lesson in instructor_lessons:
            # 신청수 계산
            app_count = Application.query.filter_by(lesson_id=lesson.id).count()
            
            # 찜수 계산
            wish_count = len(lesson.wished_by)
            
            # 평균 별점 계산
            lesson_reviews = Review.query.filter_by(lesson_id=lesson.id).all()
            lesson_avg_rating = 0
            lesson_review_count = 0
            if lesson_reviews:
                lesson_avg_rating = sum(review.rating for review in lesson_reviews) / len(lesson_reviews)
                lesson_review_count = len(lesson_reviews)
            
            lesson_data = {
                'id': lesson.id,
                'title': lesson.title,
                'description': lesson.description,
                'location': lesson.location,
                'time': lesson.time,
                'image_url': lesson.image_url,
                'application_count': app_count,
                'wish_count': wish_count,
                'avg_rating': round(lesson_avg_rating, 1),
                'review_count': lesson_review_count,
                'created_at': lesson.created_at.strftime('%Y-%m-%d %H:%M') if lesson.created_at else None
            }
            active_lessons.append(lesson_data)
        
        # 강사 상세 정보 구성
        instructor_detail = {
            'id': instructor.id,
            'name': instructor.name,
            'username': instructor.username,
            'profile_image': instructor.profile_image,
            'bio': instructor.bio,
            'phone': instructor.phone,
            'email': instructor.email,
            'role': instructor.role,
            'categories': list(categories),  # 어떤 재능기부자인지 카테고리명
            'trust_score': min(trust_score, 100),  # 신뢰도 (0-100)
            'avg_rating': round(avg_rating, 1),
            'review_count': review_count,
            'total_lesson_count': len(instructor_lessons),  # 수업 개설수
            'active_lessons': active_lessons  # 진행중인 수업 목록
        }
        
        return jsonify({
            'success': True,
            'data': instructor_detail
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@category_bp.route('/talent-exploration/<sub_category_id>/instructors/<int:instructor_id>/lessons', methods=['GET'])
def get_instructor_lessons(sub_category_id, instructor_id):
    """특정 강사의 해당 소분류 수업들을 가져옴"""
    try:
        lessons = Lesson.query.filter_by(
            sub_category_id=sub_category_id,
            instructor_id=instructor_id
        ).all()
        
        lessons_data = []
        for lesson in lessons:
            lesson_dict = lesson.to_dict()
            
            # 신청수 계산
            app_count = Application.query.filter_by(lesson_id=lesson.id).count()
            lesson_dict['application_count'] = app_count
            
            # 찜수 계산
            wish_count = len(lesson.wished_by)
            lesson_dict['wish_count'] = wish_count
            
            # 평균 별점 계산
            reviews = Review.query.filter_by(lesson_id=lesson.id).all()
            if reviews:
                avg_rating = sum(review.rating for review in reviews) / len(reviews)
                lesson_dict['avg_rating'] = round(avg_rating, 1)
                lesson_dict['review_count'] = len(reviews)
            else:
                lesson_dict['avg_rating'] = 0
                lesson_dict['review_count'] = 0
            
            lessons_data.append(lesson_dict)
        
        return jsonify({
            'success': True,
            'data': lessons_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500 