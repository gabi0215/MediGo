"""
데이터베이스 초기화 스크립트
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.database import Base, engine
from app.models import *  # noqa: F401, F403


def init_db():
    """데이터베이스 테이블 생성"""
    print("데이터베이스 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블이 생성되었습니다!")


def drop_db():
    """데이터베이스 테이블 삭제"""
    print("⚠️  데이터베이스 테이블 삭제 중...")
    Base.metadata.drop_all(bind=engine)
    print("✅ 데이터베이스 테이블이 삭제되었습니다!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        confirm = input("정말로 모든 테이블을 삭제하시겠습니까? (yes/no): ")
        if confirm.lower() == "yes":
            drop_db()
        else:
            print("취소되었습니다.")
    else:
        init_db()

