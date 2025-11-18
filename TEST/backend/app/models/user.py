"""
사용자 모델
"""
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """사용자 테이블"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # 기본 정보
    email = Column(String(255), unique=True, index=True, nullable=True)
    full_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # 카카오 OAuth
    kakao_id = Column(String(100), unique=True, index=True, nullable=True)
    kakao_profile_image = Column(Text, nullable=True)
    
    # 배달 주소
    delivery_address = Column(Text, nullable=True)
    delivery_address_detail = Column(String(255), nullable=True)
    delivery_zipcode = Column(String(10), nullable=True)
    
    # 계정 상태
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    
    # 관계
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

