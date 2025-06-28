# 코디네이터 대시보드

## 개요
코디네이터 운영 대시보드는 강의 매칭 신청을 관리하고 수업 일정을 확인할 수 있는 페이지입니다.

## 주요 기능

### 1. 날짜 선택
- 상단에 날짜 선택 바가 표시됩니다
- 오늘부터 7일간의 날짜 버튼이 제공됩니다
- 날짜를 클릭하면 해당 날짜의 정보가 표시됩니다

### 2. 신규 요청 확인
- 선택한 날짜의 신규 신청 내역을 타임라인 형태로 표시
- 각 신청에 대한 상세 정보 제공:
  - 수업명
  - 신청자 정보 (이름, 연락처)
  - 선택한 시간
  - 수업 시간 및 장소
  - 신청 시간
- 승인/거절 버튼으로 신청 상태 관리

### 3. 진행 예정 수업
- 선택한 날짜의 진행 예정 수업 목록 표시
- 각 수업에 대한 정보:
  - 수업명
  - 강사명
  - 수업 시간 및 장소
  - 신청자 수 / 최대 인원
  - 신청 현황 진행률 바

## API 엔드포인트

### 1. 대시보드 페이지
```
GET /coordinator/dashboard
```
- 코디네이터 대시보드 메인 페이지

### 2. 신규 신청 조회
```
GET /api/coordinator/new-applications/{date}
```
- 특정 날짜의 신규 신청 내역 조회
- 응답 예시:
```json
{
  "success": true,
  "applications": [
    {
      "id": 1,
      "lesson_title": "요리 수업",
      "lesson_time": "14:00-16:00",
      "lesson_location": "주민센터",
      "applicant_name": "김철수",
      "applicant_phone": "010-1234-5678",
      "selected_time": "14:00",
      "created_at": "2024-01-15 10:30",
      "status": "신청됨"
    }
  ]
}
```

### 3. 진행 예정 수업 조회
```
GET /api/coordinator/upcoming-lessons/{date}
```
- 특정 날짜의 진행 예정 수업 조회
- 응답 예시:
```json
{
  "success": true,
  "lessons": [
    {
      "id": 1,
      "title": "요리 수업",
      "time": "14:00-16:00",
      "location": "주민센터",
      "instructor_name": "박영희",
      "applicant_count": 5,
      "max_students": 10
    }
  ]
}
```

### 4. 신청 상태 업데이트
```
POST /api/coordinator/application-status
```
- 신청 상태를 승인 또는 거절로 변경
- 요청 본문:
```json
{
  "application_id": 1,
  "status": "승인됨"
}
```

### 5. 날짜 범위 조회
```
GET /api/coordinator/date-range
```
- 신청이 있는 날짜 범위 조회
- 응답 예시:
```json
{
  "success": true,
  "dates": ["2024-01-15", "2024-01-16", "2024-01-17"]
}
```

## 사용법

### 1. 서버 실행
```bash
python run.py
```

### 2. 대시보드 접근
브라우저에서 다음 URL로 접근:
```
http://localhost:5000/coordinator/dashboard
```

### 3. 테스트 실행
```bash
python test_coordinator_dashboard.py
```

## 화면 구성

### 상단 헤더
- 코디네이터 대시보드 제목
- 현재 날짜 표시

### 날짜 선택 섹션
- 오늘부터 7일간의 날짜 버튼
- 선택된 날짜는 파란색으로 강조 표시

### 신규 요청 섹션
- 선택한 날짜의 신규 신청 내역
- 타임라인 형태로 표시
- 각 신청에 대한 승인/거절 버튼

### 진행 예정 수업 섹션
- 선택한 날짜의 진행 예정 수업 목록
- 카드 형태로 표시
- 신청 현황 진행률 바 포함

## 스타일링

- Bootstrap 5.1.3 사용
- Font Awesome 6.0.0 아이콘 사용
- 반응형 디자인 적용
- 모던하고 깔끔한 UI

## 데이터베이스 연동

다음 테이블들과 연동됩니다:
- `application`: 신청 정보
- `lesson`: 수업 정보
- `user`: 사용자 정보

## 주의사항

1. 데이터베이스에 실제 신청 데이터가 있어야 정상적으로 작동합니다.
2. 날짜 형식은 'YYYY-MM-DD' 형태를 사용합니다.
3. 신청 상태는 '신청됨', '승인됨', '거절됨' 중 하나여야 합니다.
4. 이미지 URL은 실제 접근 가능한 URL이어야 합니다.

# 코디네이터 대시보드 API

