"""
복약 지도 모델
"""
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class MedicationGuidance(Base):
    """복약 지도 테이블"""

    __tablename__ = "medication_guidance"

    id = Column(Integer, primary_key=True, index=True)
    
    # 주문 정보
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    
    # 복약 지도 내용
    guidance_text = Column(Text, nullable=False)
    
    # AI 생성 여부
    is_ai_generated = Column(Boolean, default=False)
    ai_model_version = Column(String(50), nullable=True)
    
    # 발송 정보
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    
    # 사용자 확인 여부
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    order = relationship("Order", back_populates="medication_guidance")
