"""
OCR API 서버
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ocr_service import ocr_service

app = FastAPI(
    title="메디-고 OCR 서비스",
    version="1.0.0",
    description="약봉투/처방전 OCR API",
)


class OCRRequest(BaseModel):
    """OCR 요청"""

    base64_image: str


class OCRResponse(BaseModel):
    """OCR 응답"""

    raw_text: str
    detected_texts: list
    status: str
    error_message: str = None


@app.get("/", tags=["Health"])
async def health_check():
    """서버 상태 확인"""
    return {"status": "healthy", "service": "OCR API"}


@app.post("/ocr/extract", response_model=OCRResponse, tags=["OCR"])
async def extract_text(request: OCRRequest):
    """
    Base64 이미지에서 텍스트 추출

    - 한글과 영어를 지원합니다
    - 약봉투/처방전에 특화되어 있습니다
    """
    try:
        result = ocr_service.extract_text_from_base64(request.base64_image)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ocr/parse-medicine", tags=["OCR"])
async def parse_medicine(request: OCRRequest):
    """
    약봉투 이미지에서 복약 정보 추출

    - OCR + 파싱을 한 번에 수행합니다
    - 약 이름, 용법, 용량 등을 추출합니다
    """
    try:
        # OCR 수행
        ocr_result = ocr_service.extract_text_from_base64(request.base64_image)
        if ocr_result["status"] != "success":
            raise HTTPException(status_code=400, detail="OCR 실패")

        # 정보 파싱
        parsed_info = ocr_service.parse_medicine_info(ocr_result["raw_text"])

        return {
            "raw_text": ocr_result["raw_text"],
            "parsed_info": parsed_info,
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("ocr_api:app", host="0.0.0.0", port=8001, reload=True)