## 개요
코디네이터 운영 대시보드를 위한 백엔드 API입니다. 강의 매칭 신청을 관리하고 수업 일정을 확인할 수 있습니다.

## API 엔드포인트

### 1. 신청 상세 정보 조회
```
GET /api/coordinator/application-detail/{application_id}
```
- 특정 신청의 상세 정보 조회
- 응답 예시:
```json
{
  "success": true,
  "application_detail": {
    "application_id": 1,
    "status": "신청됨",
    "selected_date": "2024-01-15",
    "selected_time": "14:00",
    "created_at": "2024-01-15 10:30",
    "lesson": {
      "id": 1,
      "title": "요리 수업",
      "description": "맛있는 요리를 배워보세요",
      "time": "14:00-16:00",
      "location": "주민센터",
      "image_url": "https://example.com/image.jpg",
      "video_url": "https://example.com/video.mp4",
      "materials": "조리도구, 재료",
      "max_students": 10,
      "price": 50000,
      "instructor_name": "박영희",
      "instructor_phone": "010-9876-5432"
    },
    "applicant": {
      "id": 2,
      "name": "김철수",
      "phone": "010-1234-5678",
      "email": "kim@example.com",
      "profile_image": "https://example.com/profile.jpg"
    }
  }
}
```

### 2. 신규 신청 조회
```
GET /api/coordinator/new-applications/{date}
```
- 특정 날짜의 신규 신청 내역 조회
- 응답 예시:
```json
{
  "success": true,
  "applications": [
    {
      "id": 1,
      "lesson_title": "요리 수업",
      "lesson_time": "14:00-16:00",
      "lesson_location": "주민센터",
      "lesson_image_url": "https://example.com/image.jpg",
      "applicant_name": "김철수",
      "applicant_phone": "010-1234-5678",
      "selected_time": "14:00",
      "created_at": "2024-01-15 10:30",
      "status": "신청됨"
    }
  ]
}
```

### 3. 진행 예정 수업 조회
```
GET /api/coordinator/upcoming-lessons/{date}
```
- 특정 날짜의 진행 예정 수업 조회
- 응답 예시:
```json
{
  "success": true,
  "lessons": [
    {
      "id": 1,
      "title": "요리 수업",
      "time": "14:00-16:00",
      "location": "주민센터",
      "instructor_name": "박영희",
      "applicant_count": 5,
      "max_students": 10
    }
  ]
}
```

### 4. 신청 상태 업데이트
```
POST /api/coordinator/application-status
```
- 신청 상태를 승인 또는 거절로 변경
- 요청 본문:
```json
{
  "application_id": 1,
  "status": "승인됨"
}
```
- 응답 예시:
```json
{
  "success": true
}
```

### 5. 날짜 범위 조회
```
GET /api/coordinator/date-range
```
- 신청이 있는 날짜 범위 조회
- 응답 예시:
```json
{
  "success": true,
  "dates": ["2024-01-15", "2024-01-16", "2024-01-17"]
}
```

## 요청상세페이지 구성 요소

신청 상세 정보 API는 다음 정보들을 포함합니다:

### 수업 정보
- **사진**: `lesson.image_url`
- **강의명**: `lesson.title`
- **수업 설명**: `lesson.description`
- **수업 시간**: `lesson.time`
- **수업 장소**: `lesson.location`
- **최대 인원수**: `lesson.max_students`
- **수업 가격**: `lesson.price`
- **강사 정보**: `lesson.instructor_name`, `lesson.instructor_phone`
- **준비물**: `lesson.materials`
- **동영상**: `lesson.video_url`

### 신청 정보
- **수업 날짜**: `selected_date`
- **수업 시간**: `selected_time`
- **신청 시간**: `created_at`
- **신청 상태**: `status`

### 신청자 정보
- **신청자 이름**: `applicant.name`
- **연락처**: `applicant.phone`
- **이메일**: `applicant.email`
- **프로필 이미지**: `applicant.profile_image`

## 사용법

### 1. 서버 실행
```bash
python run.py
```

### 2. API 테스트
```bash
python test_coordinator_dashboard.py
```

## 데이터베이스 연동

다음 테이블들과 연동됩니다:
- `application`: 신청 정보
- `lesson`: 수업 정보
- `user`: 사용자 정보

## 주의사항

1. 데이터베이스에 실제 신청 데이터가 있어야 정상적으로 작동합니다.
2. 날짜 형식은 'YYYY-MM-DD' 형태를 사용합니다.
3. 신청 상태는 '신청됨', '승인됨', '거절됨' 중 하나여야 합니다.
4. 이미지 URL은 실제 접근 가능한 URL이어야 합니다. 