#!/usr/bin/env python3
"""
CORS 테스트 스크립트
"""

import requests
import json

def test_cors():
    base_url = "http://localhost:5000"
    
    print("=== CORS 테스트 ===")
    print(f"서버 URL: {base_url}")
    print()
    
    # 테스트할 엔드포인트들
    endpoints = [
        "/",
        "/api/auth/login",
        "/api/lesson",
        "/api/category"
    ]
    
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"테스트 중: {endpoint}")
        
        try:
            # OPTIONS 요청 (preflight)
            print("  OPTIONS 요청...")
            response = requests.options(url, timeout=5)
            print(f"    상태코드: {response.status_code}")
            print(f"    CORS 헤더: {dict(response.headers)}")
            
            # GET 요청
            print("  GET 요청...")
            response = requests.get(url, timeout=5)
            print(f"    상태코드: {response.status_code}")
            print(f"    CORS 헤더: {dict(response.headers)}")
            
        except requests.exceptions.ConnectionError:
            print("    ❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        except requests.exceptions.Timeout:
            print("    ❌ 요청 시간 초과")
        except Exception as e:
            print(f"    ❌ 오류: {e}")
        
        print()

if __name__ == "__main__":
    test_cors() 