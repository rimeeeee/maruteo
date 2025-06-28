from app import create_app
from app.database import db
from sqlalchemy import text

def add_new_fields():
    app = create_app()
    
    with app.app_context():
        try:
            # Lesson 테이블에 새로운 필드 추가
            db.session.execute(text("ALTER TABLE lesson ADD COLUMN max_students INTEGER"))
            print("✅ max_students 필드 추가 완료")
        except Exception as e:
            print(f"max_students 필드 이미 존재하거나 오류: {e}")
        
        try:
            db.session.execute(text("ALTER TABLE lesson ADD COLUMN price INTEGER"))
            print("✅ price 필드 추가 완료")
        except Exception as e:
            print(f"price 필드 이미 존재하거나 오류: {e}")
        
        # 기존 수업들에 기본값 설정
        try:
            db.session.execute(text("UPDATE lesson SET max_students = 10 WHERE max_students IS NULL"))
            db.session.execute(text("UPDATE lesson SET price = 50000 WHERE price IS NULL"))
            print("✅ 기존 수업들에 기본값 설정 완료")
        except Exception as e:
            print(f"기본값 설정 오류: {e}")
        
        db.session.commit()
        print("🎉 마이그레이션 완료!")

if __name__ == "__main__":
    add_new_fields() 