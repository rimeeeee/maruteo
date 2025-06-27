import urllib.request
import json

def test_lesson_detail():
    """수업 상세 정보 API 테스트"""
    print("=== 수업 상세 정보 API 테스트 ===")
    
    try:
        # 수업 상세 정보 가져오기
        url = "http://localhost:5000/api/lessons/1/detail"
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            if data.get('success'):
                print("✅ 수업 상세 정보 조회 성공")
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
                print("❌ API 응답 실패")
                print(data)
                
    except urllib.error.URLError as e:
        print(f"❌ 서버 연결 오류: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def test_lesson_list():
    """수업 목록 API 테스트"""
    print("\n=== 수업 목록 API 테스트 ===")
    
    try:
        url = "http://localhost:5000/api/lessons"
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            if data.get('success'):
                print("✅ 수업 목록 조회 성공")
                lessons = data.get('data', [])
                print(f"총 {len(lessons)}개의 수업이 있습니다.")
                
                for i, lesson in enumerate(lessons[:3], 1):  # 처음 3개만 출력
                    print(f"\n{i}. {lesson.get('title')}")
                    print(f"   강사: {lesson.get('instructor_name')}")
                    print(f"   찜수: {lesson.get('wish_count')}")
            else:
                print("❌ API 응답 실패")
                print(data)
                
    except urllib.error.URLError as e:
        print(f"❌ 서버 연결 오류: {e}")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    test_lesson_detail()
    test_lesson_list() 