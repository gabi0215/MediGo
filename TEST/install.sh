#!/bin/bash
# 메디-고 자동 설치 스크립트 (Mac/Linux)

echo "============================================"
echo "  메디-고 (Medi-Go) 설치 스크립트"
echo "============================================"
echo ""

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Python 버전 확인
echo -e "${YELLOW}Python 버전 확인 중...${NC}"
python3 --version

# 가상환경 생성
echo ""
echo -e "${YELLOW}가상환경 생성 중...${NC}"
python3 -m venv venv

# 가상환경 활성화
echo -e "${YELLOW}가상환경 활성화 중...${NC}"
source venv/bin/activate

# pip 업그레이드
echo ""
echo -e "${YELLOW}pip 업그레이드 중...${NC}"
python -m pip install --upgrade pip

# Python 패키지 설치
echo ""
echo -e "${YELLOW}Python 패키지 설치 중...${NC}"
echo -e "${GRAY}(시간이 좀 걸릴 수 있습니다...)${NC}"
pip install -r requirements.txt

# Backend 환경 설정
echo ""
echo -e "${YELLOW}Backend 환경 설정 중...${NC}"
if [ ! -f "backend/.env" ]; then
    cp backend/env.example backend/.env
    echo -e "${GREEN}✓ .env 파일 생성 완료${NC}"
    echo -e "${GRAY}  → backend/.env 파일을 편집하여 설정을 완료하세요${NC}"
else
    echo -e "${GREEN}✓ .env 파일이 이미 존재합니다${NC}"
fi

# Node.js 확인
echo ""
echo -e "${YELLOW}Node.js 확인 중...${NC}"
if command -v node &> /dev/null; then
    node --version
    NODE_INSTALLED=true
else
    echo -e "${RED}⚠ Node.js가 설치되어 있지 않습니다${NC}"
    echo -e "${GRAY}  Frontend 설치를 건너뜁니다${NC}"
    NODE_INSTALLED=false
fi

# Frontend 설치
if [ "$NODE_INSTALLED" = true ]; then
    echo ""
    echo -e "${YELLOW}Frontend 패키지 설치 중...${NC}"
    cd frontend
    npm install
    cd ..
    echo -e "${GREEN}✓ Frontend 설치 완료${NC}"

    # Admin 설치
    echo ""
    echo -e "${YELLOW}Admin 패키지 설치 중...${NC}"
    cd admin
    npm install
    cd ..
    echo -e "${GREEN}✓ Admin 설치 완료${NC}"
fi

# 완료 메시지
echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${GREEN}  설치 완료!${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""
echo -e "${YELLOW}다음 단계:${NC}"
echo -e "${NC}1. backend/.env 파일 설정${NC}"
echo -e "${NC}2. PostgreSQL 데이터베이스 생성${NC}"
echo -e "${NC}3. 서버 실행:${NC}"
echo -e "${GRAY}   cd backend${NC}"
echo -e "${GRAY}   source ../venv/bin/activate${NC}"
echo -e "${GRAY}   python -m uvicorn app.main:app --reload${NC}"
echo ""
echo -e "${CYAN}자세한 내용은 QUICKSTART.md를 참고하세요!${NC}"
echo ""

