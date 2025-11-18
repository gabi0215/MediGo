"""
사용자 스키마
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """사용자 기본 스키마"""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_address_detail: Optional[str] = None
    delivery_zipcode: Optional[str] = None


class UserCreate(UserBase):
    """사용자 생성 스키마"""

    kakao_id: Optional[str] = None
    kakao_profile_image: Optional[str] = None


class UserUpdate(UserBase):
    """사용자 수정 스키마"""

    pass


class User(UserBase):
    """사용자 응답 스키마"""

    id: int
    kakao_id: Optional[str] = None
    kakao_profile_image: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """사용자 프로필 스키마"""

    id: int
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    kakao_profile_image: Optional[str] = None
    delivery_address: Optional[str] = None
    delivery_address_detail: Optional[str] = None
    delivery_zipcode: Optional[str] = None

    class Config:
        from_attributes = True

