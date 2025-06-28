#!/usr/bin/env python3
"""
간단한 코디네이터 API 테스트
"""

import requests
import json
from datetime import datetime

# 서버 URL
BASE_URL = "http://localhost:5000"

def test_coordinator_apis():
    """코디네이터 API 테스트"""
    
    print("=== 간단한 코디네이터 API 테스트 ===\n")
    
    # 1. 날짜 범위 API 테스트
    print("1. 날짜 범위 API 테스트")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinator/date-range")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data}")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 2. 오늘 날짜 신규 신청 조회
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"2. 오늘({today}) 신규 신청 조회")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinator/new-applications/{today}")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data}")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 3. 오늘 날짜 진행 예정 수업 조회
    print(f"3. 오늘({today}) 진행 예정 수업 조회")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinator/upcoming-lessons/{today}")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data}")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 4. 존재하지 않는 신청 상세 정보 조회 (404 테스트)
    print("4. 존재하지 않는 신청 상세 정보 조회 (404 테스트)")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinator/application-detail/99999")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data}")
        elif response.status_code == 404:
            print("   ✅ 예상된 404 응답")
        else:
            print(f"   ❌ 예상과 다른 응답: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 5. 신청 상태 업데이트 테스트 (존재하지 않는 ID)
    print("5. 신청 상태 업데이트 테스트 (존재하지 않는 ID)")
    try:
        response = requests.post(f"{BASE_URL}/api/coordinator/application-status", 
                               json={"application_id": 99999, "status": "승인됨"})
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data}")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print("\n=== 테스트 완료 ===")

if __name__ == "__main__":
    test_coordinator_apis() 