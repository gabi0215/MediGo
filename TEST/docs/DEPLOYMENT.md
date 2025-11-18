# 메디-고 배포 가이드

## AWS 배포 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                     사용자/관리자                          │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │   CloudFront    │ (CDN)
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │   S3 Bucket     │ (Frontend 정적 파일)
         └─────────────────┘
                  │
         ┌────────▼────────┐
         │  API Gateway    │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌────────┐
│ EC2    │   │ EC2    │   │ EC2    │
│Backend │   │  OCR   │   │  ML    │
└───┬────┘   └────────┘   └────────┘
    │
    ▼
┌────────┐        ┌────────┐
│  RDS   │◄───────┤   S3   │
│Postgres│        │(Images)│
└────────┘        └────────┘
```

## 배포 단계

### 1. AWS 리소스 생성

#### RDS (PostgreSQL)
```bash
# AWS CLI로 RDS 인스턴스 생성
aws rds create-db-instance \
    --db-instance-identifier medigo-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username postgres \
    --master-user-password <YOUR_PASSWORD> \
    --allocated-storage 20
```

#### S3 버킷
```bash
# 처방전/약봉투 이미지 저장용
aws s3 mb s3://medigo-prescriptions --region ap-northeast-2

# 버킷 암호화 설정
aws s3api put-bucket-encryption \
    --bucket medigo-prescriptions \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'
```

#### EC2 인스턴스
```bash
# Backend 서버용 (t3.small)
# OCR 서비스용 (t3.medium - CPU 집약적)
# ML 학습용 (g4dn.xlarge - GPU 필요 시)
```

### 2. Backend 배포

```bash
# EC2 인스턴스에 SSH 접속
ssh -i your-key.pem ec2-user@your-ec2-ip

# 프로젝트 클론
git clone https://github.com/your-repo/medigo.git
cd medigo/backend

# Python 환경 설정
sudo apt update
sudo apt install python3.11 python3.11-venv
python3.11 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
nano .env  # 프로덕션 값으로 수정

# 데이터베이스 마이그레이션
alembic upgrade head

# Gunicorn으로 실행
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

#### Systemd 서비스 설정
```ini
# /etc/systemd/system/medigo-backend.service
[Unit]
Description=Medigo Backend API
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/medigo/backend
Environment="PATH=/home/ec2-user/medigo/backend/venv/bin"
ExecStart=/home/ec2-user/medigo/backend/venv/bin/gunicorn \
    app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

```bash
# 서비스 시작
sudo systemctl daemon-reload
sudo systemctl enable medigo-backend
sudo systemctl start medigo-backend
```

### 3. Frontend 배포 (S3 + CloudFront)

```bash
# 로컬에서 빌드
cd frontend
npm install
npm run build

# S3 버킷 생성 (정적 호스팅용)
aws s3 mb s3://medigo-frontend
aws s3 website s3://medigo-frontend \
    --index-document index.html \
    --error-document index.html

# 빌드 파일 업로드
aws s3 sync dist/ s3://medigo-frontend --delete

# CloudFront 배포 생성 (선택사항)
# - S3를 Origin으로 설정
# - HTTPS 인증서 설정 (ACM)
# - 커스텀 도메인 연결
```

### 4. OCR 서비스 배포

```bash
# EC2 인스턴스 (CPU 최적화)
cd ml
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Systemd 서비스 설정
sudo systemctl enable medigo-ocr
sudo systemctl start medigo-ocr
```

### 5. Nginx 설정 (리버스 프록시)

```nginx
# /etc/nginx/sites-available/medigo
server {
    listen 80;
    server_name api.medigo.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name ocr.medigo.com;

    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/medigo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL 인증서 (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.medigo.com -d ocr.medigo.com
```

## 모니터링 및 로깅

### CloudWatch 설정
- EC2 메트릭 모니터링
- RDS 성능 모니터링
- S3 액세스 로그

### 애플리케이션 로깅
```python
# backend/app/core/logging.py
import logging
import watchtower

logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to EC2
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ec2-user
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd medigo/backend
            git pull
            source venv/bin/activate
            pip install -r requirements.txt
            alembic upgrade head
            sudo systemctl restart medigo-backend
```

## 백업 전략

### 데이터베이스
- RDS 자동 백업 (일일)
- 수동 스냅샷 (배포 전)

### 이미지 파일
- S3 버전 관리 활성화
- 크로스 리전 복제

## 보안 체크리스트

- [ ] 모든 API 엔드포인트 HTTPS 강제
- [ ] S3 버킷 공개 액세스 차단
- [ ] RDS 보안 그룹 설정 (EC2만 접근)
- [ ] IAM 최소 권한 원칙 적용
- [ ] 시크릿 관리 (AWS Secrets Manager)
- [ ] WAF 설정 (DDoS 방어)
- [ ] 정기적인 보안 패치

## 스케일링 전략

### 수평 확장
- EC2 Auto Scaling Group
- Application Load Balancer

### 수직 확장
- 트래픽 증가 시 인스턴스 타입 업그레이드

### 데이터베이스
- Read Replica 추가
- Connection Pooling 최적화

## 비용 최적화

- Reserved Instances 활용
- S3 Lifecycle Policy (오래된 이미지 Glacier로 이동)
- CloudWatch 알람 설정 (비용 초과 시 알림)

