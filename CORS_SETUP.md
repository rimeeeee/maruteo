# CORS 설정 가이드

## 현재 설정 (개발 환경)
- 로컬 포트 5173에서의 요청 허용
- 기본값: `http://localhost:5173,http://127.0.0.1:5173`

## 배포 시 설정 방법

### 1. 환경변수 설정
배포 플랫폼에서 `CORS_ORIGINS` 환경변수를 설정하세요.

#### 예시:
```bash
# Vercel 배포 시
CORS_ORIGINS=https://your-app.vercel.app,https://yourdomain.com

# Netlify 배포 시  
CORS_ORIGINS=https://your-app.netlify.app,https://yourdomain.com

# AWS 배포 시
CORS_ORIGINS=https://your-bucket.s3.amazonaws.com,https://yourdomain.com
```

### 2. 로컬 개발 환경 설정
프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가:

```env
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 3. 배포 플랫폼별 설정 방법

#### Vercel
1. Vercel 대시보드 → 프로젝트 → Settings → Environment Variables
2. `CORS_ORIGINS` 추가
3. 값: `https://your-app.vercel.app,https://yourdomain.com`

#### Netlify
1. Netlify 대시보드 → Site settings → Environment variables
2. `CORS_ORIGINS` 추가
3. 값: `https://your-app.netlify.app,https://yourdomain.com`

#### Railway
1. Railway 대시보드 → 프로젝트 → Variables
2. `CORS_ORIGINS` 추가
3. 값: `https://your-app.railway.app,https://yourdomain.com`

### 4. 여러 도메인 허용
여러 도메인을 허용하려면 쉼표로 구분:

```bash
CORS_ORIGINS=https://app1.vercel.app,https://app2.netlify.app,https://yourdomain.com
```

### 5. 모든 도메인 허용 (개발용)
⚠️ **보안상 권장하지 않음**

```bash
CORS_ORIGINS=*
```

## 현재 코드 구조
- `app/config.py`: 환경변수에서 CORS origins 로드
- `app/__init__.py`: CORS 설정 적용
- 기본값으로 로컬 개발 환경 지원

## 주의사항
1. 프로덕션에서는 특정 도메인만 허용하세요
2. `*` 사용은 보안상 위험합니다
3. HTTPS 도메인만 허용하는 것을 권장합니다 