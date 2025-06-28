import requests
import json
import time

# 서버 URL
BASE_URL = "http://localhost:5000/api"

def test_talent_exploration():
    """재능탐색페이지 API 테스트"""
    print("=== 재능탐색페이지 API 테스트 ===")
    
    # 서버가 실행될 때까지 잠시 대기
    print("서버 시작 대기 중...")
    time.sleep(3)
    
    # 1. 소분류별 수업 목록 조회 테스트
    print("\n1. 소분류별 수업 목록 조회 테스트")
    print("테스트할 sub_category_id: korean-food")
    
    try:
        # 로그인 없이 테스트 (비로그인 상태) - 이제 JWT 토큰이 필요하므로 401 에러 예상
        response = requests.get(f"{BASE_URL}/talent-exploration/korean-food/lessons")
        
        if response.status_code == 401:
            print("✅ 예상대로 JWT 토큰이 필요합니다.")
        elif response.status_code == 200:
            data = response.json()
            if data.get('success'):
                lessons = data.get('data', {}).get('lessons', [])
                print(f"✅ 수업 목록 조회 성공 (비로그인)")
                print(f"   총 {len(lessons)}개의 수업이 있습니다.")
                
                for i, lesson in enumerate(lessons[:3], 1):
                    print(f"   {i}. {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
            else:
                print(f"❌ API 응답 실패: {data.get('message')}")
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
        return
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    # 2. 소분류별 강사 목록 조회 테스트
    print("\n2. 소분류별 강사 목록 조회 테스트")
    
    try:
        response = requests.get(f"{BASE_URL}/talent-exploration/korean-food/instructors")
        
        if response.status_code == 401:
            print("✅ 예상대로 JWT 토큰이 필요합니다.")
        elif response.status_code == 200:
            data = response.json()
            if data.get('success'):
                instructors = data.get('data', {}).get('instructors', [])
                print(f"✅ 강사 목록 조회 성공 (비로그인)")
                print(f"   총 {len(instructors)}명의 강사가 있습니다.")
                
                for i, instructor in enumerate(instructors[:3], 1):
                    print(f"   {i}. {instructor.get('name')} (별점: {instructor.get('avg_rating')})")
            else:
                print(f"❌ API 응답 실패: {data.get('message')}")
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    # 3. 로그인 후 역할별 필터링 테스트
    print("\n3. 로그인 후 역할별 필터링 테스트")
    
    # 청년으로 로그인
    youth_login_data = {
        "email": "youth_user@test.com",  # email로 로그인
        "password": "password123"
    }
    
    try:
        # 청년 로그인
        login_response = requests.post(f"{BASE_URL}/login", json=youth_login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('accessToken')
            headers = {'Authorization': f'Bearer {token}'}
            
            print("✅ 청년 로그인 성공")
            
            # 청년으로 수업 목록 조회
            lessons_response = requests.get(f"{BASE_URL}/talent-exploration/korean-food/lessons", headers=headers)
            
            if lessons_response.status_code == 200:
                data = lessons_response.json()
                if data.get('success'):
                    lessons = data.get('data', {}).get('lessons', [])
                    print(f"✅ 청년이 조회한 수업 수: {len(lessons)}개")
                    
                    # 어르신이 만든 수업만 있는지 확인
                    all_instructor_lessons = True
                    for lesson in lessons:
                        instructor_name = lesson.get('instructor_name', '')
                        if 'elder' not in str(lesson.get('instructor_role', '')):
                            all_instructor_lessons = False
                            print(f"   ⚠️  청년이 조회했는데 어르신이 아닌 수업 발견: {lesson.get('title')}")
                    
                    if all_instructor_lessons:
                        print("✅ 청년이 조회한 수업들이 모두 어르신이 만든 수업입니다.")
                    
                    # 처음 3개 수업 정보 출력
                    for i, lesson in enumerate(lessons[:3], 1):
                        print(f"   {i}. {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ 수업 목록 조회 실패: {lessons_response.status_code}")
                print(f"응답 내용: {lessons_response.text}")
        else:
            print(f"❌ 청년 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    # 어르신으로 로그인
    print("\n4. 어르신으로 로그인 후 필터링 테스트")
    
    instructor_login_data = {
        "email": "instructor_user@test.com",  # email로 로그인
        "password": "password123"
    }
    
    try:
        # 어르신 로그인
        login_response = requests.post(f"{BASE_URL}/login", json=instructor_login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('accessToken')
            headers = {'Authorization': f'Bearer {token}'}
            
            print("✅ 어르신 로그인 성공")
            
            # 어르신으로 수업 목록 조회
            lessons_response = requests.get(f"{BASE_URL}/talent-exploration/programming/lessons", headers=headers)
            
            if lessons_response.status_code == 200:
                data = lessons_response.json()
                if data.get('success'):
                    lessons = data.get('data', {}).get('lessons', [])
                    print(f"✅ 어르신이 조회한 수업 수: {len(lessons)}개")
                    
                    # 청년이 만든 수업만 있는지 확인
                    all_student_lessons = True
                    for lesson in lessons:
                        instructor_name = lesson.get('instructor_name', '')
                        if 'young' not in str(lesson.get('instructor_role', '')):
                            all_student_lessons = False
                            print(f"   ⚠️  어르신이 조회했는데 청년이 아닌 수업 발견: {lesson.get('title')}")
                    
                    if all_student_lessons:
                        print("✅ 어르신이 조회한 수업들이 모두 청년이 만든 수업입니다.")
                    
                    # 처음 3개 수업 정보 출력
                    for i, lesson in enumerate(lessons[:3], 1):
                        print(f"   {i}. {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ 수업 목록 조회 실패: {lessons_response.status_code}")
                print(f"응답 내용: {lessons_response.text}")
        else:
            print(f"❌ 어르신 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_talent_exploration() 