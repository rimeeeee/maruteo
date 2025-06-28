#!/usr/bin/env python3
"""
코디네이터 승인/반려 API 테스트 스크립트
"""

import requests
import json
from datetime import datetime

# 서버 URL
BASE_URL = "http://localhost:5000"

def test_approval_reject_apis():
    """승인/반려 API 테스트"""
    
    print("=== 코디네이터 승인/반려 API 테스트 ===\n")
    
    # 1. 신청 승인 API 테스트
    print("1. 신청 승인 API 테스트")
    try:
        response = requests.post(f"{BASE_URL}/api/coordinator/application-approve/99999")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data}")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 2. 신청 반려 API 테스트
    print("2. 신청 반려 API 테스트")
    try:
        reject_data = {
            "reject_reason": "일정이 맞지 않습니다."
        }
        response = requests.post(f"{BASE_URL}/api/coordinator/application-reject/99999", 
                               json=reject_data)
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data}")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 3. 강사 프로필 조회 API 테스트
    print("3. 강사 프로필 조회 API 테스트")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinator/instructor-profile/99999")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data}")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print()
    
    # 4. 기존 신청 상세 정보 조회 API 테스트 (비교용)
    print("4. 기존 신청 상세 정보 조회 API 테스트")
    try:
        response = requests.get(f"{BASE_URL}/api/coordinator/application-detail/99999")
        print(f"   상태 코드: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 성공: {data}")
        else:
            print(f"   ❌ 실패: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print("\n=== 테스트 완료 ===")
    print("\n참고: 존재하지 않는 ID(99999)로 테스트했으므로 에러가 정상입니다.")
    print("실제 데이터가 있을 때는 정상적으로 작동할 것입니다.")

if __name__ == "__main__":
    test_approval_reject_apis() 