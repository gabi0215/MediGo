# 📋 메디-고 프로젝트 요약

## 🎯 프로젝트 개요

**메디-고(Medi-Go)** - AI 기반 약 배달 및 복약 지도 서비스

MVP 단계에서는 Wizard of Oz 방식으로 운영하며, 사용자에게 서비스 가치를 제공하면서 동시에 AI 모델 학습을 위한 데이터를 수집합니다.

## 📂 프로젝트 구조

```
medigo/
├── backend/              # FastAPI 백엔드 서버
│   ├── app/
│   │   ├── api/         # REST API 엔드포인트
│   │   ├── core/        # 설정, 보안, DB
│   │   ├── models/      # SQLAlchemy 모델
│   │   ├── schemas/     # Pydantic 스키마
│   │   └── services/    # 비즈니스 로직
│   ├── alembic/         # DB 마이그레이션
│   └── requirements.txt
│
├── frontend/            # React 사용자 웹앱
│   ├── src/
│   │   ├── api/        # API 클라이언트
│   │   ├── components/ # React 컴포넌트
│   │   ├── pages/      # 페이지 컴포넌트
│   │   └── stores/     # 상태 관리
│   └── package.json
│
├── admin/              # React 관리자 대시보드
│   └── package.json
│
├── ml/                 # AI/ML 모듈
│   ├── ocr/           # OCR 서비스 (EasyOCR)
│   ├── models/        # 학습된 모델 저장
│   └── training/      # 학습 스크립트
│
├── docker/            # Docker 설정
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── Dockerfile.admin
│   └── Dockerfile.ocr
│
├── docs/              # 문서
│   ├── API.md        # API 문서
│   ├── SETUP.md      # 설정 가이드
│   └── DEPLOYMENT.md # 배포 가이드
│
└── scripts/          # 유틸리티 스크립트
    ├── init_db.py
    └── create_admin.py
```

## 🏗️ 기술 스택

### Backend
- **FastAPI** 0.104+ - 고성능 비동기 웹 프레임워크
- **PostgreSQL** 15+ - 관계형 데이터베이스
- **SQLAlchemy** 2.0+ - ORM
- **Alembic** - DB 마이그레이션
- **JWT** - 인증/인가
- **AWS S3** - 이미지 저장
- **EasyOCR** - 한글 OCR

### Frontend
- **React** 18+ - UI 라이브러리
- **TypeScript** 5+ - 타입 안전성
- **Material-UI** - UI 컴포넌트
- **React Query** - 서버 상태 관리
- **Zustand** - 클라이언트 상태 관리
- **Vite** - 빌드 툴

### ML/AI
- **EasyOCR** - 약봉투/처방전 텍스트 추출
- **PyTorch** 2.0+ - 딥러닝 프레임워크
- **Transformers** - LLM (향후 사용)

### Infrastructure
- **Docker & Docker Compose** - 컨테이너화
- **AWS EC2** - 서버 호스팅
- **AWS RDS** - 데이터베이스
- **AWS S3** - 스토리지

## 🔑 핵심 기능 (MVP)

### 사용자 기능 (F-01 ~ F-06)
- ✅ **F-01**: 카카오 소셜 로그인
- ✅ **F-02**: 처방전 사진 촬영/업로드
- ✅ **F-03**: 배달 주소 입력 및 저장
- ✅ **F-04**: 주문 상태 추적 (접수 → 조제 중 → 배달 중 → 완료)
- ✅ **F-05**: 결제 방법 선택 (만나서 결제)
- ✅ **F-06**: 복약 지도 메시지 수신

### 관리자 기능 (F-07 ~ F-10)
- ✅ **F-07**: 신규 주문 접수 및 확인
- ✅ **F-08**: 주문 상태 업데이트
- ✅ **F-09**: 복약 지도 수동 작성 및 발송
- ✅ **F-10**: 약봉투 사진 업로드 (AI 데이터 수집)

## 📊 데이터베이스 스키마

### 주요 테이블
1. **users** - 사용자 정보
   - 카카오 OAuth 정보
   - 배달 주소
   - 계정 상태

2. **orders** - 주문 정보
   - 주문 상태 (submitted → processing → delivering → completed)
   - 배달 정보
   - 결제 정보

3. **prescriptions** - 처방전 정보
   - 처방전 이미지 (S3 URL)
   - 약봉투 이미지 (S3 URL)
   - OCR 텍스트

