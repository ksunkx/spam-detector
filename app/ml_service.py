import os
import logging
from transformers import pipeline

logger = logging.getLogger(__name__)

# Название модели берём из .env, по умолчанию — лёгкая модель для спама
MODEL_NAME = os.getenv("HF_MODEL", "mrm8488/bert-tiny-finetuned-sms-spam-detection")

# Загружаем модель один раз при старте (не при каждом запросе!)
try:
    logger.info(f"Загружаем модель: {MODEL_NAME}")
    classifier = pipeline("text-classification", model=MODEL_NAME)
    logger.info("Модель загружена успешно.")
except Exception as e:
    logger.error(f"Ошибка загрузки модели: {e}")
    classifier = None


def analyze_text(text: str) -> dict:
    """
    Принимает текст, возвращает результат классификации.
    Пример результата: {"result": "SPAM", "score": 0.97, "model": "..."}
    """
    if classifier is None:
        raise RuntimeError("Модель не загружена. Проверьте логи.")

    output = classifier(text)[0]  # output = {"label": "LABEL_1", "score": 0.97}

    # Модель возвращает LABEL_0 (не спам) или LABEL_1 (спам)
    label = output["label"]
    score = round(output["score"], 4)

    result = "SPAM" if label == "LABEL_1" else "NOT SPAM"

    return {
        "result": result,
        "score": score,
        "model": MODEL_NAME
    }
