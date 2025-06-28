import requests
import json

# 서버 URL
BASE_URL = "http://localhost:5000/api"

def test_simple():
    """간단한 API 테스트"""
    print("=== 간단한 API 테스트 ===")
    
    # 1. 청년으로 로그인
    print("\n1. 청년 로그인")
    youth_login_data = {
        "email": "youth_user@test.com",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/login", json=youth_login_data)
        print(f"로그인 응답: {login_response.status_code}")
        if login_response.status_code == 200:
            print("로그인 성공")
            token = login_response.json().get('accessToken')
            headers = {'Authorization': f'Bearer {token}'}
            
            # 2. 인기 수업 목록 테스트
            print("\n2. 인기 수업 목록 테스트")
            response = requests.get(f"{BASE_URL}/main/popular-lessons", headers=headers)
            print(f"인기 수업 응답: {response.status_code}")
            if response.status_code != 200:
                print(f"응답 내용: {response.text}")
            else:
                data = response.json()
                print(f"성공: {data.get('success')}")
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"수업 수: {len(lessons)}")
                    for lesson in lessons:
                        print(f"  - {lesson.get('title')}")
        else:
            print(f"로그인 실패: {login_response.text}")
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    test_simple() 