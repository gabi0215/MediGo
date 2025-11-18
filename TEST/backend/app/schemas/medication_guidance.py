"""
복약 지도 스키마
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MedicationGuidanceBase(BaseModel):
    """복약 지도 기본 스키마"""

    guidance_text: str


class MedicationGuidanceCreate(MedicationGuidanceBase):
    """복약 지도 생성 스키마"""

    order_id: int
    is_ai_generated: bool = False
    ai_model_version: Optional[str] = None


class MedicationGuidanceUpdate(BaseModel):
    """복약 지도 수정 스키마"""

    guidance_text: Optional[str] = None
    is_sent: Optional[bool] = None


class MedicationGuidance(MedicationGuidanceBase):
    """복약 지도 응답 스키마"""

    id: int
    order_id: int
    is_ai_generated: bool
    ai_model_version: Optional[str] = None
    is_sent: bool
    sent_at: Optional[datetime] = None
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

