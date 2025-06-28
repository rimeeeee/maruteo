from app import create_app, db
from app.models.user import User

app = create_app()

def migrate_roles():
    """DB의 role 필드를 young/elder로 통일"""
    print("=== Role 필드 마이그레이션 시작 ===")
    
    with app.app_context():
        try:
            # 현재 사용자들의 role 확인
            users = User.query.all()
            print(f"총 {len(users)}명의 사용자가 있습니다.")
            
            for user in users:
                print(f"사용자: {user.name} (현재 role: {user.role})")
            
            # role 변환
            print("\n=== Role 변환 시작 ===")
            
            # student → young
            student_users = User.query.filter_by(role='student').all()
            for user in student_users:
                user.role = 'young'
                print(f"변환: {user.name} (student → young)")
            
            # instructor → elder
            instructor_users = User.query.filter_by(role='instructor').all()
            for user in instructor_users:
                user.role = 'elder'
                print(f"변환: {user.name} (instructor → elder)")
            
            # DB 커밋
            db.session.commit()
            print("\n✅ Role 변환 완료!")
            
            # 변환 후 확인
            print("\n=== 변환 후 확인 ===")
            users = User.query.all()
            for user in users:
                print(f"사용자: {user.name} (변환된 role: {user.role})")
            
            print("\n🎉 마이그레이션이 성공적으로 완료되었습니다!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ 마이그레이션 실패: {e}")
            raise

if __name__ == "__main__":
    migrate_roles() 