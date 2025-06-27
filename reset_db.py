#!/usr/bin/env python3
"""
데이터베이스 초기화 및 테이블 재생성 스크립트
"""

import os
from app import create_app
from app.database import db

def reset_database():
    """데이터베이스 초기화"""
    print("🗑️ 데이터베이스 초기화 중...")
    
    # 데이터베이스 파일 삭제
    db_path = 'instance/app.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ 기존 데이터베이스 파일이 삭제되었습니다.")
    
    # 앱 컨텍스트에서 테이블 생성
    with create_app().app_context():
        db.create_all()
        print("✅ 모든 테이블이 생성되었습니다.")
        print("✅ 데이터베이스 초기화가 완료되었습니다!")

if __name__ == '__main__':
    reset_database() 