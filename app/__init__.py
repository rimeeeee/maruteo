# flask 앱 생성, 라우터 등록
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config



db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # 라우터 등록 (지금은 auth만)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    #수업등록
    from app.routes.lesson_routes import lesson_bp
    app.register_blueprint(lesson_bp, url_prefix='/api')

    #수업신청
    from app.routes.apply_routes import apply_bp
    app.register_blueprint(apply_bp, url_prefix='/api')

    return app