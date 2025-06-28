import requests
import json

# 서버 URL
BASE_URL = "http://localhost:5000/api"

def test_role_filtering():
    """역할별 필터링 테스트"""
    print("=== 역할별 필터링 테스트 ===")
    
    # 1. 청년으로 로그인
    print("\n1. 청년 로그인 후 수업 목록 조회")
    youth_login_data = {
        "email": "youth_user@test.com",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/login", json=youth_login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('accessToken')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ 청년 로그인 성공")
            
            # 필터링된 수업 목록 조회
            response = requests.get(f"{BASE_URL}/lessons/filtered", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 청년이 조회한 수업 수: {len(lessons)}개")
                    
                    # 모든 수업이 어르신이 만든 수업인지 확인
                    all_instructor_lessons = True
                    for lesson in lessons:
                        instructor_name = lesson.get('instructor_name', '')
                        if 'elder' not in str(lesson.get('instructor_role', '')):
                            all_instructor_lessons = False
                            break
                    
                    if all_instructor_lessons:
                        print("✅ 청년이 조회한 수업들이 모두 어르신이 만든 수업입니다.")
                        for i, lesson in enumerate(lessons, 1):
                            print(f"  {i}. {lesson.get('title')} (강사: {lesson.get('instructor_name')}, 역할: {lesson.get('instructor_role')})")
                    else:
                        print("❌ 청년이 조회한 수업 중 어르신이 만든 수업이 아닌 것이 있습니다.")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
        else:
            print(f"❌ 청년 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    # 2. 어르신으로 로그인
    print("\n2. 어르신 로그인 후 수업 목록 조회")
    instructor_login_data = {
        "email": "instructor_user@test.com",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/login", json=instructor_login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('accessToken')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ 어르신 로그인 성공")
            
            # 필터링된 수업 목록 조회
            response = requests.get(f"{BASE_URL}/lessons/filtered", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 어르신이 조회한 수업 수: {len(lessons)}개")
                    
                    # 모든 수업이 청년이 만든 수업인지 확인
                    all_student_lessons = True
                    for lesson in lessons:
                        instructor_name = lesson.get('instructor_name', '')
                        if 'young' not in str(lesson.get('instructor_role', '')):
                            all_student_lessons = False
                            break
                    
                    if all_student_lessons:
                        print("✅ 어르신이 조회한 수업들이 모두 청년이 만든 수업입니다.")
                        for i, lesson in enumerate(lessons, 1):
                            print(f"  {i}. {lesson.get('title')} (강사: {lesson.get('instructor_name')}, 역할: {lesson.get('instructor_role')})")
                    else:
                        print("❌ 어르신이 조회한 수업 중 청년이 만든 수업이 아닌 것이 있습니다.")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
        else:
            print(f"❌ 어르신 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    print("\n🎉 역할별 필터링 테스트 완료!")

if __name__ == "__main__":
    test_role_filtering() 