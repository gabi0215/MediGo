"""
API v1 라우터
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, orders, users, admin, kakao_channel

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["인증"])
api_router.include_router(users.router, prefix="/users", tags=["사용자"])
api_router.include_router(orders.router, prefix="/orders", tags=["주문"])
api_router.include_router(admin.router, prefix="/admin", tags=["관리자"])
api_router.include_router(kakao_channel.router, prefix="/kakao", tags=["카카오톡 채널"])

