import urllib.request
import json

def test_api(url, name):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            result = json.loads(data.decode('utf-8'))
            print(f"✅ {name} API 성공!")
            print(f"   Status: {response.status}")
            print(f"   데이터 개수: {len(result.get('data', []))}")
            return True
    except Exception as e:
        print(f"❌ {name} API 실패: {e}")
        return False

if __name__ == "__main__":
    print("=== API 테스트 시작 ===")
    
    # 카테고리 API 테스트
    test_api("http://localhost:5000/api/categories", "카테고리")
    
    # 카로셀 API 테스트
    test_api("http://localhost:5000/api/main/popular-lessons", "카로셀")
    
    # 메인 대시보드 API 테스트
    test_api("http://localhost:5000/api/main/dashboard", "메인 대시보드")
    
    print("\n=== API 테스트 완료 ===") 