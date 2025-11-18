"""
관리자 API 엔드포인트
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin_user
from app.models.user import User
from app.models.order import OrderStatus as OrderStatusEnum
from app.models.medication_guidance import MedicationGuidance
from app.schemas.order import Order, OrderUpdate
from app.schemas.medication_guidance import (
    MedicationGuidance as MedicationGuidanceSchema,
    MedicationGuidanceCreate,
)
from app.services.order_service import order_service
from app.services.kakao_channel_service import kakao_channel_service

router = APIRouter()


@router.get("/orders", response_model=List[Order], summary="전체 주문 목록 조회")
async def get_all_orders(
    status: Optional[OrderStatusEnum] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    모든 주문 목록을 조회합니다 (관리자 전용)

    - status로 필터링할 수 있습니다
    - 최신 주문부터 정렬됩니다
    """
    orders = order_service.get_all_orders(db, status, skip, limit)
    return orders


@router.put("/orders/{order_id}", response_model=Order, summary="주문 정보 수정")
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    주문 정보를 수정합니다 (관리자 전용)

    - 주문 상태 변경
    - 약값, 배달비 입력
    - 결제 완료 처리
    - 약국명, 메모 추가
    """
    order = order_service.update_order(db, order_id, order_update)
    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")

    return order


@router.post(
    "/orders/{order_id}/medicine-bag",
    summary="약봉투 사진 업로드",
)
async def upload_medicine_bag(
    order_id: int,
    base64_image: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    약봉투 사진을 업로드합니다 (관리자 전용, 데이터 수집용)

    - Base64로 인코딩된 이미지를 전송합니다
    - AI 학습 데이터로 활용됩니다
    """
    try:
        prescription = order_service.upload_medicine_bag_image(
            db, order_id, base64_image
        )
        if not prescription:
            raise HTTPException(status_code=404, detail="처방전 정보를 찾을 수 없습니다")

        return {
            "message": "약봉투 사진이 업로드되었습니다",
            "medicine_bag_url": prescription.medicine_bag_image_url,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/medication-guidance",
    response_model=MedicationGuidanceSchema,
    status_code=201,
    summary="복약 지도 작성 및 발송",
)
async def create_medication_guidance(
    guidance_data: MedicationGuidanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    복약 지도 메시지를 작성하고 발송합니다 (관리자 전용)

    - 주문 ID에 해당하는 복약 지도를 생성합니다
    - 수동 작성 또는 AI 생성 여부를 표시합니다
    - 자동으로 사용자에게 푸시 알림이 발송됩니다
    """
    from datetime import datetime

    # 이미 복약 지도가 있는지 확인
    existing = (
        db.query(MedicationGuidance)
        .filter(MedicationGuidance.order_id == guidance_data.order_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400, detail="이미 복약 지도가 존재합니다"
        )

    # 복약 지도 생성
    guidance = MedicationGuidance(
        order_id=guidance_data.order_id,
        guidance_text=guidance_data.guidance_text,
        is_ai_generated=guidance_data.is_ai_generated,
        ai_model_version=guidance_data.ai_model_version,
        is_sent=True,
        sent_at=datetime.utcnow(),
    )
    db.add(guidance)
    db.commit()
    db.refresh(guidance)

    # 카카오톡 채널로 복약 지도 메시지 발송
    try:
        order = order_service.get_order(db, guidance_data.order_id)
        if order:
            await kakao_channel_service.send_medication_guidance_message(
                user_id=str(order.user_id),
                order_id=order.id,
                guidance_text=guidance_data.guidance_text,
            )
    except Exception as e:
        print(f"카카오톡 채널 메시지 발송 오류: {str(e)}")

    return guidance


@router.get(
    "/orders/{order_id}/medication-guidance",
    response_model=MedicationGuidanceSchema,
    summary="복약 지도 조회",
)
async def get_medication_guidance(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """특정 주문의 복약 지도를 조회합니다"""
    guidance = (
        db.query(MedicationGuidance)
        .filter(MedicationGuidance.order_id == order_id)
        .first()
    )
    if not guidance:
        raise HTTPException(
            status_code=404, detail="복약 지도를 찾을 수 없습니다"
        )

    return guidance

