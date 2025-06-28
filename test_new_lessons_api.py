import requests
import json

# 서버 URL
BASE_URL = "http://localhost:5000/api"

def test_new_lessons_api():
    """새로운 수업 목록 조회 API 테스트"""
    print("=== 새로운 수업 목록 조회 API 테스트 ===")
    
    # 1. 청년으로 로그인
    print("\n1. 청년 로그인")
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
            
            # 2. 기본 수업 목록 조회
            print("\n2. 기본 수업 목록 조회")
            response = requests.get(f"{BASE_URL}/lessons", headers=headers)
            print(f"응답 상태: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    pagination = data.get('pagination', {})
                    print(f"✅ 수업 수: {len(lessons)}개")
                    print(f"페이지 정보: {pagination}")
                    for lesson in lessons:
                        print(f"  - {lesson.get('title')} (강사: {lesson.get('instructor_name')}, 역할: {lesson.get('instructor_role')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
                print(f"응답 내용: {response.text}")
            
            # 3. 카테고리 필터링 테스트
            print("\n3. 카테고리 필터링 테스트 (korean-food)")
            response = requests.get(f"{BASE_URL}/lessons?category=korean-food", headers=headers)
            print(f"응답 상태: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 한식 카테고리 수업 수: {len(lessons)}개")
                    for lesson in lessons:
                        print(f"  - {lesson.get('title')} (카테고리: {lesson.get('sub_category_id')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
            
            # 4. 강사 역할 필터링 테스트
            print("\n4. 강사 역할 필터링 테스트 (elder)")
            response = requests.get(f"{BASE_URL}/lessons?instructor_role=elder", headers=headers)
            print(f"응답 상태: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    print(f"✅ 어르신 강사 수업 수: {len(lessons)}개")
                    for lesson in lessons:
                        print(f"  - {lesson.get('title')} (강사: {lesson.get('instructor_name')}, 역할: {lesson.get('instructor_role')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
            
            # 5. 복합 필터링 테스트
            print("\n5. 복합 필터링 테스트 (category=korean-food&instructor_role=elder&sort=latest&page=1&limit=4)")
            response = requests.get(f"{BASE_URL}/lessons?category=korean-food&instructor_role=elder&sort=latest&page=1&limit=4", headers=headers)
            print(f"응답 상태: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    lessons = data.get('data', [])
                    pagination = data.get('pagination', {})
                    print(f"✅ 복합 필터링 결과: {len(lessons)}개")
                    print(f"페이지 정보: {pagination}")
                    for lesson in lessons:
                        print(f"  - {lesson.get('title')} (강사: {lesson.get('instructor_name')}, 카테고리: {lesson.get('sub_category_id')})")
                else:
                    print(f"❌ API 응답 실패: {data.get('message')}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")
                print(f"응답 내용: {response.text}")
                
        else:
            print(f"❌ 청년 로그인 실패: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    
    print("\n🎉 새로운 수업 목록 조회 API 테스트 완료!")

if __name__ == "__main__":
    test_new_lessons_api() 