"""
카카오톡 채널 API 엔드포인트
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.deps import get_current_admin_user
from app.models.user import User
from app.services.kakao_channel_service import kakao_channel_service

router = APIRouter()


class CustomerFileCreate(BaseModel):
    """고객파일 생성 요청"""

    name: str
    description: Optional[str] = ""
    schema: Optional[dict] = None


class CustomerFileAddUsers(BaseModel):
    """고객파일에 사용자 추가 요청"""

    file_id: int
    users: List[dict]
    user_type: str = "app"


class CustomerFileDeleteUsers(BaseModel):
    """고객파일에서 사용자 삭제 요청"""

    file_id: int
    user_ids: List[str]
    user_type: str = "app"


@router.get("/channel/relation/{user_id}", summary="카카오톡 채널 관계 조회")
async def check_channel_relation(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
):
    """
    특정 사용자의 카카오톡 채널 관계 조회 (관리자 전용)
    
    - 사용자가 채널을 추가했는지 확인
    """
    result = await kakao_channel_service.check_channel_relation(user_id)
    if not result:
        raise HTTPException(
            status_code=400, detail="카카오톡 채널 관계 조회에 실패했습니다"
        )

    return result


@router.post("/customer-file", summary="고객파일 생성")
async def create_customer_file(
    file_data: CustomerFileCreate,
    current_user: User = Depends(get_current_admin_user),
):
    """
    카카오톡 채널 고객파일 생성 (관리자 전용)
    
    - 고객 관리를 위한 파일 생성
    - 스키마를 정의하여 고객 정보 구조화
    """
    result = await kakao_channel_service.create_customer_file(
        name=file_data.name,
        description=file_data.description,
        schema=file_data.schema,
    )

    if not result:
        raise HTTPException(status_code=400, detail="고객파일 생성에 실패했습니다")

    return result


@router.get("/customer-file/{file_id}", summary="고객파일 조회")
async def get_customer_file(
    file_id: int,
    current_user: User = Depends(get_current_admin_user),
):
    """
    카카오톡 채널 고객파일 조회 (관리자 전용)
    
    - 등록된 고객파일의 정보 확인
    """
    result = await kakao_channel_service.get_customer_file(file_id)
    if not result:
        raise HTTPException(status_code=404, detail="고객파일을 찾을 수 없습니다")

    return result


@router.post("/customer-file/add-users", summary="고객파일에 사용자 추가")
async def add_users_to_customer_file(
    data: CustomerFileAddUsers,
    current_user: User = Depends(get_current_admin_user),
):
    """
    고객파일에 사용자 추가 (관리자 전용)
    
    - 주문 고객을 고객파일에 등록
    - 스키마에 맞는 필드 정보 입력
    """
    result = await kakao_channel_service.add_users_to_customer_file(
        file_id=data.file_id,
        users=data.users,
        user_type=data.user_type,
    )

    if not result:
        raise HTTPException(
            status_code=400, detail="고객파일에 사용자 추가에 실패했습니다"
        )

    return result


@router.post("/customer-file/delete-users", summary="고객파일에서 사용자 삭제")
async def delete_users_from_customer_file(
    data: CustomerFileDeleteUsers,
    current_user: User = Depends(get_current_admin_user),
):
    """
    고객파일에서 사용자 삭제 (관리자 전용)
    
    - 특정 사용자를 고객파일에서 제거
    """
    success = await kakao_channel_service.delete_users_from_customer_file(
        file_id=data.file_id,
        user_ids=data.user_ids,
        user_type=data.user_type,
    )

    if not success:
        raise HTTPException(
            status_code=400, detail="고객파일에서 사용자 삭제에 실패했습니다"
        )

    return {"message": "사용자가 삭제되었습니다"}

