# Gemini Routes 기술 보고서

## 📋 개요

`gemini_routes.py`는 Flask 기반의 AI 채팅 및 음성 처리 서비스를 제공하는 백엔드 모듈입니다. 어르신들을 위한 수업 예약 시스템에 특화된 대화형 AI 서비스를 구현하고 있습니다.

**파일 위치**: `app/routes/gemini_routes.py`  
**총 라인 수**: 445줄  
**주요 목적**: AI 채팅봇, 음성 인식, 음성 합성 서비스 제공

---

## 🏗️ 아키텍처 및 기술 스택

### 기술 스택
- **웹 프레임워크**: Flask (Blueprint 패턴)
- **AI 모델**: Google Gemini 1.5 Flash
- **음성 처리**: Google Speech-to-Text, Text-to-Speech API
- **세션 관리**: 인메모리 세션 저장소
- **환경 설정**: python-dotenv
- **비동기 처리**: threading (세션 정리)

### 아키텍처 패턴
```
Client Request
     ↓
Flask Blueprint
     ↓
Session Management
     ↓
AI Processing (Gemini)
     ↓
Response Generation
```

---

## 🔧 주요 기능 분석

### 1. 세션 관리 시스템

```python
sessions = {}  # 인메모리 세션 저장소
```

- **세션 생성**: UUID 기반 고유 식별자
- **메시지 히스토리**: 세션별 대화 내역 관리
- **자동 정리**: 30분 비활성 세션 자동 삭제
- **상태 추적**: 활성/비활성 상태 모니터링

### 2. AI 채팅봇 시스템

#### 특화된 시스템 프롬프트
- **대상 사용자**: 어르신층
- **서비스 도메인**: 수업 예약
- **대화 스타일**: 존댓말, 친근한 톤
- **프로세스**: 5단계 예약 프로세스 (관심사 → 시간 → 추천 → 예약 → 취소)

#### AI 모델 설정
```python
model = genai.GenerativeModel('gemini-1.5-flash')
```

### 3. 음성 처리 시스템

#### Speech-to-Text (STT)
- **지원 형식**: WEBM_OPUS
- **샘플레이트**: 48kHz
- **언어**: 한국어 (ko-KR)
- **최적화**: 짧은 오디오에 특화

#### Text-to-Speech (TTS)
- **음성**: ko-KR-Wavenet-A (여성 음성)
- **출력 형식**: MP3
- **말하기 속도**: 0.9배속 (어르신 친화적)

---

## 🌐 API 엔드포인트 상세

### 1. 헬스체크
```http
GET /health
```
**기능**: 서비스 상태 및 API 설정 확인
**응답**: 서비스 상태, 타임스탬프, Gemini API 설정 여부

### 2. 세션 관리

#### 세션 생성
```http
POST /chat/sessions
```
**기능**: 새로운 채팅 세션 생성
**응답**: 세션 ID, 생성 시간

#### 메시지 전송
```http
POST /chat/sessions/{session_id}/messages
```
**요청 본문**:
```json
{
  "content": "스마트폰 수업 듣고 싶어요",
  "type": "text"
}
```

#### 메시지 조회
```http
GET /chat/sessions/{session_id}/messages
```

#### 세션 상태 확인
```http
GET /chat/sessions/{session_id}/status
```

#### 세션 삭제
```http
DELETE /chat/sessions/{session_id}
```

### 3. 음성 처리

#### 음성 → 텍스트
```http
POST /speech-to-text
```
**요청**: Multipart form data (audio file)
**응답**: 텍스트, 신뢰도 점수

#### 텍스트 → 음성
```http
POST /text-to-speech
```
**요청 본문**:
```json
{
  "text": "안녕하세요. 수업 예약 도와드리겠습니다."
}
```

---

## 🎯 비즈니스 로직

### 수업 예약 프로세스

1. **관심사 파악**: 사용자 관심 수업 영역 확인
2. **수업 리스트 제공**: 동적 수업 목록 생성
3. **시간 확인**: 사용자 선호 시간대 조회
4. **맞춤 추천**: 시간대별 수업 추천
5. **예약 처리**: 무조건 예약 완료 처리 (거절 금지)

