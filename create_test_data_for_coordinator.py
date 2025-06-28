#!/usr/bin/env python3
"""
코디네이터 API 테스트를 위한 샘플 데이터 생성 스크립트
"""

import requests
import json
from datetime import datetime, timedelta

# 서버 URL
BASE_URL = "http://localhost:5000"

def create_test_data():
    """테스트용 데이터 생성"""
    
    print("=== 코디네이터 API 테스트용 데이터 생성 ===\n")
    
    # 1. 테스트 사용자 생성 (어르신)
    print("1. 테스트 어르신 사용자 생성")
    elder_data = {
        "username": "test_elder",
        "email": "elder@test.com",
        "password": "test123",
        "name": "김어르신",
        "phone": "010-1111-2222",
        "role": "elder"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=elder_data)
        if response.status_code == 201:
            print("   ✅ 어르신 사용자 생성 성공")
            elder_user = response.json()
        else:
            print(f"   ❌ 어르신 사용자 생성 실패: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        return
    
    # 2. 테스트 사용자 생성 (청년 - 강사)
    print("2. 테스트 청년 사용자 생성")
    young_data = {
        "username": "test_young",
        "email": "young@test.com",
        "password": "test123",
        "name": "박청년",
        "phone": "010-3333-4444",
        "role": "young"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=young_data)
        if response.status_code == 201:
            print("   ✅ 청년 사용자 생성 성공")
            young_user = response.json()
        else:
            print(f"   ❌ 청년 사용자 생성 실패: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        return
    
    # 3. 청년으로 로그인하여 수업 생성
    print("3. 청년으로 로그인")
    login_data = {
        "email": "young@test.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            print("   ✅ 청년 로그인 성공")
            login_result = response.json()
            access_token = login_result.get('access_token')
        else:
            print(f"   ❌ 청년 로그인 실패: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        return
    
    # 4. 테스트 수업 생성
    print("4. 테스트 수업 생성")
    lesson_data = {
        "title": "요리 수업",
        "description": "맛있는 요리를 배워보세요",
        "location": "주민센터",
        "time": "14:00-16:00",
        "max_students": 10,
        "price": 50000,
        "materials": "조리도구, 재료"
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/api/lesson/lessons", 
                               json=lesson_data, headers=headers)
        if response.status_code == 201:
            print("   ✅ 수업 생성 성공")
            lesson = response.json()
            lesson_id = lesson.get('id')
        else:
            print(f"   ❌ 수업 생성 실패: {response.status_code}")
            print(f"   응답: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        return
    
    # 5. 어르신으로 로그인
    print("5. 어르신으로 로그인")
    elder_login_data = {
        "email": "elder@test.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=elder_login_data)
        if response.status_code == 200:
            print("   ✅ 어르신 로그인 성공")
            elder_login_result = response.json()
            elder_access_token = elder_login_result.get('access_token')
        else:
            print(f"   ❌ 어르신 로그인 실패: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        return
    
    # 6. 어르신이 수업 신청
    print("6. 어르신이 수업 신청")
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # 오늘 날짜로 신청
    apply_data_today = {
        "selected_date": today,
        "selected_time": "14:00"
    }
    
    elder_headers = {"Authorization": f"Bearer {elder_access_token}"}
    
    try:
        response = requests.post(f"{BASE_URL}/api/lesson/lessons/{lesson_id}/apply", 
                               json=apply_data_today, headers=elder_headers)
        if response.status_code == 200:
            print("   ✅ 오늘 날짜 수업 신청 성공")
        else:
            print(f"   ❌ 오늘 날짜 수업 신청 실패: {response.status_code}")
            print(f"   응답: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    # 내일 날짜로도 신청
    apply_data_tomorrow = {
        "selected_date": tomorrow,
        "selected_time": "14:00"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/lesson/lessons/{lesson_id}/apply", 
                               json=apply_data_tomorrow, headers=elder_headers)
        if response.status_code == 200:
            print("   ✅ 내일 날짜 수업 신청 성공")
        else:
            print(f"   ❌ 내일 날짜 수업 신청 실패: {response.status_code}")
            print(f"   응답: {response.text}")
    except Exception as e:
        print(f"   ❌ 오류: {e}")
    
    print("\n=== 테스트 데이터 생성 완료 ===")
    print(f"생성된 수업 ID: {lesson_id}")
    print(f"오늘 날짜: {today}")
    print(f"내일 날짜: {tomorrow}")
    print("\n이제 test_coordinator_dashboard.py를 다시 실행해보세요!")

if __name__ == "__main__":
    create_test_data() 