4. **medication_guidance** - 복약 지도
   - 복약 지도 텍스트
   - AI 생성 여부
   - 발송 정보

5. **training_data** - AI 학습 데이터
   - 약봉투 이미지
   - OCR 텍스트 (입력)
   - 복약 지도 (정답 레이블)

## 🚀 시작하기

### 빠른 시작 (5분)

```bash
# 1. 데이터베이스 생성
createdb medigo_db

# 2. Backend 실행
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
alembic upgrade head
uvicorn app.main:app --reload

# 3. Frontend 실행 (새 터미널)
cd frontend
npm install
npm run dev
```

✅ **사용자 앱**: http://localhost:3000  
✅ **API 문서**: http://localhost:8000/docs

자세한 내용은 [QUICKSTART.md](QUICKSTART.md) 참조

## 📝 API 엔드포인트

### 인증
- `POST /api/v1/auth/kakao` - 카카오 로그인
- `POST /api/v1/auth/refresh` - 토큰 갱신

### 사용자
- `GET /api/v1/users/me` - 내 프로필 조회
- `PUT /api/v1/users/me` - 내 프로필 수정

### 주문
- `POST /api/v1/orders` - 주문 생성
- `GET /api/v1/orders` - 내 주문 목록
- `GET /api/v1/orders/{order_id}` - 주문 상세
- `GET /api/v1/orders/{order_id}/status` - 주문 상태

### 관리자
- `GET /api/v1/admin/orders` - 전체 주문 목록
- `PUT /api/v1/admin/orders/{order_id}` - 주문 수정
- `POST /api/v1/admin/orders/{order_id}/medicine-bag` - 약봉투 업로드
- `POST /api/v1/admin/medication-guidance` - 복약 지도 작성

자세한 API 문서는 [docs/API.md](docs/API.md) 참조

## 🔒 보안

- ✅ **HTTPS** - 모든 통신 암호화
- ✅ **JWT** - 토큰 기반 인증
- ✅ **S3 암호화** - 서버 사이드 암호화 (AES256)
- ✅ **DB 암호화** - 민감 정보 암호화
- ✅ **접근 제어** - RBAC (Role-Based Access Control)

## 📈 KPI (목표: MVP 출시 3개월)

| 지표 | 목표 |
|------|------|
| 누적 주문 수 | 500건 |
| 사용자 재사용률 | 15% |
| 고객 만족도 (CSAT) | 4.0점 이상 |
| 데이터 수집률 | 95% |

## 🛣️ 로드맵

### Phase 1: MVP (현재)
- ✅ 프로젝트 구조 설정
- ⏳ Backend API 개발
- ⏳ Frontend 개발
- ⏳ 관리자 대시보드
- ⏳ OCR 통합
- ⏳ 카카오 로그인 연동

### Phase 2: AI 모델 개발
- ⏳ 데이터 수집 (500+ 주문)
- ⏳ OCR 데이터 전처리
- ⏳ LLM 파인튜닝 (LLaMA 3 기반)
- ⏳ 모델 배포

### Phase 3: 고도화
- ⏳ 실시간 배달 추적
- ⏳ 인앱 결제 연동
- ⏳ 복약 알림 기능
- ⏳ 약국 전용 어드민

## ⚠️ 법적 고지

본 서비스는 다음 법규를 준수해야 합니다:

1. **약사법** - 약 배달 관련 규제
2. **의료법** - 비대면 진료 관련 규제
3. **개인정보보호법** - 민감 의료정보 처리
4. **규제 샌드박스** - 서비스 운영 범위

⚠️ **MVP 개발 착수 전, 법률 전문가와 보건복지부 유권해석을 받아야 합니다.**

## 📚 문서

- 📖 [빠른 시작 가이드](QUICKSTART.md)
- 🔧 [상세 설정 가이드](docs/SETUP.md)
- 📡 [API 문서](docs/API.md)
- 🚀 [배포 가이드](docs/DEPLOYMENT.md)

## 🛠️ 개발 도구

### 추천 IDE
- **Backend**: VS Code + Python Extension
- **Frontend**: VS Code + ESLint + Prettier

### 추천 확장
- Python
- Pylance
- ESLint
- Prettier
- Docker
- Thunder Client (API 테스트)

## 🤝 기여 가이드

1. 이슈 생성
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 푸시 (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📞 문의

프로젝트 관련 문의사항은 이슈를 생성해주세요.

---

**구현 완료 일자**: 2024-01-16  
**버전**: 1.0.0  
**라이선스**: Private

