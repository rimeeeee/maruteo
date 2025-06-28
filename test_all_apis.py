import requests
import json
import time

# 서버 URL
BASE_URL = "http://localhost:5000/api"

def test_all_apis():
    """모든 주요 API들의 역할별 필터링 테스트"""
    print("=== 모든 API 역할별 필터링 테스트 ===")
    
    # 서버가 실행될 때까지 잠시 대기
    print("서버 시작 대기 중...")
    time.sleep(2)
    
    # 1. 청년으로 로그인
    print("\n1. 청년 로그인 및 API 테스트")
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
            
            # 1-1. 필터링된 수업 목록 조회
            print("\n1-1. 필터링된 수업 목록 조회")
            response = requests.get(f"{BASE_URL}/lessons/filtered", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 청년이 조회한 수업 수: {len(lessons)}개")
                    for lesson in lessons:
                        print(f"   - {lesson.get('title')} (강사: {lesson.get('instructor_name')}, 역할: {lesson.get('instructor_role')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
            
            # 1-2. 메인 대시보드
            print("\n1-2. 메인 대시보드")
            response = requests.get(f"{BASE_URL}/main/dashboard", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    popular_lessons = data.get('data', {}).get('popular_lessons', [])
                    print(f"✅ 인기 수업 수: {len(popular_lessons)}개")
                    for lesson in popular_lessons[:2]:
                        print(f"   - {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
            
            # 1-3. 인기 수업 목록
            print("\n1-3. 인기 수업 목록")
            response = requests.get(f"{BASE_URL}/main/popular-lessons", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 인기 수업 수: {len(lessons)}개")
                    for lesson in lessons[:2]:
                        print(f"   - {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
                
        else:
            print(f"❌ 청년 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    # 2. 어르신으로 로그인
    print("\n\n2. 어르신 로그인 및 API 테스트")
    elder_login_data = {
        "email": "instructor_user@test.com",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/login", json=elder_login_data)
        if login_response.status_code == 200:
            token = login_response.json().get('accessToken')
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ 어르신 로그인 성공")
            
            # 2-1. 필터링된 수업 목록 조회
            print("\n2-1. 필터링된 수업 목록 조회")
            response = requests.get(f"{BASE_URL}/lessons/filtered", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 어르신이 조회한 수업 수: {len(lessons)}개")
                    for lesson in lessons:
                        print(f"   - {lesson.get('title')} (강사: {lesson.get('instructor_name')}, 역할: {lesson.get('instructor_role')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
            
            # 2-2. 메인 대시보드
            print("\n2-2. 메인 대시보드")
            response = requests.get(f"{BASE_URL}/main/dashboard", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    popular_lessons = data.get('data', {}).get('popular_lessons', [])
                    print(f"✅ 인기 수업 수: {len(popular_lessons)}개")
                    for lesson in popular_lessons[:2]:
                        print(f"   - {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
            
            # 2-3. 인기 수업 목록
            print("\n2-3. 인기 수업 목록")
            response = requests.get(f"{BASE_URL}/main/popular-lessons", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 인기 수업 수: {len(lessons)}개")
                    for lesson in lessons[:2]:
                        print(f"   - {lesson.get('title')} (강사: {lesson.get('instructor_name')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
                
        else:
            print(f"❌ 어르신 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    print("\n🎉 모든 API 테스트 완료!")

if __name__ == "__main__":
    test_all_apis() 