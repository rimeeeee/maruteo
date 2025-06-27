from flask import Blueprint, jsonify
from app.database import db
from app.models.category import Category, SubCategory

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