"""
인증 스키마
"""
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """토큰 응답"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """토큰 데이터"""

    user_id: Optional[int] = None
    email: Optional[str] = None


class KakaoLoginRequest(BaseModel):
    """카카오 로그인 요청"""

    access_token: str


class KakaoUserInfo(BaseModel):
    """카카오 사용자 정보"""

    id: int
    kakao_account: dict
    properties: Optional[dict] = None

