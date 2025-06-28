import requests

def check_api():
    """API 상태 확인"""
    url = "http://localhost:5000/api/lessons?category=korean-food&instructor_role=elder&sort=latest&page=1&limit=4"
    
    try:
        print(f"요청 URL: {url}")
        response = requests.get(url)
        print(f"응답 상태: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API 정상 작동")
            data = response.json()
            print(f"응답 데이터: {data}")
        elif response.status_code == 401:
            print("❌ 인증 필요 (JWT 토큰 필요)")
        elif response.status_code == 404:
            print("❌ 404 에러 - API 경로를 찾을 수 없음")
            print("가능한 원인:")
            print("1. 서버가 실행되지 않음")
            print("2. API 경로가 잘못됨")
            print("3. 라우터가 등록되지 않음")
        else:
            print(f"❌ 기타 오류: {response.status_code}")
            print(f"응답: {response.text}")
            
    except Exception as e:
        print(f"❌ 연결 오류: {e}")

if __name__ == "__main__":
    check_api() 