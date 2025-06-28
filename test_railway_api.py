import requests
import json

# 로컬 API 테스트
BASE_URL = "http://127.0.0.1:5000/api"

def test_login_and_lessons():
    print("=== 로컬 API 테스트 (슬래시 포함) ===")
    
    # 1. 로그인
    login_data = {
        "email": "young@test.com",
        "password": "password123"
    }
    
    print("1. 로그인 시도...")
    login_response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"로그인 응답: {login_response.status_code}")
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        print(f"로그인 성공: {login_result}")
        
        # JWT 토큰 추출
        access_token = login_result.get('accessToken')
        if access_token:
            print(f"토큰: {access_token[:50]}...")
            
            # 2. 수업 목록 조회 (슬래시 포함)
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            print("\n2. 수업 목록 조회 시도 (슬래시 포함)...")
            lessons_response = requests.get(f"{BASE_URL}/lessons/", headers=headers)
            print(f"수업 목록 응답: {lessons_response.status_code}")
            
            if lessons_response.status_code == 200:
                lessons = lessons_response.json()
                print(f"수업 목록 성공: {len(lessons)}개 수업")
                for lesson in lessons[:3]:  # 처음 3개만 출력
                    print(f"  - {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
            else:
                print(f"수업 목록 실패: {lessons_response.text}")
                
            # 3. 필터링된 수업 목록 조회 (Railway와 동일한 쿼리)
            print("\n3. 필터링된 수업 목록 조회 시도...")
            filter_params = {
                'category': 'korean-food',
                'instructor_role': 'elder',
                'sort': 'latest',
                'page': '1',
                'limit': '4'
            }
            filtered_response = requests.get(f"{BASE_URL}/lessons/", headers=headers, params=filter_params)
            print(f"필터링된 수업 목록 응답: {filtered_response.status_code}")
            
            if filtered_response.status_code == 200:
                filtered_lessons = filtered_response.json()
                print(f"필터링된 수업 목록 성공: {len(filtered_lessons)}개 수업")
                for lesson in filtered_lessons:
                    print(f"  - {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
            else:
                print(f"필터링된 수업 목록 실패: {filtered_response.text}")
        else:
            print("토큰을 찾을 수 없습니다.")
    else:
        print(f"로그인 실패: {login_response.text}")

if __name__ == "__main__":
    test_login_and_lessons() 