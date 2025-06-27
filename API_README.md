# 메인페이지 API 문서

## 개요
메인페이지에 필요한 기능들을 위한 백엔드 API입니다. 새로운 대분류/소분류 시스템을 지원하며, 요리 3개, IT 3개 총 6개의 인기 수업을 카로셀로 제공합니다.

## 설치 및 설정

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 데이터베이스 마이그레이션
```bash
python migrate_db.py
```

### 3. 서버 실행
```bash
python run.py
```

## 분류 시스템

### 지원하는 대분류
- **요리 (cooking)**: 한식, 중식, 일식, 양식, 기타
- **IT (it)**: 스마트폰 사용, 배달앱 사용, 인터넷 뱅킹, 키오스크 사용법, 보이스 피싱, 기타
- **악기 (instrument)**: 피아노, 기타, 드럼, 우쿨렐레, 기타
- **운동 (exercise)**: 헬스, 요가, 걷기, 탁구, 기타
- **글쓰기 (writing)**: 일기, 편지, 시, 수필, 기타
- **미술 (art)**: 수채화, 색연필화, 캘리그라피, 종이접기, 기타
- **농업 (farming)**: 텃밭 가꾸기, 화분 관리, 작물 재배, 기타

## API 엔드포인트

### 1. 분류 관련 API

#### 모든 분류 가져오기
```
GET /api/categories
```

**응답 예시:**
```json
{
  "success": true,
  "data": [
    {
      "id": "cooking",
      "name": "요리",
      "sub_categories": [
        {
          "id": "korean-food",
          "name": "한식",
          "categoryId": "cooking"
        },
        {
          "id": "chinese-food",
          "name": "중식",
          "categoryId": "cooking"
        }
      ]
    }
  ]
}
```

#### 특정 대분류의 소분류 가져오기
```
GET /api/categories/{category_id}/subcategories
```

### 2. 수업 관련 API

#### 대분류별 수업 목록
```
GET /api/lessons/by-category/{category_id}
```

#### 소분류별 수업 목록
```
GET /api/lessons/by-subcategory/{sub_category_id}
```

#### 수업 상세 정보 조회
**GET** `/api/lessons/{lesson_id}/detail`

수업의 상세 정보를 조회합니다.

