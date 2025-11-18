# 메디-고 Backend만 빠른 설치 (Python 3.13)
# ML/OCR 제외, API 서버만 설치

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  메디-고 Backend 빠른 설치 (Python 3.13)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Python 버전 확인
Write-Host "Python 버전 확인 중..." -ForegroundColor Yellow
$pythonVersion = python --version
Write-Host $pythonVersion -ForegroundColor Green

if ($pythonVersion -notmatch "3\.13") {
    Write-Host "⚠ Python 3.13이 아닙니다. 계속하시겠습니까? (Y/N)" -ForegroundColor Yellow
    $continue = Read-Host
    if ($continue -ne "Y" -and $continue -ne "y") {
        exit
    }
}

# 가상환경 생성
Write-Host ""
Write-Host "가상환경 생성 중..." -ForegroundColor Yellow
python -m venv venv

# 가상환경 활성화
Write-Host "가상환경 활성화 중..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# pip 업그레이드
Write-Host ""
Write-Host "pip 업그레이드 중..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Backend 필수 패키지만 설치
Write-Host ""
Write-Host "Backend 필수 패키지 설치 중..." -ForegroundColor Yellow
Write-Host "(약 1-2분 소요)" -ForegroundColor Gray

pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings python-jose passlib PyJWT httpx boto3 alembic python-multipart email-validator Pillow

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ 설치 완료!" -ForegroundColor Green
    
    # .env 파일 생성
    if (!(Test-Path "backend\.env")) {
        Copy-Item "backend\env.example" "backend\.env"
        Write-Host "✅ .env 파일 생성 완료" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "  다음 단계:" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. backend\.env 파일 설정" -ForegroundColor White
    Write-Host "2. 서버 실행:" -ForegroundColor White
    Write-Host "   cd backend" -ForegroundColor Gray
    Write-Host "   python -m uvicorn app.main:app --reload" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. 브라우저에서 확인:" -ForegroundColor White
    Write-Host "   http://localhost:8000/docs" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ 설치 중 오류 발생" -ForegroundColor Red
    Write-Host "   위 오류 메시지를 확인하세요" -ForegroundColor Yellow
}

