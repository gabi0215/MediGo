# 메디-고 자동 설치 스크립트 (Windows PowerShell)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  메디-고 (Medi-Go) 설치 스크립트" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Python 버전 확인
Write-Host "Python 버전 확인 중..." -ForegroundColor Yellow
python --version

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

# Python 패키지 설치
Write-Host ""
Write-Host "Python 패키지 설치 중..." -ForegroundColor Yellow
Write-Host "(시간이 좀 걸릴 수 있습니다...)" -ForegroundColor Gray
pip install -r requirements.txt

# Backend 환경 설정
Write-Host ""
Write-Host "Backend 환경 설정 중..." -ForegroundColor Yellow
if (!(Test-Path "backend\.env")) {
    Copy-Item "backend\env.example" "backend\.env"
    Write-Host "✓ .env 파일 생성 완료" -ForegroundColor Green
    Write-Host "  → backend\.env 파일을 편집하여 설정을 완료하세요" -ForegroundColor Gray
} else {
    Write-Host "✓ .env 파일이 이미 존재합니다" -ForegroundColor Green
}

# Node.js 확인
Write-Host ""
Write-Host "Node.js 확인 중..." -ForegroundColor Yellow
try {
    node --version
    $nodeInstalled = $true
} catch {
    Write-Host "⚠ Node.js가 설치되어 있지 않습니다" -ForegroundColor Red
    Write-Host "  Frontend 설치를 건너뜁니다" -ForegroundColor Gray
    $nodeInstalled = $false
}

# Frontend 설치
if ($nodeInstalled) {
    Write-Host ""
    Write-Host "Frontend 패키지 설치 중..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
    Write-Host "✓ Frontend 설치 완료" -ForegroundColor Green

    # Admin 설치
    Write-Host ""
    Write-Host "Admin 패키지 설치 중..." -ForegroundColor Yellow
    Set-Location admin
    npm install
    Set-Location ..
    Write-Host "✓ Admin 설치 완료" -ForegroundColor Green
}

# 완료 메시지
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  설치 완료!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "다음 단계:" -ForegroundColor Yellow
Write-Host "1. backend\.env 파일 설정" -ForegroundColor White
Write-Host "2. PostgreSQL 데이터베이스 생성" -ForegroundColor White
Write-Host "3. 서버 실행:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   python -m uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "자세한 내용은 QUICKSTART.md를 참고하세요!" -ForegroundColor Cyan
Write-Host ""