**응답 예시:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "김치찌개 만들기",
    "description": "맛있는 김치찌개를 만드는 방법을 배워봅시다...",
    "location": "서울시 강남구",
    "time": "오후 2시-4시",
    "image_url": "https://example.com/kimchi.jpg",
    "video_url": "https://example.com/kimchi-video.mp4",
    "materials": ["김치", "돼지고기", "두부", "양파", "대파", "고춧가루", "간장", "참기름"],
    "instructor": {
      "id": 1,
      "name": "김요리",
      "profile_image": "https://example.com/profile.jpg",
      "bio": "요리 전문가입니다",
      "role": "youth"
    },
    "category": {
      "name": "요리",
      "sub_category_name": "한식"
    },
    "stats": {
      "application_count": 5,
      "wish_count": 12,
      "avg_rating": 4.5,
      "review_count": 8
    },
    "user_info": {
      "is_wished": false,
      "can_apply": true
    },
    "created_at": "2024-01-15 14:30"
  }
}
```

#### 수업 찜하기/찜해제
**POST** `/api/lessons/{lesson_id}/wish`

수업을 찜하거나 찜해제합니다.

**응답 예시:**
```json
{
  "success": true,
  "action": "added",
  "wish_count": 13,
  "message": "찜하기가 added되었습니다."
}
```

#### 수업 신청
**POST** `/api/lessons/{lesson_id}/apply`

수업에 신청합니다.

**응답 예시:**
```json
{
  "success": true,
  "message": "수업 신청이 완료되었습니다."
}
```

### 3. 메인 대시보드 (모든 데이터 한번에)
```
GET /api/main/dashboard
```

**응답 예시:**
```json
{
  "success": true,
  "data": {
    "popular_lessons": [
      {
        "id": 1,
        "title": "맛있는 한식 요리",
        "description": "전통 한식 요리 배우기",
        "location": "서울시 강남구",
        "time": "오후 2시",
        "media_url": "https://example.com/video.mp4",
        "image_url": "https://res.cloudinary.com/example/image/upload/v123/cooking.jpg",
        "sub_category_id": "korean-food",
        "sub_category_name": "한식",
        "category_id": "cooking",
        "category_name": "요리",
        "instructor_id": 1,
        "instructor_name": "김요리",
        "wish_count": 0,
        "application_count": 5,
        "avg_rating": 4.5,
        "review_count": 12
      }
    ],
    "popular_instructors": [
      {
        "id": 1,
        "name": "김요리",
        "username": "chef_kim",
        "profile_image": "https://example.com/profile.jpg",
        "bio": "10년 경력의 요리 강사",
        "total_applications": 15,
        "lesson_count": 3
      }
    ],
    "wished_lessons": [
      {
        "id": 2,
        "title": "스마트폰 기초 사용법",
        "description": "스마트폰 기본 기능 배우기",
        "location": "서울시 서초구",
        "time": "오전 10시",
        "media_url": "https://example.com/video.mp4",
        "image_url": "https://res.cloudinary.com/example/image/upload/v123/smartphone.jpg",
        "sub_category_id": "smartphone-usage",
        "sub_category_name": "스마트폰 사용",
        "category_id": "it",
        "category_name": "IT",
        "instructor_id": 2,
        "instructor_name": "박IT",
        "wish_count": 0,
        "application_count": 3,
        "avg_rating": 4.2,
        "review_count": 8
      }
    ]
  }
}
```

### 4. 인기 수업 카로셀 (요리 3개, IT 3개)
```
GET /api/main/popular-lessons
```

**설명:** 요리 분류에서 3개, IT 분류에서 3개 총 6개의 인기 수업을 신청수 기준으로 정렬하여 반환합니다.

**응답 예시:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "맛있는 한식 요리",
      "description": "전통 한식 요리 배우기",
      "location": "서울시 강남구",
      "time": "오후 2시",
      "media_url": "https://example.com/video.mp4",
      "image_url": "https://res.cloudinary.com/example/image/upload/v123/cooking.jpg",
      "sub_category_id": "korean-food",
      "sub_category_name": "한식",
      "category_id": "cooking",
      "category_name": "요리",
      "instructor_id": 1,
      "instructor_name": "김요리",
      "wish_count": 0,
      "application_count": 5,
      "avg_rating": 4.5,
      "review_count": 12
    },
    {
      "id": 2,
      "title": "스마트폰 기초 사용법",
      "description": "스마트폰 기본 기능 배우기",
      "location": "서울시 서초구",
      "time": "오전 10시",
      "media_url": "https://example.com/video.mp4",
      "image_url": "https://res.cloudinary.com/example/image/upload/v123/smartphone.jpg",
      "sub_category_id": "smartphone-usage",
      "sub_category_name": "스마트폰 사용",
      "category_id": "it",
      "category_name": "IT",
      "instructor_id": 2,
      "instructor_name": "박IT",
      "wish_count": 0,
      "application_count": 3,
      "avg_rating": 4.2,
      "review_count": 8
    }
  ]
}
```

### 5. 찜한 수업 목록
```
GET /api/main/wished-lessons
```

**설명:** 현재 로그인한 사용자가 찜한 수업들을 반환합니다.
**인증:** 로그인 필요

### 6. 인기 강사 목록
```
GET /api/main/popular-instructors
```

**설명:** 신청수가 많은 순으로 정렬된 인기 강사들을 반환합니다.

### 7. 리뷰 관련 API

#### 수업 리뷰 목록 가져오기
```
GET /api/lesson/{lesson_id}/reviews
```

#### 리뷰 작성
```
POST /api/lesson/{lesson_id}/reviews
```

**요청 본문:**
```json
{
  "rating": 5,
  "comment": "정말 좋은 수업이었습니다!"
}
```

#### 리뷰 수정
```
PUT /api/review/{review_id}
```

#### 리뷰 삭제
```
DELETE /api/review/{review_id}
```

## 데이터베이스 스키마

### 새로운 테이블들

#### Category (대분류)
```sql
CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    category_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);
```

#### SubCategory (소분류)
```sql
CREATE TABLE sub_category (
    id INTEGER PRIMARY KEY,
    sub_category_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    category_id VARCHAR(50) REFERENCES category(category_id)
);
```

