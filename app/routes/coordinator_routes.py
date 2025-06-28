from flask import Blueprint, jsonify, request
from app.models.application import Application
from app.models.lesson import Lesson
from app.models.user import User
from app.database import db
from datetime import datetime, timedelta
from sqlalchemy import or_
import json

coordinator_bp = Blueprint('coordinator', __name__)

@coordinator_bp.route('/api/coordinator/application-detail/<int:application_id>')
def get_application_detail(application_id):
    """신청 상세 정보 조회"""
    try:
        # 신청 정보 조회
        application = Application.query.get(application_id)
        if not application:
            return jsonify({'success': False, 'error': '신청을 찾을 수 없습니다.'})
        
        # 관련 정보 조회
        lesson = Lesson.query.get(application.lesson_id)
        user = User.query.get(application.user_id)
        
        if not lesson or not user:
            return jsonify({'success': False, 'error': '수업 또는 사용자 정보를 찾을 수 없습니다.'})
        
        # 상세 정보 구성
        result = {
            'application_id': application.id,
            'status': application.status,
            'selected_date': application.selected_date,
            'selected_time': application.selected_time,
            'created_at': application.created_at.strftime('%Y-%m-%d %H:%M'),
            
            # 수업 정보
            'lesson': {
                'id': lesson.id,
                'title': lesson.title,
                'description': lesson.description,
                'time': lesson.time,
                'location': lesson.location,
                'image_url': lesson.image_url,
                'video_url': lesson.video_url,
                'materials': lesson.materials,
                'max_students': lesson.max_students,
                'price': lesson.price,
                'instructor_name': lesson.instructor.name if lesson.instructor else None,
                'instructor_phone': lesson.instructor.phone if lesson.instructor else None
            },
            
            # 신청자 정보
            'applicant': {
                'id': user.id,
                'name': user.name,
                'phone': user.phone,
                'email': user.email,
                'profile_image': user.profile_image
            }
        }
        
        return jsonify({'success': True, 'application_detail': result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@coordinator_bp.route('/api/coordinator/new-applications/<date>')
def get_new_applications(date):
    """특정 날짜의 신규 신청 내역 조회"""
    try:
        # 해당 날짜의 신청 내역 조회
        applications = Application.query.filter(
            Application.selected_date == date,
            Application.status == '신청됨'
        ).order_by(Application.created_at.desc()).all()
        
        result = []
        for app in applications:
            # 관련 정보 조회
            lesson = Lesson.query.get(app.lesson_id)
            user = User.query.get(app.user_id)
            
            if lesson and user:
                result.append({
                    'id': app.id,
                    'lesson_title': lesson.title,
                    'lesson_time': lesson.time,
                    'lesson_location': lesson.location,
                    'lesson_image_url': lesson.image_url,
                    'applicant_name': user.name,
                    'applicant_phone': user.phone,
                    'selected_time': app.selected_time,
                    'created_at': app.created_at.strftime('%Y-%m-%d %H:%M'),
                    'status': app.status
                })
        
        return jsonify({'success': True, 'applications': result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@coordinator_bp.route('/api/coordinator/upcoming-lessons/<date>')
def get_upcoming_lessons(date):
    """특정 날짜의 진행 예정 수업 조회"""
    try:
        # 해당 날짜에 신청된 수업들 조회
        applications = Application.query.filter(
            Application.selected_date == date,
            or_(Application.status == '신청됨', Application.status == '승인됨')
        ).all()
        
        # 수업 ID 목록 추출
        lesson_ids = list(set([app.lesson_id for app in applications]))
        
        # 수업 정보 조회
        lessons = Lesson.query.filter(Lesson.id.in_(lesson_ids)).all()
        
        result = []
        for lesson in lessons:
            # 해당 수업의 신청자 수 계산
            applicant_count = Application.query.filter(
                Application.lesson_id == lesson.id,
                Application.selected_date == date,
                or_(Application.status == '신청됨', Application.status == '승인됨')
            ).count()
            
            result.append({
                'id': lesson.id,
                'title': lesson.title,
                'time': lesson.time,
                'location': lesson.location,
                'instructor_name': lesson.instructor.name if lesson.instructor else None,
                'applicant_count': applicant_count,
                'max_students': lesson.max_students
            })
        
        return jsonify({'success': True, 'lessons': result})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@coordinator_bp.route('/api/coordinator/application-status', methods=['POST'])
def update_application_status():
    """신청 상태 업데이트"""
    try:
        data = request.get_json()
        application_id = data.get('application_id')
        new_status = data.get('status')
        
        application = Application.query.get(application_id)
        if application:
            application.status = new_status
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': '신청을 찾을 수 없습니다.'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@coordinator_bp.route('/api/coordinator/date-range')
def get_date_range():
    """신청이 있는 날짜 범위 조회"""
    try:
        # 최근 30일간의 신청 데이터 조회
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        applications = Application.query.filter(
            Application.created_at >= start_date
        ).all()
        
        # 신청이 있는 날짜들 추출
        dates_with_applications = list(set([app.selected_date for app in applications if app.selected_date]))
        dates_with_applications.sort()
        
        return jsonify({'success': True, 'dates': dates_with_applications})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}) 