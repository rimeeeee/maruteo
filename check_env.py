#!/usr/bin/env python3
"""
Railway 환경변수 확인 스크립트
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def check_environment_variables():
    print("=== Railway 환경변수 확인 ===")
    print()
    
    # 주요 환경변수들 확인
    env_vars = [
        'DATABASE_URL',
        'JWT_SECRET_KEY', 
        'SECRET_KEY',
        'CORS_ORIGINS',
        'FLASK_ENV',
        'PORT'
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            # 민감한 정보는 일부만 표시
            if 'SECRET' in var or 'KEY' in var:
                display_value = value[:10] + "..." if len(value) > 10 else value
            elif 'DATABASE_URL' in var:
                # 데이터베이스 URL에서 비밀번호 부분 숨김
                if '@' in value:
                    parts = value.split('@')
                    if len(parts) == 2:
                        user_pass = parts[0].split('://')
                        if len(user_pass) == 2:
                            protocol = user_pass[0]
                            user = user_pass[1].split(':')[0]
                            display_value = f"{protocol}://{user}:***@{parts[1]}"
                        else:
                            display_value = "***"
                    else:
                        display_value = "***"
                else:
                    display_value = value
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: 설정되지 않음")
    
    print()
    print("=== 추가 환경변수들 ===")
    
    # 모든 환경변수 출력 (민감한 정보 제외)
    for key, value in os.environ.items():
        if any(sensitive in key.upper() for sensitive in ['SECRET', 'KEY', 'PASSWORD', 'TOKEN']):
            display_value = value[:10] + "..." if len(value) > 10 else value
        else:
            display_value = value
        print(f"{key}: {display_value}")

if __name__ == "__main__":
    check_environment_variables() 