#### Review (리뷰)
```sql
CREATE TABLE review (
    id INTEGER PRIMARY KEY,
    lesson_id INTEGER REFERENCES lesson(id),
    user_id INTEGER REFERENCES user(id),
    rating INTEGER NOT NULL,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Wishlist (찜한 수업)
```sql
CREATE TABLE wishlist (
    user_id INTEGER REFERENCES user(id),
    lesson_id INTEGER REFERENCES lesson(id),
    PRIMARY KEY (user_id, lesson_id)
);
```

### 수정된 모델
- **Lesson 모델:** `sub_category_id` 필드 추가, `image_url` 필드 추가, `categori_high`, `categori_middle` 제거
- **User 모델:** `wished_lessons` 관계 추가, Flask-Login 지원

## 사용 예시

### 프론트엔드에서 API 호출 예시

```javascript
// 카로셀 데이터 가져오기 (요리 3개, IT 3개)
fetch('/api/main/popular-lessons')
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      renderCarousel(data.data);
    }
  });

// 분류 데이터 가져오기
fetch('/api/categories')
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      renderCategories(data.data);
    }
  });

// 특정 대분류의 수업들 가져오기
function getLessonsByCategory(categoryId) {
  fetch(`/api/lessons/by-category/${categoryId}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        renderLessons(data.data);
      }
    });
}

// 메인 대시보드 데이터 가져오기
fetch('/api/main/dashboard')
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      const { popular_lessons, popular_instructors, wished_lessons } = data.data;
      
      // 인기 수업 카로셀 렌더링
      renderPopularLessons(popular_lessons);
      
      // 인기 강사 목록 렌더링
      renderPopularInstructors(popular_instructors);
      
      // 찜한 수업 목록 렌더링
      renderWishedLessons(wished_lessons);
    }
  });

// 수업 찜하기
function toggleWish(lessonId) {
  fetch(`/api/lesson/${lessonId}/wish`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include'
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // UI 업데이트
      updateWishButton(lessonId, data.action);
    }
  });
}

// 리뷰 작성
function createReview(lessonId, rating, comment) {
  fetch(`/api/lesson/${lessonId}/reviews`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      rating: rating,
      comment: comment
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert('리뷰가 작성되었습니다.');
      // 리뷰 목록 새로고침
      loadReviews(lessonId);
    }
  });
}
```

## 카로셀 데이터 구조

카로셀에서 반환되는 각 수업 데이터는 다음 정보를 포함합니다:

- **사진**: `image_url` (클라우디너리 URL)
- **분류**: `category_name` (예: "요리", "IT")
- **수업명**: `title`
- **강사명**: `instructor_name`
- **별점**: `avg_rating` (평균 별점, 소수점 첫째 자리까지)
- **리뷰수**: `review_count`

## 테스트 방법

### 브라우저에서 직접 테스트
1. 서버 실행: `python run.py`
2. 브라우저에서 다음 URL 접속:
   - 분류 목록: `http://localhost:5000/api/categories`
   - 카로셀: `http://localhost:5000/api/main/popular-lessons`
   - 메인 대시보드: `http://localhost:5000/api/main/dashboard`

### PowerShell에서 테스트
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/categories" -Method GET
Invoke-WebRequest -Uri "http://localhost:5000/api/main/popular-lessons" -Method GET
```

## 주의사항

1. **인증:** 찜하기 기능과 찜한 수업 조회는 로그인이 필요합니다.
2. **CORS:** 프론트엔드에서 API를 호출할 때 CORS 설정이 되어 있습니다.
3. **데이터베이스:** 새로운 분류 테이블들과 리뷰 테이블이 추가되므로 마이그레이션을 실행해야 합니다.
4. **Flask-Login:** 사용자 인증을 위해 Flask-Login이 설정되어 있습니다.
5. **분류 시스템:** 기존의 `categori_high`, `categori_middle` 필드는 `sub_category_id`로 대체되었습니다.
6. **라우트 수정:** 모든 API 엔드포인트에서 `/api` prefix 중복 문제를 해결했습니다.
7. **이미지 URL:** 클라우디너리에 업로드된 이미지 URL을 `image_url` 필드에 저장합니다.
8. **카로셀 구성:** 요리 3개, IT 3개 총 6개의 수업이 신청수 기준으로 정렬되어 반환됩니다. 