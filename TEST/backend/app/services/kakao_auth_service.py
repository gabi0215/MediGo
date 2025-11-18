"""
카카오 OAuth 서비스
"""
import httpx
from typing import Optional, Dict

from app.core.config import settings


class KakaoAuthService:
    """카카오 OAuth 인증 서비스"""

    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    async def get_user_info(self, access_token: str) -> Optional[Dict]:
        """
        카카오 액세스 토큰으로 사용자 정보 가져오기

        Args:
            access_token: 카카오 액세스 토큰

        Returns:
            사용자 정보 딕셔너리 또는 None
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.KAKAO_USER_INFO_URL, headers=headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"카카오 API 오류: {str(e)}")
                return None

    def extract_user_data(self, kakao_user_info: Dict) -> Dict:
        """
        카카오 사용자 정보에서 필요한 데이터 추출

        Args:
            kakao_user_info: 카카오 API 응답

        Returns:
            추출된 사용자 데이터
        """
        kakao_id = str(kakao_user_info.get("id"))
        kakao_account = kakao_user_info.get("kakao_account", {})
        properties = kakao_user_info.get("properties", {})

        return {
            "kakao_id": kakao_id,
            "email": kakao_account.get("email"),
            "full_name": properties.get("nickname"),
            "kakao_profile_image": properties.get("profile_image"),
        }


# 싱글톤 인스턴스
kakao_auth_service = KakaoAuthService()

