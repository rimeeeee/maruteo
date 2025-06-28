#!/usr/bin/env python3
"""
코디네이터 대시보드 테스트 스크립트
"""

import requests
import json
from datetime import datetime, timedelta

# 서버 URL (로컬 테스트용)
BASE_URL = "http://localhost:5000"

def test_coordinator_dashboard():
    """코디네이터 대시보드 API 테스트"""
    
    print("=== 코디네이터 대시보드 테스트 ===\n")
    
    # 1. 대시보드 페이지 접근 테스트
    print("1. 대시보드 페이지 접근 테스트")
    try:
        response = requests.get(f"{BASE_URL}/coordinator/dashboard")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 대시보드 페이지 접근 성공")
        else:
            print("   ❌ 대시보드 페이지 접근 실패")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 2. 날짜 범위 API 테스트
    print("2. 날짜 범위 API 테스트")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinator/date-range")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 날짜 범위 조회 성공")
            print(f"   📅 조회된 날짜 수: {len(data.get('dates', []))}")
            if data.get('dates'):
                print(f"   📅 첫 번째 날짜: {data['dates'][0]}")
        else:
            print("   ❌ 날짜 범위 조회 실패")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 3. 오늘 날짜의 신규 신청 조회 테스트
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"3. 오늘({today}) 신규 신청 조회 테스트")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinator/new-applications/{today}")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 신규 신청 조회 성공")
            print(f"   📋 신청 건수: {len(data.get('applications', []))}")
            if data.get('applications'):
                app = data['applications'][0]
                print(f"   📋 첫 번째 신청: {app.get('lesson_title', 'N/A')} - {app.get('applicant_name', 'N/A')}")
                # 첫 번째 신청의 상세 정보 테스트를 위해 ID 저장
                first_application_id = app.get('id')
            else:
                first_application_id = None
        else:
            print("   ❌ 신규 신청 조회 실패")
            first_application_id = None
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        first_application_id = None
    
    print()
    
    # 4. 신청 상세 정보 조회 테스트
    if first_application_id:
        print(f"4. 신청 상세 정보 조회 테스트 (ID: {first_application_id})")
        try:
            response = requests.get(f"{BASE_URL}/api/coordinator/application-detail/{first_application_id}")
            print(f"   상태 코드: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 신청 상세 정보 조회 성공")
                detail = data.get('application_detail', {})
                print(f"   📋 수업명: {detail.get('lesson', {}).get('title', 'N/A')}")
                print(f"   👤 신청자: {detail.get('applicant', {}).get('name', 'N/A')}")
                print(f"   📅 선택 날짜: {detail.get('selected_date', 'N/A')}")
                print(f"   ⏰ 선택 시간: {detail.get('selected_time', 'N/A')}")
                print(f"   📍 수업 장소: {detail.get('lesson', {}).get('location', 'N/A')}")
                print(f"   👨‍🏫 강사: {detail.get('lesson', {}).get('instructor_name', 'N/A')}")
                print(f"   📸 수업 이미지: {'있음' if detail.get('lesson', {}).get('image_url') else '없음'}")
            else:
                print("   ❌ 신청 상세 정보 조회 실패")
        except Exception as e:
            print(f"   ❌ 오류: {e}")
    else:
        print("4. 신청 상세 정보 조회 테스트 (건너뜀 - 신청 데이터 없음)")
    
    print()
    
    # 5. 오늘 날짜의 진행 예정 수업 조회 테스트
    print(f"5. 오늘({today}) 진행 예정 수업 조회 테스트")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinator/upcoming-lessons/{today}")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 진행 예정 수업 조회 성공")
            print(f"   📚 수업 건수: {len(data.get('lessons', []))}")
            if data.get('lessons'):
                lesson = data['lessons'][0]
                print(f"   📚 첫 번째 수업: {lesson.get('title', 'N/A')} - {lesson.get('instructor_name', 'N/A')}")
        else:
            print("   ❌ 진행 예정 수업 조회 실패")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 6. 내일 날짜 테스트
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"6. 내일({tomorrow}) 데이터 조회 테스트")
    try:
        # 신규 신청 조회
        response = requests.get(f"{BASE_URL}/api/coordinator/new-applications/{tomorrow}")
        print(f"   신규 신청 상태 코드: {response.status_code}")
        
        # 진행 예정 수업 조회
        response = requests.get(f"{BASE_URL}/api/coordinator/upcoming-lessons/{tomorrow}")
        print(f"   진행 예정 수업 상태 코드: {response.status_code}")
        
        print("   ✅ 내일 날짜 데이터 조회 테스트 완료")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 7. 신청 상태 업데이트 테스트 (실제로는 신청 데이터가 있을 때만)
    if first_application_id:
        print(f"7. 신청 상태 업데이트 테스트 (ID: {first_application_id})")
        try:
            # 승인 테스트
            response = requests.post(f"{BASE_URL}/api/coordinator/application-status", 
                                   json={"application_id": first_application_id, "status": "승인됨"})
            print(f"   승인 요청 상태 코드: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("   ✅ 신청 승인 성공")
                else:
                    print(f"   ❌ 신청 승인 실패: {data.get('error', '알 수 없는 오류')}")
            else:
                print("   ❌ 신청 승인 요청 실패")
                
        except Exception as e:
            print(f"   ❌ 오류: {e}")
    else:
        print("7. 신청 상태 업데이트 테스트 (건너뜀 - 신청 데이터 없음)")
    
    print("\n=== 테스트 완료 ===")

if __name__ == "__main__":
    test_coordinator_dashboard() 