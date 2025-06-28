# flask 앱 생성, 라우터 등록
from flask import Flask
from flask_cors import CORS
from app.database import db
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from app.config import Config

jwt = JWTManager()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # CORS 허용 설정 - 모든 origin, 모든 경로 허용
    CORS(app, 
         origins="*",
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"])

    db.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'  # type: ignore

    # 라우터 등록 (지금은 auth만)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    #수업등록
    from app.routes.lesson_routes import lesson_bp
    app.register_blueprint(lesson_bp, url_prefix='/api/lesson')

    #수업신청
    from app.routes.apply_routes import apply_bp
    app.register_blueprint(apply_bp, url_prefix='/api/apply')

    #프로필 등록/수정
    from app.routes.profile_routes import profile_bp
    app.register_blueprint(profile_bp, url_prefix='/api/profile')

    #출석/이행률 계산 API
    from app.routes.mypage_routes import mypage_bp
    app.register_blueprint(mypage_bp, url_prefix='/api/mypage')
    
    #메인페이지
    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    
    #카테고리
    from app.routes.category_routes import category_bp
    app.register_blueprint(category_bp, url_prefix='/api/category')
    
    #리뷰
    from app.routes.review_routes import review_bp
    app.register_blueprint(review_bp, url_prefix='/api/review')
    
    #데이터베이스 관련 블루프린트
    from app.routes.db_routes import db_bp
    app.register_blueprint(db_bp, url_prefix='/api/db')
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))