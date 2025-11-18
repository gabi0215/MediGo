"""
주문 모델
"""
from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class OrderStatus(str, enum.Enum):
    """주문 상태"""

    SUBMITTED = "submitted"  # 접수 완료
    PROCESSING = "processing"  # 약국 조제 중
    DELIVERING = "delivering"  # 배달 중
    COMPLETED = "completed"  # 배달 완료
    CANCELLED = "cancelled"  # 취소


class PaymentMethod(str, enum.Enum):
    """결제 방법"""

    PAY_AT_DOOR = "pay_at_door"  # 만나서 결제
    CARD = "card"  # 카드
    CASH = "cash"  # 현금


class Order(Base):
    """주문 테이블"""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    
    # 사용자 정보
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 주문 상태
    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.SUBMITTED,
        nullable=False,
        index=True,
    )
    
    # 배달 정보
    delivery_address = Column(Text, nullable=False)
    delivery_address_detail = Column(String(255), nullable=True)
    delivery_zipcode = Column(String(10), nullable=True)
    delivery_phone = Column(String(20), nullable=False)
    delivery_note = Column(Text, nullable=True)
    
    # 결제 정보
    payment_method = Column(
        Enum(PaymentMethod),
        default=PaymentMethod.PAY_AT_DOOR,
        nullable=False,
    )
    medicine_price = Column(Float, nullable=True)  # 약값
    delivery_fee = Column(Float, default=3000.0)  # 배달비
    total_price = Column(Float, nullable=True)  # 총 금액
    is_paid = Column(Boolean, default=False)
    
    # 운영팀 메모
    admin_note = Column(Text, nullable=True)
    pharmacy_name = Column(String(100), nullable=True)  # 제휴 약국명
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    processing_at = Column(DateTime, nullable=True)
    delivering_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # 관계
    user = relationship("User", back_populates="orders")
    prescription = relationship(
        "Prescription", back_populates="order", uselist=False, cascade="all, delete-orphan"
    )
    medication_guidance = relationship(
        "MedicationGuidance",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
    )

