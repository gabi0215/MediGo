"""
OCR 서비스 (EasyOCR 기반)
"""
import io
import base64
from typing import Dict, List, Optional

import easyocr
import numpy as np
from PIL import Image


class OCRService:
    """약봉투/처방전 OCR 서비스"""

    def __init__(self):
        """
        EasyOCR 초기화
        - 한글과 영어를 지원
        - GPU 사용 가능 시 자동으로 GPU 사용
        """
        self.reader = easyocr.Reader(["ko", "en"], gpu=True)

    def extract_text_from_base64(self, base64_image: str) -> Dict:
        """
        Base64 이미지에서 텍스트 추출

        Args:
            base64_image: Base64 인코딩된 이미지

        Returns:
            추출 결과 딕셔너리
            {
                "raw_text": "전체 텍스트",
                "detected_texts": [{"text": "...", "confidence": 0.95, "bbox": [...]}]
            }
        """
        try:
            # Base64 디코딩
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))

            # numpy 배열로 변환
            image_array = np.array(image)

            # OCR 수행
            results = self.reader.readtext(image_array)

            # 결과 포맷팅
            detected_texts = []
            raw_text_parts = []

            for bbox, text, confidence in results:
                detected_texts.append(
                    {
                        "text": text,
                        "confidence": float(confidence),
                        "bbox": bbox,
                    }
                )
                raw_text_parts.append(text)

            return {
                "raw_text": " ".join(raw_text_parts),
                "detected_texts": detected_texts,
                "status": "success",
            }

        except Exception as e:
            return {
                "raw_text": "",
                "detected_texts": [],
                "status": "error",
                "error_message": str(e),
            }

    def extract_text_from_url(self, image_url: str) -> Dict:
        """
        URL 이미지에서 텍스트 추출

        Args:
            image_url: 이미지 URL

        Returns:
            추출 결과 딕셔너리
        """
        try:
            # URL에서 이미지 다운로드
            import requests

            response = requests.get(image_url)
            image = Image.open(io.BytesIO(response.content))

            # numpy 배열로 변환
            image_array = np.array(image)

            # OCR 수행
            results = self.reader.readtext(image_array)

            # 결과 포맷팅
            detected_texts = []
            raw_text_parts = []

            for bbox, text, confidence in results:
                detected_texts.append(
                    {
                        "text": text,
                        "confidence": float(confidence),
                        "bbox": bbox,
                    }
                )
                raw_text_parts.append(text)

            return {
                "raw_text": " ".join(raw_text_parts),
                "detected_texts": detected_texts,
                "status": "success",
            }

        except Exception as e:
            return {
                "raw_text": "",
                "detected_texts": [],
                "status": "error",
                "error_message": str(e),
            }

    def parse_medicine_info(self, raw_text: str) -> Dict:
        """
        약봉투 OCR 텍스트에서 핵심 정보 추출 (간단한 파싱)

        Args:
            raw_text: OCR로 추출된 텍스트

        Returns:
            파싱된 정보 딕셔너리
        """
        # TODO: 더 정교한 파싱 로직 구현
        # 현재는 간단한 키워드 기반 추출

        info = {
            "medicine_names": [],
            "dosage": None,
            "frequency": None,
            "duration": None,
            "notes": [],
        }

        text_lower = raw_text.lower()

        # 복용 횟수 추출
        if "1일" in raw_text:
            for keyword in ["1회", "2회", "3회"]:
                if keyword in raw_text:
                    info["frequency"] = f"1일 {keyword}"
                    break

        # 식전/식후 정보 추출
        if "식후" in raw_text:
            info["notes"].append("식후 복용")
        elif "식전" in raw_text:
            info["notes"].append("식전 복용")

        # 주의사항 추출
        if "졸음" in raw_text or "졸릴" in raw_text:
            info["notes"].append("졸음 주의")

        return info


# 싱글톤 인스턴스
ocr_service = OCRService()

