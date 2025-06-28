import requests
import json

# 서버 URL
BASE_URL = "http://localhost:5000/api"

def test_role_filtering():
    """역할별 필터링 테스트"""
    print("=== 역할별 필터링 테스트 ===")
    
    # 1. 청년으로 로그인하여 수업 목록 조회
    print("\n1. 청년으로 로그인하여 수업 목록 조회")
    
    # 청년 로그인 (실제 토큰이 필요함)
    youth_login_data = {
        "username": "youth_user",  # 실제 청년 사용자명
        "password": "password123"   # 실제 비밀번호
    }
    
    try:
        # 로그인하여 토큰 받기
        login_response = requests.post(f"{BASE_URL}/login", json=youth_login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('access_token')
            headers = {'Authorization': f'Bearer {token}'}
            
            # 필터링된 수업 목록 조회
            lessons_response = requests.get(f"{BASE_URL}/lessons/filtered", headers=headers)
            
            if lessons_response.status_code == 200:
                data = lessons_response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 청년이 조회한 수업 수: {len(lessons)}개")
                    
                    # 어르신이 만든 수업만 있는지 확인
                    all_instructor_lessons = True
                    for lesson in lessons:
                        if lesson.get('instructor_role') != 'instructor':
                            all_instructor_lessons = False
                            print(f"❌ 청년이 조회했는데 어르신이 아닌 수업 발견: {lesson.get('title')}")
                            break
                    
                    if all_instructor_lessons:
                        print("✅ 청년이 조회한 수업들이 모두 어르신이 만든 수업입니다.")
                    else:
                        print("❌ 청년이 조회한 수업 중 어르신이 아닌 수업이 있습니다.")
                    
                    # 처음 3개 수업 정보 출력
                    for i, lesson in enumerate(lessons[:3], 1):
                        print(f"  {i}. {lesson.get('title')} (강사: {lesson.get('instructor_name')}, 역할: {lesson.get('instructor_role')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ 수업 목록 조회 실패: {lessons_response.status_code}")
        else:
            print(f"❌ 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    # 2. 어르신으로 로그인하여 수업 목록 조회
    print("\n2. 어르신으로 로그인하여 수업 목록 조회")
    
    # 어르신 로그인 (실제 토큰이 필요함)
    instructor_login_data = {
        "username": "instructor_user",  # 실제 어르신 사용자명
        "password": "password123"        # 실제 비밀번호
    }
    
    try:
        # 로그인하여 토큰 받기
        login_response = requests.post(f"{BASE_URL}/login", json=instructor_login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('access_token')
            headers = {'Authorization': f'Bearer {token}'}
            
            # 필터링된 수업 목록 조회
            lessons_response = requests.get(f"{BASE_URL}/lessons/filtered", headers=headers)
            
            if lessons_response.status_code == 200:
                data = lessons_response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 어르신이 조회한 수업 수: {len(lessons)}개")
                    
                    # 청년이 만든 수업만 있는지 확인
                    all_student_lessons = True
                    for lesson in lessons:
                        if lesson.get('instructor_role') != 'student':
                            all_student_lessons = False
                            print(f"❌ 어르신이 조회했는데 청년이 아닌 수업 발견: {lesson.get('title')}")
                            break
                    
                    if all_student_lessons:
                        print("✅ 어르신이 조회한 수업들이 모두 청년이 만든 수업입니다.")
                    else:
                        print("❌ 어르신이 조회한 수업 중 청년이 아닌 수업이 있습니다.")
                    
                    # 처음 3개 수업 정보 출력
                    for i, lesson in enumerate(lessons[:3], 1):
                        print(f"  {i}. {lesson.get('title')} (강사: {lesson.get('instructor_name')}, 역할: {lesson.get('instructor_role')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ 수업 목록 조회 실패: {lessons_response.status_code}")
        else:
            print(f"❌ 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_role_filtering() 