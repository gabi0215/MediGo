"""
주문 API 엔드포인트
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.order import Order, OrderCreate, OrderStatus as OrderStatusSchema
from app.services.order_service import order_service

router = APIRouter()


@router.post("", response_model=Order, status_code=201, summary="주문 생성")
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    새로운 약 배달 주문을 생성합니다

    - 처방전 이미지를 Base64로 인코딩하여 전송합니다
    - 배달 주소와 연락처는 필수입니다
    - 결제 방법은 기본적으로 '만나서 결제'입니다
    """
    try:
        order = order_service.create_order(db, order_data, current_user.id)
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[Order], summary="내 주문 목록 조회")
async def get_my_orders(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    현재 로그인한 사용자의 주문 목록을 조회합니다

    - 최신 주문부터 정렬됩니다
    - 페이징을 지원합니다 (skip, limit)
    """
    orders = order_service.get_user_orders(db, current_user.id, skip, limit)
    return orders


@router.get("/{order_id}", response_model=Order, summary="주문 상세 조회")
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    특정 주문의 상세 정보를 조회합니다

    - 본인의 주문만 조회할 수 있습니다
    - 처방전 이미지, 약봉투 이미지, 복약 지도 등을 확인할 수 있습니다
    """
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")

    # 본인의 주문인지 확인
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="접근 권한이 없습니다")

    return order


@router.get("/{order_id}/status", response_model=OrderStatusSchema, summary="주문 상태 조회")
async def get_order_status(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    주문의 현재 상태를 조회합니다

    - submitted: 접수 완료
    - processing: 약국 조제 중
    - delivering: 배달 중
    - completed: 배달 완료
    - cancelled: 취소
    """
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")

    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="접근 권한이 없습니다")

    status_messages = {
        "submitted": "주문이 접수되었습니다. 곧 처리 예정입니다.",
        "processing": "약국에서 조제 중입니다.",
        "delivering": "배달 중입니다. 곧 도착합니다!",
        "completed": "배달이 완료되었습니다.",
        "cancelled": "주문이 취소되었습니다.",
    }

    return {
        "order_id": order.id,
        "status": order.status,
        "status_message": status_messages.get(order.status.value, ""),
        "updated_at": order.updated_at,
    }

