from flask import Blueprint, jsonify, request
from app.database import db
from app.models.lesson import Lesson, wishlist
from app.models.user import User
from app.models.application import Application
from app.models.category import Category, SubCategory
from app.models.review import Review
from sqlalchemy import func, desc
from flask_login import login_required, current_user
from functools import wraps
import jwt
from app.config import Config

main_bp = Blueprint('main', __name__)

def jwt_required(f):
    """JWT 토큰 인증 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Authorization 헤더에서 토큰 추출
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # "Bearer <token>"
            except IndexError:
                return jsonify({'message': '토큰이 없습니다!'}), 401
        
        if not token:
            return jsonify({'message': '토큰이 필요합니다!'}), 401
        
        try:
            # 토큰 디코딩
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            # flask_jwt_extended는 identity 키를 사용
            user_id = data.get('sub') or data.get('identity') or data.get('user_id')
            if not user_id:
                return jsonify({'message': '유효하지 않은 토큰입니다!'}), 401
                
            current_user = User.query.get(user_id)
            
            if not current_user:
                return jsonify({'message': '유효하지 않은 토큰입니다!'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '토큰이 만료되었습니다!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '유효하지 않은 토큰입니다!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function

@main_bp.route('/main/popular-lessons', methods=['GET'])
@jwt_required
def get_popular_lessons(current_user):
    """인기 수업 카로셀 - 요리 3개, IT 3개 총 6개"""
    try:
        # 현재 로그인한 사용자의 역할 확인
        user_role = current_user.role
        
        # 간단한 방법으로 모든 수업을 가져와서 분류별로 나누기
        all_lessons_query = Lesson.query
        
        # 역할에 따른 필터링
        if user_role == 'young':  # 청년이 로그인한 경우
            # 어르신이 만든 수업만 보여줌
            all_lessons_query = all_lessons_query.join(User).filter(User.role == 'elder')
        elif user_role == 'elder':  # 어르신이 로그인한 경우
            # 청년이 만든 수업만 보여줌
            all_lessons_query = all_lessons_query.join(User).filter(User.role == 'young')
        
        all_lessons = all_lessons_query.all()
        
        # 요리 수업들 (sub_category_id가 요리 관련인 것들)
        cooking_lessons = []
        it_lessons = []
        
        for lesson in all_lessons:
            if lesson.sub_category_id and 'food' in lesson.sub_category_id:
                cooking_lessons.append(lesson)
            elif lesson.sub_category_id and lesson.sub_category_id in ['programming', 'smartphone-usage', 'computer-usage']:
                it_lessons.append(lesson)
        
        # 각 분류별로 최대 3개씩 선택
        cooking_lessons = cooking_lessons[:3]
        it_lessons = it_lessons[:3]
        
        # 결과 데이터 구성
        lessons_data = []
        
        # 요리 수업들 추가
        for lesson in cooking_lessons:
            lesson_dict = lesson.to_dict()
            # 신청수 계산 (간단하게)
            app_count = Application.query.filter_by(lesson_id=lesson.id).count()
            lesson_dict['application_count'] = app_count
            lessons_data.append(lesson_dict)
        
        # IT 수업들 추가
        for lesson in it_lessons:
            lesson_dict = lesson.to_dict()
            # 신청수 계산 (간단하게)
            app_count = Application.query.filter_by(lesson_id=lesson.id).count()
            lesson_dict['application_count'] = app_count
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

@main_bp.route('/main/wished-lessons', methods=['GET'])
@login_required
def get_wished_lessons():
    """현재 로그인한 사용자가 찜한 수업들"""
    try:
        # 현재 사용자가 찜한 수업들을 가져옴
        wished_lessons = current_user.wished_lessons
        
        lessons_data = []
        for lesson in wished_lessons:
            lesson_dict = lesson.to_dict()
            # 신청수 계산
            app_count = Application.query.filter_by(lesson_id=lesson.id).count()
            lesson_dict['application_count'] = app_count
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

@main_bp.route('/main/popular-instructors', methods=['GET'])
def get_popular_instructors():
    """인기 강사 - 신청수가 많은 순으로 정렬"""
    try:
        # 간단한 방법으로 강사들을 가져옴
        instructors = User.query.filter_by(role='instructor').all()
        
        instructors_data = []
        for instructor in instructors:
            # 해당 강사의 수업들의 신청수 합계 계산
            total_applications = 0
            for lesson in instructor.lessons:
                app_count = Application.query.filter_by(lesson_id=lesson.id).count()
                total_applications += app_count
            
            instructor_data = {
                'id': instructor.id,
                'name': instructor.name,
                'username': instructor.username,
                'profile_image': instructor.profile_image,
                'bio': instructor.bio,
                'total_applications': total_applications,
                'lesson_count': len(instructor.lessons)
            }
            instructors_data.append(instructor_data)
        
        # 신청수 기준으로 정렬
        instructors_data.sort(key=lambda x: x['total_applications'], reverse=True)
        instructors_data = instructors_data[:10]  # 상위 10명만
        
        return jsonify({
            'success': True,
            'data': instructors_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@main_bp.route('/lesson/<int:lesson_id>/wish', methods=['POST'])
@login_required
def toggle_wish_lesson(lesson_id):
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
        
        return jsonify({
            'success': True,
            'action': action,
            'message': f'찜하기가 {action}되었습니다.'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@main_bp.route('/main/dashboard', methods=['GET'])
@jwt_required
def get_main_dashboard(current_user):
    """메인 대시보드 - 모든 데이터를 한번에 가져옴"""
    try:
        # 현재 로그인한 사용자의 역할 확인
        user_role = current_user.role
        
        # 간단한 방법으로 모든 수업을 가져와서 분류별로 나누기
        all_lessons_query = Lesson.query
        
        # 역할에 따른 필터링
        if user_role == 'young':  # 청년이 로그인한 경우
            # 어르신이 만든 수업만 보여줌
            all_lessons_query = all_lessons_query.join(User).filter(User.role == 'elder')
        elif user_role == 'elder':  # 어르신이 로그인한 경우
            # 청년이 만든 수업만 보여줌
            all_lessons_query = all_lessons_query.join(User).filter(User.role == 'young')
        
        all_lessons = all_lessons_query.all()
        
        # 요리 수업들
        cooking_lessons = []
        it_lessons = []
        
        for lesson in all_lessons:
            if lesson.sub_category_id and 'food' in lesson.sub_category_id:
                cooking_lessons.append(lesson)
            elif lesson.sub_category_id and lesson.sub_category_id in ['programming', 'smartphone-usage', 'computer-usage']:
                it_lessons.append(lesson)
        
        # 각 분류별로 최대 3개씩 선택
        cooking_lessons = cooking_lessons[:3]
        it_lessons = it_lessons[:3]
        
        # 인기 수업 데이터 구성
        popular_lessons_data = []
        
        # 요리 수업들 추가
        for lesson in cooking_lessons:
            lesson_dict = lesson.to_dict()
            app_count = Application.query.filter_by(lesson_id=lesson.id).count()
            lesson_dict['application_count'] = app_count
            popular_lessons_data.append(lesson_dict)
        
        # IT 수업들 추가
        for lesson in it_lessons:
            lesson_dict = lesson.to_dict()
            app_count = Application.query.filter_by(lesson_id=lesson.id).count()
            lesson_dict['application_count'] = app_count
            popular_lessons_data.append(lesson_dict)
        
        # 인기 강사 데이터 (역할에 따른 필터링)
        if user_role == 'young':  # 청년이 로그인한 경우
            # 어르신 강사들만 보여줌
            instructors = User.query.filter_by(role='elder').all()
        elif user_role == 'elder':  # 어르신이 로그인한 경우
            # 청년 강사들만 보여줌
            instructors = User.query.filter_by(role='young').all()
        else:
            # 기본적으로 모든 강사
            instructors = User.query.filter(User.role.in_(['young', 'elder'])).all()
        
        popular_instructors_data = []
        
        for instructor in instructors:
            total_applications = 0
            for lesson in instructor.lessons:
                app_count = Application.query.filter_by(lesson_id=lesson.id).count()
                total_applications += app_count
            
            instructor_data = {
                'id': instructor.id,
                'name': instructor.name,
                'username': instructor.username,
                'profile_image': instructor.profile_image,
                'bio': instructor.bio,
                'total_applications': total_applications,
                'lesson_count': len(instructor.lessons)
            }
            popular_instructors_data.append(instructor_data)
        
        # 신청수 기준으로 정렬
        popular_instructors_data.sort(key=lambda x: x['total_applications'], reverse=True)
        popular_instructors_data = popular_instructors_data[:10]
        
        return jsonify({
            'success': True,
            'data': {
                'popular_lessons': popular_lessons_data,
                'popular_instructors': popular_instructors_data
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@main_bp.route('/lessons/by-category/<category_id>', methods=['GET'])
def get_lessons_by_category(category_id):
    """카테고리별 수업 조회"""
    try:
        # 현재 로그인한 사용자의 역할 확인
        user_role = None
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            user_role = current_user.role
        
        # 해당 카테고리의 소분류들 가져오기
        sub_categories = SubCategory.query.filter_by(category_id=category_id).all()
        sub_category_ids = [sub.sub_category_id for sub in sub_categories]
        
        # 해당 소분류들의 수업들 가져오기
        if sub_category_ids:
            lessons_query = Lesson.query.filter(Lesson.sub_category_id.in_(sub_category_ids))
            
            # 역할에 따른 필터링
            if user_role == 'young':  # 청년이 로그인한 경우
                # 어르신이 만든 수업만 보여줌
                lessons_query = lessons_query.join(User).filter(User.role == 'elder')
            elif user_role == 'elder':  # 어르신이 로그인한 경우
                # 청년이 만든 수업만 보여줌
                lessons_query = lessons_query.join(User).filter(User.role == 'young')
            
            lessons = lessons_query.all()
        else:
            lessons = []
        
        lessons_data = []
        for lesson in lessons:
            lesson_dict = lesson.to_dict()
            app_count = Application.query.filter_by(lesson_id=lesson.id).count()
            lesson_dict['application_count'] = app_count
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

@main_bp.route('/lessons/by-subcategory/<sub_category_id>', methods=['GET'])
def get_lessons_by_subcategory(sub_category_id):
    """소분류별 수업 조회"""
    try:
        # 현재 로그인한 사용자의 역할 확인
        user_role = None
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            user_role = current_user.role
        
        # 해당 소분류의 수업들 가져오기
        lessons_query = Lesson.query.filter_by(sub_category_id=sub_category_id)
        
        # 역할에 따른 필터링
        if user_role == 'young':  # 청년이 로그인한 경우
            # 어르신이 만든 수업만 보여줌
            lessons_query = lessons_query.join(User).filter(User.role == 'elder')
        elif user_role == 'elder':  # 어르신이 로그인한 경우
            # 청년이 만든 수업만 보여줌
            lessons_query = lessons_query.join(User).filter(User.role == 'young')
        
        lessons = lessons_query.all()
        
        lessons_data = []
        for lesson in lessons:
            lesson_dict = lesson.to_dict()
            app_count = Application.query.filter_by(lesson_id=lesson.id).count()
            lesson_dict['application_count'] = app_count
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