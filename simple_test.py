import urllib.request
import json

def test_categories():
    """분류 API 테스트"""
    try:
        url = "http://localhost:5000/api/categories"
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req) as response:
            data = response.read()
            result = json.loads(data.decode('utf-8'))
            
            print("✅ 분류 API 성공!")
            print(f"Status Code: {response.status}")
            print(f"분류 개수: {len(result.get('data', []))}")
            
            for category in result.get('data', []):
                print(f"  - {category['name']} ({category['id']}): {len(category['sub_categories'])}개 소분류")
                
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    print("=== API 테스트 시작 ===")
    test_categories()
    print("\n=== API 테스트 완료 ===") 