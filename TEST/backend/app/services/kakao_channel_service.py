"""
카카오톡 채널 서비스
참고: https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api
"""
import httpx
from typing import Optional, Dict, List
from datetime import datetime

from app.core.config import settings


class KakaoChannelService:
    """
    카카오톡 채널 관리 서비스
    
    주요 기능:
    - 카카오톡 채널 관계 조회
    - 고객파일 관리 (등록, 조회, 사용자 추가/삭제)
    - 메시지 발송 (복약 지도 등)
    """

    def __init__(self):
        self.api_url = settings.KAKAO_CHANNEL_API_URL
        self.rest_api_key = settings.KAKAO_REST_API_KEY
        self.admin_key = settings.KAKAO_ADMIN_KEY
        self.channel_public_id = settings.KAKAO_CHANNEL_PUBLIC_ID

    def _get_headers(self, use_admin_key: bool = False) -> Dict[str, str]:
        """
        API 요청 헤더 생성
        
        Args:
            use_admin_key: 어드민 키 사용 여부
            
        Returns:
            헤더 딕셔너리
        """
        if use_admin_key:
            return {
                "Authorization": f"KakaoAK {self.admin_key}",
                "Content-Type": "application/json",
            }
        return {
            "Authorization": f"KakaoAK {self.rest_api_key}",
            "Content-Type": "application/json",
        }

    async def check_channel_relation(self, user_id: int) -> Optional[Dict]:
        """
        사용자의 카카오톡 채널 관계 조회
        
        URL: GET https://kapi.kakao.com/v2/api/talk/channels
        참고: https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#check-channel-relation
        
        Args:
            user_id: 사용자 ID (앱 회원번호)
            
        Returns:
            채널 관계 정보 또는 None
        """
        url = f"{self.api_url}/v2/api/talk/channels"
        headers = self._get_headers()

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    headers=headers,
                    params={"channel_public_ids": self.channel_public_id},
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"카카오톡 채널 관계 조회 오류: {str(e)}")
                return None

    async def create_customer_file(
        self, 
        name: str, 
        description: str = "",
        schema: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        고객파일 등록
        
        URL: POST https://kapi.kakao.com/v1/talkchannel/register/target_user_file
        참고: https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#register-customer-file
        
        Args:
            name: 고객파일 이름
            description: 고객파일 설명
            schema: 스키마 정의 (선택사항)
            
        Returns:
            생성된 고객파일 정보
        """
        url = f"{self.api_url}/v1/talkchannel/register/target_user_file"
        headers = self._get_headers()

        data = {
            "channel_public_id": self.channel_public_id,
            "name": name,
            "description": description,
        }

        if schema:
            data["schema"] = schema

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"고객파일 등록 오류: {str(e)}")
                return None

    async def get_customer_file(self, file_id: int) -> Optional[Dict]:
        """
        고객파일 조회
        
        URL: GET https://kapi.kakao.com/v1/talkchannel/target_user_file
        참고: https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#get-customer-file
        
        Args:
            file_id: 고객파일 ID
            
        Returns:
            고객파일 정보
        """
        url = f"{self.api_url}/v1/talkchannel/target_user_file"
        headers = self._get_headers()

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    headers=headers,
                    params={
                        "file_id": file_id,
                        "channel_public_id": self.channel_public_id,
                    },
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"고객파일 조회 오류: {str(e)}")
                return None

    async def add_users_to_customer_file(
        self, 
        file_id: int, 
        users: List[Dict],
        user_type: str = "app"
    ) -> Optional[Dict]:
        """
        고객파일에 사용자 추가
        
        URL: POST https://kapi.kakao.com/v1/talkchannel/update/target_users
        참고: https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#add-users-to-customer-file
        
        Args:
            file_id: 고객파일 ID
            users: 추가할 사용자 목록
                   [{"id": "12345", "field": {"생년월일": "2000-01-01", ...}}, ...]
            user_type: 사용자 ID 유형 ("app" 또는 "phone")
            
        Returns:
            추가 결과 정보
        """
        url = f"{self.api_url}/v1/talkchannel/update/target_users"
        headers = self._get_headers()

        data = {
            "file_id": file_id,
            "channel_public_id": self.channel_public_id,
            "user_type": user_type,
            "users": users,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"고객파일에 사용자 추가 오류: {str(e)}")
                return None

    async def delete_users_from_customer_file(
        self, 
        file_id: int, 
        user_ids: List[str],
        user_type: str = "app"
    ) -> bool:
        """
        고객파일에서 사용자 삭제
        
        URL: POST https://kapi.kakao.com/v1/talkchannel/delete/target_users
        참고: https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#delete-users-from-customer-file
        
        Args:
            file_id: 고객파일 ID
            user_ids: 삭제할 사용자 ID 목록
            user_type: 사용자 ID 유형 ("app" 또는 "phone")
            
        Returns:
            성공 여부
        """
        url = f"{self.api_url}/v1/talkchannel/delete/target_users"
        headers = self._get_headers()

        data = {
            "file_id": file_id,
            "channel_public_id": self.channel_public_id,
            "user_type": user_type,
            "user_ids": user_ids,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=data)
                response.raise_for_status()
                return True
            except httpx.HTTPError as e:
                print(f"고객파일에서 사용자 삭제 오류: {str(e)}")
                return False

    async def send_medication_guidance_message(
        self, 
        user_id: str,
        order_id: int,
        guidance_text: str
    ) -> bool:
        """
        복약 지도 메시지 발송 (카카오톡 채널 메시지)
        
        Note: 실제 메시지 발송은 카카오톡 채널 관리자센터에서 설정한 
              메시지 템플릿을 사용해야 합니다.
              
        Args:
            user_id: 사용자 ID
            order_id: 주문 ID
            guidance_text: 복약 지도 내용
            
        Returns:
            발송 성공 여부
        """
        # TODO: 실제 메시지 발송 API 구현
        # 카카오톡 채널 메시지는 관리자센터에서 템플릿을 먼저 등록해야 합니다.
        # https://developers.kakao.com/docs/latest/ko/message/rest-api
        
        print(f"[카카오톡 채널] 복약 지도 메시지 발송")
        print(f"  - 사용자 ID: {user_id}")
        print(f"  - 주문 ID: {order_id}")
        print(f"  - 내용: {guidance_text[:50]}...")
        
        # 임시: 항상 성공으로 처리
        return True

    async def register_order_customer(
        self,
        user_id: int,
        order_id: int,
        order_data: Dict
    ) -> bool:
        """
        주문 고객을 카카오톡 채널 고객파일에 등록
        
        Args:
            user_id: 사용자 ID
            order_id: 주문 ID
            order_data: 주문 데이터 (주소, 연락처 등)
            
        Returns:
            등록 성공 여부
        """
        # 메디-고 고객파일 (file_id는 미리 생성된 파일 ID 사용)
        # 실제로는 DB에서 관리하거나 설정 파일에 저장
        MEDIGO_CUSTOMER_FILE_ID = 1  # 예시

        users = [
            {
                "id": str(user_id),
                "field": {
                    "주문번호": str(order_id),
                    "주문일시": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "배달주소": order_data.get("delivery_address", ""),
                    "연락처": order_data.get("delivery_phone", ""),
                },
            }
        ]

        result = await self.add_users_to_customer_file(
            file_id=MEDIGO_CUSTOMER_FILE_ID,
            users=users,
            user_type="app",
        )

        return result is not None


# 싱글톤 인스턴스
kakao_channel_service = KakaoChannelService()

