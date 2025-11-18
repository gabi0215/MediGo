"""
주문 스키마
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.models.order import OrderStatus as OrderStatusEnum
from app.models.order import PaymentMethod


class OrderBase(BaseModel):
    """주문 기본 스키마"""

    delivery_address: str
    delivery_address_detail: Optional[str] = None
    delivery_zipcode: Optional[str] = None
    delivery_phone: str
    delivery_note: Optional[str] = None
    payment_method: PaymentMethod = PaymentMethod.PAY_AT_DOOR


class OrderCreate(OrderBase):
    """주문 생성 스키마"""

    prescription_image_base64: str  # Base64 인코딩된 처방전 이미지


class OrderUpdate(BaseModel):
    """주문 수정 스키마 (관리자용)"""

    status: Optional[OrderStatusEnum] = None
    medicine_price: Optional[float] = None
    delivery_fee: Optional[float] = None
    is_paid: Optional[bool] = None
    admin_note: Optional[str] = None
    pharmacy_name: Optional[str] = None


class PrescriptionInfo(BaseModel):
    """처방전 정보"""

    prescription_image_url: str
    medicine_bag_image_url: Optional[str] = None
    prescription_ocr_text: Optional[str] = None
    medicine_bag_ocr_text: Optional[str] = None

    class Config:
        from_attributes = True


class Order(OrderBase):
    """주문 응답 스키마"""

    id: int
    user_id: int
    status: OrderStatusEnum
    medicine_price: Optional[float] = None
    delivery_fee: float
    total_price: Optional[float] = None
    is_paid: bool
    admin_note: Optional[str] = None
    pharmacy_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime
    processing_at: Optional[datetime] = None
    delivering_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # 처방전 정보 (옵션)
    prescription: Optional[PrescriptionInfo] = None

    class Config:
        from_attributes = True


class OrderStatus(BaseModel):
    """주문 상태 응답"""

    order_id: int
    status: OrderStatusEnum
    status_message: str
    updated_at: datetime

    class Config:
        from_attributes = True

