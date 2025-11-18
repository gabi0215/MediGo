# 메디-고 프로젝트 설정 가이드

## 사전 요구사항

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- AWS 계정 (S3 사용)

## 1. 환경 변수 설정

### Backend (.env)

```bash
cd backend
cp .env.example .env
```

`.env` 파일을 열어 다음 값들을 설정하세요:

```env
# 필수 설정
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/medigo_db

# AWS 설정
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
S3_BUCKET_NAME=medigo-prescriptions

# 카카오 OAuth
KAKAO_CLIENT_ID=your-kakao-rest-api-key
KAKAO_CLIENT_SECRET=your-kakao-client-secret
```

## 2. 데이터베이스 설정

### PostgreSQL 설치 및 데이터베이스 생성

```bash
# PostgreSQL 설치 (Ubuntu)
sudo apt update
sudo apt install postgresql postgresql-contrib

# PostgreSQL 서비스 시작
sudo systemctl start postgresql

# 데이터베이스 생성
sudo -u postgres psql
CREATE DATABASE medigo_db;
CREATE USER medigo_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE medigo_db TO medigo_user;
\q
```

## 3. Backend 설정

```bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
alembic upgrade head

# 개발 서버 실행
uvicorn app.main:app --reload
```

API 문서: http://localhost:8000/docs

## 4. Frontend 설정

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

사용자 앱: http://localhost:3000

## 5. Admin 대시보드 설정

```bash
cd admin

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

관리자 대시보드: http://localhost:3001

## 6. ML/OCR 서비스 설정

```bash
cd ml

# 가상환경 생성
python -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# OCR 서비스 실행
cd ocr
python ocr_api.py
```

OCR API: http://localhost:8001

## 7. Docker를 사용한 설정 (선택사항)

```bash
# 프로젝트 루트에서
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 종료
docker-compose down
```

## AWS S3 버킷 설정

1. AWS 콘솔에서 S3 버킷 생성
   - 버킷명: `medigo-prescriptions` (또는 원하는 이름)
   - 리전: `ap-northeast-2` (서울)

2. 버킷 정책 설정 (서버 사이드 암호화 활성화)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowBackendAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:user/medigo-backend"
      },
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::medigo-prescriptions/*"
    }
  ]
}
```

3. IAM 사용자 생성 및 Access Key 발급

## 카카오 OAuth 설정

1. [Kakao Developers](https://developers.kakao.com)에서 애플리케이션 등록
2. REST API 키 복사 → `.env`의 `KAKAO_CLIENT_ID`에 설정
3. Redirect URI 설정: `http://localhost:3000/auth/kakao/callback`

## 트러블슈팅

### 데이터베이스 연결 오류

```bash
# PostgreSQL이 실행 중인지 확인
sudo systemctl status postgresql

# 연결 테스트
psql -h localhost -U postgres -d medigo_db
```

### 포트 충돌

- Backend: 8000
- OCR: 8001
- Frontend: 3000
- Admin: 3001
- PostgreSQL: 5432

이미 사용 중인 포트가 있다면 설정 파일에서 변경하세요.

### Python 패키지 설치 오류

```bash
# pip 업그레이드
pip install --upgrade pip

# 특정 패키지 재설치
pip install --force-reinstall package-name
```

## 다음 단계

- [ ] 테스트 데이터 생성
- [ ] API 엔드포인트 테스트
- [ ] 첫 주문 테스트
- [ ] OCR 정확도 테스트

