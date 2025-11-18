"""
AI 학습 데이터 모델
"""
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class TrainingData(Base):
    """AI 학습 데이터 테이블"""

    __tablename__ = "training_data"

    id = Column(Integer, primary_key=True, index=True)
    
    # 이미지 정보
    medicine_bag_image_url = Column(Text, nullable=False)
    medicine_bag_image_key = Column(String(500), nullable=False)
    
    # OCR 텍스트 (입력)
    ocr_raw_text = Column(Text, nullable=False)
    
    # 복약 지도 텍스트 (정답 레이블)
    guidance_text = Column(Text, nullable=False)
    
    # 데이터 품질
    is_verified = Column(Boolean, default=False)  # 검증 완료
    quality_score = Column(Integer, nullable=True)  # 품질 점수 (1-5)
    
    # 메타데이터
    order_id = Column(Integer, nullable=True)  # 연관 주문 ID (선택)
    notes = Column(Text, nullable=True)  # 메모
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

