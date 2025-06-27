# flask 앱 생성, 라우터 등록
from flask import Flask
from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy
from app.database import db
from flask_jwt_extended import JWTManager
from app.config import Config



#db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    #app.config.from_object(Config)
    app.config.from_object('app.config.Config')

    # CORS 허용 설정
    #CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    db.init_app(app)
    jwt.init_app(app)

    # 라우터 등록 (지금은 auth만)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    from app.routes.test_routes import test_bp
    app.register_blueprint(test_bp)
    
    #수업등록
    from app.routes.lesson_routes import lesson_bp
    app.register_blueprint(lesson_bp, url_prefix='/api')

    #수업신청
    from app.routes.apply_routes import apply_bp
    app.register_blueprint(apply_bp, url_prefix='/api')

    #프로필 등록/수정
    from app.routes.profile_routes import profile_bp
    app.register_blueprint(profile_bp, url_prefix='/api')

    #출석/이행률 계산 API
    from app.routes.mypage_routes import mypage_bp
    app.register_blueprint(mypage_bp, url_prefix='/api')
    return app