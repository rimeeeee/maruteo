from flask import Blueprint

test_bp = Blueprint('test', __name__)

@test_bp.route('/')
def home():
    return "의성 마루터 백엔드입니다!"