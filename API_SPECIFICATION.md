# 마루터 플랫폼 API 명세서

## 목차
1. [인증 API](#인증-api)
2. [수업 API](#수업-api)
3. [메인 페이지 API](#메인-페이지-api)
4. [카테고리 API](#카테고리-api)
5. [프로필 API](#프로필-api)
6. [마이페이지 API](#마이페이지-api)
7. [수업 신청 API](#수업-신청-api)
8. [리뷰 API](#리뷰-api)
9. [데이터베이스 관리 API](#데이터베이스-관리-api)

---

## 인증 API

### 1. 회원가입
- **기능**: 새로운 사용자 회원가입
- **Endpoint**: `/api/auth/register`
- **Method**: `POST`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body (JSON)**:
```json
{
  "role": "young|elder",
  "name": "홍길동",
  "email": "user@example.com",
  "phone": "010-1234-5678",
  "birth": "1990-01-01",
  "password": "password123",
  "confirm_password": "password123",
  "gender": "male|female",
  "address": "서울시 강남구",
  "bio": "한 줄 소개",
  "username": "nickname",
  "profile_image": "https://example.com/image.jpg",
  "have_talents": ["요리", "프로그래밍"],
  "want_talents": ["영어", "음악"]
}
```
- **Response**:
```json
{
  "message": "가입 성공"
}
```
- **예시 호출**:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "role": "young",
    "name": "홍길동",
    "email": "user@example.com",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

### 2. 로그인
- **기능**: 사용자 로그인 및 JWT 토큰 발급
- **Endpoint**: `/api/auth/login`
- **Method**: `POST`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body (JSON)**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
- **Response**:
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "1",
    "email": "user@example.com",
    "name": "홍길동",
    "userType": "young",
    "phone": "010-1234-5678",
    "birthDate": "1990-01-01"
  }
}
```
- **예시 호출**:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

---

## 수업 API

### 3. 수업 목록 조회 (역할별 필터링)
- **기능**: 사용자 역할에 따라 필터링된 수업 목록 조회 (청년은 어르신 수업만, 어르신은 청년 수업만)
- **Endpoint**: `/api/lesson/lessons`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
[
  {
    "id": 1,
    "title": "김치찌개 만들기",
    "description": "맛있는 김치찌개 만드는 방법",
    "location": "서울시 강남구",
    "time": "오후 2시-4시",
    "unavailable": [],
    "media_url": "https://example.com/video.mp4",
    "instructor_name": "김요리사",
    "instructor_role": "elder"
  }
]
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/lesson/lessons \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 4. 수업 등록
- **기능**: 새로운 수업 등록
- **Endpoint**: `/api/lesson/lessons`
- **Method**: `POST`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body (JSON)**:
```json
{
  "title": "김치찌개 만들기",
  "description": "맛있는 김치찌개 만드는 방법을 배워봅시다",
  "location": "서울시 강남구",
  "time": "오후 2시-4시",
  "unavailable": [],
  "media_url": "https://example.com/video.mp4"
}
```
- **Response**:
```json
{
  "msg": "Lesson created successfully"
}
```
- **예시 호출**:
```bash
curl -X POST http://localhost:5000/api/lesson/lessons \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "김치찌개 만들기",
    "description": "맛있는 김치찌개 만드는 방법",
    "location": "서울시 강남구",
    "time": "오후 2시-4시"
  }'
```

### 5. 수업 삭제
- **기능**: 내가 등록한 수업 삭제
- **Endpoint**: `/api/lesson/lessons/{lesson_id}`
- **Method**: `DELETE`
- **Path Params**: `lesson_id` (수업 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "msg": "수업이 삭제되었습니다"
}
```
- **예시 호출**:
```bash
curl -X DELETE http://localhost:5000/api/lesson/lessons/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6. 수업 상세 정보 조회
- **기능**: 특정 수업의 상세 정보 조회
- **Endpoint**: `/api/lesson/lessons/{lesson_id}/detail`
- **Method**: `GET`
- **Path Params**: `lesson_id` (수업 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "김치찌개 만들기",
    "description": "맛있는 김치찌개 만드는 방법",
    "location": "서울시 강남구",
    "time": "오후 2시-4시",
    "image_url": "https://example.com/image.jpg",
    "video_url": "https://example.com/video.mp4",
    "materials": ["김치", "돼지고기", "두부"],
    "instructor": {
      "id": 1,
      "name": "김요리사",
      "profile_image": "https://example.com/profile.jpg",
      "bio": "30년 경력의 요리사",
      "role": "elder"
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
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/lesson/lessons/1/detail
```

### 7. 수업 찜하기/찜해제
- **기능**: 수업 찜하기 또는 찜해제
- **Endpoint**: `/api/lesson/lessons/{lesson_id}/wish`
- **Method**: `POST`
- **Path Params**: `lesson_id` (수업 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "action": "added",
  "wish_count": 13,
  "message": "찜하기가 added되었습니다."
}
```
- **예시 호출**:
```bash
curl -X POST http://localhost:5000/api/lesson/lessons/1/wish \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 8. 수업 신청 폼 조회
- **기능**: 수업 신청 시 필요한 폼 정보 조회
- **Endpoint**: `/api/lesson/lessons/{lesson_id}/apply-form`
- **Method**: `GET`
- **Path Params**: `lesson_id` (수업 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": {
    "lesson": {
      "id": 1,
      "title": "김치찌개 만들기",
      "description": "맛있는 김치찌개 만드는 방법",
      "location": "서울시 강남구",
      "time": "오후 2시-4시",
      "max_students": 10,
      "price": 50000
    },
    "instructor": {
      "name": "김요리사",
      "profile_image": "https://example.com/profile.jpg",
      "bio": "30년 경력의 요리사"
    }
  }
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/lesson/lessons/1/apply-form
```

### 9. 수업 신청
- **기능**: 수업 신청하기
- **Endpoint**: `/api/lesson/lessons/{lesson_id}/apply`
- **Method**: `POST`
- **Path Params**: `lesson_id` (수업 ID)
- **Query Params**: 없음
- **Request Body (JSON)**:
```json
{
  "message": "수업 신청합니다!"
}
```
- **Response**:
```json
{
  "success": true,
  "message": "수업 신청이 완료되었습니다."
}
```
- **예시 호출**:
```bash
curl -X POST http://localhost:5000/api/lesson/lessons/1/apply \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "수업 신청합니다!"
  }'
```

### 10. 필터링된 수업 목록 조회
- **기능**: 역할별 필터링된 수업 목록 조회 (상세 버전)
- **Endpoint**: `/api/lesson/lessons/filtered`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "김치찌개 만들기",
      "description": "맛있는 김치찌개 만드는 방법",
      "location": "서울시 강남구",
      "time": "오후 2시-4시",
      "unavailable": [],
      "media_url": "https://example.com/video.mp4",
      "image_url": "https://example.com/image.jpg",
      "instructor_name": "김요리사",
      "instructor_role": "elder",
      "instructor_profile_image": "https://example.com/profile.jpg",
      "application_count": 5,
      "wish_count": 12,
      "avg_rating": 4.5,
      "review_count": 8,
      "created_at": "2024-01-15 14:30"
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/lesson/lessons/filtered \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 11. 쿼리 파라미터를 지원하는 수업 목록 조회
- **기능**: 다양한 필터링 옵션을 지원하는 수업 목록 조회
- **Endpoint**: `/api/lesson/`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 
  - `category`: 카테고리 ID (예: korean-food)
  - `instructor_role`: 강사 역할 (elder, young)
  - `sort`: 정렬 기준 (latest, popular, rating)
  - `page`: 페이지 번호 (기본값: 1)
  - `limit`: 페이지당 항목 수 (기본값: 10)
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "김치찌개 만들기",
      "description": "맛있는 김치찌개 만드는 방법",
      "location": "서울시 강남구",
      "time": "오후 2시-4시",
      "unavailable": [],
      "media_url": "https://example.com/video.mp4",
      "image_url": "https://example.com/image.jpg",
      "video_url": "https://example.com/video.mp4",
      "sub_category_id": "korean-food",
      "max_students": 10,
      "price": 50000,
      "instructor_name": "김요리사",
      "instructor_role": "elder",
      "instructor_profile_image": "https://example.com/profile.jpg",
      "application_count": 5,
      "wish_count": 12,
      "avg_rating": 4.5,
      "review_count": 8,
      "created_at": "2024-01-15 14:30"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "total_pages": 3
  }
}
```
- **예시 호출**:
```bash
curl -X GET "http://localhost:5000/api/lesson/?category=korean-food&instructor_role=elder&sort=latest&page=1&limit=4" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 메인 페이지 API

### 12. 첫화면 메시지
- **기능**: 첫화면 소개 메시지
- **Endpoint**: `/`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "message": "의성 해커톤 백엔드입니다~ 🚀",
  "description": "마루터 플랫폼 API 서버",
  "version": "1.0.0",
  "endpoints": {
    "auth": "/api/auth/login, /api/auth/register",
    "lessons": "/api/lesson/lessons",
    "main": "/main/dashboard",
    "categories": "/api/category/categories"
  }
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/
```

### 13. 인기 수업 카로셀
- **기능**: 인기 수업 카로셀 (요리 3개, IT 3개 총 6개)
- **Endpoint**: `/main/popular-lessons`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "김치찌개 만들기",
      "description": "맛있는 김치찌개 만드는 방법",
      "application_count": 5
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/main/popular-lessons \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 14. 찜한 수업 목록
- **기능**: 현재 로그인한 사용자가 찜한 수업들
- **Endpoint**: `/main/wished-lessons`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "김치찌개 만들기",
      "description": "맛있는 김치찌개 만드는 방법",
      "application_count": 5
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/main/wished-lessons \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 15. 인기 강사 목록
- **기능**: 인기 강사 - 신청수가 많은 순으로 정렬
- **Endpoint**: `/main/popular-instructors`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "김요리사",
      "username": "chef_kim",
      "profile_image": "https://example.com/profile.jpg",
      "bio": "30년 경력의 요리사",
      "total_applications": 25,
      "lesson_count": 5
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/main/popular-instructors
```

### 16. 메인 대시보드
- **기능**: 메인 대시보드 정보 조회
- **Endpoint**: `/main/dashboard`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "name": "홍길동",
      "role": "young"
    },
    "popular_lessons": [...],
    "wished_lessons": [...],
    "popular_instructors": [...]
  }
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/main/dashboard \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 17. 카테고리별 수업 목록
- **기능**: 특정 카테고리의 수업 목록 조회
- **Endpoint**: `/lessons/by-category/{category_id}`
- **Method**: `GET`
- **Path Params**: `category_id` (카테고리 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "김치찌개 만들기",
      "description": "맛있는 김치찌개 만드는 방법"
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/lessons/by-category/cooking
```

### 18. 소분류별 수업 목록
- **기능**: 특정 소분류의 수업 목록 조회
- **Endpoint**: `/lessons/by-subcategory/{sub_category_id}`
- **Method**: `GET`
- **Path Params**: `sub_category_id` (소분류 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "김치찌개 만들기",
      "description": "맛있는 김치찌개 만드는 방법"
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/lessons/by-subcategory/korean-food
```

---

## 카테고리 API

### 19. 모든 분류 정보 조회
- **기능**: 모든 분류 정보를 가져옴
- **Endpoint**: `/api/category/categories`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
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
        }
      ]
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/category/categories
```

### 20. 특정 대분류의 소분류 조회
- **기능**: 특정 대분류의 소분류들을 가져옴
- **Endpoint**: `/api/category/categories/{category_id}/subcategories`
- **Method**: `GET`
- **Path Params**: `category_id` (카테고리 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "korean-food",
      "name": "한식",
      "categoryId": "cooking"
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/category/categories/cooking/subcategories
```

### 21. 재능탐색 - 특정 소분류의 강사 목록
- **기능**: 특정 소분류의 강사 목록을 가져옴 (재능탐색 페이지)
- **Endpoint**: `/api/category/talent-exploration/{sub_category_id}/instructors`
- **Method**: `GET`
- **Path Params**: `sub_category_id` (소분류 ID)
- **Query Params**: 
  - `sort`: 정렬 기준 (latest, popular, wish_count, rating)
  - `page`: 페이지 번호 (기본값: 1)
  - `per_page`: 페이지당 항목 수 (기본값: 10)
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": {
    "instructors": [
      {
        "id": 1,
        "name": "김요리사",
        "username": "chef_kim",
        "profile_image": "https://example.com/profile.jpg",
        "bio": "30년 경력의 요리사",
        "avg_rating": 4.5,
        "review_count": 8,
        "total_wish_count": 25,
        "total_application_count": 15,
        "lesson_count": 5,
        "latest_lesson_date": "2024-01-15T14:30:00"
      }
    ],
    "total_count": 10,
    "page": 1,
    "per_page": 10,
    "total_pages": 1
  }
}
```
- **예시 호출**:
```bash
curl -X GET "http://localhost:5000/api/category/talent-exploration/korean-food/instructors?sort=popular&page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 22. 재능탐색 - 특정 소분류의 수업 목록
- **기능**: 특정 소분류의 수업 목록을 가져옴 (재능탐색 페이지)
- **Endpoint**: `/api/category/talent-exploration/{sub_category_id}/lessons`
- **Method**: `GET`
- **Path Params**: `sub_category_id` (소분류 ID)
- **Query Params**: 
  - `sort`: 정렬 기준 (latest, popular, wish_count, rating)
  - `page`: 페이지 번호 (기본값: 1)
  - `per_page`: 페이지당 항목 수 (기본값: 10)
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": {
    "lessons": [
      {
        "id": 1,
        "title": "김치찌개 만들기",
        "description": "맛있는 김치찌개 만드는 방법",
        "instructor_name": "김요리사",
        "avg_rating": 4.5,
        "wish_count": 12,
        "application_count": 5
      }
    ],
    "total_count": 10,
    "page": 1,
    "per_page": 10,
    "total_pages": 1
  }
}
```
- **예시 호출**:
```bash
curl -X GET "http://localhost:5000/api/category/talent-exploration/korean-food/lessons?sort=popular&page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 23. 재능탐색 - 강사 상세 정보
- **기능**: 특정 강사의 상세 정보 조회
- **Endpoint**: `/api/category/talent-exploration/instructors/{instructor_id}/detail`
- **Method**: `GET`
- **Path Params**: `instructor_id` (강사 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "김요리사",
    "username": "chef_kim",
    "profile_image": "https://example.com/profile.jpg",
    "bio": "30년 경력의 요리사",
    "avg_rating": 4.5,
    "review_count": 8,
    "total_wish_count": 25,
    "total_application_count": 15,
    "lesson_count": 5,
    "lessons": [...]
  }
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/category/talent-exploration/instructors/1/detail
```

### 24. 재능탐색 - 특정 강사의 수업 목록
- **기능**: 특정 강사의 수업 목록 조회
- **Endpoint**: `/api/category/talent-exploration/{sub_category_id}/instructors/{instructor_id}/lessons`
- **Method**: `cc`
- **Path Params**: 
  - `sub_category_id` (소분류 ID)
  - `instructor_id` (강사 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "김치찌개 만들기",
      "description": "맛있는 김치찌개 만드는 방법",
      "avg_rating": 4.5,
      "wish_count": 12,
      "application_count": 5
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/category/talent-exploration/korean-food/instructors/1/lessons
```

---

## 프로필 API

### 25. 프로필 조회
- **기능**: 현재 로그인한 사용자의 프로필 정보 조회
- **Endpoint**: `/api/profile/profile`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "id": 1,
  "role": "young",
  "name": "홍길동",
  "email": "user@example.com",
  "phone": "010-1234-5678",
  "birth": "1990-01-01",
  "gender": "male",
  "address": "서울시 강남구",
  "bio": "안녕하세요!",
  "username": "nickname",
  "profile_image": "https://example.com/image.jpg",
  "have_talents": ["요리", "프로그래밍"],
  "want_talents": ["영어", "음악"],
  "badges": ["찜 10회 이상", "활동 1년 이상"]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/profile/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 26. 프로필 수정
- **기능**: 현재 로그인한 사용자의 프로필 정보 수정
- **Endpoint**: `/api/profile/profile`
- **Method**: `PUT`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body (JSON)**:
```json
{
  "gender": "male",
  "address": "서울시 강남구",
  "bio": "안녕하세요!",
  "username": "nickname",
  "profile_image": "https://example.com/image.jpg",
  "have_talents": ["요리", "프로그래밍"],
  "want_talents": ["영어", "음악"]
}
```
- **Response**:
```json
{
  "msg": "Profile updated successfully"
}
```
- **예시 호출**:
```bash
curl -X PUT http://localhost:5000/api/profile/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "안녕하세요!",
    "username": "nickname"
  }'
```

---

## 마이페이지 API

### 27. 출석 및 약속 이행률 조회
- **기능**: 출석 및 약속 이행률 계산
- **Endpoint**: `/api/mypage/mypage/statistics`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "attendance_rate": 85.5,
  "fulfillment_rate": 92.3
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/mypage/mypage/statistics \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 28. 뱃지 조회
- **기능**: 사용자의 뱃지 정보 조회
- **Endpoint**: `/api/mypage/mypage/badges`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "badges": {
    "찜 10회 이상": false,
    "수업 진행 10회 이상": true,
    "활동 기간 1년 이상": false,
    "출석 및 약속 이행률 90% 이상": true
  }
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/mypage/mypage/badges \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 수업 신청 API

### 29. 수업 신청
- **기능**: 수업 신청하기
- **Endpoint**: `/api/apply/apply`
- **Method**: `POST`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body (JSON)**:
```json
{
  "lesson_id": 1
}
```
- **Response**:
```json
{
  "message": "수업 신청 완료"
}
```
- **예시 호출**:
```bash
curl -X POST http://localhost:5000/api/apply/apply \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "lesson_id": 1
  }'
```

### 30. 내 신청 목록 조회
- **기능**: 내가 신청한 수업 목록 조회
- **Endpoint**: `/api/apply/apply`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "lesson_id": 1,
    "status": "pending",
    "created_at": "2024-01-15T14:30:00"
  }u
]
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/apply/apply \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 리뷰 API

### 31. 수업 리뷰 목록 조회
- **기능**: 특정 수업의 리뷰들을 가져옴
- **Endpoint**: `/api/review/lesson/{lesson_id}/reviews`
- **Method**: `GET`
- **Path Params**: `lesson_id` (수업 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "lesson_id": 1,
      "user_id": 1,
      "rating": 5,
      "comment": "정말 좋은 수업이었습니다!",
      "created_at": "2024-01-15T14:30:00"
    }
  ]
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/review/lesson/1/reviews
```

### 32. 수업 리뷰 작성
- **기능**: 수업 리뷰 작성
- **Endpoint**: `/api/review/lesson/{lesson_id}/reviews`
- **Method**: `POST`
- **Path Params**: `lesson_id` (수업 ID)
- **Query Params**: 없음
- **Request Body (JSON)**:
```json
{
  "rating": 5,
  "comment": "정말 좋은 수업이었습니다!"
}
```
- **Response**:
```json
{
  "success": true,
  "message": "리뷰가 성공적으로 작성되었습니다.",
  "data": {
    "id": 1,
    "lesson_id": 1,
    "user_id": 1,
    "rating": 5,
    "comment": "정말 좋은 수업이었습니다!",
    "created_at": "2024-01-15T14:30:00"
  }
}
```
- **예시 호출**:
```bash
curl -X POST http://localhost:5000/api/review/lesson/1/reviews \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "정말 좋은 수업이었습니다!"
  }'
```

### 33. 리뷰 수정
- **기능**: 리뷰 수정
- **Endpoint**: `/api/review/review/{review_id}`
- **Method**: `PUT`
- **Path Params**: `review_id` (리뷰 ID)
- **Query Params**: 없음
- **Request Body (JSON)**:
```json
{
  "rating": 4,
  "comment": "수정된 리뷰입니다."
}
```
- **Response**:
```json
{
  "success": true,
  "message": "리뷰가 성공적으로 수정되었습니다.",
  "data": {
    "id": 1,
    "lesson_id": 1,
    "user_id": 1,
    "rating": 4,
    "comment": "수정된 리뷰입니다.",
    "created_at": "2024-01-15T14:30:00"
  }
}
```
- **예시 호출**:
```bash
curl -X PUT http://localhost:5000/api/review/review/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 4,
    "comment": "수정된 리뷰입니다."
  }'
```

### 34. 리뷰 삭제
- **기능**: 리뷰 삭제
- **Endpoint**: `/api/review/review/{review_id}`
- **Method**: `DELETE`
- **Path Params**: `review_id` (리뷰 ID)
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "message": "리뷰가 성공적으로 삭제되었습니다."
}
```
- **예시 호출**:
```bash
curl -X DELETE http://localhost:5000/api/review/review/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 데이터베이스 관리 API

### 35. 데이터베이스 초기화
- **기능**: 데이터베이스 초기화 및 샘플 데이터 추가
- **Endpoint**: `/api/db/init-db`
- **Method**: `POST`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "message": "데이터베이스가 초기화되었습니다"
}
```
- **예시 호출**:
```bash
curl -X POST http://localhost:5000/api/db/init-db
```

### 36. 테이블 재생성
- **기능**: 테이블만 다시 생성 (파일 삭제 없이)
- **Endpoint**: `/api/db/db/recreate-tables`
- **Method**: `GET, POST`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "message": "테이블이 다시 생성되고 샘플 데이터가 추가되었습니다."
}
```
- **예시 호출**:
```bash
curl -X POST http://localhost:5000/api/db/db/recreate-tables
```

### 37. 데이터베이스 상태 확인
- **기능**: 데이터베이스 상태 확인
- **Endpoint**: `/api/db/db/status`
- **Method**: `GET`
- **Path Params**: 없음
- **Query Params**: 없음
- **Request Body**: 없음
- **Response**:
```json
{
  "success": true,
  "data": {
    "users": 10,
    "lessons": 25
  }
}
```
- **예시 호출**:
```bash
curl -X GET http://localhost:5000/api/db/db/status
```

---

## 인증 헤더

대부분의 API는 JWT 토큰 인증이 필요합니다. 다음과 같이 Authorization 헤더를 포함해야 합니다:

```bash
Authorization: Bearer YOUR_JWT_TOKEN
```

## 에러 응답 형식

에러 발생 시 다음과 같은 형식으로 응답됩니다:

```json
{
  "success": false,
  "message": "에러 메시지"
}
```

## HTTP 상태 코드

- `200`: 성공
- `201`: 생성 성공
- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `404`: 리소스를 찾을 수 없음
- `500`: 서버 내부 오류 