import requests

def test_home():
    """첫화면 메시지 테스트"""
    try:
        response = requests.get('http://localhost:5000/')
        print(f"응답 상태: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ 첫화면 메시지:")
            print(f"메시지: {data.get('message')}")
            print(f"설명: {data.get('description')}")
            print(f"버전: {data.get('version')}")
            print("엔드포인트:")
            for key, value in data.get('endpoints', {}).items():
                print(f"  {key}: {value}")
        else:
            print(f"❌ 오류: {response.status_code}")
            print(f"응답: {response.text}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_home() 