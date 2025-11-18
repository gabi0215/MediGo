"""
애플리케이션 설정
"""
from typing import List
from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # Application
    APP_NAME: str = "메디-고 API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str

    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "ap-northeast-2"
    S3_BUCKET_NAME: str

    # Kakao OAuth
    KAKAO_CLIENT_ID: str
    KAKAO_CLIENT_SECRET: str
    KAKAO_REDIRECT_URI: str

    # Kakao Talk Channel
    KAKAO_REST_API_KEY: str
    KAKAO_ADMIN_KEY: str
    KAKAO_CHANNEL_PUBLIC_ID: str
    KAKAO_CHANNEL_API_URL: str = "https://kapi.kakao.com"

    # CORS - 내부적으로 문자열로 저장
    _allowed_origins_str: str = Field(
        default="http://localhost:3000,http://localhost:3001",
        alias="ALLOWED_ORIGINS"
    )

    # OCR Service
    OCR_SERVICE_URL: str = "http://localhost:8001"

    # Admin
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """CORS origins를 리스트로 반환"""
        return [origin.strip() for origin in self._allowed_origins_str.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()

