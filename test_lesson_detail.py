import requests
import json

# 서버 URL
BASE_URL = "http://localhost:5000/api"

def test_lesson_detail():
    """수업 상세 정보 API 테스트"""
    print("=== 수업 상세 정보 API 테스트 ===")
    
    # 수업 상세 정보 가져오기
    lesson_id = 1
    response = requests.get(f"{BASE_URL}/lessons/{lesson_id}/detail")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 수업 상세 정보 조회 성공")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 주요 정보 확인
        lesson_data = data.get('data', {})
        print(f"\n📋 수업 정보:")
        print(f"  - 제목: {lesson_data.get('title')}")
        print(f"  - 설명: {lesson_data.get('description')}")
        print(f"  - 시간: {lesson_data.get('time')}")
        print(f"  - 장소: {lesson_data.get('location')}")
        
        print(f"\n👨‍🏫 강사 정보:")
        instructor = lesson_data.get('instructor', {})
        print(f"  - 이름: {instructor.get('name')}")
        print(f"  - 역할: {instructor.get('role')}")
        
        print(f"\n📂 카테고리:")
        category = lesson_data.get('category', {})
        print(f"  - 대분류: {category.get('name')}")
        print(f"  - 소분류: {category.get('sub_category_name')}")
        
        print(f"\n📊 통계:")
        stats = lesson_data.get('stats', {})
        print(f"  - 찜수: {stats.get('wish_count')}")
        print(f"  - 신청수: {stats.get('application_count')}")
        print(f"  - 평균 별점: {stats.get('avg_rating')}")
        print(f"  - 리뷰수: {stats.get('review_count')}")
        
        print(f"\n🖼️ 미디어:")
        print(f"  - 이미지: {lesson_data.get('image_url')}")
        print(f"  - 동영상: {lesson_data.get('video_url')}")
        
        print(f"\n📝 준비물:")
        materials = lesson_data.get('materials', [])
        for i, material in enumerate(materials, 1):
            print(f"  {i}. {material}")
            
    else:
        print(f"❌ 수업 상세 정보 조회 실패: {response.status_code}")
        print(response.text)

def test_lesson_wish():
    """수업 찜하기 API 테스트"""
    print("\n=== 수업 찜하기 API 테스트 ===")
    
    lesson_id = 1
    response = requests.post(f"{BASE_URL}/lessons/{lesson_id}/wish")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 찜하기 성공")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ 찜하기 실패: {response.status_code}")
        print(response.text)

def test_lesson_apply():
    """수업 신청 API 테스트"""
    print("\n=== 수업 신청 API 테스트 ===")
    
    lesson_id = 1
    response = requests.post(f"{BASE_URL}/lessons/{lesson_id}/apply")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 수업 신청 성공")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"❌ 수업 신청 실패: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    try:
        test_lesson_detail()
        test_lesson_wish()
        test_lesson_apply()
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}") 