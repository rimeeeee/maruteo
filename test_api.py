import requests
import json

# API 기본 URL
BASE_URL = "http://localhost:5000/api"

def test_categories():
    """분류 API 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/categories")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ 분류 API 성공!")
            print(f"분류 개수: {len(data.get('data', []))}")
            for category in data.get('data', []):
                print(f"  - {category['name']} ({category['id']}): {len(category['sub_categories'])}개 소분류")
        else:
            print("❌ 분류 API 실패")
            print(f"응답: {response.text}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def test_main_dashboard():
    """메인 대시보드 API 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/main/dashboard")
        print(f"\nStatus Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ 메인 대시보드 API 성공!")
            dashboard_data = data.get('data', {})
            print(f"인기 수업: {len(dashboard_data.get('popular_lessons', []))}개")
            print(f"인기 강사: {len(dashboard_data.get('popular_instructors', []))}개")
            print(f"찜한 수업: {len(dashboard_data.get('wished_lessons', []))}개")
        else:
            print("❌ 메인 대시보드 API 실패")
            print(f"응답: {response.text}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    print("=== API 테스트 시작 ===")
    test_categories()
    test_main_dashboard()
    print("\n=== API 테스트 완료 ===") 