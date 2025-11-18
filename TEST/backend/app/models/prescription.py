"""
처방전 모델
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Prescription(Base):
    """처방전 테이블"""

    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    
    # 주문 정보
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    
    # 처방전 이미지
    prescription_image_url = Column(Text, nullable=False)  # S3 URL
    prescription_image_key = Column(String(500), nullable=False)  # S3 Key
    
    # 약봉투 이미지 (데이터 수집용)
    medicine_bag_image_url = Column(Text, nullable=True)
    medicine_bag_image_key = Column(String(500), nullable=True)
    
    # OCR 결과
    prescription_ocr_text = Column(Text, nullable=True)  # 처방전 OCR
    medicine_bag_ocr_text = Column(Text, nullable=True)  # 약봉투 OCR
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    order = relationship("Order", back_populates="prescription")
