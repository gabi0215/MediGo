# 📦 메디-고 설치 가이드

## 🎯 빠른 설치

### Python 환경 (Backend + ML)

```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. 전체 패키지 설치
pip install -r requirements.txt
```

### Node.js 환경 (Frontend + Admin)

```bash
# Frontend 설치
cd frontend
npm install

# Admin 설치
cd ../admin
npm install
```

## 📋 상세 설치 가이드

### 1️⃣ Python 패키지 (Backend + ML)

#### 옵션 A: 전체 설치 (권장)

```bash
pip install -r requirements.txt
```

#### 옵션 B: 개별 설치

**Backend만 설치:**
```bash
cd backend
pip install -r requirements.txt
```

**ML/OCR만 설치:**
```bash
cd ml
pip install -r requirements.txt
```

### 2️⃣ Frontend (React 사용자 앱)

```bash
cd frontend
npm install

# 또는
yarn install
```

**주요 패키지:**
- React 18
- TypeScript 5
- Material-UI (MUI)
- React Query
- Zustand
- Vite

### 3️⃣ Admin (관리자 대시보드)

```bash
cd admin
npm install
```

**주요 패키지:**
- React 18
- React Admin
- Material-UI

## 🔧 필수 시스템 요구사항

### Python
- **버전**: Python 3.11 이상
- **확인**: `python --version`

### Node.js
- **버전**: Node.js 18 이상
- **확인**: `node --version`

### PostgreSQL
- **버전**: PostgreSQL 15 이상
- **확인**: `psql --version`

### 운영체제
- Windows 10/11
- macOS 10.15+
- Ubuntu 20.04+

## 📦 패키지 목록

### Backend Core (FastAPI)
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
alembic==1.13.0
```

### Authentication
```
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
PyJWT==2.8.0
```

### Database
```
psycopg2-binary==2.9.9
```

### AWS Services
```
boto3==1.34.10
```

### OCR & ML
```
easyocr==1.7.0
opencv-python==4.8.1.78
torch==2.1.1
transformers==4.35.2
```

## 🚀 설치 확인

### Backend 서버 실행

```bash
cd backend
python -m uvicorn app.main:app --reload
```

성공하면:
```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

### Frontend 실행

```bash
cd frontend
npm run dev
```

성공하면:
```
VITE v5.0.8  ready in 500 ms
➜  Local:   http://localhost:3000/
```

### OCR 서비스 실행

```bash
cd ml
python ocr/ocr_api.py
```

성공하면:
```
INFO: Uvicorn running on http://127.0.0.1:8001
```

## 🐛 트러블슈팅

### Python 패키지 설치 오류

**오류**: `error: Microsoft Visual C++ 14.0 or greater is required`

**해결**:
```bash
# pip 업그레이드
pip install --upgrade pip

# 문제 패키지 재설치
pip install --no-cache-dir package-name
```

### PyTorch 설치 오류

**CPU 버전만 필요한 경우**:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**GPU (CUDA) 버전**:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### EasyOCR 설치 오류

**OpenCV 의존성 문제**:
```bash
pip install opencv-python-headless
```

### psycopg2 설치 오류

**Windows에서**:
```bash
pip install psycopg2-binary
```

**Mac에서**:
```bash
brew install postgresql
pip install psycopg2-binary
```

### Node.js 패키지 설치 오류

```bash
# 캐시 삭제
npm cache clean --force

# 재설치
rm -rf node_modules package-lock.json
npm install
```

## 📊 설치 용량

- **Backend**: ~500MB
- **ML/OCR**: ~2GB (PyTorch 포함)
- **Frontend**: ~300MB
- **Admin**: ~200MB
- **총**: ~3GB

## ⚡ 빠른 설치 스크립트

### Windows (PowerShell)

```powershell
# install.ps1
Write-Host "메디-고 설치 시작..." -ForegroundColor Green

# Python 패키지
Write-Host "Python 패키지 설치 중..." -ForegroundColor Yellow
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt

# Frontend
Write-Host "Frontend 패키지 설치 중..." -ForegroundColor Yellow
cd frontend
npm install
cd ..

# Admin
Write-Host "Admin 패키지 설치 중..." -ForegroundColor Yellow
cd admin
npm install
cd ..

Write-Host "설치 완료!" -ForegroundColor Green
```

### Mac/Linux (Bash)

```bash
#!/bin/bash
# install.sh

echo "메디-고 설치 시작..."

# Python 패키지
echo "Python 패키지 설치 중..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
echo "Frontend 패키지 설치 중..."
cd frontend
npm install
cd ..

# Admin
echo "Admin 패키지 설치 중..."
cd admin
npm install
cd ..

echo "설치 완료!"
```

**실행**:
```bash
# Mac/Linux
chmod +x install.sh
./install.sh

# Windows
powershell -ExecutionPolicy Bypass -File install.ps1
```

## 🔄 업데이트

```bash
# Python 패키지 업데이트
pip install -r requirements.txt --upgrade

# Node.js 패키지 업데이트
cd frontend && npm update
cd ../admin && npm update
```

## 📚 다음 단계

설치가 완료되면:

1. [환경 변수 설정](docs/SETUP.md)
2. [데이터베이스 설정](docs/SETUP.md#2-데이터베이스-설정)
3. [서버 실행](QUICKSTART.md)
4. [카카오톡 채널 설정](KAKAO_CHANNEL_QUICKSTART.md)

## 💡 팁

- **개발 환경**: Backend만 설치해도 API 개발 가능
- **GPU 없는 환경**: `torch` 대신 `torch-cpu` 설치
- **메모리 부족**: ML 패키지는 나중에 설치 가능
- **빠른 설치**: `--no-cache-dir` 옵션 사용

---

문의사항은 이슈를 생성해주세요!

