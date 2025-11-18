# 🚀 메디-고 빠른 시작 가이드

이 가이드는 프로젝트를 가장 빠르게 실행하는 방법을 안내합니다.

## ⚡ 5분 만에 시작하기

### 1단계: 필수 프로그램 설치 확인

```bash
# Python 버전 확인 (3.11 이상)
python --version

# Node.js 버전 확인 (18 이상)
node --version

# PostgreSQL 확인
psql --version
```

### 2단계: 데이터베이스 생성

```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE medigo_db;
\q
```

### 3단계: Backend 실행

```bash
# 백엔드 디렉토리로 이동
cd backend

# 가상환경 생성 및 활성화
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 복사
copy env.example .env    # Windows
cp env.example .env      # Mac/Linux

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload
```

✅ Backend API: http://localhost:8000/docs

### 4단계: Frontend 실행 (새 터미널)

```bash
# 프론트엔드 디렉토리로 이동
cd frontend

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```

✅ 사용자 앱: http://localhost:3000

### 5단계: 로그인

1. http://localhost:3000 접속
2. "데모 로그인" 버튼 클릭
3. 홈 화면으로 이동

## 🎉 완료!

이제 다음 기능을 테스트할 수 있습니다:
- ✅ 처방전 업로드 (이미지 파일)
- ✅ 주문 생성
- ✅ 주문 목록 조회
- ✅ 프로필 관리

## 🔧 문제 해결

### 데이터베이스 연결 오류
```bash
# PostgreSQL이 실행 중인지 확인
# Windows
services.msc → PostgreSQL 서비스 확인

# Mac
brew services list

# Linux
sudo systemctl status postgresql
```

### 포트 이미 사용 중 오류
```bash
# Windows: 포트 사용 중인 프로세스 종료
netstat -ano | findstr :8000
taskkill /PID <PID번호> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Python 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

## 📚 다음 단계

1. [상세 설정 가이드](docs/SETUP.md)
2. [API 문서](docs/API.md)
3. [배포 가이드](docs/DEPLOYMENT.md)

## 💡 주요 URL

| 서비스 | URL | 설명 |
|--------|-----|------|
| Backend API | http://localhost:8000 | FastAPI 서버 |
| API 문서 | http://localhost:8000/docs | Swagger UI |
| 사용자 앱 | http://localhost:3000 | React 앱 |
| 관리자 대시보드 | http://localhost:3001 | Admin 패널 |
| OCR 서비스 | http://localhost:8001 | OCR API |

## 🆘 도움이 필요하신가요?

- 📖 [전체 문서](docs/) 폴더 확인
- 🐛 이슈 생성
- 💬 팀원에게 문의

