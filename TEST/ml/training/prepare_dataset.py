"""
AI 학습 데이터셋 준비 스크립트
"""
import json
import os
from typing import List, Dict

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DatasetPreparer:
    """학습 데이터셋 준비 클래스"""

    def __init__(self):
        """데이터베이스 연결"""
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))

    def fetch_training_data(self) -> List[Dict]:
        """
        데이터베이스에서 학습 데이터 가져오기

        Returns:
            학습 데이터 리스트
        """
        cursor = self.conn.cursor()

        query = """
        SELECT 
            td.id,
            td.ocr_raw_text,
            td.guidance_text,
            td.is_verified,
            td.quality_score
        FROM training_data td
        WHERE td.is_verified = TRUE
        ORDER BY td.created_at DESC
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        dataset = []
        for row in rows:
            dataset.append(
                {
                    "id": row[0],
                    "input": row[1],  # OCR 텍스트
                    "output": row[2],  # 복약 지도
                    "is_verified": row[3],
                    "quality_score": row[4],
                }
            )

        cursor.close()
        return dataset

    def save_dataset_to_json(self, dataset: List[Dict], output_path: str):
        """
        데이터셋을 JSON 파일로 저장

        Args:
            dataset: 데이터셋
            output_path: 출력 파일 경로
        """
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)

        print(f"데이터셋 저장 완료: {output_path}")
        print(f"총 데이터 수: {len(dataset)}")

    def prepare_fine_tuning_format(self, dataset: List[Dict]) -> List[Dict]:
        """
        Fine-tuning을 위한 프롬프트 형식으로 변환

        Args:
            dataset: 원본 데이터셋

        Returns:
            Fine-tuning 형식의 데이터셋
        """
        formatted_data = []

        for item in dataset:
            prompt = f"""### 지시: 다음 약봉투 정보에 대한 복약 지도 메시지를 환자에게 보내는 것처럼 친절하게 작성하세요.

### 입력: {item['input']}

### 출력: {item['output']}"""

            formatted_data.append(
                {
                    "id": item["id"],
                    "prompt": prompt,
                    "input": item["input"],
                    "output": item["output"],
                }
            )

        return formatted_data

    def close(self):
        """데이터베이스 연결 종료"""
        self.conn.close()


if __name__ == "__main__":
    preparer = DatasetPreparer()

    # 학습 데이터 가져오기
    print("데이터베이스에서 학습 데이터 가져오는 중...")
    dataset = preparer.fetch_training_data()

    if len(dataset) == 0:
        print("⚠️  학습 데이터가 없습니다. 먼저 주문을 처리하고 데이터를 수집하세요.")
    else:
        # Fine-tuning 형식으로 변환
        formatted_dataset = preparer.prepare_fine_tuning_format(dataset)

        # JSON 파일로 저장
        output_dir = "../data"
        os.makedirs(output_dir, exist_ok=True)

        preparer.save_dataset_to_json(
            formatted_dataset, f"{output_dir}/training_dataset.json"
        )

        print(f"\n✅ 데이터셋 준비 완료!")
        print(f"   - 총 {len(formatted_dataset)}개의 학습 데이터")
        print(f"   - 저장 위치: {output_dir}/training_dataset.json")

    preparer.close()

