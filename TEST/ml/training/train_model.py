"""
복약 지도 생성 모델 학습 스크립트

향후 LLaMA 3 기반 한국어 모델을 Fine-tuning하는 예제
현재는 스켈레톤 코드만 제공
"""
import json
import os
from typing import List, Dict

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
)

# TODO: 실제 학습 시 주석 해제 및 수정 필요


class MedicationGuidanceTrainer:
    """복약 지도 생성 모델 학습 클래스"""

    def __init__(self, model_name: str = "beomi/llama-3-open-ko-8b"):
        """
        모델 초기화

        Args:
            model_name: Hugging Face 모델 이름
        """
        self.model_name = model_name
        print(f"모델 로드 중: {model_name}")

        # TODO: 실제 학습 시 활성화
        # self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # self.model = AutoModelForCausalLM.from_pretrained(
        #     model_name,
        #     torch_dtype=torch.float16,
        #     device_map="auto"
        # )

    def load_dataset(self, dataset_path: str) -> List[Dict]:
        """
        학습 데이터셋 로드

        Args:
            dataset_path: 데이터셋 JSON 파일 경로

        Returns:
            데이터셋 리스트
        """
        with open(dataset_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        print(f"데이터셋 로드 완료: {len(dataset)}개")
        return dataset

    def prepare_training_data(self, dataset: List[Dict]):
        """
        학습 데이터 전처리

        Args:
            dataset: 원본 데이터셋

        Returns:
            전처리된 데이터셋
        """
        # TODO: 토크나이징 및 전처리
        pass

    def train(self, train_dataset, eval_dataset=None):
        """
        모델 학습

        Args:
            train_dataset: 학습 데이터셋
            eval_dataset: 검증 데이터셋
        """
        # TODO: 학습 설정 및 실행
        """
        training_args = TrainingArguments(
            output_dir="./models/medication-guidance-v1",
            num_train_epochs=3,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            learning_rate=2e-5,
            fp16=True,
            logging_steps=10,
            save_steps=100,
            evaluation_strategy="steps" if eval_dataset else "no",
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
        )

        trainer.train()
        """
        print("⚠️  모델 학습은 충분한 데이터가 수집된 후 진행합니다.")
        print("   현재는 스켈레톤 코드만 제공됩니다.")

    def save_model(self, output_dir: str):
        """
        학습된 모델 저장

        Args:
            output_dir: 모델 저장 경로
        """
        # TODO: 모델 저장
        """
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        """
        pass


if __name__ == "__main__":
    print("=" * 60)
    print("메디-고 복약 지도 생성 모델 학습")
    print("=" * 60)
    print()

    # 데이터셋 경로
    dataset_path = "../data/training_dataset.json"

    if not os.path.exists(dataset_path):
        print(f"❌ 데이터셋 파일을 찾을 수 없습니다: {dataset_path}")
        print("   먼저 prepare_dataset.py를 실행하여 데이터셋을 준비하세요.")
        exit(1)

    print(f"📁 데이터셋: {dataset_path}")
    print()

    print("🚧 현재는 학습 스켈레톤 코드만 제공됩니다.")
    print("   실제 학습은 다음 조건이 충족되면 진행합니다:")
    print("   - 최소 500개 이상의 검증된 학습 데이터")
    print("   - GPU 서버 (AWS EC2 g4dn.xlarge 이상)")
    print("   - 충분한 메모리 (16GB+ VRAM)")
    print()
    print("📊 현재 단계: MVP - 데이터 수집 단계")
    print("   운영팀이 수동으로 복약 지도를 작성하면서 데이터를 축적 중입니다.")