### 핵심 규칙
- 예약 요청 시 **절대 거절 금지**
- 수업 목록 동적 생성
- 어르신 친화적 언어 사용

---

## 🔒 보안 및 성능 고려사항

### 보안 이슈
1. **API 키 노출 위험**: 환경변수로 관리하지만 추가 보안 필요
2. **세션 하이재킹**: 인메모리 저장으로 서버 재시작 시 세션 소실
3. **파일 업로드 검증**: 음성 파일 크기/형식 제한 없음
4. **Rate Limiting**: API 호출 제한 없음

### 성능 이슈
1. **메모리 사용**: 모든 세션을 메모리에 저장
2. **동시성**: 멀티 스레드 환경에서 세션 경합 상태 가능
3. **API 의존성**: Google API 장애 시 서비스 중단

---

## ⚠️ 현재 문제점

### 1. 의존성 문제
```
- google.generativeai 모듈 누락
- dotenv 패키지 누락  
- google.cloud.texttospeech 모듈 사용하지 않음
```

### 2. 세션 관리
- **데이터 영속성 부족**: 서버 재시작 시 모든 세션 소실
- **확장성 제한**: 단일 서버 메모리에 의존
- **동시성 문제**: Thread-safe하지 않은 딕셔너리 사용

### 3. 오류 처리
- **부분적 오류 처리**: 일부 예외 상황 미처리
- **로깅 부족**: 디버깅을 위한 상세 로그 부족

---

## 🚀 개선 권장사항

### 1. 즉시 개선 사항

#### 의존성 설치
```bash
pip install google-generativeai python-dotenv
```

#### 환경변수 설정
```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_SPEECH_API_KEY=your_speech_api_key
```

### 2. 아키텍처 개선

#### 세션 저장소 변경
```python
# Redis 또는 데이터베이스 사용
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
```

#### Thread-safe 세션 관리
```python
import threading
session_lock = threading.Lock()
```

### 3. 보안 강화

#### Rate Limiting 추가
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@limiter.limit("10 per minute")
@gemini_bp.route('/chat/sessions/<session_id>/messages', methods=['POST'])
```

#### 파일 업로드 검증
```python
ALLOWED_AUDIO_TYPES = {'audio/webm', 'audio/wav', 'audio/mp3'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

### 4. 모니터링 및 로깅

#### 구조화된 로깅
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

#### 메트릭 수집
```python
# 세션 수, API 호출 수, 응답 시간 등
metrics = {
    'active_sessions': len(sessions),
    'total_messages': sum(len(s['messages']) for s in sessions.values())
}
```

---

## 📊 성능 메트릭

### 현재 상태
- **메모리 사용량**: 세션당 약 1-2KB
- **응답 시간**: Gemini API 의존 (평균 2-5초)
- **동시 사용자**: 메모리 제한에 따라 결정

### 예상 확장성
- **단일 서버**: 최대 1,000 동시 세션
- **Redis 사용 시**: 10,000+ 세션 가능
- **로드 밸런싱**: 무제한 확장 가능

---

## 🔮 향후 개발 방향

### 1. 마이크로서비스 분리
- AI 처리 서비스 분리
- 음성 처리 서비스 분리
- 세션 관리 서비스 분리

### 2. 실시간 기능 추가
- WebSocket 지원
- 실시간 음성 스트리밍
- 실시간 AI 응답

### 3. 고급 AI 기능
- 음성 감정 인식
- 개인화된 대화 패턴 학습
- 다국어 지원

---

## 📝 결론

`gemini_routes.py`는 어르신을 위한 수업 예약 서비스의 핵심 AI 모듈로서, Gemini AI와 Google Speech API를 활용한 포괄적인 대화형 인터페이스를 제공합니다. 

**장점**:
- 사용자 친화적 인터페이스
- 포괄적인 음성 처리 기능
- 체계적인 비즈니스 로직

**개선 필요 사항**:
- 의존성 및 보안 문제 해결
- 확장성을 위한 아키텍처 개선
- 모니터링 및 로깅 시스템 구축

적절한 개선을 통해 안정적이고 확장 가능한 AI 서비스로 발전시킬 수 있을 것으로 판단됩니다. 