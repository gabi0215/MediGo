"""
AWS S3 서비스
"""
import base64
import uuid
from datetime import datetime
from typing import Tuple

import boto3
from botocore.exceptions import ClientError

from app.core.config import settings


class S3Service:
    """S3 파일 업로드/다운로드 서비스"""

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    def upload_base64_image(
        self, base64_data: str, folder: str = "prescriptions"
    ) -> Tuple[str, str]:
        """
        Base64 이미지를 S3에 업로드

        Args:
            base64_data: Base64 인코딩된 이미지 데이터
            folder: S3 내 폴더명

        Returns:
            (s3_url, s3_key) 튜플
        """
        try:
            # Base64 디코딩
            image_data = base64.b64decode(base64_data)

            # 파일명 생성 (UUID + 타임스탬프)
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_name = f"{folder}/{timestamp}_{uuid.uuid4()}.jpg"

            # S3 업로드
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=image_data,
                ContentType="image/jpeg",
                ServerSideEncryption="AES256",  # 서버 사이드 암호화
            )

            # S3 URL 생성
            s3_url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}"

            return s3_url, file_name

        except ClientError as e:
            raise Exception(f"S3 업로드 실패: {str(e)}")

    def upload_file(self, file_path: str, s3_key: str) -> str:
        """
        로컬 파일을 S3에 업로드

        Args:
            file_path: 로컬 파일 경로
            s3_key: S3 키

        Returns:
            S3 URL
        """
        try:
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                s3_key,
                ExtraArgs={"ServerSideEncryption": "AES256"},
            )

            s3_url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
            return s3_url

        except ClientError as e:
            raise Exception(f"S3 업로드 실패: {str(e)}")

    def get_presigned_url(self, s3_key: str, expiration: int = 3600) -> str:
        """
        S3 객체의 Presigned URL 생성

        Args:
            s3_key: S3 키
            expiration: URL 만료 시간 (초)

        Returns:
            Presigned URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": s3_key},
                ExpiresIn=expiration,
            )
            return url

        except ClientError as e:
            raise Exception(f"Presigned URL 생성 실패: {str(e)}")


# 싱글톤 인스턴스
s3_service = S3Service()

