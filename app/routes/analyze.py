import logging
import json
from fastapi import APIRouter, HTTPException
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.ml_service import analyze_text, MODEL_NAME
from app.db import get_connection

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    """
    Принимает текст, классифицирует его как SPAM / NOT SPAM,
    сохраняет в БД и возвращает результат.
    """
    logger.info(f"Входящий запрос /analyze: '{request.text[:60]}...'")

    # Валидация: не принимаем пустой текст
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Текст не может быть пустым.")

    # Ограничение длины текста
    if len(request.text) > 500:
        raise HTTPException(status_code=400, detail="Текст не должен превышать 500 символов.")

    # Запускаем модель
    try:
        analysis = analyze_text(request.text)
    except RuntimeError as e:
        logger.error(f"Ошибка модели: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    # Сохраняем в БД
    result_json = json.dumps({"result": analysis["result"], "score": analysis["score"]})
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO requests_history (input_text, result_text, model_name) VALUES (%s, %s, %s)",
                (request.text, result_json, MODEL_NAME)
            )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка сохранения в БД: {e}")
        # Не прерываем запрос — результат уже есть, просто логируем ошибку БД

    return AnalyzeResponse(
        result=analysis["result"],
        score=analysis["score"],
        model=analysis["model"]
    )
