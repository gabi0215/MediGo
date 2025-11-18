"""
관리자 계정 생성 스크립트
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.config import settings


def create_admin():
    """관리자 계정 생성"""
    db = SessionLocal()

    try:
        # 기존 관리자 확인
        existing_admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if existing_admin:
            print(f"⚠️  관리자 계정이 이미 존재합니다: {settings.ADMIN_EMAIL}")
            return

        # 관리자 생성
        admin = User(
            email=settings.ADMIN_EMAIL,
            full_name="관리자",
            is_active=True,
            is_admin=True,
        )
        db.add(admin)
        db.commit()

        print("✅ 관리자 계정이 생성되었습니다!")
        print(f"   이메일: {settings.ADMIN_EMAIL}")
        print(f"   초기 비밀번호: {settings.ADMIN_PASSWORD}")
        print("   ⚠️  보안을 위해 초기 비밀번호를 변경하세요!")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()

