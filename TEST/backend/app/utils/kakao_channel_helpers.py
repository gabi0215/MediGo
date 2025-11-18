"""
카카오톡 채널 헬퍼 함수
"""
from typing import Dict


def format_medication_guidance_message(
    user_name: str, guidance_text: str, order_id: int
) -> str:
    """
    복약 지도 메시지 포맷팅
    
    Args:
        user_name: 사용자 이름
        guidance_text: 복약 지도 내용
        order_id: 주문 ID
        
    Returns:
        포맷팅된 메시지
    """
    message = f"""안녕하세요 {user_name}님,
처방받으신 약이 배달 완료되었습니다. 💊

[복약 지도]
{guidance_text}

궁금하신 사항이 있으시면 언제든 문의해주세요.
건강하세요!

- 메디-고 팀
(주문번호: {order_id})
"""
    return message


def format_order_status_message(
    user_name: str, order_id: int, status: str, status_message: str
) -> str:
    """
    주문 상태 알림 메시지 포맷팅
    
    Args:
        user_name: 사용자 이름
        order_id: 주문 ID
        status: 주문 상태
        status_message: 상태 메시지
        
    Returns:
        포맷팅된 메시지
    """
    status_emoji = {
        "submitted": "✅",
        "processing": "⚗️",
        "delivering": "🚚",
        "completed": "🎉",
    }

    emoji = status_emoji.get(status, "📦")

    message = f"""{emoji} {user_name}님의 주문 상태가 업데이트되었습니다.

주문번호: {order_id}
상태: {status_message}

메디-고를 이용해주셔서 감사합니다!
"""
    return message


def create_customer_schema() -> Dict:
    """
    메디-고 고객 스키마 생성
    
    Returns:
        고객 스키마 딕셔너리
    """
    schema = {
        "주문번호": "Number",
        "주문일시": "String",
        "배달주소": "String",
        "연락처": "String",
        "주문상태": "String",
        "약값": "Number",
    }
    return schema


def validate_phone_number(phone: str) -> bool:
    """
    전화번호 유효성 검사
    
    Args:
        phone: 전화번호
        
    Returns:
        유효 여부
    """
    import re

    # 010-1234-5678 또는 01012345678 형식
    pattern = r"^01[0-9]-?\d{3,4}-?\d{4}$"
    return bool(re.match(pattern, phone))

