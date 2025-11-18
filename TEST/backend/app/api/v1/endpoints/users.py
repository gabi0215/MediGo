"""
사용자 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate, UserProfile

router = APIRouter()


@router.get("/me", response_model=UserProfile, summary="내 프로필 조회")
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
):
    """현재 로그인한 사용자의 프로필 정보를 조회합니다"""
    return current_user


@router.put("/me", response_model=UserProfile, summary="내 프로필 수정")
async def update_my_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    현재 로그인한 사용자의 프로필 정보를 수정합니다

    - 이름, 전화번호, 배달 주소 등을 수정할 수 있습니다
    """
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=UserSchema, summary="사용자 조회")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    특정 사용자의 정보를 조회합니다 (본인 또는 관리자만 가능)
    """
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="접근 권한이 없습니다")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    return user

