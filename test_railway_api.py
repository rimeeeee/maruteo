import requests
import json

def test_railway_api():
    """Railway 배포된 API 테스트"""
    base_url = "https://maruteo-production-d290.up.railway.app"
    
    # 1. 루트 경로 테스트
    print("1. 루트 경로 테스트")
    try:
        response = requests.get(f"{base_url}/")
        print(f"루트 응답: {response.status_code}")
        if response.status_code == 200:
            print("✅ 서버 정상 실행 중")
            data = response.json()
            print(f"메시지: {data.get('message')}")
        else:
            print(f"❌ 루트 접근 실패: {response.text}")
    except Exception as e:
        print(f"❌ 연결 오류: {e}")
    
    # 2. API 경로 존재 여부 테스트 (인증 없이)
    print("\n2. API 경로 존재 여부 테스트")
    url = f"{base_url}/api/lessons?category=korean-food&instructor_role=elder&sort=latest&page=1&limit=4"
    print(f"요청 URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"API 응답: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ API 경로는 존재하지만 인증이 필요함 (정상)")
        elif response.status_code == 404:
            print("❌ 404 에러 - API 경로를 찾을 수 없음")
            print("가능한 원인:")
            print("1. Railway 배포 시 최신 코드가 반영되지 않음")
            print("2. lesson_routes.py의 /lessons 경로가 없음")
            print("3. 블루프린트가 제대로 등록되지 않음")
        else:
            print(f"기타 응답: {response.status_code}")
            print(f"응답: {response.text}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_railway_api() 