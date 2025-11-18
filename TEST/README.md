# 메디-고 (Medi-Go) 🏥💊

AI 기반 약 배달 및 복약 지도 서비스

## 📋 프로젝트 개요

처방전 사진을 앱으로 전송하면, 운영팀이 약국 조제 및 배달을 대행하고, 복약 지도 메시지를 앱을 통해 텍스트로 전달하는 서비스입니다.

### 핵심 기능 (MVP)
- 📱 카카오 소셜 로그인
- 📸 처방전 사진 업로드
- 🚚 약 배달 주문 및 상태 추적
- 💊 맞춤형 복약 지도 메시지 수신
- 💬 카카오톡 채널 메시지 발송
- 👥 고객 관리 (카카오톡 채널 고객파일)
- 👨‍💼 관리자 대시보드 (주문 관리, 복약 지도 작성)
- 🤖 AI 학습 데이터 수집 (OCR + 복약 지도 페어)

## 🏗️ 기술 스택

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0+
- **Migration**: Alembic
- **Authentication**: JWT + OAuth 2.0 (Kakao)
- **Image Storage**: AWS S3
- **OCR**: EasyOCR (한글 지원)

### Frontend (User App)
- **Framework**: React 18+
- **Language**: TypeScript 5+
- **UI Library**: Material-UI (MUI)
- **State Management**: React Query + Zustand
- **HTTP Client**: Axios
- **Build Tool**: Vite

### Admin Dashboard
- **Framework**: React 18+
- **Language**: TypeScript 5+
- **UI Library**: Material-UI (MUI) + React Admin
- **State Management**: React Query + Zustand

### AI/ML
- **OCR**: EasyOCR
- **Framework**: PyTorch 2.0+
- **Model**: Transformers (Hugging Face)
- **Target Model**: LLaMA 3 기반 한국어 모델 (향후)

### Infrastructure
- **Cloud**: AWS (EC2, S3, RDS)
- **Container**: Docker
- **Orchestration**: Docker Compose

## 📁 프로젝트 구조

```
medigo/
├── backend/              # FastAPI 백엔드 서버
│   ├── app/
│   │   ├── api/         # API 엔드포인트
│   │   ├── core/        # 설정, 보안, 의존성
│   │   ├── models/      # SQLAlchemy 모델
│   │   ├── schemas/     # Pydantic 스키마
│   │   ├── services/    # 비즈니스 로직
│   │   ├── utils/       # 유틸리티 함수
│   │   └── main.py      # 앱 진입점
│   ├── alembic/         # DB 마이그레이션
│   ├── tests/           # 테스트
│   └── requirements.txt
├── frontend/            # 사용자 웹앱 (React)
├── admin/              # 관리자 대시보드 (React)
├── ml/                 # AI/ML 모듈
│   ├── ocr/           # OCR 서비스
│   ├── models/        # 학습된 모델
│   ├── training/      # 학습 스크립트
│   └── requirements.txt
├── docs/              # 문서
│   ├── api/          # API 문서
│   ├── architecture/ # 아키텍처 문서
│   └── setup/        # 설정 가이드
├── scripts/          # 유틸리티 스크립트
├── docker/           # Docker 설정
└── docker-compose.yml
```

## 🚀 시작하기

### 사전 요구사항
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (선택사항)

### 1. Backend 설정

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload
```

### 2. Frontend 설정

```bash
cd frontend
npm install
cp .env.example .env
# .env 파일 편집

npm run dev
```

### 3. Admin 설정

```bash
cd admin
npm install
cp .env.example .env
npm run dev
```

### 4. ML 서비스 설정

```bash
cd ml
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 데이터베이스 스키마

주요 테이블:
- `users` - 사용자 정보
- `orders` - 주문 정보
- `prescriptions` - 처방전 정보
- `medication_guidance` - 복약 지도
- `training_data` - AI 학습 데이터

자세한 스키마는 `docs/database/schema.md` 참조

## 🔐 보안

- 모든 API 통신: HTTPS (SSL/TLS)
- 처방전 이미지: S3 서버 사이드 암호화
- 민감 정보: DB 암호화
- 인증: JWT 토큰 (Access + Refresh)
- 접근 제어: RBAC (Role-Based Access Control)

## 📝 API 문서

Backend 서버 실행 후:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 테스트

```bash
# Backend 테스트
cd backend
pytest

# Frontend 테스트
cd frontend
npm test
```

## 📈 개발 로드맵

### Phase 1: MVP (현재)
- [x] 프로젝트 구조 설정
- [ ] 백엔드 API 개발
- [ ] 프론트엔드 개발
- [ ] 관리자 대시보드 개발
- [ ] OCR 통합
- [ ] 카카오 로그인 연동

### Phase 2: AI 모델 개발
- [ ] 데이터 수집 (500+ 주문)
- [ ] OCR 데이터 전처리
- [ ] LLM 파인튜닝
- [ ] 모델 배포

### Phase 3: 고도화
- [ ] 실시간 배달 추적
- [ ] 인앱 결제 연동
- [ ] 복약 알림 기능
- [ ] 약국 전용 어드민

## ⚠️ 법적 고지

본 서비스는 약사법 및 의료법을 준수해야 합니다:
- 비대면 진료 및 약 배달 관련 규제 확인 필수
- 개인정보보호법 준수 (민감 의료정보 처리)
- 서비스 운영 전 법률 자문 필수

## 📞 문의

프로젝트 관련 문의사항은 이슈를 생성해주세요.

## 📄 라이선스

Private - All Rights Reserved

