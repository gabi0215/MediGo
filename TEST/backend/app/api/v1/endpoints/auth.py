"""
인증 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.auth import Token, KakaoLoginRequest
from app.services.kakao_auth_service import kakao_auth_service

router = APIRouter()


@router.post("/kakao", response_model=Token, summary="카카오 로그인")
async def kakao_login(
    login_data: KakaoLoginRequest,
    db: Session = Depends(get_db),
):
    """
    카카오 OAuth 로그인

    - 카카오 액세스 토큰을 받아 사용자 정보를 가져옵니다
    - 신규 사용자의 경우 자동으로 회원가입을 진행합니다
    - JWT 액세스 토큰과 리프레시 토큰을 반환합니다
    """
    # 카카오 사용자 정보 가져오기
    kakao_user_info = await kakao_auth_service.get_user_info(login_data.access_token)
    if not kakao_user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="카카오 인증에 실패했습니다",
        )

    # 사용자 데이터 추출
    user_data = kakao_auth_service.extract_user_data(kakao_user_info)
    kakao_id = user_data["kakao_id"]

    # 기존 사용자 조회
    user = db.query(User).filter(User.kakao_id == kakao_id).first()

    if not user:
        # 신규 사용자 생성
        user = User(
            kakao_id=kakao_id,
            email=user_data.get("email"),
            full_name=user_data.get("full_name"),
            kakao_profile_image=user_data.get("kakao_profile_image"),
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token, summary="토큰 갱신")
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    """
    리프레시 토큰으로 새로운 액세스 토큰 발급
    """
    from app.core.security import verify_token

    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 리프레시 토큰입니다",
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다",
        )

    # 새 토큰 생성
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }

