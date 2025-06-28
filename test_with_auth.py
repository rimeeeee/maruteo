import requests
import json

def test_with_auth():
    """인증을 포함한 API 테스트"""
    base_url = "http://localhost:5000/api"
    
    # 1. 로그인
    print("1. 로그인 시도...")
    login_data = {
        "email": "youth_user@test.com",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/login", json=login_data)
        print(f"로그인 응답: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token = login_response.json().get('accessToken')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ 로그인 성공")
            
            # 2. API 호출
            print("\n2. 수업 목록 API 호출...")
            url = f"{base_url}/lessons?category=korean-food&instructor_role=elder&sort=latest&page=1&limit=4"
            print(f"요청 URL: {url}")
            
            response = requests.get(url, headers=headers)
            print(f"API 응답: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ API 정상 작동!")
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"수업 수: {len(lessons)}개")
                    for lesson in lessons:
                        print(f"  - {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
                else:
                    print(f"API 오류: {data.get('message')}")
            elif response.status_code == 404:
                print("❌ 404 에러 - API 경로를 찾을 수 없음")
                print("가능한 원인:")
                print("1. lesson_routes.py에 /lessons 경로가 없음")
                print("2. 블루프린트가 제대로 등록되지 않음")
            else:
                print(f"❌ 기타 오류: {response.status_code}")
                print(f"응답: {response.text}")
        else:
            print(f"❌ 로그인 실패: {login_response.status_code}")
            print(f"응답: {login_response.text}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_with_auth() 