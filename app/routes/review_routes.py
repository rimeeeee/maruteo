from flask import Blueprint, jsonify, request
from app.database import db
from app.models.review import Review
from app.models.lesson import Lesson
from app.models.user import User
from flask_login import login_required, current_user

review_bp = Blueprint('review', __name__)

@review_bp.route('/lesson/<int:lesson_id>/reviews', methods=['GET'])
def get_lesson_reviews(lesson_id):
    """특정 수업의 리뷰들을 가져옴"""
    try:
        reviews = Review.query.filter_by(lesson_id=lesson_id).order_by(Review.created_at.desc()).all()
        
        reviews_data = []
        for review in reviews:
            reviews_data.append(review.to_dict())
        
        return jsonify({
            'success': True,
            'data': reviews_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@review_bp.route('/lesson/<int:lesson_id>/reviews', methods=['POST'])
@login_required
def create_review(lesson_id):
    """수업 리뷰 작성"""
    try:
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({
                'success': False,
                'message': '별점은 1-5 사이의 정수여야 합니다.'
            }), 400
        
        # 이미 리뷰를 작성했는지 확인
        existing_review = Review.query.filter_by(
            lesson_id=lesson_id, 
            user_id=current_user.id
        ).first()
        
        if existing_review:
            return jsonify({
                'success': False,
                'message': '이미 이 수업에 대한 리뷰를 작성했습니다.'
            }), 400
        
        # 새 리뷰 생성
        review = Review(
            lesson_id=lesson_id,
            user_id=current_user.id,
            rating=rating,
            comment=comment
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '리뷰가 성공적으로 작성되었습니다.',
            'data': review.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@review_bp.route('/review/<int:review_id>', methods=['PUT'])
@login_required
def update_review(review_id):
    """리뷰 수정"""
    try:
        review = Review.query.get_or_404(review_id)
        
        # 리뷰 작성자만 수정 가능
        if review.user_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '리뷰를 수정할 권한이 없습니다.'
            }), 403
        
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if rating is not None:
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                return jsonify({
                    'success': False,
                    'message': '별점은 1-5 사이의 정수여야 합니다.'
                }), 400
            review.rating = rating
        
        review.comment = comment
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '리뷰가 성공적으로 수정되었습니다.',
            'data': review.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@review_bp.route('/review/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    """리뷰 삭제"""
    try:
        review = Review.query.get_or_404(review_id)
        
        # 리뷰 작성자만 삭제 가능
        if review.user_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '리뷰를 삭제할 권한이 없습니다.'
            }), 403
        
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '리뷰가 성공적으로 삭제되었습니다.'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500 