from app import create_app
from app.models.user import User
from app.models.lesson import Lesson

app = create_app()

with app.app_context():
    print("=== 현재 DB 상태 확인 ===")
    
    # 사용자 목록
    users = User.query.all()
    print(f"\n📋 사용자 목록 (총 {len(users)}명):")
    for user in users:
        print(f"  - {user.name} (role: {user.role}, id: {user.id})")
    
    # 수업 목록
    lessons = Lesson.query.all()
    print(f"\n📚 수업 목록 (총 {len(lessons)}개):")
    for lesson in lessons:
        instructor = User.query.get(lesson.instructor_id)
        print(f"  - {lesson.title} (강사: {instructor.name if instructor else 'Unknown'}, 강사 role: {instructor.role if instructor else 'Unknown'})")
    
    # 필터링 테스트
    print(f"\n🔍 필터링 테스트:")
    
    # 청년이 조회할 때 (어르신 수업만 보여야 함)
    young_lessons = Lesson.query.join(User).filter(User.role == 'elder').all()
    print(f"  - 청년이 조회할 수업 수: {len(young_lessons)}개")
    for lesson in young_lessons:
        instructor = User.query.get(lesson.instructor_id)
        print(f"    * {lesson.title} (강사: {instructor.name}, role: {instructor.role})")
    
    # 어르신이 조회할 때 (청년 수업만 보여야 함)
    elder_lessons = Lesson.query.join(User).filter(User.role == 'young').all()
    print(f"  - 어르신이 조회할 수업 수: {len(elder_lessons)}개")
    for lesson in elder_lessons:
        instructor = User.query.get(lesson.instructor_id)
        print(f"    * {lesson.title} (강사: {instructor.name}, role: {instructor.role})") 