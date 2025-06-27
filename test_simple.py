#!/usr/bin/env python3
"""
간단한 API 테스트 스크립트
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_popular_lessons():
    """인기 수업 API 테스트"""
    print("🔍 인기 수업 API 테스트 중...")
    try:
        response = requests.get(f"{BASE_URL}/main/popular-lessons")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_popular_instructors():
    """인기 강사 API 테스트"""
    print("\n🔍 인기 강사 API 테스트 중...")
    try:
        response = requests.get(f"{BASE_URL}/main/popular-instructors")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_main_dashboard():
    """메인 대시보드 API 테스트"""
    print("\n🔍 메인 대시보드 API 테스트 중...")
    try:
        response = requests.get(f"{BASE_URL}/main/dashboard")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def test_categories():
    """카테고리 API 테스트"""
    print("\n🔍 카테고리 API 테스트 중...")
    try:
        response = requests.get(f"{BASE_URL}/categories")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("🚀 API 테스트를 시작합니다...")
    print("서버가 실행 중인지 확인하세요: http://localhost:5000")
    
    tests = [
        test_popular_lessons,
        test_popular_instructors,
        test_main_dashboard,
        test_categories
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print(f"\n📊 테스트 결과:")
    print(f"성공: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 모든 테스트가 성공했습니다!")
    else:
        print("⚠️ 일부 테스트가 실패했습니다.")

if __name__ == '__main__':
    main() 