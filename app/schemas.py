from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnalyzeRequest(BaseModel):
    """Схема входящего запроса на анализ текста."""
    text: str


class AnalyzeResponse(BaseModel):
    """Схема ответа после анализа."""
    result: str
    score: float
    model: str


class HistoryItem(BaseModel):
    """Схема одной записи из истории."""
    id: int
    input_text: str
    result_text: str
    model_name: str
    created_at: Optional[datetime]
