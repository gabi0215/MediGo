"""
주문 서비스
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.models.prescription import Prescription
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.s3_service import s3_service


class OrderService:
    """주문 관리 서비스"""

    def create_order(
        self, db: Session, order_data: OrderCreate, user_id: int
    ) -> Order:
        """
        새 주문 생성

        Args:
            db: 데이터베이스 세션
            order_data: 주문 데이터
            user_id: 사용자 ID

        Returns:
            생성된 주문
        """
        # S3에 처방전 이미지 업로드
        prescription_url, prescription_key = s3_service.upload_base64_image(
            order_data.prescription_image_base64, folder="prescriptions"
        )

        # 주문 생성
        order = Order(
            user_id=user_id,
            status=OrderStatus.SUBMITTED,
            delivery_address=order_data.delivery_address,
            delivery_address_detail=order_data.delivery_address_detail,
            delivery_zipcode=order_data.delivery_zipcode,
            delivery_phone=order_data.delivery_phone,
            delivery_note=order_data.delivery_note,
            payment_method=order_data.payment_method,
            submitted_at=datetime.utcnow(),
        )
        db.add(order)
        db.flush()

        # 처방전 정보 생성
        prescription = Prescription(
            order_id=order.id,
            prescription_image_url=prescription_url,
            prescription_image_key=prescription_key,
        )
        db.add(prescription)
        db.commit()
        db.refresh(order)

        return order

    def get_order(self, db: Session, order_id: int) -> Optional[Order]:
        """주문 조회"""
        return db.query(Order).filter(Order.id == order_id).first()

    def get_user_orders(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 20
    ) -> List[Order]:
        """사용자의 주문 목록 조회"""
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_orders(
        self,
        db: Session,
        status: Optional[OrderStatus] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Order]:
        """모든 주문 목록 조회 (관리자용)"""
        query = db.query(Order)
        if status:
            query = query.filter(Order.status == status)
        return query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    def update_order(
        self, db: Session, order_id: int, order_update: OrderUpdate
    ) -> Optional[Order]:
        """
        주문 정보 수정 (관리자용)

        Args:
            db: 데이터베이스 세션
            order_id: 주문 ID
            order_update: 수정할 데이터

        Returns:
            수정된 주문
        """
        order = self.get_order(db, order_id)
        if not order:
            return None

        # 상태 변경 시 타임스탬프 업데이트
        if order_update.status and order_update.status != order.status:
            if order_update.status == OrderStatus.PROCESSING:
                order.processing_at = datetime.utcnow()
            elif order_update.status == OrderStatus.DELIVERING:
                order.delivering_at = datetime.utcnow()
            elif order_update.status == OrderStatus.COMPLETED:
                order.completed_at = datetime.utcnow()

        # 필드 업데이트
        update_data = order_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(order, field, value)

        # 총 금액 계산
        if order.medicine_price is not None:
            order.total_price = order.medicine_price + (order.delivery_fee or 0)

        db.commit()
        db.refresh(order)
        return order

    def upload_medicine_bag_image(
        self, db: Session, order_id: int, base64_image: str
    ) -> Optional[Prescription]:
        """
        약봉투 사진 업로드 (데이터 수집용)

        Args:
            db: 데이터베이스 세션
            order_id: 주문 ID
            base64_image: Base64 인코딩된 이미지

        Returns:
            업데이트된 처방전 정보
        """
        prescription = (
            db.query(Prescription).filter(Prescription.order_id == order_id).first()
        )
        if not prescription:
            return None

        # S3에 약봉투 이미지 업로드
        medicine_bag_url, medicine_bag_key = s3_service.upload_base64_image(
            base64_image, folder="medicine_bags"
        )

        prescription.medicine_bag_image_url = medicine_bag_url
        prescription.medicine_bag_image_key = medicine_bag_key

        db.commit()
        db.refresh(prescription)
        return prescription


# 싱글톤 인스턴스
order_service = OrderService()

