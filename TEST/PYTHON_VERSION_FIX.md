# Python 버전 문제 해결

## 🔴 문제

Python 3.13은 너무 최신 버전이라 많은 패키지들이 아직 wheel을 제공하지 않습니다:
- `psycopg2-binary` ✅ (2.9.10으로 해결됨)
- `Pillow` ❌ 
- `torch`, `easyocr` 등도 문제 가능성 높음

## ✅ 해결 방법

### 방법 1: Python 3.11 사용 (권장 ⭐)

1. **Python 3.11 다운로드**
   - https://www.python.org/downloads/
   - Python 3.11.x 최신 버전 선택

2. **새로운 가상환경 생성**
   ```bash
   # 기존 venv 삭제
   rmdir /s venv
   
   # Python 3.11로 새 가상환경
   py -3.11 -m venv venv
   
   # 활성화
   venv\Scripts\activate
   
   # 패키지 설치
   pip install -r requirements.txt
   ```

### 방법 2: 패키지 버전 업데이트 (임시 해결)

최신 버전으로 업데이트하여 Python 3.13 지원 확인:

```bash
# Pillow 최신 버전
pip install Pillow --upgrade

# 또는 개별 설치
pip install Pillow==11.0.0
pip install torch==2.2.0
pip install easyocr==1.7.2
```

### 방법 3: Backend만 먼저 설치

ML/OCR 없이 Backend만 우선 설치:

```bash
cd backend
pip install -r requirements.txt
```

## 🎯 권장 환경

| 구성 요소 | 권장 버전 | 이유 |
|----------|----------|------|
| Python | **3.11.x** | 안정성, 패키지 호환성 최고 |
| Python | 3.12.x | 대부분 호환, 일부 문제 가능 |
| Python | 3.13.x | 최신이라 호환성 문제 많음 ❌ |

## 📝 현재 시스템

```bash
python --version
# Python 3.13.x ← 이게 문제!
```

## 🚀 빠른 해결 (Backend만 실행)

ML 기능 없이 Backend API만 실행하려면:

```bash
# 1. Backend 필수 패키지만 설치
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic python-jose passlib httpx boto3

# 2. 서버 실행
cd backend
python -m uvicorn app.main:app --reload
```

이렇게 하면 ML/OCR 제외하고 나머지 기능 모두 사용 가능합니다!

